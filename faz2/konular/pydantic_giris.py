from pydantic import BaseModel, ValidationError, EmailStr, Field

class Kullanici(BaseModel):
    id: int
    isim: str
    yas: int | None = None  # Yaş bilgisi opsiyonel (boş olabilir)

# id değerine string olarak "123" veriyoruz:
k1 = Kullanici(id="123", isim="oguz")
print(k1.id)  # Çıktı: 123 (Otomatik olarak integer sayıya çevrildi!)


try:
    # id değerine harf gönderiyoruz (sayıya çevrilemez!)
    k2 = Kullanici(id="yuz-yirmi-uc", isim="oguz")
except ValidationError as e:
    print("Hata Yakalandı:\n", e)


class Urun(BaseModel):
    # En az 3, en fazla 50 karakterli bir isim olmalı
    ad: str = Field(min_length=3, max_length=50)
    
    # gt = greater than (0'dan büyük float olmalı)
    fiyat: float = Field(gt=0) 


class KullaniciGiris(BaseModel):
    email: EmailStr  # Otomatik email doğrulaması
    sifre: str = Field(min_length=8, description="En az 8 karakter olmalı")


# 1. Urun modelini hatalı fiyatla test edelim
print("\n--- Ürün Hata Testi ---")
try:
    # Fiyatı negatif veriyoruz (gt=0 kuralına aykırı!)
    u = Urun(ad="Laptop", fiyat=-500)
except ValidationError as e:
    print("Ürün Hatası:\n", e)

# 2. KullaniciGiris modelini hatalı e-posta ve kısa şifre ile test edelim
print("\n--- Giriş Hata Testi ---")
try:
    # E-postayı geçersiz formatta ve şifreyi 5 karakterli veriyoruz (min_length=8 olmalı!)
    g = KullaniciGiris(email="oguz-mail-degil", sifre="12345")
except ValidationError as e:
    print("Giriş Hatası:\n", e)
