# faz3/proje_sql_chat/models.py
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


# =====================================================================
# 🎯 TODO 5: PDF DOSYA VE PARAGRAF TABLOLARINI YAZIN (RAG İÇİN)
# =====================================================================
# PDFDosyaTablosu (tablo adı: "pdf_dosyalari") ve PDFParagrafTablosu (tablo adı: "pdf_paragraflar") modellerini ekleyin.
# (Referans: faz3/proje_pdf_chat/models.py dosyasındaki iki tablo modelini birebir buraya kopyalayabilirsiniz.)
# =====================================================================
