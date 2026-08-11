from google import genai
from google.genai import types  # <--- Bu satırı ekliyoruz

# Gemini'ye sunacağımız Python fonksiyonunu tanımlıyoruz.
# Neden? Yapay zeka stok sormak istediğinde bu fonksiyonu çağıracak.
# Önemli: Fonksiyonun parametrelerinin tipleri (str, int) ve docstring'i (açıklama metni)
# mutlaka yazılmalıdır. Çünkü Gemini bu açıklamaları okuyarak fonksiyonun ne işe yaradığını anlar!
def stok_kontrol_et(urun_adi: str) -> str:
    """Belirtilen ürünün depodaki güncel stok durumunu döner."""
    
    # Küçük harfe çevirip basitçe kontrol ediyoruz (Simüle edilmiş veritabanı)
    urun = urun_adi.lower()
    if "iphone" in urun:
        return "Stokta 5 adet iPhone var."
    elif "macbook" in urun:
        return "Stokta 2 adet Macbook var."
    else:
        return f"Maalesef {urun_adi} stoklarımızda bulunmuyor."


# 1. Gemini elçimizi (client) başlatıyoruz.
# Neden? API ile haberleşmeyi kurmak için.
client = genai.Client()

# 2. Gemini'ye sorumuzu ve kullanabileceği araçları (tools) gönderiyoruz.
response = client.models.generate_content(
    model='gemini-3.5-flash',
    contents='Depomuzda Macbook var mı, stok durumu nedir?',
    # config içinde tools listesine fonksiyonumuzu ekliyoruz:
    config=types.GenerateContentConfig(
        tools=[stok_kontrol_et]  # Gemini'ye "Bu fonksiyonu kullanabilirsin" yetkisi veriyoruz.
    )
)

# 3. Gelen yanıtı kontrol ediyoruz.
print("Gemini'nin Son Cevabı:")
print(response.text)
