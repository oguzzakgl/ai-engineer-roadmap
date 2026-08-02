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
    return {"message": "Doldurulacak"}


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
    niyet = "BELGE_ARAMA" # Gemini'den gelecek olan değer
    
    # -----------------------------------------------------------------
    # ADIM 2: EĞER NİYET "BELGE_ARAMA" İSE (RAG AKIŞI)
    # -----------------------------------------------------------------
    # - Soru vektörünü çıkarın (Referans: RAG projesi main.py L71).
    # - En yakın 3 paragrafı çekin (Referans: RAG projesi main.py L75).
    # - Prompt'u zenginleştirin ve Gemini'ye cevaplatın (Referans: RAG projesi main.py L89-L105).
    # - Geriye: schemas.ChatCevapResponse(niyet="BELGE_ARAMA", cevap=..., kaynaklar=...) dönün.
    if niyet == "BELGE_ARAMA":
        return schemas.ChatCevapResponse(niyet="BELGE_ARAMA", cevap="RAG Dönecek")

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
