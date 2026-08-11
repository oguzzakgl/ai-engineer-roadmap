# 03_generative_ai_ve_rag_temelleri/proje_sql_chat/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base  # database.py dosyasındaki Base sınıfını içe aktarıyoruz

# =====================================================================
# 🎯 TODO 2: MÜŞTERİ TABLOSUNU OLUŞTURUN (MusteriTablosu)
# =====================================================================
# Tablo Adı: "musteriler"
# Kolonlar:
# - id: Birincil Anahtar (Integer, primary_key=True, index=True)
# - ad: Müşteri adı (String, nullable=False)
# - sehir: Yaşadığı şehir (String, nullable=False)
#
# İlişki (Relationship):
# - siparisler: SiparisTablosu ile ilişki (relationship, back_populates="musteri")
# =====================================================================
class MusteriTablosu(Base):
    __tablename__ = "musteriler"
    id = Column(Integer, primary_key=True, index=True)
    ad = Column(String, nullable=False)
    sehir = Column(String, nullable=False)

    siparisler = relationship("SiparisTablosu", back_populates="musteri")


# =====================================================================
# 🎯 TODO 3: ÜRÜN TABLOSUNU OLUŞTURUN (UrunTablosu)
# =====================================================================
# Tablo Adı: "urunler"
# Kolonlar:
# - id: Birincil Anahtar (Integer, primary_key=True, index=True)
# - ad: Ürün adı (String, nullable=False)
# - fiyat: Ürün fiyatı (Float, nullable=False)
# - stok: Kalan stok adeti (Integer, nullable=False)
#
# İlişki (Relationship):
# - siparisler: SiparisTablosu ile ilişki (relationship, back_populates="urun")
# =====================================================================

class UrunTablosu(Base):
    __tablename__ = "urunler"
    id = Column(Integer, primary_key=True, index=True)
    ad = Column(String, nullable=False)
    fiyat = Column(Float, nullable=False)
    stok = Column(Integer, nullable=False)

    siparisler = relationship("SiparisTablosu", back_populates="urun")
    

# =====================================================================
# 🎯 TODO 4: SİPARİŞ TABLOSUNU OLUŞTURUN (SiparisTablosu)
# =====================================================================
# Tablo Adı: "siparisler"
# Kolonlar:
# - id: Birincil Anahtar (Integer, primary_key=True, index=True)
# - musteri_id: Müşteri tablosuna bağlayan Foreign Key (Integer, ForeignKey("musteriler.id"), nullable=False)
# - urun_id: Ürün tablosuna bağlayan Foreign Key (Integer, ForeignKey("urunler.id"), nullable=False)
# - adet: Satın alınan adet miktarı (Integer, nullable=False)
# - tarih: Siparişin tarihi (String, nullable=False)
#
# İlişkiler (Relationships):
# - musteri: MusteriTablosu'na geri bağlayan köprü (relationship, back_populates="siparisler")
# - urun: UrunTablosu'na geri bağlayan köprü (relationship, back_populates="siparisler")
# =====================================================================
class SiparisTablosu(Base):
    __tablename__ = "siparisler"
    id = Column(Integer, primary_key=True, index=True)
    musteri_id = Column(Integer, ForeignKey("musteriler.id"), nullable=False)
    urun_id = Column(Integer, ForeignKey("urunler.id"), nullable=False)
    adet = Column(Integer, nullable=False)
    tarih = Column(String, nullable=False)

    musteri = relationship("MusteriTablosu", back_populates="siparisler")
    urun = relationship("UrunTablosu", back_populates="siparisler")
    
# =====================================================================
# 🎯 TODO 5: PDF DOSYA VE PARAGRAF TABLOLARINI YAZIN (RAG İÇİN)
# =====================================================================
# PDFDosyaTablosu (tablo adı: "pdf_dosyalari") ve PDFParagrafTablosu (tablo adı: "pdf_paragraflar") modellerini ekleyin.
# (Referans: faz3/proje_pdf_chat/models.py dosyasındaki iki tablo modelini birebir buraya kopyalayabilirsiniz.)
# =====================================================================

class PDFDosyaTablosu(Base):
    __tablename__ = "pdf_dosyalari"
    id = Column(Integer, primary_key=True, index=True)
    dosya_adi = Column(String, nullable=False)
    paragraflar = relationship("PDFParagrafTablosu", back_populates="pdf", cascade="all, delete-orphan")

class PDFParagrafTablosu(Base):
    __tablename__ = "pdf_paragraflar"
    id = Column(Integer, primary_key=True, index=True)
    pdf_id = Column(Integer, ForeignKey("pdf_dosyalari.id", ondelete="CASCADE"), nullable=False)
    metin_icerigi = Column(Text, nullable=False)
    embedding = Column(Text, nullable=True)

    pdf = relationship("PDFDosyaTablosu", back_populates="paragraflar")
    