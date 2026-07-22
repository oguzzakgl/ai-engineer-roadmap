# =====================================================================
# 🟢 FAZ 1 GENEL TEKRAR VE PEKİŞTİRME ÇALIŞMASI
# =====================================================================
# Bu dosyada Faz 1'deki 4 ana konuyu özetledim.
# Her yorum satırının altındaki boşluğa ilgili kodu kendin yazacaksın.
# =====================================================================
import json
import asyncio

# ---------------------------------------------------------------------
# 📝 BÖLÜM 1: TYPE HINTING (TİP BELİRTEÇLERİ)
# ---------------------------------------------------------------------
# Soru:
# 1. 'ad' adında bir string ve 'yas' adında bir integer değişkeni tanımla ve tip belirt.
# 2. İki sayıyı toplayıp geriye float döndüren 'sayi_topla' adında bir fonksiyon yaz.
#    Fonksiyon parametreleri ve dönüş tipi mutlaka type hint içermeli.

# KODUNU BURAYA YAZ:

ad: str = "Oğuz"
yas: int = 25

def sayi_topla(sayi1: float, sayi2: float) -> float:
    return sayi1 + sayi2


# ---------------------------------------------------------------------
# 💾 BÖLÜM 2: DOSYA VE JSON İŞLEMLERİ
# ---------------------------------------------------------------------
# Soru:
# 1. Bir Python sözlüğü (dict) oluştur: {"kitap": "Suç ve Ceza", "yazar": "Dostoyevski"}
# 2. Bu sözlüğü 'json.dumps' ile JSON metnine (string) çevir ve ekrana yazdır.
# 3. 'with open' kullanarak 'kitap.txt' adında bir dosya oluştur ve içine "En sevdiğim kitap" yaz.

# KODUNU BURAYA YAZ:

kutuphane = {
    "kitap": "Suç ve Ceza",
    "yazar": "Dostoyevski"
}

json_metni = json.dumps(kutuphane, ensure_ascii=False, indent=4)

print(json_metni)

with open("kitap.txt", "w", encoding="utf-8") as f:
    f.write("En sevdiğim kitap")


# ---------------------------------------------------------------------
# ⚠️ BÖLÜM 3: HATA YÖNETİMİ (EXCEPTION HANDLING)
# ---------------------------------------------------------------------
# Soru:
# 1. 'try...except' yapısı kullanarak 10 sayısını 0'a bölmeyi dene.
# 2. 'ZeroDivisionError' hatasını yakala ve ekrana "0'a bölünme hatası!" yazdır.
# 3. 'finally' bloğu ekleyerek ekrana "Bölme işlemi denendi." yazdır.

# KODUNU BURAYA YAZ:

a = 12
b = 0

try:
    sonuc = a / b
except ZeroDivisionError:
    print("0'a bölünme hatası!")
finally:
    print("Bölme işlemi denendi.")


# ---------------------------------------------------------------------
# ⏳ BÖLÜM 4: ASENKRON PYTHON (ASYNCIO)
# ---------------------------------------------------------------------
# Soru:
# 1. Asenkron bir fonksiyon tanımla: 'async def selam_ver()'
# 2. Fonksiyonun içinde 1 saniye asenkron bekleme yap (asyncio.sleep).
# 3. Ekrana "Merhaba Asenkron Dünya!" yazdır.
# 4. En dışarıda bu fonksiyonu 'asyncio.run()' kullanarak çalıştır.

# KODUNU BURAYA YAZ:

async def selam_ver():
    await asyncio.sleep(3)
    print("Merhaba Asenkron Dünya!")

asyncio.run(selam_ver())

