"""
🧩 Pratik #2: Kosinüs Benzerliği Hesaplama (Cosine Similarity)

Senaryo:
    RAG sistemimizde kullanıcının sorusunu vektöre çevirip,
    veritabanındaki paragraf vektörleriyle karşılaştırıyoruz.
    Bu karşılaştırmayı yapan matematiksel formül: Kosinüs Benzerliği.

    Formül:
        similarity = (A · B) / (|A| * |B|)

    Burada:
        A · B   = İki vektörün nokta çarpımı (dot product)
                  Her eleman çarpılır, sonra toplanır.
                  Örnek: [1,2] · [3,4] = (1*3) + (2*4) = 11

        |A|     = A vektörünün uzunluğu (magnitude)
                  Her elemanın karesi toplanır, karekök alınır.
                  Örnek: |[1,2]| = sqrt(1² + 2²) = sqrt(5) ≈ 2.236

Sonuç:
    1.0  → Vektörler tamamen aynı yönde (maksimum benzerlik)
    0.0  → Vektörler birbirinden tamamen bağımsız
   -1.0  → Vektörler tamamen zıt yönde

Senden istenen:
    Hazır kütüphane (numpy, sklearn vb.) KULLANMADAN,
    sadece saf Python ile kosinüs benzerliğini hesapla.

İPUCU:
    - math.sqrt() → karekök almak için
    - sum()       → liste elemanlarını toplamak için
    - zip(a, b)   → iki listeyi eş zamanlı gezmek için
      Örnek: list(zip([1,2], [3,4])) → [(1,3), (2,4)]
"""

import math


def kosinus_benzerligi(a: list[float], b: list[float]) -> float:
    pass  # <-- Buraya yaz!


# =====================================================================
# TEST - Dosyayı çalıştır: python pratik/pratik_02_cosine.py
# =====================================================================
if __name__ == "__main__":
    # Test 1: Aynı vektörler → sonuç 1.0 olmalı
    v1 = [1.0, 0.0, 0.0]
    v2 = [1.0, 0.0, 0.0]
    sonuc = kosinus_benzerligi(v1, v2)
    print(f"Test 1 - Aynı vektörler:  {sonuc:.4f}  (Beklenen: 1.0000)")

    # Test 2: Dik vektörler → sonuç 0.0 olmalı
    v3 = [1.0, 0.0]
    v4 = [0.0, 1.0]
    sonuc2 = kosinus_benzerligi(v3, v4)
    print(f"Test 2 - Dik vektörler:   {sonuc2:.4f}  (Beklenen: 0.0000)")

    # Test 3: Gerçekçi örnek
    v5 = [1.0, 2.0, 3.0]
    v6 = [4.0, 5.0, 6.0]
    sonuc3 = kosinus_benzerligi(v5, v6)
    print(f"Test 3 - Gerçekçi örnek:  {sonuc3:.4f}  (Beklenen: 0.9746)")

    print("\n=== KONTROL ===")
    test1_ok = abs(sonuc - 1.0) < 0.0001
    test2_ok = abs(sonuc2 - 0.0) < 0.0001
    test3_ok = abs(sonuc3 - 0.9746) < 0.0001
    tumu_ok = test1_ok and test2_ok and test3_ok
    print(f"Tüm testler geçti mi? {'EVET' if tumu_ok else 'HAYIR - Bir veya daha fazla test basarisiz'}")
