"""
🧩 Pratik #5: Nesne Yönelimli Programlama (Python Classes / OOP)

Senaryo:
    Yazılım mülakatlarında nesne yönelimli programlama (OOP) mantığı
    çok sık sorulur. Biz de projemizde modellerimizi tanımlarken
    SQLAlchemy sınıfları (MusteriTablosu vb.) kullandık.

Senden İstenen:
    Temel bir `Musteri` sınıfı (Class) oluşturman ve bu sınıfın
    içine bazı metotlar (fonksiyonlar) yazman.

Önemli OOP Bilgileri (Kılavuz):
    1. Sınıf Tanımlama:
       class SinifAdi:
           ...

    2. Başlatıcı Metot (__init__):
       Sınıftan yeni bir nesne üretildiğinde otomatik çalışan metottur.
       Değerleri nesneye kaydetmek için `self` kullanılır.
       
       def __init__(self, ad, sehir):
           self.ad = ad
           self.sehir = sehir

    3. Sınıf İçi Metotlar (Functions):
       Sınıf içindeki her fonksiyonun ilk parametresi `self` olmalıdır.
       Bu sayede nesnenin kendi bilgilerine (self.ad vb.) erişebilir.

       def kendini_tanit(self):
           return f"Benim adım {self.ad}"
"""


# =====================================================================
# SORU 1:
# Bir "Musteri" sınıfı tanımla.
# Bu sınıf başlatılırken (init metodunda) şu 3 bilgiyi alsın ve kaydetsin:
#   - ad
#   - sehir
#   - bakiye (varsayılan değeri 0.0 olsun)
# =====================================================================

# SORU 1 KODUNU BURAYA YAZ:
# 
class Musteri:
    def  __init__(self, ad, sehir, bakiye=0):
        self.ad=ad
        self.sehir=sehir
        self.bakiye=bakiye
# =====================================================================
# SORU 2:
# Musteri sınıfının içine iki metot yaz:
#   1. para_yukle(self, miktar):
#      Müşterinin bakiyesine gelen miktarı eklesin (self.bakiye += miktar).
#
#   2. harcama_yap(self, miktar):
#      Müşterinin bakiyesinden harcanan miktarı düşsün.
#      Ancak bakiye miktardan az ise "Yetersiz bakiye!" diye bir hata fırlatsın (ValueError).
# =====================================================================

# SORU 2 KODUNU BURAYA YAZ / SORU 1'DEKİ SINIFIN İÇİNE EKLE:
# 
    def para_yukle(self,miktar):
        self.bakiye +=miktar

    def harcama_yap(self,miktar):
        if self.bakiye >= miktar:
            self.bakiye -=miktar
        else:
            raise ValueError("Yetersiz bakiye!")

# =====================================================================
# TEST - Dosyayı çalıştır: python pratik/pratik_05_class.py
# =====================================================================
if __name__ == "__main__":
    try:
        # Test 1: Müşteri oluşturma
        m = Musteri(ad="Ahmet", sehir="Istanbul", bakiye=100.0)
        print(f"Müşteri: {m.ad}, Şehir: {m.sehir}, Bakiye: {m.bakiye} TL")

        # Test 2: Para yükleme
        m.para_yukle(50.0)
        print(f"Yeni Bakiye (Yükleme sonrası): {m.bakiye} TL (Beklenen: 150.0)")

        # Test 3: Harcama yapma
        m.harcama_yap(70.0)
        print(f"Yeni Bakiye (Harcama sonrası): {m.bakiye} TL (Beklenen: 80.0)")

        # Test 4: Yetersiz bakiye kontrolü
        print("\nYetersiz bakiye testi yapılıyor...")
        m.harcama_yap(200.0)
    except NameError:
        print("\nHata: 'Musteri' sınıfı henüz tanımlanmamış!")
    except ValueError as e:
        print(f"Hata yakalandı (Beklenen): {e} ✅")
