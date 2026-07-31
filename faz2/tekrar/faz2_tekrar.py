# =====================================================================
# 🔵 FAZ 2 TEKRAR ÖDEVİ: UÇTAN UCA PROMPT SİSTEMİ
# =====================================================================
# Bu dosyada sırasıyla Pydantic, SQLAlchemy ve FastAPI konularını
# kapsayan görevleri tek tek yorum satırlarının altına kod yazarak tamamla.
#
# NOT: Kolayca test edebilmek için bulut veritabanı yerine bellek içi (in-memory)
# SQLite veritabanı ("sqlite:///:memory:") kullanacağız.
# =====================================================================

# GEREKLİ TÜM KÜTÜPHANE IMPORT'LARINI BURAYA YAZ:
# (ipucu: pydantic, sqlalchemy, fastapi, sqlalchemy.orm vb.)

# KODUNU BURAYA YAZ:



# =====================================================================
# 🛡️ BÖLÜM 1: PYDANTIC VERİ DOĞRULAMA (VALIDATION)
# =====================================================================
# GÖREV: 'PromptSemasi' adında bir Pydantic modeli tanımla.
# Kurallar:
# 1. 'baslik': En az 3, en fazla 50 karakter olmalı.
# 2. 'prompt_metni': En az 10 karakter olmalı.
# 3. 'zorluk': 1 ile 5 arasında (dahil) bir tam sayı olmalı (gt=0, lt=6).
# 4. Özel Doğrulayıcı (@field_validator): 'baslik' içinde "deneme" veya
#    "test" kelimeleri (büyük/küçük harf fark etmeksizin) geçiyorsa 
#    ValueError fırlatmalı.

# KODUNU BURAYA YAZ:



# =====================================================================
# 🗄️ BÖLÜM 2: SQLALCHEMY MODELLERİ & VERİTABANI BAĞLANTISI
# =====================================================================
# GÖREV: 
# 1. SQLite bellek içi ("sqlite:///:memory:") veritabanı motorunu (engine) kur.
# 2. SessionLocal oturum sınıfını tanımla.
# 3. Base sınıfını oluştur.
# 4. 'SQLPromptTablosu' adında bir veritabanı tablosu tanımla:
#    - id: primary key, otomatik artan sayı.
#    - baslik: string (boş olamaz).
#    - prompt_metni: text/string (boş olamaz).
#    - zorluk: integer.
# 5. Tüm tabloları veritabanında oluştur (create_all).
# 6. FastAPI için veritabanı oturumunu yöneten 'get_db' jeneratör (yield) fonksiyonunu yaz.

# KODUNU BURAYA YAZ:



# =====================================================================
# ✍️ BÖLÜM 3: CRUD İŞLEMLERİ (VERİTABANI EKLEME & LİSTELEME)
# =====================================================================
# GÖREV: 
# 1. 'prompt_ekle_db(db, prompt_data)' fonksiyonunu yaz:
#    - Girdi olarak veritabanı oturumu (db) ve Pydantic şeması (prompt_data) alsın.
#    - Veriyi veritabanına ekleyip kaydetsin (add, commit, refresh) ve nesneyi dönsün.
# 2. 'prompt_listele_db(db)' fonksiyonunu yaz:
#    - Veritabanındaki tüm prompt kayıtlarını çekip liste olarak dönsün.

# KODUNU BURAYA YAZ:



# =====================================================================
# 🚀 BÖLÜM 4: FASTAPI ENDPOINT'LERİ (API GİRİŞ KAPILARI)
# =====================================================================
# GÖREV:
# 1. Bir FastAPI uygulama örneği (app) oluştur.
# 2. 'POST /prompts' endpoint'ini yaz:
#    - Kullanıcıdan 'PromptSemasi' tipinde gövde (payload) alsın.
#    - 'Depends(get_db)' kullanarak veritabanı oturumunu enjekte etsin.
#    - CRUD fonksiyonunu çağırarak veriyi veritabanına eklesin.
#    - Geriye eklenen nesneyi ve 201 Created durum kodunu dönsün.
# 3. 'GET /prompts' endpoint'ini yaz:
#    - 'Depends(get_db)' kullansın.
#    - Veritabanındaki tüm promptları listelesin ve dönsün.

# KODUNU BURAYA YAZ:



# =====================================================================
# 🧪 BÖLÜM 5: TEST ÇALIŞTIRMA (HATA VE BAŞARI DURUMLARI)
# =====================================================================
# Bu bölümü değiştirme. Kendi yazdığın kodları test etmek için bu bloğu 
# kullanacağız. Kütüphaneleri ve endpoint'leri simüle eden test kodları:

if __name__ == "__main__":
    import uvicorn
    print("FastAPI Sunucusu Başlatılıyor...")
    print("Swagger Dokümantasyonu için tarayıcıda adrese gidin: http://127.0.0.1:8000/docs")
    # Sunucuyu başlatmak için aşağıdaki satırı kullanacağız
    # uvicorn.run(app, host="127.0.0.1", port=8000)
