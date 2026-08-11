# =====================================================================
# 🔵 FAZ 2 - KONU 2.4: SIFIRDAN RAW (HAM) SQL TEMELLERİ
# =====================================================================
# Bu dosyada bulut veritabanımıza SQLAlchemy ORM kullanmadan,
# doğrudan ham (raw) SQL komutları göndererek veri ekleyecek, 
# listeleyecek, güncelleyecek ve sileceğiz.
# =====================================================================

import os
from sqlalchemy import create_engine, text

# Bulut veritabanı adresimiz (pythonDev projesi)
DATABASE_URL = "postgresql+psycopg2://neondb_owner:npg_tIU6WbK5ysYA@ep-noisy-shadow-ayl4dhke-pooler.c-5.us-east-2.aws.neon.tech/neondb?sslmode=require"
engine = create_engine(DATABASE_URL)

# Tabloları temizlemek ve sıfırdan oluşturmak için başlangıç kurulumu
with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS promptlar CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS categories CASCADE;"))
    
    # Kategori tablosunu oluşturma (SQL komutuyla)
    conn.execute(text("""
        CREATE TABLE categories (
            id SERIAL PRIMARY KEY,
            ad VARCHAR(50) UNIQUE NOT NULL
        );
    """))
    
    # Promptlar tablosunu oluşturma (SQL komutuyla)
    conn.execute(text("""
        CREATE TABLE promptlar (
            id SERIAL PRIMARY KEY,
            baslik VARCHAR(100) NOT NULL,
            prompt_metni TEXT NOT NULL,
            begeni_sayisi INTEGER DEFAULT 0,
            kategori_id INTEGER REFERENCES categories(id) ON DELETE CASCADE
        );
    """))
    conn.commit()
    print("Tablolar sıfırlandı ve SQL ile yeniden oluşturuldu!")


# ---------------------------------------------------------------------
# 📝 BÖLÜM 1: INSERT (VERİ EKLEME)
# ---------------------------------------------------------------------
# Kural: INSERT INTO tablo_adi (kolon1, kolon2) VALUES (deger1, deger2);
# ---------------------------------------------------------------------
# ÖDEV: 
# 1. 'categories' tablosuna 'Yazılım' kategorisini ekle.
# 2. 'categories' tablosuna 'Tasarım' kategorisini ekle.
# KODUNU AŞAĞIDAKİ TIKNAKLARIN İÇİNE YAZ:

sorgu_kategori_ekle = """
-- SQL KODUNU BURAYA YAZ
"""


# ---------------------------------------------------------------------
# 📝 BÖLÜM 2: SELECT (VERİ OKUMA) & WHERE (FİLTRELEME)
# ---------------------------------------------------------------------
# Kural: SELECT kolon1, kolon2 FROM tablo_adi WHERE kosul;
# ---------------------------------------------------------------------
# ÖDEV: 
# 1. Kategori tablosundaki tüm sütunları çek.
# KODUNU AŞAĞIDAKİ TIKNAKLARIN İÇİNE YAZ:

sorgu_kategori_listele = """
-- SQL KODUNU BURAYA YAZ
"""


# ---------------------------------------------------------------------
# 🚀 ÇALIŞTIRMA VE TEST ALANI
# ---------------------------------------------------------------------
# Aşağıdaki fonksiyon yazdığın SQL komutlarını veritabanında çalıştırır.
# ---------------------------------------------------------------------

def sql_calistir(sorgu_metni, aciklama):
    if not sorgu_metni.strip() or "BURAYA YAZ" in sorgu_metni:
        return
    print(f"\n--- {aciklama} ---")
    with engine.connect() as conn:
        result = conn.execute(text(sorgu_metni))
        conn.commit()
        
        # Eğer bir select sorgusuysa sonuçları ekrana yazdır
        if sorgu_metni.strip().lower().startswith("select"):
            rows = result.fetchall()
            for r in rows:
                print(r)
        else:
            print("Sorgu başarıyla çalıştırıldı (Değişiklik kaydedildi).")

# Testleri çalıştırmak için aşağıdaki yorum satırlarını kaldırabilirsin:
# sql_calistir(sorgu_kategori_ekle, "Kategori Ekleme İşlemi")
# sql_calistir(sorgu_kategori_listele, "Kategori Listeleme Sonuçları")
