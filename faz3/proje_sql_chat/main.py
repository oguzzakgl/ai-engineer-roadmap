# faz3/proje_sql_chat/main.py
import os
import shutil
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel, Field
from google import genai
from database import engine, Base, get_db
import models
import schemas
import crud
import pdf_processor

# =====================================================================
# 🕸️ VERİTABANI BAŞLANGIÇ AYARLARI
# =====================================================================
with engine.connect() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
    conn.commit()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Kurumsal AI Analiz ve RAG Asistanı")

# Gemini istemcisini başlatıyoruz
client = genai.Client()


# =====================================================================
# 🧠 GEMINI YAPILANDIRILMIŞ ÇIKTI ŞEMASI (NİYET ANALİZİ)
# =====================================================================
# Kullanıcının sorduğu sorunun hangi kanala (SQL mi, RAG mi) gideceğini
# belirlemek için Gemini'den bu Pydantic formatında cevap isteyeceğiz.
class NiyetAnalizi(BaseModel):
    niyet: str = Field(
        description="Soru eğer şirket kuralları, izin politikası, IK veya dökümanlar hakkındaysa 'BELGE_ARAMA'; "
                    "eğer ciro, sipariş adetleri, satış rakamları veya müşteri listesi gibi rakamsal analizler hakkındaysa 'VERITABANI_ANALIZ' dönmelidir."
    )


# =====================================================================
# 🎯 TODO 12: VERİTABANI SEED (ÖRNEK VERİ YÜKLEME) ENDPOINT'İ (/seed)
# =====================================================================
# Metot: POST
# Path: "/seed"
# Amacı: crud.py dosyasındaki veritabani_seed_et(db) fonksiyonunu çağırır ve
#        veritabanına örnek tabloları doldurur.
# =====================================================================
@app.post("/seed")
def veritabani_hazirla(db: Session = Depends(get_db)):
    # Adım 1: crud.py içindeki veritabani_seed_et() fonksiyonunu çağırın.
    # Adım 2: Başarılı mesajı içeren bir sözlük dönün (Örn: {"status": "success", "message": "..."})
    crud.veritabani_seed_et(db)
    return {"status": "success", "message": "Veritabanı başarıyla örnek verilerle dolduruldu."}


# =====================================================================
# 🎯 TODO 13: SOHBET VE KARAR DESTEK ENDPOINT'İ (/chat)
# =====================================================================
# Metot: POST
# Path: "/chat"
# Yanıt Modeli: schemas.ChatCevapResponse
# =====================================================================
@app.post("/chat", response_model=schemas.ChatCevapResponse)
def kurumsal_asistan(request: schemas.ChatSoruRequest, db: Session = Depends(get_db)):
    
    # -----------------------------------------------------------------
    # ADIM 1: NİYET ANALİZİ (Intent Classification)
    # -----------------------------------------------------------------
    # - Gemini API'sini Structured Output (Yapılandırılmış Çıktı) kullanarak çağırın.
    # - response_schema olarak yukarıdaki NiyetAnalizi sınıfını verin.
    # - Gemini'nin kullanıcının sorusuna verdiği niyeti ("BELGE_ARAMA" veya "VERITABANI_ANALIZ") okuyun.
    try:
        cevap = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"'{request.soru}' sorusunu analiz et. Hangi kategoriye giriyor? BELGE_ARAMA veya VERITABANI_ANALIZ olarak yanıt ver.",
            config={
                "response_mime_type": "application/json",
                "response_schema": NiyetAnalizi
            }
        ).text

        niyet_analizi = NiyetAnalizi.model_validate_json(cevap)
        niyet = niyet_analizi.niyet
    except Exception as e:
        return schemas.ChatCevapResponse(
            niyet="BELGE_ARAMA", 
            cevap=f"Niyet analizi hatası: {e}", 
            kaynaklar=[]
        )
    # -----------------------------------------------------------------
    # ADIM 2: EĞER NİYET "BELGE_ARAMA" İSE (RAG AKIŞI)
    # -----------------------------------------------------------------
    if niyet == "BELGE_ARAMA":
        soru_vektoru = pdf_processor.parca_vektorlerini_uret([request.soru])[0]
        benzer_paragraflar = crud.en_benzer_paragraflari_bul(db, soru_vektoru, limit=3)
        
        kaynak_metinler = [p.metin_icerigi for p in benzer_paragraflar]
        kaynaklar_birlestirilmis = "\n---".join(kaynak_metinler)
        
        zenginlestirilmis_prompt = f"""
Sana bir soru ve bu soruya yanıt vermen için kaynak dökümanlardan alınmış paragraflar verilecek.
Lütfen SADECE sana verilen kaynak paragrafları baz alarak soruyu cevapla.
Eğer verilen kaynak paragraflarda sorunun cevabı yoksa, "Verilen kaynaklarda bu bilgi bulunmuyor." şeklinde yanıt ver.

KAYNAK PARAGRAFLAR:
{kaynaklar_birlestirilmis}

SORU:
{request.soru}
"""
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=zenginlestirilmis_prompt
        )
        
        return schemas.ChatCevapResponse(niyet="BELGE_ARAMA", cevap=response.text, kaynaklar=kaynak_metinler)
    # -----------------------------------------------------------------
    # ADIM 3: EĞER NİYET "VERITABANI_ANALIZ" İSE (SQL AKIŞI)
    # -----------------------------------------------------------------
    #
    # Adım 3a: SQL Sorgusu Üretme (Text-to-SQL)
    # - Gemini'ye veritabanı şemamızı (musteriler, urunler, siparisler tablolarının sütun adlarını) 
    #   ve aralarındaki ilişkileri (Foreign Key) anlatan bir prompt hazırlayın.
    # - Gemini'ye bu şemaya göre kullanıcının sorusunu yanıtlayacak GEÇERLİ bir SQL sorgusu üretmesini söyleyin.
    # - Gemini'den dönen temiz SQL sorgu string'ini alın.
    sql_sorgusu = "SELECT * FROM siparisler;" # Gemini'den gelecek olan sorgu
    
    # Adım 3b: SQL'i Çalıştırma
    # - crud.py dosyasında yazacağımız dinamik_sql_calistir(db, sql_sorgusu) fonksiyonunu çağırın.
    # - Dönen ham tablo sonuçlarını bir değişkene atayın (tablo_verileri).
    tablo_verileri = []
    
    # Adım 3c: Sonuçları Gemini ile Yorumlatma
    # - Elde ettiğimiz tablo verilerini ve kullanıcının sorusunu tekrar Gemini'ye gönderip,
    #   insanların anlayacağı dilde, kibar bir analiz özeti yazmasını isteyin.
    # - Örn Prompt: "Kullanıcı sorusu: ... Çalıştırılan SQL sonucu gelen veriler: ... Lütfen bunu yorumla."
    analiz_ozeti = "Grafikte de görebileceğiniz gibi..." # Gemini'den gelecek özet metin
    
    # Adım 3d: Yanıt Dönme
    # - Geriye: schemas.ChatCevapResponse(
    #               niyet="VERITABANI_ANALIZ", 
    #               cevap=analiz_ozeti, 
    #               sql_sorgusu=sql_sorgusu, 
    #               tablo_verisi=tablo_verileri
    #           ) dönün.
    return schemas.ChatCevapResponse(niyet="VERITABANI_ANALIZ", cevap="SQL Dönecek")


# =====================================================================
# 🎯 TODO 14: PDF YÜKLEME ENDPOINT'İ VE STATIC FILES MOUNT İŞLEMLERİ
# =====================================================================
# - RAG için PDF dosyalarını sunucuya alacak olan "/upload-pdf" endpoint'ini yazın.
#   (Referans: RAG projesi main.py L33-L58)
# - 'frontend' klasörünü StaticFiles yardımıyla ana dizine (/) bağlayın.
#   (Referans: RAG projesi main.py L121-L125)
# =====================================================================
