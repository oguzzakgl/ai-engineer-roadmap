# Hata Yönetimi (try...except...else...finally...Custom Exception)

# 1. Sıfıra Bölme Hatası (ZeroDivisionError) Yakalama
try:
    sayi1: int = 10
    sayi2: int = 0
    sonuc: float = sayi1 / sayi2
    print("Sonuç:", sonuc)
except ZeroDivisionError:
    print("⚠️ Hata Yakalandı: Bir sayı 0'a bölünemez!")


# 2. Çoklu Hata Yakalama Örneği
print("\n--- 2. Çoklu Hata Yakalama Testi ---")
try:
    with open("olmayan_dosya.txt", "r", encoding="utf-8") as f:
        icerik = f.read()
except FileNotFoundError:
    print("⚠️ Hata: Aradığınız dosya sistemde bulunamadı!")
except Exception as e:
    print(f"⚠️ Bilinmeyen bir hata oluştu: {e}")


# 3. try...except...else...finally Tam Yapısı
print("\n--- 3. else ve finally Bloğu Testi ---")

def kullanici_yas_kontrol(girilen_yas: str) -> None:
    try:
        # Metni sayıya çevirmeyi deniyoruz
        yas: int = int(girilen_yas)
    except ValueError:
        # Hata VARSA çalışır
        print(f"❌ Hata: '{girilen_yas}' bir sayı değildir!")
    else:
        # Hata YOKSA (başarılıysa) çalışır
        print(f"🎉 Başarılı! Kullanıcının yaşı: {yas}")
    finally:
        # Hata çıksa da çıkmasa da HER ZAMAN çalışır
        print("🔒 [Sistem]: Yaş doğrulama işlemi sonlandı.\n")

# Hatalı Girdi Testi (ValueError tetikler)
kullanici_yas_kontrol("yirmibes")

# Başarılı Girdi Testi (else bloğu çalışır)
kullanici_yas_kontrol("25")


# 4. Özel Hata Sınıfı (Custom Exception) ve raise Kullanımı
print("--- 4. Özel Hata Sınıfları (Custom Exception) ---")

# Kendi özel hata sınıfımızı yazıyoruz (Exception sınıfından türetiyoruz)
class GecersizYasHatasi(Exception):
    """Yaş değeri negatif olduğunda fırlatılacak özel hata sınıfı."""
    pass

def yas_dogrula(yas: int) -> None:
    if yas < 0:
        # Kendi özel hatamızı fırlatıyoruz!
        raise GecersizYasHatasi("Yaş değeri negatif bir sayı olamaz!")
    print(f"✅ Kayıt Başarılı, Kullanıcı Yaşı: {yas}")

try:
    yas_dogrula(-5)  # Negatif yaş girdik, özel hatamızı tetikleyecek
except GecersizYasHatasi as e:
    print(f"⚠️ Özel Hata Yakalandı: {e}")
