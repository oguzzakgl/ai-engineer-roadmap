"""
🧩 Pratik #1: Akıllı Metin Parçalayıcı (RAG Chunking)

Senaryo:
    RAG sistemimizde PDF metnini 800 karakterlik parçalara bölüyoruz.
    Ama şu kural var: Kelimeler ortadan kesilmez!

Senden istenen:
    Aşağıdaki fonksiyonu tamamla.

KURAL: Kelime ortasında asla kesme!
    Yani 800. karakter bir kelimenin ortasına denk geliyorsa,
    o kelime bitmeden bir sonraki parçaya geçemezsin.

İPUCU:
    - Metni kelimelerine ayır (str.split() kullanabilirsin)
    - Kelimeleri tek tek gez ve mevcut parçaya ekle
    - Parça boyutu dolunca yeni bir parça başlat
    - Döngü bitince en sondaki parçayı unutma!
"""


def metni_parcalara_bol(metin: str, parca_boyutu: int = 800) -> list[str]:
    words = metin.split()
    parcalar = []
    current_chunk = []
    current_length = 0

    for word in words:
        current_chunk.append(word)
        current_length += len(word) + 1

        if current_length >= parca_boyutu:
            parcalar.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0

    if current_chunk:
        parcalar.append(" ".join(current_chunk))

    return parcalar


# =====================================================================
# TEST - Dosyayı çalıştır: python pratik_01_chunking.py
# =====================================================================
if __name__ == "__main__":
    test_metin = (
        "Bu bir test metnidir. Python programlama dili çok güçlüdür. "
        "RAG sistemleri yapay zeka dünyasında çok kullanılır."
    )

    parcalar = metni_parcalara_bol(test_metin, parca_boyutu=50)

    print("=== TEST SONUCU ===\n")
    for i, p in enumerate(parcalar):
        print(f"Parça {i + 1} ({len(p)} karakter): '{p}'")

    # Beklenen: Her parça 50 karakteri AŞMASIN ve kelime ortasında kesilmesin!
    print("\n=== KONTROL ===")
    basarili = all(len(p) <= 50 for p in parcalar)
    print(f"Tüm parçalar 50 karakter sınırına uyuyor mu? {'✅ EVET' if basarili else '❌ HAYIR'}")
