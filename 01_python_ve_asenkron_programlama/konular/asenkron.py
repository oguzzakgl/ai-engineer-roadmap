# Asenkron Python (asyncio) - async & await Mantığı

import asyncio


# 1. Asenkron Yardımcı Fonksiyon
async def veri_getir() -> str:
    print("⏳ Sunucudan veri isteniyor (2 saniye bekleme)...")
    await asyncio.sleep(2)  # Simüle edilmiş bekleme süresi
    return "✅ Veri başarıyla alındı!"


# 2. Ana Asenkron Fonksiyon
async def ana_fonksiyon() -> None:
    print("🚀 Ana fonksiyon başladı.")

    # Async fonksiyon İÇİNDE olduğumuz için 'await' kullanıyoruz:
    sonuc: str = await veri_getir()

    print(f"Gelen Sonuç: {sonuc}")
    print("🎉 Ana fonksiyon bitti.")


# 3. Dosyanın En Dış Seviyesi (Fonksiyon Dışı)
# Async fonksiyon DIŞINDA olduğumuz için 'asyncio.run()' ile başlatıyoruz:
if __name__ == "__main__":
    asyncio.run(ana_fonksiyon())
