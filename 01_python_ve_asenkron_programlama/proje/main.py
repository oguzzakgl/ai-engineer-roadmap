# main.py
# Bu dosya uygulamanın giriş noktası (entry point) olacak ve görevleri tetikleyecek.

import asyncio
from gorev_yonetici import GorevYoneticisi
from modeller import GorevBulunamadiHatasi

async def main() -> None:
    yonetici = GorevYoneticisi()

    print("--- 1. GÖREVLER EKLENİYOR ---")
    yonetici.gorev_ekle("Yapay Zeka Modeli Yükleniyor", 3)
    yonetici.gorev_ekle("API Bağlantısı Kuruluyor", 1)
    yonetici.gorev_ekle("Kullanıcı Verileri Okunuyor", 2)

    # Görevleri listele
    yonetici.gorev_listele()

    print(f"Tamamlanan Görev Sayısı: {yonetici.gorevleri_say()}")
    print(f"Tamamlanmamış Görev Sayısı: {yonetici.tamamlanmamis_gorevleri_say()}")

    print("--- 2. GÖREVLER ASENKRON OLARAK BAŞLATILIYOR ---")
    # gather ile 3 görevi aynı anda çalıştırıyoruz
    await asyncio.gather(
        yonetici.gorev_calistir(1),
        yonetici.gorev_calistir(2),
        yonetici.gorev_calistir(3)
    )

    # Tamamlanmış halini listele
    yonetici.gorev_listele()

    print("--- 3. HATA YÖNETİMİ TESTİ ---")
    try:
        # Olmayan bir görevi çalıştırmayı deniyoruz
        await yonetici.gorev_calistir(99)
    except GorevBulunamadiHatasi as e:
        print(f"Hata Başarıyla Yakalandı: {e}")

if __name__ == "__main__":
    asyncio.run(main())
