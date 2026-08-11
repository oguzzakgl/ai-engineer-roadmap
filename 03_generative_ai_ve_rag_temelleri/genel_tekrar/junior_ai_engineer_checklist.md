# 📋 JUNIOR AI ENGINEER TEKNİK BİLGİ LİSTESİ (CHECKLIST)

Junior seviyesinde bir AI Product / Backend Engineer adayının mülakatlarda kesinlikle bilmesi gereken terimler, kavramlar ve çalışma mantıkları.

---

## 1. YAPAY ZEKA VE LLM KAVRAMLARI 🧠

*   **LLM (Large Language Model):** Milyarlarca kelimeyle eğitilmiş, bir sonraki kelimeyi tahmin etme mantığıyla çalışan dil modelleri (Gemini, Claude, GPT).
*   **Token (Simge):** Modellerin kelimeleri anlama birimi. 100 kelime yaklaşık 130 token eder. Giriş ve çıkış limitleri (context window) token cinsinden ölçülür.
*   **System Prompt:** Modele kimlik kazandıran ve uyması gereken kuralları belirleyen ana girdi.
*   **Temperature (Sıcaklık):** Modelin çıktılarındaki rastgeleliği belirler. 
    *   `0.0` ➔ Kesin, tutarlı, matematiksel çıktılar (SQL, kod yazımı için idealdir).
    *   `1.0+` ➔ Yaratıcı, sanatsal, değişken çıktılar.
*   **Structured Output (Yapılandırılmış Çıktı):** Modelden serbest metin yerine kesin bir JSON formatı (Örn: Pydantic şeması) dönmesini istemek.
*   **Hallucination (Halüsinasyon):** Modelin veritabanında veya bağlamında olmayan bir bilgiyi uydurarak doğruymuş gibi sunması.

---

## 2. RAG (RETRIEVAL-AUGMENTED GENERATION) TERİMLERİ 📂

*   **Semantic Search (Anlamsal Arama):** Anahtar kelimelere takılmadan, cümlenin arkasındaki anlama göre arama yapma.
*   **Embedding (Vektör Temsili):** Metinlerin yapay zekanın anlayacağı koordinat sayılarına (vektör listelerine) çevrilmesi.
*   **Chunking (Parçalama):** Büyük dökümanları anlamlı küçük parçalara (örneğin 800 karakterlik paragraflara) bölme işlemi.
*   **Overlap (Çakışma):** Parçalar bölünürken anlam bütünlüğü bozulmasın diye sınır kısımlarında bırakılan ortak karakter payı.
*   **Vector Database (Vektör Veritabanı):** Vektör embedding verilerini saklayan ve bunlar arasında hızlıca benzerlik araması (Kosinüs Benzerliği) yapan sistem (Örn: `pgvector`).
*   **Hybrid Search (Melez Arama):** Geleneksel anahtar kelime araması (keyword/BM25) ile vektörel (semantik) aramayı birleştirerek arama doğruluğunu en üst düzeye çıkarma yöntemi.

---

## 3. BACKEND & VERİTABANI TERİMLERİ 🕸️

*   **API (Application Programming Interface):** Arayüz ile sunucu (backend) arasındaki veri trafiğini sağlayan kapılar.
*   **FastAPI:** Hızlı, otomatik dökümantasyon üreten modern Python backend çatısı.
*   **Endpoint (Rota):** İstek atılan yollar (Örn: `POST /chat`).
*   **Pydantic:** Gelen verilerin doğruluğunu kontrol eden tip doğrulama kütüphanesi (`BaseModel`).
*   **SQLAlchemy (ORM):** Veritabanı tablolarını Python sınıfı (class) olarak tanımlamamızı ve ham SQL yazmadan veritabanı yönetmemizi sağlayan kütüphane.
*   **get_db (Dependency Injection):** Her API isteğinde veritabanı oturumunu otomatik açıp, işlem bitince güvenle kapatan mekanizma.

---

## 🛠️ GELİŞTİRİCİ ARAÇLARI (TOOLS)

*   **Git & GitHub:** Sürüm kontrolü ve kod paylaşım platformu.
*   **Swagger UI (`/docs`):** FastAPI'nin otomatik sunduğu, endpoint'leri tarayıcıdan test etmeye yarayan arayüz.
*   **`.env`:** API Key gibi hassas şifreleri kodun içine yazmayıp sunucu hafızasında gizleyen dosya.
