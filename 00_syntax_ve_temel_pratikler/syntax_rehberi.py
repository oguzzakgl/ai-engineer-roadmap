# =====================================================================
# 📚 EN ÇOK KULLANILAN PYTHON & BACKEND SYNTAX REHBERİ
# Bu dosyayı kapatmayın, kod yazarken takıldığınızda kopyalayıp yapıştırın.
# =====================================================================


# ─────────────────────────────────────────────────────────────────────
# 1. FASTAPI - TEMEL ŞABLON & ENDPOINT SYNTAX'I
# ─────────────────────────────────────────────────────────────────────
# FastAPI uygulamasını başlatmak ve endpoint yazmak için:

from fastapi import FastAPI

app = FastAPI()

# GET (Veri çekmek için)
@app.get("/yol")
def veri_oku():
    return {"mesaj": "Veri başarıyla çekildi"}

# POST (Yeni veri kaydetmek/göndermek için)
@app.post("/yol")
def veri_kaydet(request_body: dict):
    return {"gelen_veri": request_body}


# ─────────────────────────────────────────────────────────────────────
# 2. PYDANTIC - ŞEMA (REQUEST/RESPONSE) SYNTAX'I
# ─────────────────────────────────────────────────────────────────────
# Dışarıdan gelen verinin tipini kontrol etmek için:

from pydantic import BaseModel, Field

class UrunSemasi(BaseModel):
    ad: str                                    # Metin tipi, zorunlu
    fiyat: float                               # Ondalık sayı, zorunlu
    stok: int = 0                              # Tam sayı, varsayılan değeri 0
    aciklama: str | None = None                # İsteğe bağlı (opsiyonel) veri


# ─────────────────────────────────────────────────────────────────────
# 3. SQLALCHEMY - MODEL (TABLO) TANIMLAMA SYNTAX'I
# ─────────────────────────────────────────────────────────────────────
# Veritabanında tablo oluşturmak için:

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class MusteriTablosu(Base):
    __tablename__ = "musteriler"               # Veritabanındaki tablo adı
    
    id = Column(Integer, primary_key=True)     # Otomatik artan ID
    ad = Column(String, nullable=False)        # Boş geçilemez metin
    sehir = Column(String)                     # Boş geçebilir metin


# ─────────────────────────────────────────────────────────────────────
# 4. SQLALCHEMY - CRUD (VERİTABANI İŞLEMLERİ) SYNTAX'I
# ─────────────────────────────────────────────────────────────────────
# db oturumu (Session) kullanarak veri tabanına yazma ve okuma:

# A. Yeni Veri Ekleme (Create)
def urun_ekle(db, ad, fiyat):
    yeni_urun = UrunTablosu(ad=ad, fiyat=fiyat)
    db.add(yeni_urun)                          # Sepete ekle
    db.commit()                                # Veritabanına kaydet
    db.refresh(yeni_urun)                      # ID'yi veritabanından geri yükle
    return yeni_urun

# B. Tüm Verileri Çekme (Read - List)
def urunleri_getir(db):
    return db.query(UrunTablosu).all()         # select * from urunler

# C. Filtreleyerek Tek Bir Veri Çekme (Read - Detail)
def urun_bul_id_ile(db, urun_id):
    return db.query(UrunTablosu).filter(UrunTablosu.id == urun_id).first()


# ─────────────────────────────────────────────────────────────────────
# 5. PYTHON - CLASS (SINIF) TANIMLAMA SYNTAX'I
# ─────────────────────────────────────────────────────────────────────
# Temel nesne yönelimli programlama yapısı:

class Araba:
    # Başlatıcı (init) metot. Nesne ilk oluştuğunda çalışır.
    def __init__(self, marka, model):
        self.marka = marka                     # self. ile nesneye kaydedilir
        self.model = model
        self.hiz = 0

    # Sınıf içi fonksiyon (ilk parametre hep self olur!)
    def gaz_la(self, miktar):
        self.hiz += miktar
        return f"{self.marka} hızlandı. Yeni hız: {self.hiz} km/s"



