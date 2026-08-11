"""
=====================================================================
🚀 SQL HIZLANDIRILMIŞ KURS - SIFIRDAN MÜLAKAT SEVİYESİNE
=====================================================================
Proje tablolarımız:
    musteriler  → id, ad, sehir
    urunler     → id, ad, fiyat, stok
    siparisler  → id, musteri_id, urun_id, adet, tarih

Bu dosyayı yukarıdan aşağıya oku ve her dersin altındaki
mini soruyu çöz. Cevap anahtarı en altta.
"""


# ═══════════════════════════════════════════════════════════════════
# DERS 1: SELECT & FROM — "Ne istiyorum, nereden?"
# ═══════════════════════════════════════════════════════════════════
#
# SQL her zaman şu soruyu cevaplar:
#   "Hangi TABLODAN (FROM), hangi SÜTUNLARI (SELECT) getir?"
#
# Sözdizimi:
#   SELECT sütun1, sütun2  FROM tablo_adı;
#
# Örnekler:
#   SELECT * FROM musteriler;             → Tüm müşterileri getir
#   SELECT ad FROM musteriler;            → Sadece ad sütununu getir
#   SELECT ad, sehir FROM musteriler;     → Ad ve şehri getir
#
# ★ MİNİ SORU 1:
#   Tüm ürünlerin adını ve fiyatını getiren sorguyu yaz.
#
SORU_D1 = """
    SELECT ad, fiyat FROM urunler;
"""


# ═══════════════════════════════════════════════════════════════════
# DERS 2: WHERE — "Hangi koşulda?"
# ═══════════════════════════════════════════════════════════════════
#
# Tüm tabloyu değil, belirli satırları filtrelemek için kullanılır.
# "Sadece şu koşula uyan satırları getir" der.
#
# Sözdizimi:
#   SELECT ... FROM ... WHERE koşul;
#
# Koşullar:
#   =     eşit                    WHERE sehir = 'Istanbul'
#   >     büyüktür                WHERE fiyat > 100
#   <     küçüktür                WHERE stok < 5
#   >=    büyük eşit              WHERE fiyat >= 50
#   AND   iki koşul aynı anda     WHERE stok > 0 AND fiyat < 200
#   OR    koşullardan biri        WHERE sehir = 'Ankara' OR sehir = 'Izmir'
#
# Örnekler:
#   SELECT * FROM musteriler WHERE sehir = 'Istanbul';
#   SELECT ad, fiyat FROM urunler WHERE fiyat > 500;
#   SELECT * FROM urunler WHERE stok > 0 AND fiyat < 300;
#
# ★ MİNİ SORU 2:
#   Stoğu 10'dan fazla olan ürünlerin adını ve stok miktarını getir.
#
SORU_D2 = """
    SELECT ad, stok FROM urunler WHERE stok > 10;
"""


# ═══════════════════════════════════════════════════════════════════
# DERS 3: AS — "Sütuna takma ad ver"
# ═══════════════════════════════════════════════════════════════════
#
# Sütun adlarını daha okunabilir yapmak için kullanılır.
# Özellikle hesaplama sonuçlarını isimlendirmek için şart!
#
# Sözdizimi:
#   SELECT sütun AS yeni_ad FROM tablo;
#
# Örnekler:
#   SELECT ad AS urun_adi, fiyat AS fiyat_tl FROM urunler;
#   SELECT id AS siparis_no, adet AS miktar FROM siparisler;
#
# ★ MİNİ SORU 3:
#   Müşteri tablosundan id sütununu "musteri_no", ad sütununu
#   "tam_ad", sehir sütununu "yasadigi_sehir" olarak getir.
#
SORU_D3 = """
    SELECT id AS musteri_no, ad AS tam_ad, sehir AS yasadigi_sehir 
    FROM musteriler;
"""


# ═══════════════════════════════════════════════════════════════════
# DERS 4: ORDER BY — "Sırala"
# ═══════════════════════════════════════════════════════════════════
#
# Sonuçları bir sütuna göre sıralamak için kullanılır.
#   ASC  → Küçükten büyüğe (varsayılan, yazmasan da olur)
#   DESC → Büyükten küçüğe
#
# Sözdizimi:
#   SELECT ... FROM ... ORDER BY sütun DESC;
#
# Örnekler:
#   SELECT * FROM urunler ORDER BY fiyat;          → En ucuzdan pahalıya
#   SELECT * FROM urunler ORDER BY fiyat DESC;     → En pahalıdan ucuza
#   SELECT * FROM musteriler ORDER BY ad;          → Alfabetik sıra
#
# ★ MİNİ SORU 4:
#   Ürünleri fiyatına göre pahalıdan ucuza sırala.
#   Sadece ad ve fiyat sütunlarını getir.
#
SORU_D4 = """
    SELECT ad, fiyat FROM urunler ORDER BY fiyat DESC;
"""


# ═══════════════════════════════════════════════════════════════════
# DERS 5: JOIN — "Tabloları birleştir"  ⭐ En Önemli Ders!
# ═══════════════════════════════════════════════════════════════════
#
# Farklı tablolardaki verileri birleştirmek için kullanılır.
# Bağlantı noktası genellikle bir "yabancı anahtar" (foreign key).
#
# siparisler tablosunda musteri_id var ama müşteri adı yok.
# musteriler tablosunda id ve ad var.
# JOIN bunları birleştirir!
#
# Sözdizimi:
#   SELECT ...
#   FROM ana_tablo  t1_kisaltma
#   JOIN diger_tablo t2_kisaltma ON t1.yabanci_anahtar = t2.id;
#
# Görsel Örnek:
#   siparisler tablosu:           musteriler tablosu:
#   id | musteri_id | adet        id | ad
#   1  |     1      |  3          1  | Ahmet
#   2  |     2      |  5          2  | Ayşe
#
#   JOIN sonucu → id | musteri_adi | adet
#                  1  | Ahmet       |  3
#                  2  | Ayşe        |  5
#
# Örnek:
#   SELECT s.id, m.ad AS musteri_adi, s.adet
#   FROM siparisler s
#   JOIN musteriler m ON s.musteri_id = m.id;
#
# ★ MİNİ SORU 5:
#   Her siparişin yanında o siparişe ait ürünün adını göster.
#   (siparisler → urunler birleştirmesi, urun_id ile)
#   Sütunlar: siparis_id, urun_adi, adet
#
SORU_D5 = """
    SELECT s.id AS siparis_id, u.ad AS urun_adi, s.adet
    FROM siparisler s
    JOIN urunler u ON s.urun_id = u.id;
"""


# ═══════════════════════════════════════════════════════════════════
# DERS 6: GROUP BY + SUM/COUNT — "Grupla ve hesapla"
# ═══════════════════════════════════════════════════════════════════
#
# Aynı değere sahip satırları bir araya toplar ve
# her grup için bir hesaplama yapar.
#
# Mantık: "Her müşteri için ayrı bir grup oluştur,
#           her grubun toplam adet siparişini hesapla."
#
# Aggregate Fonksiyonlar:
#   SUM(sütun)   → Gruptaki değerleri toplar
#   COUNT(*)     → Gruptaki satır sayısını sayar
#   AVG(sütun)   → Ortalamasını alır
#   MAX(sütun)   → En büyük değeri bulur
#   MIN(sütun)   → En küçük değeri bulur
#
# KURAL: SELECT'te yazdığın sütunlar ya GROUP BY'da olmalı
#         ya da bir aggregate fonksiyon içinde olmalı!
#
# Sözdizimi:
#   SELECT sütun, SUM(diger_sutun) AS toplam
#   FROM tablo
#   GROUP BY sütun
#   ORDER BY toplam DESC;
#
# Örnek - Her şehirde kaç müşteri var?
#   SELECT sehir, COUNT(*) AS musteri_sayisi
#   FROM musteriler
#   GROUP BY sehir
#   ORDER BY musteri_sayisi DESC;
#
# ★ MİNİ SORU 6:
#   Her müşterinin toplam kaç adet sipariş verdiğini bul.
#   (siparisler → musteriler JOIN kullan)
#   Sütunlar: musteri_adi, toplam_adet
#   En çok sipariş verenden en aza sırala.
#
SORU_D6 = """
    SELECT m.ad AS musteri_adi, SUM(s.adet) AS toplam_adet
    FROM musteriler m
    JOIN siparisler s ON m.id = s.musteri_id
    GROUP BY m.ad
    ORDER BY toplam_adet DESC;
"""


# ═══════════════════════════════════════════════════════════════════
# DERS 7: 3 Tablo JOIN + Hesaplama — Final Boss! 🎯
# ═══════════════════════════════════════════════════════════════════
#
# Birden fazla JOIN kullanılabilir. Her JOIN yeni bir tablo ekler.
#
# Örnek:
#   FROM siparisler s
#   JOIN musteriler m ON s.musteri_id = m.id    ← 1. bağlantı
#   JOIN urunler u    ON s.urun_id    = u.id    ← 2. bağlantı
#
# Artık s, m ve u tablolarının tüm sütunlarına erişebilirsin.
# Örneğin: m.ad (müşteri adı), u.fiyat (ürün fiyatı)
#
# Hesaplama:
#   Toplam tutar = adet * fiyat → s.adet * u.fiyat
#   Müşteri bazında toplam → SUM(s.adet * u.fiyat)
#
# ★ MİNİ SORU 7 (FINAL):
#   Her müşterinin toplam ne kadar harcadığını hesapla.
#   Toplam harcama = SUM(adet * fiyat)
#   (3 tabloyu da birleştirmen gerekiyor!)
#   Sütunlar: musteri_adi, toplam_harcama
#   En çok harcayandan en aza sırala.
#
SORU_D7 = """

"""


# ═══════════════════════════════════════════════════════════════════
# CEVAP ANAHTARI — Önce kendi çöz!
# Görmek için bu bloğu bir print ile çağır.
# ═══════════════════════════════════════════════════════════════════
CEVAPLAR = """
-- DERS 1:
SELECT ad, fiyat FROM urunler;

-- DERS 2:
SELECT ad, stok FROM urunler WHERE stok > 10;

-- DERS 3:
SELECT id AS musteri_no, ad AS tam_ad, sehir AS yasadigi_sehir FROM musteriler;

-- DERS 4:
SELECT ad, fiyat FROM urunler ORDER BY fiyat DESC;

-- DERS 5:
SELECT s.id AS siparis_id, u.ad AS urun_adi, s.adet
FROM siparisler s
JOIN urunler u ON s.urun_id = u.id;

-- DERS 6:
SELECT m.ad AS musteri_adi, SUM(s.adet) AS toplam_adet
FROM siparisler s
JOIN musteriler m ON s.musteri_id = m.id
GROUP BY m.ad
ORDER BY toplam_adet DESC;

-- DERS 7:
SELECT m.ad AS musteri_adi, SUM(s.adet * u.fiyat) AS toplam_harcama
FROM siparisler s
JOIN musteriler m ON s.musteri_id = m.id
JOIN urunler u    ON s.urun_id    = u.id
GROUP BY m.ad
ORDER BY toplam_harcama DESC;
"""





"""
Hangi tablolar lazım? ➔ Bize FROM ve JOIN satırlarını verir.
Bağlantı ne? ➔ Bize ON ... = ... kısmını verir.
Toplama/Hesaplama ne? ➔ Bize SELECT içindeki SUM(), COUNT() gibi fonksiyonları verir.
Gruplama neye göre? ➔ Bize GROUP BY satırını verir.


Şimdi bu Şablonu Kullanarak BONUS SORU 2'yi Yazalım:


Soru 1 (Tablolar): musteriler m ve siparisler s ➔ FROM musteriler m JOIN siparisler s
Soru 2 (Bağlantı): s.musteri_id = m.id ➔ ON s.musteri_id = m.id
Soru 3 (Toplama): SUM(s.adet) ve şehri göster (m.sehir) ➔ SELECT m.sehir, SUM(s.adet) AS toplam_adet
Soru 4 (Gruplama): GROUP BY m.sehir ➔ GROUP BY m.sehir
(Ekstra - Sıralama): ORDER BY toplam_adet DESC




urun ve siparis tablosu lazım, 
baglantı siparis.urun.id ile urunlerdeki urun.id, 
hesap siparis urun id ile urunlerdeki urun.id eslesenler kactaneyse, 
gruplama urunid 
orderbvy desc 

FROM urunler u JOIN siparisler s 
ON s.urun.id = u.id
COUNT(s.id) AS siparis_sayisi
group by urun.id
order by COUNT(s.id) desc








"""

