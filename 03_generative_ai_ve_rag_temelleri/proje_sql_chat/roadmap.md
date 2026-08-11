# 🗺️ Proje 2: AI-Powered Voice-to-SQL Analytics Dashboard Roadmap

Bu projede, kullanıcının yazılı veya sesli (mikrofondan konuşarak) olarak gönderdiği analiz sorularını Gemini kullanarak SQL sorgularına dönüştüren, bu sorguları Neon PostgreSQL veritabanımızda çalıştırıp dönen sonuçları modern grafiklerle (Chart.js) raporlayan bir otonom analiz paneli geliştireceğiz.

---

## 🛠️ Teknoloji Yığını (Tech Stack)
* **Backend:** FastAPI (Python 3.13)
* **Veritabanı:** Neon PostgreSQL
* **ORM / Veri Tabanı İletişimi:** SQLAlchemy
* **Yapay Zeka (AI):** Gemini 3.5-Flash (Hem metin hem de mikrofondan ses/ses dosyası girdi desteği ile)
* **Frontend:** Modern CSS, HTML, Vanilla JS, Chart.js (Grafik çizimleri için)

---

## 📂 Klasör Yapısı (Planlanan)
```text
faz3/proje_sql_chat/
├── database.py       # DB bağlantısı ve Session yönetimi
├── models.py         # Analiz yapacağımız örnek tablolar (Müşteriler, Ürünler, Siparişler)
├── schemas.py        # API Request/Response şemaları
├── crud.py           # DB üzerinde dinamik SQL çalıştıracak güvenli katman
├── main.py           # FastAPI uç noktaları (Sorgu API'si ve Arayüz sunumu)
├── roadmap.md        # Bu dosya
└── frontend/         # Arayüz dosyaları (HTML, CSS, JS, Grafikler)
```

---

## 📅 Yol Haritası ve Aşamalar

### 📍 Aşama 1: Veritabanı Tablo Tasarımları & Örnek Veriler (Seed Data)
* [ ] `models.py` içinde `MusteriTablosu`, `UrunTablosu` ve `SiparisTablosu` tablolarını oluşturmak.
* [ ] Veritabanında sorgulama yapabilmemiz için içerisine 15-20 satırlık gerçekçi örnek satış ve müşteri verileri (Seed Data) yüklemek.

### 📍 Aşama 2: Gemini Doğal Dil ➔ SQL Çevirici Motoru
* [ ] Gemini'ye veritabanı şemamızı (tablo ve kolon adlarını) öğreterek sadece geçerli SQL üretecek bir Prompt tasarlamak.
* [ ] Gemini'nin ürettiği SQL kodunun güvenli olup olmadığını (zararlı komutlar: DROP, DELETE, TRUNCATE vb. içerip içermediğini) denetleyecek güvenlik katmanı yazmak.

### 📍 Aşama 3: Akıllı Yönlendirici (Intent Router) ve Gemini SQL Entegrasyonu
* [ ] Gemini Structured Outputs ile niyet analizi (Intent Classifier) yapısını kurmak.
* [ ] Niyete göre soruyu RAG (PDF) veya SQL (Veritabanı) kanallarına yönlendirecek yönlendiriciyi yazmak.
* [ ] Gemini'ye veritabanı şemamızı öğretip, yazılı sorulardan güvenli SQL sorguları üretmesini sağlamak.

### 📍 Aşama 4: Dinamik SQL Çalıştırıcı & API
* [ ] Üretilen SQL sorgusunu PostgreSQL üzerinde koşturup sonuçları JSON listesi olarak dönecek yapıyı kurmak.
* [ ] Dönen SQL sonuçlarını Gemini'ye yorumlatarak doğal dilde özet yazdırmak.

### 📍 Aşama 5: Dashboard Arayüzü & Grafik Çizimi (Chart.js)
* [ ] Mor/Mavi tonlarda premium bir karanlık mod kontrol paneli (dashboard) arayüzü çizmek.
* [ ] Gelen analiz verilerini Chart.js ile dinamik çizgi, sütun ve pasta grafiklerine dönüştürmek.

---

## 🔮 Gelecek Geliştirmeler (Bonus Aşama)
* **Sesli Sorgulama (Voice-to-SQL):** Kullanıcının tarayıcıdan kaydettiği ses dosyasını Gemini'ye gönderip, Gemini'nin sesi dinleyerek SQL sorgusuna dönüştürmesini sağlamak.
