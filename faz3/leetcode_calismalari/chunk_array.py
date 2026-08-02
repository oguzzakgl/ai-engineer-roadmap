# faz3/leetcode_calismalari/chunk_array.py

"""
🎯 LEETCODE CHALLENGE: CHUNK ARRAY (Diziyi Parçalara Böl)

Açıklama:
Sana bir liste (arr) ve bir parça boyutu (size) verilecek. 
Görevin, bu listeyi alt listelere (chunk'lara) bölüp geriye iki boyutlu bir liste dönmek.
Her bir alt listenin uzunluğu 'size' değerine eşit olmalıdır. En sondaki parça 'size'dan küçük kalabilir.

Örnek 1:
Girdi: arr = [1, 2, 3, 4, 5], size = 2
Çıktı: [[1, 2], [3, 4], [5]]

Örnek 2:
Girdi: arr = [1, 9, 6, 3, 2, 8], size = 3
Çıktı: [[1, 9, 6], [3, 2, 8]]

Örnek 3:
Girdi: arr = [], size = 1
Çıktı: []
"""

def chunk_array(arr: list, size: int) -> list[list]:
    # =====================================================================
    # 🎯 SENİN ÇÖZÜMÜN:
    # =====================================================================
    # Buraya listeyi 'size' boyutunda parçalara ayıran kodunu yaz.
    # (İpucu: Python'ın dilimleme (slicing) özelliğini 'arr[start:end]' kullanabilirsin,
    # ya da döngülerle boş bir listeye parçaları ekleyebilirsin.)
    # =====================================================================
    pass


# =====================================================================
# 🧪 TEST KODLARI (Kendi kodunu test etmek için çalıştırabilirsin)
# =====================================================================
if __name__ == "__main__":
    test1 = chunk_array([1, 2, 3, 4, 5], 2)
    print("Test 1 Sonucu:", test1, "-> Beklenen: [[1, 2], [3, 4], [5]]")
    
    test2 = chunk_array([1, 9, 6, 3, 2, 8], 3)
    print("Test 2 Sonucu:", test2, "-> Beklenen: [[1, 9, 6], [3, 2, 8]]")
    
    test3 = chunk_array([], 1)
    print("Test 3 Sonucu:", test3, "-> Beklenen: []")
