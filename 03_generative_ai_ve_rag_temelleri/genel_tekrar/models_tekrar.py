# =====================================================================
# 📂 GENEL TEKRAR - models_tekrar.py
# =====================================================================
# Bu dosyada veritabanı tablolarımızı (modellerimizi) tanımlayacağız.
# Kılavuz olarak pratik/syntax_rehberi.py 3. bölümü kullanabilirsiniz.

from sqlalchemy import Column, ForeignKey, Float, Integer, String
from database_tekrar import Base  # database_tekrar dosyasından Base'i çektik

# 1. Müşteriler Tablosu (MusteriTablosu)
# Tablo adı veritabanında "musteriler" olmalı.
# Sütunlar:
#   - id: Integer, primary_key=True
#   - ad: String, boş geçilemez (nullable=False)
#   - sehir: String
# =====================================================================
# KODUNUZU BURAYA YAZIN:
class MusteriTablosu(Base):
    __tablename__="musteriler"  
    id=Column(Integer,primary_key=True)
    ad=Column(String,nullable=False)
    sehir=Column(String)


# 2. Ürünler Tablosu (UrunTablosu)
# Tablo adı veritabanında "urunler" olmalı.
# Sütunlar:
#   - id: Integer, primary_key=True
#   - ad: String, boş geçilemez
#   - fiyat: Float, boş geçilemez
#   - stok: Integer, varsayılan değeri 0 (default=0)
# =====================================================================
# KODUNUZU BURAYA YAZIN:

class UrunTablosu(Base):
    __tablename__ = "urunler"
    id=Column(Integer,primary_key=True)
    ad=Column(String,nullable=False)
    fiyat=Column(Float,nullable=False)
    stok=Column(Integer,default=0)

# 3. Siparişler Tablosu (SiparisTablosu)
# Tablo adı veritabanında "siparisler" olmalı.
# Sütunlar:
#   - id: Integer, primary_key=True
#   - musteri_id: Integer, musteriler.id tablosuna Foreign Key olmalı.
#   - urun_id: Integer, urunler.id tablosuna Foreign Key olmalı.
#   - adet: Integer, boş geçilemez
#   - tarih: String (sipariş tarihi örn: '2026-08-04')
# =====================================================================
# KODUNUZU BURAYA YAZIN:


class SiparisTablosu(Base):
    __tablename__ = "siparisler"
    id=Column(Integer,primary_key=True)
    musteri_id=Column(Integer,ForeignKey("musteriler.id"))
    urun_id=Column(Integer,ForeignKey("urunler.id"))
    adet=Column(Integer,nullable=False)
    tarih=Column(String)