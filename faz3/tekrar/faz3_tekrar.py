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

# ---------------------------------------------------------------------
# TODO 1: GELÇİ (CLIENT) KURULUMU
# Gemini API ile konuşmamızı sağlayacak client nesnesini tanımla.
# ---------------------------------------------------------------------
client = None # TODO: Buraya client başlatma kodunu yaz.


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
    pass # TODO: Alanları tanımla.


def kitap_analiz_et():
    print("\n--- Adım 1: Kitap Analizi Yapılıyor ---")
    # TODO 3: Gemini'den "Sefiller" kitabı için KitapAnalizi şablonuna 
    # uygun bir JSON çıktısı iste ve ekrana yazdır.
    # Model olarak 'gemini-3.5-flash' kullan.
    pass


# =====================================================================
# 🎯 ADIM 2: FUNCTION CALLING (ARAÇ KULLANIMI)
# =====================================================================
# TODO 4: Aşağıdaki gibi bir indirim hesaplama fonksiyonu tanımla.
# Fonksiyonun docstring açıklamasını ve parametre tipini eksiksiz yaz.
def indirim_hesapla(fiyat: float) -> str:
    """Verilen fiyat üzerinden %20 indirim hesaplar ve yeni fiyatı döner."""
    pass # TODO: Fiyatın %20 indirimli halini hesapla ve string olarak geri dön.


def indirim_asistani():
    print("\n--- Adım 2: İndirim Asistanı Çalışıyor ---")
    # TODO 5: Gemini'ye "1000 TL olan mont için indirim hesaplar mısın?" sorusunu sor.
    # Yukarıda tanımladığın 'indirim_hesapla' fonksiyonunu Gemini'ye araç (tool) olarak ver.
    # Son cevabı ekrana yazdır.
    pass


# =====================================================================
# 🎯 ADIM 3: EMBEDDING (VEKTÖRLEŞTİRME)
# =====================================================================
def embedding_test():
    print("\n--- Adım 3: Metin Vektörleştiriliyor ---")
    # TODO 6: "Python ile yapay zeka geliştirmek çok zevkli." cümlesinin 
    # 'gemini-embedding-2' modelini kullanarak embedding vektörünü al.
    # Vektörün boyutunu ve ilk 3 sayısını ekrana yazdır.
    pass


# =====================================================================
# 🎯 ADIM 4: VEKTÖR VERİTABANI (PGVECTOR) SQL SORGUSU
# =====================================================================
# TODO 7: Veritabanımızda 'koordinat' sütunundaki vektörlerle 
# ':soru_vektoru' parametresini Kosinüs Mesafesiyle karşılaştırıp, 
# en yakın 3 kaydı getiren ham SQL sorgusunu metin (string) olarak yaz.
sql_sorgusu = """
-- TODO: Buraya pgvector kosinüs mesafesi sorgusunu yaz.
"""

# =====================================================================
# 🚀 ÇALIŞTIRMA KISMI
# =====================================================================
if __name__ == "__main__":
    # Testleri sırayla çalıştıracağız. Doldurdukça yorum satırlarını kaldırabilirsin.
    pass
    # kitap_analiz_et()
    # indirim_asistani()
    # embedding_test()
