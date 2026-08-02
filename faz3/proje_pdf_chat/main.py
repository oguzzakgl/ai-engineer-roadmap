# faz3/proje_pdf_chat/main.py
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
# PostgreSQL üzerinde pgvector eklentisini açıyoruz
with engine.connect() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
    conn.commit()

# Tabloları veritabanında oluşturuyoruz
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Akıllı PDF Asistanı API (RAG)")


# =====================================================================
# 🎯 TODO 12: PDF DOSYASI YÜKLEME ENDPOINT'İ (/upload-pdf)
# =====================================================================
# Dışarıdan yüklenen PDF dosyasını alır, geçici olarak kaydeder,
# pdf_dosyasini_isle() fonksiyonunu çağırıp DB'ye kaydeder ve yanıt döner.
# Metot: POST
# Path: "/upload-pdf"
# Yanıt Modeli: schemas.PDFDosyaResponse
# =====================================================================
@app.post("/upload-pdf", response_model=schemas.PDFDosyaResponse)
def pdf_yukle(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # 1. Gelen dosyanın PDF olup olmadığını kontrol et (uzantısı .pdf mi?)
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Lütfen sadece PDF dosyası yükleyin.")
        
    # 2. Geçici bir klasör oluştur ve dosyayı oraya kaydet
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, file.filename)
    
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        # TODO: pdf_processor'daki pdf_dosyasini_isle() fonksiyonunu çağırarak 
        # dosyayı DB'ye kaydet ve dönen nesneyi 'db_dosya' değişkenine ata.
        # pdf_dosyasini_isle(temp_file_path, file.filename, db)
        db_dosya = pdf_dosyasini_isle(temp_file_path, file.filename, db)
        return db_dosya
    finally:
        # 3. İşlem bittikten sonra sunucuda yer kaplamaması için geçici dosyayı siliyoruz
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


# =====================================================================
# 🎯 TODO 13: AKILLI SOHBET / RAG ENDPOINT'İ (/chat)
# =====================================================================
# Kullanıcıdan bir soru alır, soruyu vektörleştirir, DB'de arar,
# en alakalı paragraflarla zenginleştirilmiş prompt'u Gemini'ye sorup cevap döner.
# Metot: POST
# Path: "/chat"
# Yanıt Modeli: schemas.ChatCevapResponse
# =====================================================================
@app.post("/chat", response_model=schemas.ChatCevapResponse)
def pdf_ile_sohbet(request: schemas.ChatSoruRequest, db: Session = Depends(get_db)):
    
    # 1. Kullanıcının sorusunun vektörünü üretiyoruz
    # parca_vektorlerini_uret() list alan bir fonksiyon olduğu için [request.soru] veriyoruz
    soru_vektoru = parca_vektorlerini_uret([request.soru])[0]
    
    # 2. Veritabanından bu soruya en benzer 3 paragrafı çekiyoruz
    # TODO: crud.py'deki en_benzer_paragraflari_bul() fonksiyonunu çağırarak 
    # en yakın paragrafları bul ve 'benzer_paragraflar' değişkenine ata.
    benzer_paragraflar = crud.en_benzer_paragraflari_bul(db, soru_vektoru, limit=3)

    if not benzer_paragraflar:
        raise HTTPException(status_code=404, detail="Soruyla ilgili veritabanında kaynak bilgi bulunamadı.")
        
    # 3. Benzer paragrafların metin içeriklerini bir listede topluyoruz
    kaynak_metinler = [p.metin_icerigi for p in benzer_paragraflar]
    
    # 4. Prompt'u bu kaynak bilgilerle zenginleştiriyoruz (Context Augmentation)
    kaynaklar_birlestirilmis = "\n---\n".join(kaynak_metinler)
    
    zenginlestirilmis_prompt = f"""
Sana bir soru ve bu soruya yanıt vermen için kaynak dökümanlardan alınmış paragraflar verilecek.
Lütfen SADECE sana verilen kaynak paragrafları baz alarak soruyu cevapla.
Eğer verilen kaynak paragraflarda sorunun cevabı yoksa, "Verilen kaynaklarda bu bilgi bulunmuyor." şeklinde yanıt ver.

KAYNAK PARAGRAFLAR:
{kaynaklar_birlestirilmis}

SORU:
{request.soru}
"""
    
    # 5. Gemini'yi çalıştırıyoruz
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=zenginlestirilmis_prompt
    )
    
    # TODO: schemas.ChatCevapResponse formatına uygun olarak cevap ve kaynaklar listesini dön.
    # return schemas.ChatCevapResponse(cevap=..., kaynaklar=...)
    return schemas.ChatCevapResponse(cevap=response.text, kaynaklar=kaynak_metinler)


# =====================================================================
# 🎯 TODO 14: PDF DOSYALARINI LİSTELEME ENDPOINT'İ (/files)
# =====================================================================
# Veritabanında kayıtlı tüm PDF dosyalarının adlarını listeler.
# Metot: GET
# Path: "/files"
# Yanıt Modeli: list[schemas.PDFDosyaResponse]
# =====================================================================
@app.get("/files", response_model=list[schemas.PDFDosyaResponse])
def dosyalari_listele(db: Session = Depends(get_db)):
    # TODO: crud.py'deki tum_dosyalari_getir() fonksiyonunu çağırıp sonuçları dön.
    return crud.tum_dosyalari_getir(db)

