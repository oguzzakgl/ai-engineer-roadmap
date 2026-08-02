# faz3/proje_pdf_chat/crud.py
from sqlalchemy import text
from sqlalchemy.orm import Session
from models import PDFDosyaTablosu, PDFParagrafTablosu

# =====================================================================
# 🎯 TODO 10: VERİTABANINDA VEKTÖR ARAMASI YAPMAK (SIMILARITY SEARCH)
# =====================================================================
# Kullanıcının sorduğu sorunun vektörünü alıp, veritabanındaki paragraflarla
# Cosine Distance (<=>) kullanarak karşılaştırır ve en benzer 3 paragrafı döner.
# Girdi: db (Session), soru_vektoru (list[float]), limit (int = 3)
# Çıktı: En benzer paragrafların listesi (list[PDFParagrafTablosu])
# İpucu:
# sorgu = text("""
#     SELECT id, pdf_id, metin_icerigi, embedding
#     FROM pdf_paragraflar
#     ORDER BY CAST(embedding AS vector) <=> :soru_vektoru
#     LIMIT :limit
# """)
# =====================================================================
def en_benzer_paragraflari_bul(db: Session, soru_vektoru: list[float], limit: int = 3) -> list[PDFParagrafTablosu]:
    # TODO: Raw SQL sorgusunu execute edip, gelen sonuçları nesne olarak geri dön.
    return []


# =====================================================================
# 🎯 TODO 11: YÜKLENEN TÜM PDF DOSYALARINI LİSTELEMEK
# =====================================================================
# Arayüzde listelemek için veritabanındaki tüm PDFDosyaTablosu kayıtlarını döner.
# Girdi: db (Session)
# Çıktı: PDFDosyaTablosu listesi (list[PDFDosyaTablosu])
# =====================================================================
def tum_dosyalari_getir(db: Session) -> list[PDFDosyaTablosu]:
    # TODO: db.query() kullanarak tüm dosyaları çek.
    return []
