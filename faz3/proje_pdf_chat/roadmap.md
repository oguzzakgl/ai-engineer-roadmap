# 🗺️ Phase 3 Capstone: PDF Chatbot Assistant (RAG) Roadmap

Bu projede, kullanıcının yüklediği herhangi bir PDF belgesini okuyan, parçalara ayıran, bunları buluttaki Neon PostgreSQL (`pgvector`) veritabanına kaydeden ve ardından kullanıcının bu PDF ile sohbet etmesini sağlayan modern bir web uygulaması (SaaS tarzı) geliştireceğiz.

---

## 🛠️ Teknoloji Yığını (Tech Stack)
* **Backend:** FastAPI (Python 3.13)
* **Veritabanı:** Neon PostgreSQL (`pgvector` eklentisiyle birlikte)
* **ORM:** SQLAlchemy (Raw SQL / ORM hibrit)
* **PDF Okuyucu:** `pypdf` kütüphanesi
* **Yapay Zeka:** Google `google-genai` SDK (`gemini-embedding-2` ve `gemini-3.5-flash`)
* **Frontend:** Modern CSS, HTML ve Vanilla JS (Vibrant Dark Mode, glassmorphism, responsive chat kabarcıkları)

---

## 📅 Yol Haritası ve Aşama Detayları

### 📍 Aşama 1: Proje Kurulumu & Bağımlılıklar
* [ ] Proje klasör yapısının oluşturulması
* [ ] Gerekli Python paketlerinin kurulması (`pypdf`, `fastapi`, `uvicorn`, vb.)
* [ ] Veritabanı bağlantı motorunun (`database.py`) hazırlanması

### 📍 Aşama 2: Veritabanı Katmanı & Tablolar (`models.py`)
* [ ] `pdf_dosyalari` tablosu (id, dosya_adi, yuklenme_tarihi)
* [ ] `pdf_paragraflar` tablosu (id, pdf_id, metin_icerigi, koordinat (VECTOR(3072)))
* [ ] pgvector eklentisinin otomatik açılması ve tabloların bulutta oluşturulması

### 📍 Aşama 3: PDF Parçalama (Chunking) & Vektörleştirme (`processor.py`)
* [ ] `pypdf` kütüphanesiyle yüklenen PDF'ten metin çıkarma
* [ ] Metinleri anlamsal bütünlüğü bozmadan 500-1000 karakterlik parçalara bölme (Chunking)
* [ ] Her bir parçayı `gemini-embedding-2` ile 3072 boyutlu vektöre çevirme
* [ ] Parçaları ve vektörleri toplu olarak (bulk insert) veritabanına kaydetme

### 📍 Aşama 4: RAG Arama ve Gemini Entegrasyonu (`main.py` / `crud.py`)
* [ ] `/upload-pdf` endpoint'i (PDF dosyasını yükleyip işleyecek)
* [ ] `/chat` endpoint'i:
  - Kullanıcının sorusunun vektörünü alacak
  - Bulut DB'de `<=>` operatörüyle en benzer 3 paragrafı çekecek
  - Bu paragrafları prompt'a kaynak bilgi olarak ekleyip Gemini'ye cevaplatacak

### 📍 Aşama 5: Premium Arayüz Geliştirme (`frontend/`)
* [ ] Modern karanlık mod (Dark mode), animasyonlu sürükle-bırak (drag-and-drop) PDF yükleme alanı
* [ ] Canlı yazma efekti (typing indicator) barındıran şık sohbet ekranı
* [ ] Yapay zekanın verdiği cevabın hangi sayfadan veya paragraftan alındığını gösteren "Kaynak Gösterimi" (Citations)
