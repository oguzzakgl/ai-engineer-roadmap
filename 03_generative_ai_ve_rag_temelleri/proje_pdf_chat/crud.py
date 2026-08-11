# faz3/proje_pdf_chat/crud.py
from sqlalchemy import text
from sqlalchemy.orm import Session
from models import PDFDosyaTablosu, PDFParagrafTablosu

# =====================================================================
# 📂 1. İŞLEM: VERİTABANINDA VEKTÖR BENZERLİK ARAMASI (en_benzer_paragraflari_bul)
# =====================================================================
# Girdi: db (Oturum), soru_vektoru (Sorunun koordinat listesi), limit (Kaç paragraf getirilecek)
# Çıktı: En yakın paragrafların listesi (list[PDFParagrafTablosu])
def en_benzer_paragraflari_bul(db: Session, soru_vektoru: list[float], limit: int = 3) -> list[PDFParagrafTablosu]:
    # 1. Python float listesini veritabanına sorgu parametresi olarak göndermek için string yapıyoruz.
    # Örn: "[0.123, -0.456, ...]"
    soru_vektoru_str = str(soru_vektoru)
    
    # 2. pgvector eklentisinin kosinüs mesafesi operatörünü (<=>) kullanan SQL sorgumuz.
    # CAST(embedding AS vector): Kaydettiğimiz TEXT tipindeki vektörü sorgu esnasında VECTOR tipine çevirir.
    # <=> : İki vektör arasındaki açısal mesafeyi hesaplar. Mesafe ne kadar küçükse anlamsal benzerlik o kadar yüksektir.
    # ORDER BY ... ASC: En küçük mesafeden (yani en benzer olandan) başlayarak sıralar.
    sorgu = text("""
        SELECT id, pdf_id, metin_icerigi, embedding
        FROM pdf_paragraflar
        ORDER BY CAST(embedding AS vector) <=> :soru_vektoru
        LIMIT :limit
    """)
    
    # 3. SQL sorgusunu çalıştırıyor ve tüm eşleşen satırları çekiyoruz.
    # fetchall() bize ham Tuple (demet) listesi döner: [(id, pdf_id, metin, vektör), ...]
    sonuclar = db.execute(sorgu, {"soru_vektoru": soru_vektoru_str, "limit": limit}).fetchall()
    
    # 4. Veritabanından gelen bu ham tuple verileri, kodun kalanında nokta (.) ile erişebilmek için
    # SQLAlchemy model nesnelerine (PDFParagrafTablosu) dönüştürüyoruz.
    paragraflar = []
    for row in sonuclar:
        paragraf = PDFParagrafTablosu(
            id=row[0],
            pdf_id=row[1],
            metin_icerigi=row[2],
            embedding=row[3]
        )
        paragraflar.append(paragraf)
        
    return paragraflar


# =====================================================================
# 📂 2. İŞLEM: TÜM PDF DOSYALARINI LİSTELEMEK (tum_dosyalari_getir)
# =====================================================================
# Girdi: db (Oturum)
# Çıktı: Veritabanında kayıtlı tüm dosyaların listesi (list[PDFDosyaTablosu])
def tum_dosyalari_getir(db: Session) -> list[PDFDosyaTablosu]:
    # db.query(PDFDosyaTablosu).all(): Veritabanındaki 'pdf_dosyalari' tablosundaki
    # tüm satırları çeker ve Python nesnesi olarak döner.
    return db.query(PDFDosyaTablosu).all()
