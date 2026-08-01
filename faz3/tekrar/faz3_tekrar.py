# faz3/tekrar/faz3_tekrar.py
# =====================================================================
# 🌟 FAZ 3: GENAI ENTEGRASYONU TEKRAR ÖDEVİ 🌟
# =====================================================================
# Bu dosyada Faz 3 boyunca öğrendiğimiz tüm temel kavramları tek bir
# şablon üzerinde uygulayarak tekrar edeceğiz. 
# Her adımın altındaki # TODO yorumlarını takip ederek kodları doldur.

from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# ---------------------------------------------------------------------
# TODO 1: GELÇİ (CLIENT) KURULUMU
# Gemini API ile konuşmamızı sağlayacak client nesnesini tanımla.
# ---------------------------------------------------------------------
client = genai.Client() # TODO: Buraya client başlatma kodunu yaz.
DATABASE_URL = "postgresql+psycopg2://neondb_owner:npg_tIU6WbK5ysYA@ep-noisy-shadow-ayl4dhke-pooler.c-5.us-east-2.aws.neon.tech/neondb?sslmode=require"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()



# =====================================================================
# 🎯 ADIM 1: STRUKTURED OUTPUTS (YAPILANDIRILMIŞ ÇIKTI)
# =====================================================================
# TODO 2: Bir kitap analizi için Pydantic şablonu (BaseModel) oluştur.
# Şablonda şu alanlar olsun:
# - kitap_adi (yazı)
# - yazar (yazı)
# - sayfa_sayisi (sayı)
# - ozet (yazı - Field açıklamasıyla birlikte)
# - puan (1-10 arası sayı - Field sınırlayıcılarıyla birlikte)
class KitapAnalizi(BaseModel):
    kitap_adi: str
    yazar: str
    sayfa_sayisi: int
    ozet: str = Field(description="Kitabın tek cümlelik kısa özeti")
    puan: int = Field(description="1-10 arasında kitaba verilen puan", ge=1, le=10)


def kitap_analiz_et():
    print("\n--- Adım 1: Kitap Analizi Yapılıyor ---")
    # TODO 3: Gemini'den "Sefiller" kitabı için KitapAnalizi şablonuna 
    # uygun bir JSON çıktısı iste ve ekrana yazdır.
    # Model olarak 'gemini-3.5-flash' kullan.
    response = client.models.generate_content(
        model='gemini-3.5-flash',
        contents="Sefiller kitabını analiz et.",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=KitapAnalizi,
        )
    )
    print(response.text)


# =====================================================================
# 🎯 ADIM 2: FUNCTION CALLING (ARAÇ KULLANIMI)
# =====================================================================
# TODO 4: Aşağıdaki gibi bir indirim hesaplama fonksiyonu tanımla.
# Fonksiyonun docstring açıklamasını ve parametre tipini eksiksiz yaz.
def indirim_hesapla(fiyat: float) -> str:
    """Verilen fiyat üzerinden %20 indirim hesaplar ve yeni fiyatı döner."""
    return f"{(fiyat * 0.80)} TL"


def indirim_asistani():
    print("\n--- Adım 2: İndirim Asistanı Çalışıyor ---")
    response = client.models.generate_content(
        model='gemini-3.5-flash',
        contents="1000 TL olan mont için indirim hesaplar mısın?",
        config=types.GenerateContentConfig(
            tools=[indirim_hesapla]
        )
    )
    print(response.text)


# =====================================================================
# 🎯 ADIM 3: EMBEDDING (VEKTÖRLEŞTİRME)
# =====================================================================
def embedding_test():
    print("\n--- Adım 3: Metin Vektörleştiriliyor ---")
    # TODO 6: "Python ile yapay zeka geliştirmek çok zevkli." cümlesinin 
    # 'gemini-embedding-2' modelini kullanarak embedding vektörünü al.
    # Vektörün boyutunu ve ilk 3 sayısını ekrana yazdır.
    response = client.models.embed_content(
        model='gemini-embedding-2',
        contents="Python ile yapay zeka geliştirmek çok zevkli."
    )
    vektor = response.embeddings[0].values
    print("Vektör Boyutu:", len(vektor))
    print("İlk 3 Sayı:", vektor[:3])


# =====================================================================
# 🎯 ADIM 4: VEKTÖR VERİTABANI (PGVECTOR) SQL SORGUSU
# =====================================================================
# TODO 7: Veritabanımızda 'koordinat' sütunundaki vektörlerle 
# ':soru_vektoru' parametresini Kosinüs Mesafesiyle karşılaştırıp, 
# en yakın 3 kaydı getiren ham SQL sorgusunu metin (string) olarak yaz.
sql_sorgusu = """
SELECT *, (koordinat <=> :soru_vektoru) AS mesafe 
FROM rehber 
ORDER BY mesafe
LIMIT 3; 
"""

# =====================================================================
# 🚀 ÇALIŞTIRMA KISMI
# =====================================================================
if __name__ == "__main__":
    kitap_analiz_et()
    indirim_asistani()
    embedding_test()

