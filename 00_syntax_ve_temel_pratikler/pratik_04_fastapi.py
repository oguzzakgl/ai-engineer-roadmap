"""
🧩 Pratik #4: FastAPI Endpoint Yazma

Senaryo:
    FastAPI kullanarak bir şirket API'si yazıyoruz.
    Veritabanımızdaki ürünleri listeleyen ve yeni ürün ekleyen
    iki adet API endpoint'i yazman gerekiyor.

Önemli FastAPI Bilgileri (Kılavuz):
    1. Uygulama Tanımlama:
       app = FastAPI()

    2. GET Metodu (Veri Çekme):
       @app.get("/yol")
       def fonksiyon_adi():
           ...

    3. POST Metodu (Veri Gönderme):
       @app.post("/yol")
       def fonksiyon_adi(body_verisi: PydanticSemasi):
           ...

    4. Bağımlılık Enjeksiyonu (Dependency Injection - DB Bağlantısı):
       FastAPI'de veritabanı oturumuna erişmek içinDepends kullanırız:
       def endpoint_fonksiyonu(db: Session = Depends(get_db)):
           ...
"""

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

# FastAPI uygulamamızı başlatalım
app = FastAPI()


# SQLAlchemy için taklit (mock) veritabanı fonksiyonumuz
# Normalde bu database.py'den gelir
def get_db():
    # Bu bir taklit fonksiyondur, test için
    pass


# Yeni ürün eklerken doğrulama yapacağımız Pydantic Şeması
class UrunEkleRequest(BaseModel):
    ad: str
    fiyat: float
    stok: int


# =====================================================================
# SORU 1 (Kolay - GET):
# Tüm ürünleri listeleyen bir GET endpoint'i yaz.
# Yol (Route): "/urunler"
# Fonksiyon parametresi olarak veritabanı oturumunu (db: Session = Depends(get_db)) almalı.
# Fonksiyonun içinde db.query().all() çalıştırıp sonuçları dönmeli.
# Normalde urunler tablosu için SQLAlchemy modelimiz: UrunTablosu (mock edelim)
# =====================================================================
# MOCK model taklidi: db.query(UrunTablosu).all() şeklinde kullanılabilir.
class UrunTablosu:
    pass


# SORU 1 KODUNU BURAYA YAZ:
@app.get("/urunler")
def urunleri_listele(db: Session = Depends(get_db)):
    return db.query(UrunTablosu).all()


# =====================================================================
# SORU 2 (Orta - POST):
# Yeni ürün ekleyen bir POST endpoint'i yaz.
# Yol (Route): "/urunler"
# Fonksiyon parametresi olarak:
#   1. body verisini (request: UrunEkleRequest)
#   2. db oturumunu (db: Session = Depends(get_db)) almalı.
# Fonksiyonun içinde yeni bir UrunTablosu nesnesi oluşturup db'ye eklemeli ve kaydetmeli:
#   yeni_urun = UrunTablosu(ad=request.ad, fiyat=request.fiyat, stok=request.stok)
#   db.add(yeni_urun)
#   db.commit()
#   db.refresh(yeni_urun)
# =====================================================================

# SORU 2 KODUNU BURAYA YAZ:
@app.post("/urunler")
def yeni_urun_ekle(request: UrunEkleRequest, db: Session = Depends(get_db)):
    yeni_urun = UrunTablosu(ad=request.ad, fiyat=request.fiyat, stok=request.stok)
    db.add(yeni_urun)
    db.commit()
    db.refresh(yeni_urun)
    return yeni_urun
