# faz3/proje_sql_chat/crud.py
from sqlalchemy import text
from sqlalchemy.orm import Session
from models import PDFDosyaTablosu, PDFParagrafTablosu, MusteriTablosu, UrunTablosu, SiparisTablosu

# =====================================================================
# 🎯 TODO 9: PDF BENZERLİK ARAMASI (en_benzer_paragraflari_bul)
# =====================================================================
# (Referans: faz3/proje_pdf_chat/crud.py içindeki en_benzer_paragraflari_bul fonksiyonu.)
# =====================================================================


# =====================================================================
# 🎯 TODO 10: DİNAMİK SQL ÇALIŞTIRICI FONKSİYON (dinamik_sql_calistir)
# =====================================================================
# Girdi: db (Session), sql_sorgusu (Gemini'nin ürettiği ham SQL string'i)
# Çıktı: list[dict] (Veritabanından dönen satırların kolon isimleriyle eşleştiği liste)
#
# Adım 1: SQL sorgusunu text() fonksiyonu ile sarmalayarak db.execute() ile çalıştırın.
# Adım 2: Gelen sonuç nesnesinin kolon isimlerini (anahtarlarını) alın.
#        (İpucu: 'sonuc.keys()' ile kolon adlarını alabilirsiniz).
# Adım 3: Dönen satırları (.fetchall()) zip yardımıyla kolon isimleriyle eşleştirip 
#        birer Python sözlüğüne (dictionary) çevirin ve bir listede toplayın.
#        Örn: [{"urun_adi": "Laptop", "toplam_satis": 12}, ...]
# Adım 4: Bu sözlük listesini geriye dönün.
# =====================================================================


# =====================================================================
# 🎯 TODO 11: VERİTABANI ÖRNEK VERİ YÜKLEYİCİ (veritabani_seed_et)
# =====================================================================
# Girdi: db (Session)
# Amacı: Veritabanında MusteriTablosu, UrunTablosu ve SiparisTablosu boş ise 
#        içlerine 10-15 satırlık gerçekçi analiz yapabileceğimiz örnek veriler yazar.
#
# Adım 1: db.query(MusteriTablosu).first() yazarak tablonun boş olup olmadığını kontrol edin.
# Adım 2: Eğer boşsa:
#         - 5 adet örnek müşteri (ad, sehir) ekleyin ve db.add() yapın.
#         - 5 adet örnek ürün (ad, fiyat, stok) ekleyin ve db.add() yapın.
#         - db.commit() ve db.refresh() ile bunların ID'lerini alın.
#         - Bu ID'leri kullanarak 10 adet ilişkili örnek sipariş (musteri_id, urun_id, adet, tarih) 
#           ekleyin ve db.add() yapın.
# Adım 3: db.commit() ile tüm verileri Neon PostgreSQL veritabanına kaydedin.
# =====================================================================
