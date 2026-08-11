"""
🧩 Pratik #3: SQL JOIN + GROUP BY

Senaryo:
    Projemizdeki veritabanında 3 tablo var:
    - musteriler (id, ad, sehir)
    - urunler    (id, ad, fiyat, stok)
    - siparisler (id, musteri_id, urun_id, adet, tarih)

    Bu tablolarla ilgili sık sorulan SQL sorgu sorularını çöz.

HATIRLATMA:
    JOIN  → İki tabloyu ortak bir sütun üzerinden birleştirir
    GROUP BY → Aynı değere sahip satırları gruplar
    SUM() → Gruptaki sayıları toplar
    COUNT() → Gruptaki satır sayısını sayar
    ORDER BY → Sonuçları sıralar
    DESC → Büyükten küçüğe sıralama
"""


# =====================================================================
# SORU 1 (Kolay - JOIN):
# Her siparişin yanında müşteri adını da göster.
# Beklenen sütunlar: siparis_id, musteri_adi, adet, tarih
#
# İPUCU: siparisler tablosunu musteriler tablosuyla birleştir.
# =====================================================================
SORU_1 = """
    SELECT s.id as siparis_id, m.ad as musteri_adi, s.adet, s.tarih
    FROM siparisler s
    JOIN musteriler m ON s.musteri_id = m.id
"""


# =====================================================================
# SORU 2 (Orta - GROUP BY + JOIN):
# Her müşterinin toplam kaç adet sipariş verdiğini listele.
# Beklenen sütunlar: musteri_adi, toplam_adet
# En çok sipariş verenden en aza doğru sırala.
#
# İPUCU: SUM(adet) ve GROUP BY musteri_adi kullan.
# =====================================================================
SORU_2 = """
SELECT 
"""  # <-- Buraya yaz!


# =====================================================================
# SORU 3 (Zor - 3 Tablo JOIN + Hesaplama):
# Her müşterinin toplam harcamasını hesapla.
# Toplam harcama = SUM(siparis.adet * urun.fiyat)
# Beklenen sütunlar: musteri_adi, toplam_harcama
# En çok harcayandan en aza doğru sırala.
#
# İPUCU: 3 tabloyu da birleştirmen lazım!
#        siparisler → musteriler (musteri_id ile)
#        siparisler → urunler    (urun_id ile)
# =====================================================================
SORU_3 = """

"""  # <-- Buraya yaz!


# =====================================================================
# CEVAP ANAHTARI - Yazmadan önce çözmeye çalış!
# Cevapları görmek için aşağıdaki satırı YORUMDAN ÇIKAR (# sil):
# =====================================================================
# print(CEVAP_ANAHTARI)

CEVAP_ANAHTARI = """
-- SORU 1:
SELECT s.id AS siparis_id, m.ad AS musteri_adi, s.adet, s.tarih
FROM siparisler s
JOIN musteriler m ON s.musteri_id = m.id;

-- SORU 2:
SELECT m.ad AS musteri_adi, SUM(s.adet) AS toplam_adet
FROM siparisler s
JOIN musteriler m ON s.musteri_id = m.id
GROUP BY m.ad
ORDER BY toplam_adet DESC;

-- SORU 3:
SELECT m.ad AS musteri_adi, SUM(s.adet * u.fiyat) AS toplam_harcama
FROM siparisler s
JOIN musteriler m ON s.musteri_id = m.id
JOIN urunler u ON s.urun_id = u.id
GROUP BY m.ad
ORDER BY toplam_harcama DESC;
"""
