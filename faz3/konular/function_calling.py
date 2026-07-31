# faz3/konular/function_calling.py
from google import genai

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
