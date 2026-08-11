# 🗺️ MİMARİ DOSYA ÖZETLERİ VE GÖREVLERİ

Bu kılavuz, geliştirdiğimiz kurumsal AI asistanı projesinin hangi dosyasında ne yazılması gerektiğini ve bu dosyaların arka plandaki çalışma mantıklarını açıklar.

---

## 1. `database.py` ➔ Bağlantı Köprüsü 🔌
*   **Görevi:** Python kodumuz ile buluttaki (Neon PostgreSQL) veritabanımız arasındaki fiziksel bağlantı hattını kurar.
*   **İçindekiler:**
    *   `DATABASE_URL`: Veritabanı adresi.
    *   `engine`: Bağlantıyı yürüten motor.
    *   `SessionLocal`: Veritabanına her istek atacağımızda yeni bir oturum (temas) açan fabrika.
    *   `Base`: Tablo modellerimizin miras alacağı ortak SQLAlchemy sınıfı.
    *   `get_db()`: FastAPI rotalarında veritabanı bağlantısının otomatik açılıp güvenle kapatılmasını sağlayan fonksiyon.

---

## 2. `models.py` ➔ Tablo Tasarımları (Şema) 📐
*   **Görevi:** Veritabanımızda hangi tabloların olacağını, bu tabloların kolon adlarını ve veri tiplerini belirler.
*   **İçindekiler:**
    *   `MusteriTablosu` ➔ `musteriler` tablosu (id, ad, sehir).
    *   `UrunTablosu` ➔ `urunler` tablosu (id, ad, fiyat, stok).
    *   `SiparisTablosu` ➔ `siparisler` tablosu (id, musteri_id, urun_id, adet, tarih).

---

## 3. `schemas.py` ➔ Girdi / Çıktı Muhafızları 🛡️
*   **Görevi:** API'ye dış dünyadan gelen (Request) ve API'den dış dünyaya giden (Response) verilerin yapısını doğrular. JSON verisini Python nesnelerine dönüştürür.
*   **İçindekiler:**
    *   `ChatIstekRequest`: Kullanıcının tarayıcıdan gönderdiği soru formatı (`soru: str`).
    *   `ChatCevapResponse`: Sunucunun arayüze döneceği birleşik JSON formatı (niyet, cevap, sql_sorgusu, tablo_verisi, kaynaklar).

---

## 4. `crud.py` ➔ Arka Plan İş Emirleri (Veritabanı İşleri) ⚙️
*   **Görevi:** Doğrudan veritabanı üzerinde işlem yapan (veri ekleyen, veri çeken, SQL çalıştıran) tüm sorgu ve arama fonksiyonlarını barındırır.
*   **İçindekiler:**
    *   `dinamik_sql_calistir(db, sql_sorgusu)`: Yapay zekanın ürettiği SQL metnini veritabanında çalıştırıp satırları sözlük listesi (`list[dict]`) olarak dönen fonksiyon.
    *   *RAG projesinde:* `en_benzer_paragraflari_bul(db, embedding)`: Kosinüs benzerliği sorgusunu çalıştıran fonksiyon.

---

## 5. `main.py` ➔ Orkestra Şefi (Trafik Polisi) 🚥
*   **Görevi:** Kullanıcıdan gelen HTTP isteklerini karşılar, yapay zekayı (Gemini) devreye sokar, `crud.py` fonksiyonlarını çağırarak verileri işler ve sonucu arayüze döner.
*   **İçindekiler:**
    *   `FastAPI` uygulaması başlatma.
    *   `/chat` endpoint'i: Kullanıcı sorusunu alıp niyet analizi (BELGE_ARAMA / VERITABANI_ANALIZ) yapan ve doğru akışa yönlendiren ana fonksiyon.
    *   `/upload-pdf` endpoint'i: Kullanıcının yüklediği PDF dosyasını okuyup veritabanına kaydeden fonksiyon.
    *   `app.mount("/", StaticFiles(...))`: Arayüz (frontend) klasörünü sunucuya bağlayan kod.
