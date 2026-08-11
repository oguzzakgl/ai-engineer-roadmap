# 03_generative_ai_ve_rag_temelleri/proje_pdf_chat/main.py
import os
import shutil
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import engine, Base, get_db
import crud
import schemas
from pdf_processor import pdf_dosyasini_isle, parca_vektorlerini_uret, client

# =====================================================================
# 🕸️ VERİTABANI BAŞLANGIÇ AYARLARI
# =====================================================================
# Sunucu her açıldığında veritabanında pgvector eklentisinin aktif olduğundan emin oluyoruz.
with engine.connect() as conn:
    # CREATE EXTENSION IF NOT EXISTS vector: PostgreSQL veritabanında vektör arama
    # yapabilmemizi sağlayan pgvector eklentisini aktif eder.
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
    conn.commit()

# models.py'de tanımladığımız tablolar veritabanında yoksa otomatik oluşturulur.
Base.metadata.create_all(bind=engine)

# FastAPI uygulamamızı başlatıyoruz
app = FastAPI(title="Akıllı PDF Asistanı API (RAG)")


# =====================================================================
# 📂 1. ENDPOINT: PDF YÜKLEME (POST /upload-pdf)
# =====================================================================
# Kullanıcının bilgisayarından seçtiği PDF dosyasını alır ve veritabanına kaydeder.
@app.post("/upload-pdf", response_model=schemas.PDFDosyaResponse)
def pdf_yukle(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # 1. Dosya Güvenlik Kontrolü (Sadece PDF dosyalarına izin veriyoruz)
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Lütfen sadece PDF dosyası yükleyin.")
        
    # 2. Geçici Klasör Ayarı
    # Dosya işleme (okuma/parçalama) yapabilmek için dosyayı geçici olarak sunucu diskine yazıyoruz.
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, file.filename)
    
    # Gelen dosyayı diskteki geçici dosyaya kopyalıyoruz
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        # 3. PDF İşleme Fabrikasını Çalıştırma:
        # pdf_dosyasini_isle fonksiyonunu çağırarak okuma, bölme, vektörleme ve DB kaydetme adımlarını yapıyoruz.
        db_dosya = pdf_dosyasini_isle(temp_file_path, file.filename, db)
        return db_dosya
    finally:
        # 4. Temizlik Aşaması:
        # İşlem başarılı veya başarısız olsun, sunucuda çöp dosya kalmaması için geçici dosyayı siliyoruz.
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


# =====================================================================
# 📂 2. ENDPOINT: AKILLI SOHBET / RAG (POST /chat)
# =====================================================================
# Kullanıcının sorusuna, veritabanından en alakalı döküman parçalarını bulup
# o parçalar eşliğinde Gemini ile yanıt üretir.
@app.post("/chat", response_model=schemas.ChatCevapResponse)
def pdf_ile_sohbet(request: schemas.ChatSoruRequest, db: Session = Depends(get_db)):
    
    # 1. Adım: Kullanıcının sorusunu embedding vektörüne (koordinatlara) çeviriyoruz
    # parca_vektorlerini_uret fonksiyonu liste kabul ettiği için soruyu liste içine koyduk.
    soru_vektoru = parca_vektorlerini_uret([request.soru])[0]
    
    # 2. Adım: Veritabanında en benzer 3 paragrafı aratıyoruz
    # crud.py dosyasında yazdığımız kosinüs benzerliği sorgusunu çalıştırıyoruz.
    benzer_paragraflar = crud.en_benzer_paragraflari_bul(db, soru_vektoru, limit=3)
    
    # Eğer veritabanında hiçbir paragraf yoksa (kullanıcı henüz PDF yüklemediyse) hata dönüyoruz
    if not benzer_paragraflar:
        raise HTTPException(status_code=404, detail="Soruyla ilgili veritabanında kaynak bilgi bulunamadı. Lütfen önce bir PDF yükleyin.")
        
    # 3. Adım: Benzer paragrafların metin içeriklerini bir listede topluyoruz
    kaynak_metinler = [p.metin_icerigi for p in benzer_paragraflar]
    
    # 4. Adım: Paragrafları aralarına çizgiler koyarak tek bir metin bloğu haline getiriyoruz
    kaynaklar_birlestirilmis = "\n---\n".join(kaynak_metinler)
    
    # 5. Adım: Zenginleştirilmiş Prompt (Context Augmentation)
    # Gemini'ye sadece bu kaynakları kullanmasını, kafasından uydurmamasını (hallucination) emrediyoruz.
    zenginlestirilmis_prompt = f"""
Sana bir soru ve bu soruya yanıt vermen için kaynak dökümanlardan alınmış paragraflar verilecek.
Lütfen SADECE sana verilen kaynak paragrafları baz alarak soruyu cevapla.
Eğer verilen kaynak paragraflarda sorunun cevabı yoksa, "Verilen kaynaklarda bu bilgi bulunmuyor." şeklinde yanıt ver.

KAYNAK PARAGRAFLAR:
{kaynaklar_birlestirilmis}

SORU:
{request.soru}
"""
    
    # 6. Adım: Gemini'yi çalıştırıp cevabı alıyoruz
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=zenginlestirilmis_prompt
    )
    
    # 7. Adım: Cevabı ve faydalandığımız kaynak paragrafları şemaya uygun şekilde dönüyoruz
    return schemas.ChatCevapResponse(cevap=response.text, kaynaklar=kaynak_metinler)


# =====================================================================
# 📂 3. ENDPOINT: PDF DOSYALARINI LİSTELEME (GET /files)
# =====================================================================
# Veritabanında kayıtlı tüm PDF dosyalarının adlarını listeler.
@app.get("/files", response_model=list[schemas.PDFDosyaResponse])
def dosyalari_listele(db: Session = Depends(get_db)):
    # crud.py'deki tum_dosyalari_getir fonksiyonuyla tüm dosyaları çekip dönüyoruz
    return crud.tum_dosyalari_getir(db)


# ---------------------------------------------------------------------
# 📂 ARAYÜZ DOSYALARINI DIŞARIYA SUNMA (STATIC FILES)
# ---------------------------------------------------------------------
from fastapi.staticfiles import StaticFiles

# 'frontend' klasörünü tarayıcının ana dizinine (/) bağlıyoruz
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

