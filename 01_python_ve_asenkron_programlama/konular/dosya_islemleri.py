# TXT ve Metin Dosya İşlemleri (with open)

# 1. Dosyaya Yazma ("w" - Write)
with open("deneme.txt", "w", encoding="utf-8") as f:
    f.write("Merhaba, Python Yapay Zeka Yolculuğu!")

# 2. Dosyayı Okuma ("r" - Read)
with open("deneme.txt", "r", encoding="utf-8") as f:
    icerik: str = f.read()
    print("TXT İÇERİK:\n", icerik)

# 3. Dosyaya Ekleme Yapma ("a" - Append)
with open("deneme.txt", "a", encoding="utf-8") as f:
    f.write("\nYeni eklenen satır!")
