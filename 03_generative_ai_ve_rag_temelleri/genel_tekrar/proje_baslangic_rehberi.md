# 🚀 SIFIRDAN BİR BACKEND PROJESİNE BAŞLAMA REHBERİ

Yeni bir projeye başlarken paniklememek için her zaman aşağıdaki 5 adımlık kontrol listesini (checklist) sırasıyla takip edin.

---

## 1. Adım: Çalışma Alanını Kurmak (Klasör & Sanal Ortam)
Her yeni proje izole bir ortamda başlamalıdır.

1.  Masaüstünde yeni bir klasör oluşturun (Örn: `proje_sql_chat`).
2.  Terminalden bu klasörün içine girin.
3.  Python sanal ortamını (virtual environment) oluşturun ve aktifleştirin:
    ```powershell
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    ```
    *(Sanal ortam aktif olduğunda terminal satırının başında `(venv)` yazar).*

---

## 2. Adım: Bağımlılıkları Yüklemek
Projede kullanacağımız kütüphaneleri sanal ortama kurun:
```powershell
pip install fastapi uvicorn sqlalchemy psycopg2 google-genai pydantic
```

---

## 3. Adım: Veritabanı Bağlantısını Yapmak (`database.py`)
İlk kod dosyası her zaman veritabanı bağlantısıdır.

1.  `database.py` dosyasını oluşturun.
2.  `create_engine`, `sessionmaker` ve `declarative_base` yapılarını kurun.
3.  Veritabanı bağlantı adresini (`DATABASE_URL`) buraya ekleyin.

---

## 4. Adım: Tabloları Tanımlamak (`models.py`)
Veritabanında hangi verileri saklayacağımızı belirleriz.

1.  `models.py` dosyasını oluşturun.
2.  `database.py` içindeki `Base` sınıfını import edin.
3.  Tabloları sınıf (class) yapısıyla tanımlayın.
4.  Tabloları veritabanında oluşturmak için `main.py` veya `database.py` içinde şu komutu tetikleyin:
    ```python
    models.Base.metadata.create_all(bind=engine)
    ```

---

## 5. Adım: Akışı İnşa Etmek (`schemas.py` ➔ `crud.py` ➔ `main.py`)
Modeller tamamlandıktan sonra sırasıyla veri akışını yazarız:

1.  **`schemas.py`:** API istek ve yanıtlarının sınırlarını belirleyen Pydantic modellerini yazın.
2.  **`crud.py`:** Veritabanına kayıt ekleyen veya sorgu atan arka plan fonksiyonlarını hazırlayın.
3.  **`main.py`:** FastAPI sunucusunu ayağa kaldırın, rotaları ve endpoint'leri (`@app.get`, `@app.post`) tanımlayın.

---

## 🚀 Sunucuyu Çalıştırma
Her şey bittiğinde terminalde şu komutla sunucuyu ayağa kaldırın:
```powershell
uvicorn main:app --reload --port 8000
```
Tarayıcıdan `http://127.0.0.1:8000/docs` adresine giderek endpoint'lerinizi test edin.
