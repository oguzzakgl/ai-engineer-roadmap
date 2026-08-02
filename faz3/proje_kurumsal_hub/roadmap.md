# 🗺️ Proje 2: Enterprise Q&A & Analytics Hub (Kurumsal Bilgi ve Analiz Portalı)

Bu projede, kurumsal bir şirketin hem yapısal olmayan verilerini (PDF prosedürleri, İK yönetmelikleri, kılavuzlar) hem de yapısal verilerini (satış veritabanı, üye listeleri, siparişler) tek bir sohbet arayüzünden sorgulatabilen hibrit bir yapay zeka portalı geliştireceğiz.

---

## 🛠️ Teknoloji Yığını (Tech Stack)
* **Backend:** FastAPI (Python 3.13)
* **Veritabanı:** Neon PostgreSQL (`pgvector` eklentisi ile birlikte)
* **ORM:** SQLAlchemy (ORM Modelleri ve Dinamik SQL Çalıştırıcı)
* **AI Yönlendirme & LLM:** Gemini 3.5-Flash (Metin sınıflandırma, SQL üretimi ve RAG cevaplama)
* **Arayüz (Frontend):** Modern CSS, HTML, Vanilla JS, Chart.js (Grafik görselleştirme)

---

## 📂 Klasör Yapısı
```text
faz3/proje_kurumsal_hub/
├── database.py       # DB bağlantısı ve Session
├── models.py         # 1) Satış Tabloları (SQL) 2) PDF & Paragraf Vektör Tabloları (Vector DB)
├── schemas.py        # API İstek/Yanıt Şemaları
├── crud.py           # Vektör Arama & Dinamik SQL Çalıştırma fonksiyonları
├── pdf_processor.py  # PDF yükleme, parçalama ve vektörleştirme (Önceki projeden entegre edilecek)
├── ai_router.py      # Gelen sorunun SQL'e mi yoksa PDF RAG'e mi gideceğine karar veren zeka
├── main.py           # FastAPI API uç noktaları
└── frontend/         # Grafik destekli, ses kayıt özellikli premium web arayüzü
```

---

## 📅 Yol Haritası ve Aşamalar

### 📍 Aşama 1: Kurumsal Veritabanı ve Şemanın Kurulması
* [ ] **SQL Tarafı (Yapısal Veriler):** `musteriler`, `urunler` ve `siparisler` tablolarını oluşturmak ve içine 20 satırlık örnek veri eklemek.
* [ ] **RAG Tarafı (Vektör Veriler):** `pdf_dosyalari` ve `pdf_paragraflar` tablolarını veritabanına eklemek.

### 📍 Aşama 2: AI Yönlendirici (Intent Router) Yazılması
* [ ] Kullanıcı sorusunu analiz ederek `SQL_QUERY` veya `DOCUMENT_RAG` yönlendirmesi yapacak `ai_router.py` dosyasını kodlamak.

### 📍 Aşama 3: Doğal Dil ➔ SQL Motoru & Güvenlik Duvarı
* [ ] Gemini'ye SQL şemasını öğretip güvenli SQL sorguları ürettirmek.
* [ ] DROP, DELETE, TRUNCATE gibi kurumsal verileri silebilecek tehlikeli komutları engelleyen güvenlik katmanı yazmak.

### 📍 Aşama 4: PDF RAG Entegrasyonu
* [ ] Önceki projede yazdığımız PDF okuma, parçalama ve vektör arama motorunu bu projeye adapte etmek.

### 📍 Aşama 5: API Uç Noktaları & Birleştirme
* [ ] `/upload-pdf` ve `/files` endpoint'lerini açmak.
* [ ] `/chat` endpoint'inde önce AI Router'ı çalıştırıp, çıkan karara göre SQL veya RAG sonucunu dönmek.

### 📍 Aşama 6: Dashboard Arayüzü & Chart.js Grafik Çizimi
* [ ] Sol paneli dosya listesi, sağ paneli ise geniş bir sohbet penceresi olan premium arayüz yapmak.
* [ ] Yapay zeka SQL veritabanından veri çektiğinde bunu dinamik olarak pasta/bar grafiklerine dönüştürmek.
