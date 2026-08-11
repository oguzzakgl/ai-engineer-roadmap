# faz3/konular/canli_sohbet.py
from google import genai

# 1. Gemini client'ımızı başlatıyoruz.
client = genai.Client()

# 2. Canlı sohbet oturumu (Chat Session) başlatıyoruz.
# Neden? Bu nesne sohbet geçmişini (hafızayı) arka planda otomatik olarak tutar.
chat = client.chats.create(model="gemini-3.5-flash")

print("====================================================")
print("🤖 Canlı Gemini Sohbet Odasına Hoş Geldiniz!")
print("Çıkmak için 'cikis', 'exit' veya 'quit' yazabilirsiniz.")
print("====================================================\n")

while True:
    # Kullanıcıdan terminal girdisi alıyoruz (Sen:)
    kullanici_girdisi = input("Sen: ")
    
    # Çıkış kelimelerinden birini yazdıysa döngüyü bitiriyoruz
    if kullanici_girdisi.strip().lower() in ["cikis", "exit", "quit"]:
        print("\n🤖 Gemini: Görüşmek üzere, harika bir gün dilerim!")
        break
        
    # Boş mesaj yollanmasını engelliyoruz
    if not kullanici_girdisi.strip():
        continue
        
    # Gemini'ye mesajı gönderiyoruz
    # send_message() metodu hem mesajı yollar, hem de geçmişe kaydeder.
    response = chat.send_message(kullanici_girdisi)
    
    # Cevabı ekrana yazdırıyoruz
    print(f"Gemini: {response.text}\n")
