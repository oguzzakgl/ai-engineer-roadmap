# faz3/konular/structured_output.py
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

# Gemini'nin uymasını istediğimiz şablon:
class FilmAnalizi(BaseModel):
    film_adi: str
    tur: str
    ozet: str = Field(description="Filmin tek cümlelik kısa özeti")
    puan: int = Field(description="1-10 arasında filme verilen puan", ge=1, le=10)

# 1. Elçimizi (client) başlatıyoruz
client = genai.Client()

# 2. Gemini'ye isteği şablon ile birlikte gönderiyoruz
response = client.models.generate_content(
    model='gemini-3.5-flash',
    contents='Inception filmini analiz eder misin?',
    # Yapılandırma (config) kısmında şablonumuzu tanımlıyoruz:
    config=types.GenerateContentConfig(
        response_mime_type="application/json",  # Çıktının JSON olacağını zorunlu kılıyoruz
        response_schema=FilmAnalizi,           # Hangi şablona uyacağını söylüyoruz
    ),
)

# 3. Sonucu ekrana yazdırıyoruz
print("Gemini'den Gelen Yapılandırılmış JSON Yanıtı:")
print(response.text)


# ---------------------------------------------------------------------
# 🛠️ GELEN VERİYİ PYTHON'DA KULLANMA
# ---------------------------------------------------------------------

# 'json' kütüphanesini içe aktarıyoruz.
# Neden? Metin formatındaki JSON verisini Python sözlüğüne (dict) çevirmek için.
import json

# json.loads() fonksiyonunu kullanıyoruz.
# Neden? Gemini'den gelen ham metni (response.text) Python Sözlüğüne (Dictionary) dönüştürür.
film_sozlugu = json.loads(response.text)

# Artık verilere sözlük anahtarlarıyla erişebiliriz.
print("\n--- SÖZLÜK YÖNTEMİ ---")
print("Filmin Türü:", film_sozlugu["tur"])
print("Filmin Puanı:", film_sozlugu["puan"])


# 🌟 ALTERNATİF VE EN SENIOR YÖNTEM: Pydantic Nesnesine Çevirmek
# Neden? Sözlük yönteminde anahtar ismini yanlış yazarsak (örn: "tür" yerine "turr")
# Python bize hata vermez ama kod çalışma zamanında çöker. 
# Pydantic nesnesi ise bize otomatik tamamlama ve tip güvenliği (Type Safety) sağlar.
film_nesnesi = FilmAnalizi.model_validate_json(response.text)

print("\n--- PYDANTIC NESNESİ YÖNTEMİ ---")
# Nokta (.) koyarak verilere güvenle erişebiliriz, IDE bize otomatik tamamlar:
print("Film Adı:", film_nesnesi.film_adi)
print("Film Puanı:", film_nesnesi.puan)
