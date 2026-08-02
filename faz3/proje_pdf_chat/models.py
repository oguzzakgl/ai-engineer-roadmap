# faz3/proje_pdf_chat/models.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base  # database.py'deki Base sınıfını içe aktarıyoruz

# =====================================================================
# 🎯 TODO 1: PDF DOSYA TABLOSU (pdf_dosyalari)
# =====================================================================
# Bu tablo, yüklenen PDF dosyalarının adlarını ve bilgilerini saklayacak.
# Sınıf adı: PDFDosyaTablosu
# Tablo adı (__tablename__): "pdf_dosyalari"
# Alanlar:
# - id: Integer, primary_key=True, index=True
# - dosya_adi: String, nullable=False (PDF dosyasının adı)
# - paragraflar: relationship("PDFParagrafTablosu", back_populates="pdf", cascade="all, delete-orphan")
#   (Yani dosya silinirse, ona bağlı paragraflar da otomatik silinsin)
# =====================================================================
class PDFDosyaTablosu(Base):
    __tablename__="pdf_dosyalari"
    id = Column(Integer, primary_key=True, index=True)
    dosya_adi=Column(String, nullable=False)
    paragraflar=relationship("PDFParagrafTablosu", back_populates="pdf", cascade="all, delete-orphan")


# =====================================================================
# 🎯 TODO 2: PDF PARAGRAF TABLOSU (pdf_paragraflar)
# =====================================================================
# Bu tablo, PDF'ten kırpılan ham paragrafları ve onların vektörlerini saklayacak.
# Sınıf adı: PDFParagrafTablosu
# Tablo adı (__tablename__): "pdf_paragraflar"
# Alanlar:
# - id: Integer, primary_key=True, index=True
# - pdf_id: Integer, ForeignKey("pdf_dosyalari.id", ondelete="CASCADE"), nullable=False
# - metin_icerigi: Text, nullable=False (Kırpılan ham metin parçası)
# - embedding: Text, nullable=True (3072 boyutlu vektörün string hali)
# - pdf: relationship("PDFDosyaTablosu", back_populates="paragraflar")
# =====================================================================
class PDFParagrafTablosu(Base):
    __tablename__="pdf_paragraflar"
    id=Column(Integer, primary_key=True, index=True)
    pdf_id=Column(Integer, ForeignKey("pdf_dosyalari.id", ondelete="CASCADE"), nullable=False)
    metin_icerigi=Column(Text, nullable=False)
    embedding=Column(Text, nullable=True)
    pdf=relationship("PDFDosyaTablosu", back_populates="paragraflar")

