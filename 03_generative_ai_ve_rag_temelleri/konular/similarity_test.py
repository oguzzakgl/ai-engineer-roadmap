# faz3/konular/similarity_test.py
import math
from google import genai

# Gemini elçimizi başlatıyoruz.
client = genai.Client()

# Matematiksel Kosinüs Benzerliği (Cosine Similarity) Fonksiyonu:
# Neden? İki adet 3072 boyutlu sayı listesini (vektörü) alır ve aralarındaki anlamsal yakınlığı
# -1 ile 1 arasında bir skor olarak hesaplar. 1'e ne kadar yakınsa, cümleler o kadar benzerdir.
def kosinus_benzerligi(vektor_a, vektor_b):
    # İki vektörün karşılıklı sayılarının çarpımlarının toplamı (Dot Product)
    dot_product = sum(a * b for a, b in zip(vektor_a, vektor_b))
    
    # Vektör A'nın matematiksel büyüklüğü (boyu)
    magnitude_a = math.sqrt(sum(a * a for a in vektor_a))
    
    # Vektör B'nin matematiksel büyüklüğü (boyu)
    magnitude_b = math.sqrt(sum(b * b for b in vektor_b))
    
    # Sıfıra bölme hatasını engellemek için kontrol
    if not magnitude_a or not magnitude_b:
        return 0.0
        
    # Kosinüs benzerliği formülü
    return dot_product / (magnitude_a * magnitude_b)


# Gemini'den embedding vektörü alan yardımcı fonksiyon
# Neden? Kod tekrarını önlemek için embedding alma işlemini tek bir fonksiyona topluyoruz.
def vektor_al(metin: str):
    response = client.models.embed_content(
        model='gemini-embedding-2',
        contents=metin
    )
    return response.embeddings[0].values


# ---------------------------------------------------------------------
# 🚀 ANLAMSAL ARAMA DENEYİ
# ---------------------------------------------------------------------

# Kullanıcının arama yaptığı cümle (Referans)
referans_cumle = "Evimde sevimli bir köpek besliyorum."

# Karşılaştıracağımız iki farklı cümle
cumle_benzer = "Bahçede oynayan küçük bir kedi var."  # Anlamsal olarak yakın (Evcil hayvan)
cumle_uzak = "Yarın yeni bir bilgisayar satın alacağım." # Anlamsal olarak tamamen uzak (Teknoloji)

print("Cümlelerin vektörleri alınıyor (Lütfen bekleyin)...")
v_referans = vektor_al(referans_cumle)
v_benzer = vektor_al(cumle_benzer)
v_uzak = vektor_al(cumle_uzak)

# Benzerlik skorlarını hesaplıyoruz
skor_benzer = kosinus_benzerligi(v_referans, v_benzer)
skor_uzak = kosinus_benzerligi(v_referans, v_uzak)

print("\n--- DENEY SONUÇLARI ---")
print(f"Referans Cümle: '{referans_cumle}'\n")

print(f"1. Cümle: '{cumle_benzer}'")
print(f"--> Yakınlık Derecesi: {skor_benzer:.4f} (1'e ne kadar yakınsa o kadar benzerdir)\n")

print(f"2. Cümle: '{cumle_uzak}'")
print(f"--> Yakınlık Derecesi: {skor_uzak:.4f}")
