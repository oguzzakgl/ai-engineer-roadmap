from sqlalchemy import text
from sqlalchemy.orm import Session
from models import PDFDosyaTablosu, PDFParagrafTablosu, MusteriTablosu, UrunTablosu, SiparisTablosu

# =====================================================================
# 🎯 TODO 9: PDF BENZERLİK ARAMASI (en_benzer_paragraflari_bul)
# =====================================================================
# (Referans: faz3/proje_pdf_chat/crud.py içindeki en_benzer_paragraflari_bul fonksiyonu.)
# =====================================================================

def en_benzer_paragraflari_bul(db:Session, soru_vektoru: list[float], limit:int=3) -> list[PDFParagrafTablosu]:

    soru_vektoru_str = str(soru_vektoru)

    sorgu = text("""
        SELECT id, pdf_id, metin_icerigi, embedding
        FROM pdf_paragraflar
        ORDER BY CAST(embedding AS vector) <=> :soru_vektoru
        LIMIT :limit
    """)

    sonuc = db.execute(sorgu, {"soru_vektoru": soru_vektoru_str, "limit": limit}).fetchall()
    
    paragraflar = []
    for row in sonuc:
        paragraf = PDFParagrafTablosu(
            id=row[0],
            pdf_id=row[1],
            metin_icerigi=row[2],
            embedding=row[3]
        )
        paragraflar.append(paragraf)
        
    return paragraflar

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
def dinamik_sql_calistir(db:Session, sql_sorgusu:str) -> list[dict]:
    sorgu = text(sql_sorgusu)

    sonuc = db.execute(sorgu).fetchall()

    kolonlar = list(sonuc[0]._mapping.keys()) if sonuc else []

    veriler = [dict(row._mapping) for row in sonuc]

    return veriler

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
def veritabani_seed_et(db: Session):
    # 1. Adım: Müşteri tablosu boş mu kontrolü
    if db.query(MusteriTablosu).first() is None:
        
        # 2. Adım: Örnek Müşteriler oluşturup ekliyoruz
        m1 = MusteriTablosu(ad="Ahmet Yılmaz", sehir="İstanbul")
        m2 = MusteriTablosu(ad="Mehmet Kaya", sehir="Ankara")
        m3 = MusteriTablosu(ad="Ayşe Demir", sehir="İzmir")
        m4 = MusteriTablosu(ad="Fatma Çelik", sehir="Bursa")
        m5 = MusteriTablosu(ad="Ali Öztürk", sehir="Antalya")
        db.add_all([m1, m2, m3, m4, m5])
        db.commit() # Müşterilerin ID'lerini (id: 1, 2, 3...) almak için commit ediyoruz

        # 3. Adım: Örnek Ürünler oluşturup ekliyoruz
        u1 = UrunTablosu(ad="Laptop", fiyat=25000.0, stok=10)
        u2 = UrunTablosu(ad="Akıllı Telefon", fiyat=15000.0, stok=20)
        u3 = UrunTablosu(ad="Kablosuz Kulaklık", fiyat=2000.0, stok=50)
        u4 = UrunTablosu(ad="Oyuncu Mouse", fiyat=1200.0, stok=40)
        u5 = UrunTablosu(ad="Mekanik Klavye", fiyat=2500.0, stok=15)
        db.add_all([u1, u2, u3, u4, u5])
        db.commit() # Ürünlerin ID'lerini almak için commit ediyoruz

        # 4. Adım: İlişkili Örnek Siparişleri ekliyoruz (Müşteri ve Ürün ID'lerini eşleştirerek)
        s1 = SiparisTablosu(musteri_id=m1.id, urun_id=u1.id, adet=1, tarih="2026-07-01")
        s2 = SiparisTablosu(musteri_id=m2.id, urun_id=u2.id, adet=2, tarih="2026-07-03")
        s3 = SiparisTablosu(musteri_id=m3.id, urun_id=u3.id, adet=5, tarih="2026-07-05")
        s4 = SiparisTablosu(musteri_id=m4.id, urun_id=u4.id, adet=1, tarih="2026-07-10")
        s5 = SiparisTablosu(musteri_id=m5.id, urun_id=u5.id, adet=2, tarih="2026-07-12")
        s6 = SiparisTablosu(musteri_id=m1.id, urun_id=u3.id, adet=1, tarih="2026-07-15")
        s7 = SiparisTablosu(musteri_id=m2.id, urun_id=u1.id, adet=1, tarih="2026-07-18")
        s8 = SiparisTablosu(musteri_id=m3.id, urun_id=u5.id, adet=3, tarih="2026-07-20")
        s9 = SiparisTablosu(musteri_id=m4.id, urun_id=u2.id, adet=1, tarih="2026-07-22")
        s10 = SiparisTablosu(musteri_id=m5.id, urun_id=u4.id, adet=4, tarih="2026-07-25")
        db.add_all([s1, s2, s3, s4, s5, s6, s7, s8, s9, s10])
        db.commit()

        print("✅ Veritabanı başarıyla örnek verilerle dolduruldu (Seed tamamlandı).")
