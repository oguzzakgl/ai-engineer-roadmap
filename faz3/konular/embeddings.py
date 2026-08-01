# faz3/konular/embeddings.py
from google import genai

# Gemini elçimizi başlatıyoruz.
client = genai.Client()

# embed_content fonksiyonunu çağırıyoruz.
# Neden? Metnimizi yapay zekanın anlamsal uzayındaki sayısal koordinatlara (vektörlere) çevirmek için.
response = client.models.embed_content(
    model='text-embedding-004',  # Google'ın resmi, güçlü embedding modeli
    contents='Yapay zeka backend mühendisliğini kolaylaştırıyor.'
)

# Gelen yanıtın içinden ilk metnin sayısal vektörünü çekiyoruz.
# Bu bize 768 adet float (ondalıklı) sayı içeren bir Python listesi verecek.
vektor = response.embeddings[0].values

print("Vektörün Boyutu (Boyut Sayısı):", len(vektor))  # Ekrana 768 basmalı.
print("\nKoordinatların İlk 5 Sayısı:")
print(vektor[:5])  # Devasa listenin sadece ilk 5 koordinatını önizliyoruz.
