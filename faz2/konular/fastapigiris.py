from fastapi import FastAPI
from pydantic import BaseModel
import json
import os



# 1. FastAPI uygulamamızı başlatıyoruz
app = FastAPI()

class YeniGorevSemasi(BaseModel):
    baslik: str
    sure: int

DOSYA_YOLU = "faz2/konular/gorevler.json"

if os.path.exists(DOSYA_YOLU):
    with open(DOSYA_YOLU, "r", encoding="utf-8") as f:
        GOREVLER = json.load(f)
else:
    GOREVLER = [
        {"id": 1, "baslik": "Python Çalış", "tamamlandi": True},
        {"id": 2, "baslik": "FastAPI Öğren", "tamamlandi": False},
        {"id": 3, "baslik": "PostgreSQL Öğren", "tamamlandi": False}
    ]
    # İlk başta dosyayı oluşturalım
    with open(DOSYA_YOLU, "w", encoding="utf-8") as f:
        json.dump(GOREVLER, f, ensure_ascii=False, indent=4)


# 2. Ana dizine GET isteği geldiğinde çalışacak endpoint
@app.get("/")
def tum_gorevleri_getir():
    return GOREVLER

@app.get("/gorevler/{id}")
def tek_gorevi_getir(id:int):
    for gorev in GOREVLER:
        if gorev["id"] == id:
            return gorev
    return {"mesaj": "Gorev bulunamadı"}


@app.post("/gorevler")
def gorev_ekle(yeni_gorev: YeniGorevSemasi):
    # Pydantic gelen veriyi otomatik doğruladı!
    yeni_id = len(GOREVLER) + 1
    
    eklenecek_gorev = {
        "id": yeni_id,
        "baslik": yeni_gorev.baslik,  # nesne özelliklerine nokta ile erişiriz
        "tamamlandi": False
    }
    
    GOREVLER.append(eklenecek_gorev)
    # Değişikliği JSON dosyasına kaydediyoruz:
    with open(DOSYA_YOLU, "w", encoding="utf-8") as f:
        json.dump(GOREVLER, f, ensure_ascii=False, indent=4)
        
    return {"mesaj": "Görev başarıyla eklendi", "veri": eklenecek_gorev}
