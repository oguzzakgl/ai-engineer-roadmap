# =====================================================================
# 📖 SQL REFERANS KILAVUZU
# Bu dosyayı pratik sorularını çözerken yanında açık tut.
# =====================================================================


# ─────────────────────────────────────────────────────────────────────
# 1. TEMEL SELECT
# ─────────────────────────────────────────────────────────────────────
# Tablodaki tüm sütunları getir:
#   SELECT * FROM musteriler;

# Belirli sütunları getir:
#   SELECT id, ad FROM musteriler;

# Sütuna takma ad (alias) ver:
#   SELECT ad AS musteri_adi FROM musteriler;


# ─────────────────────────────────────────────────────────────────────
# 2. WHERE - Filtreleme
# ─────────────────────────────────────────────────────────────────────
#   SELECT * FROM musteriler WHERE sehir = 'Istanbul';
#   SELECT * FROM urunler WHERE fiyat > 100;
#   SELECT * FROM urunler WHERE stok > 0 AND fiyat < 500;


# ─────────────────────────────────────────────────────────────────────
# 3. JOIN - Tabloları Birleştirme
# ─────────────────────────────────────────────────────────────────────
# Mantık: "siparisler tablosundaki her satır için,
#          musteri_id'si eşleşen musteriler satırını yanına ekle."

#   SELECT s.id, m.ad, s.adet
#   FROM siparisler s           ← s: siparisler tablosunun kısaltması
#   JOIN musteriler m           ← m: musteriler tablosunun kısaltması
#   ON s.musteri_id = m.id;     ← bağlantı noktası

# 2 JOIN aynı anda (3 tablo):
#   SELECT s.id, m.ad, u.ad, s.adet
#   FROM siparisler s
#   JOIN musteriler m ON s.musteri_id = m.id
#   JOIN urunler u    ON s.urun_id    = u.id;


# ─────────────────────────────────────────────────────────────────────
# 4. GROUP BY + Aggregate Fonksiyonlar
# ─────────────────────────────────────────────────────────────────────
# Mantık: "Aynı şehirdeki müşterileri bir grup yap, her grubun sayısını ver."

# COUNT → Kaç satır var?
#   SELECT sehir, COUNT(*) AS musteri_sayisi
#   FROM musteriler
#   GROUP BY sehir;

# SUM → Gruptaki sayıları topla:
#   SELECT musteri_id, SUM(adet) AS toplam_adet
#   FROM siparisler
#   GROUP BY musteri_id;

# AVG, MAX, MIN de kullanılabilir:
#   SELECT urun_id, AVG(adet) AS ortalama_adet, MAX(adet) AS en_fazla
#   FROM siparisler
#   GROUP BY urun_id;


# ─────────────────────────────────────────────────────────────────────
# 5. ORDER BY - Sıralama
# ─────────────────────────────────────────────────────────────────────
# Küçükten büyüğe (varsayılan):
#   SELECT * FROM urunler ORDER BY fiyat;

# Büyükten küçüğe (DESC):
#   SELECT * FROM urunler ORDER BY fiyat DESC;

# Hesaplanan sütuna göre sıralama:
#   SELECT m.ad, SUM(s.adet) AS toplam
#   FROM siparisler s
#   JOIN musteriler m ON s.musteri_id = m.id
#   GROUP BY m.ad
#   ORDER BY toplam DESC;


# ─────────────────────────────────────────────────────────────────────
# 6. Çarpımla Hesaplama
# ─────────────────────────────────────────────────────────────────────
# Toplam tutar = adet * fiyat
#
#   SELECT s.id, s.adet * u.fiyat AS toplam_tutar
#   FROM siparisler s
#   JOIN urunler u ON s.urun_id = u.id;

# Müşteri bazında toplam harcama:
#   SELECT m.ad, SUM(s.adet * u.fiyat) AS toplam_harcama
#   FROM siparisler s
#   JOIN musteriler m ON s.musteri_id = m.id
#   JOIN urunler u    ON s.urun_id    = u.id
#   GROUP BY m.ad
#   ORDER BY toplam_harcama DESC;


# ─────────────────────────────────────────────────────────────────────
# 7. GENEL SIRA (Her zaman bu sırayı takip et!)
# ─────────────────────────────────────────────────────────────────────
#   SELECT   ← neyi almak istiyorum?
#   FROM     ← hangi ana tablodan?
#   JOIN     ← hangi tablolarla birleştir?
#   WHERE    ← hangi satırları filtrele?
#   GROUP BY ← neye göre grupla?
#   ORDER BY ← neye göre sırala?
#   LIMIT    ← kaç satır getir?
