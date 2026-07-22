# gorev_yonetici.py
# Bu dosyaya asenkron görev ekleme, listeleme ve tamamlama mantığını yazacaksın.
import json
import asyncio
from typing import List 
from modeller import Gorev, GorevBulunamadiHatasi


class GorevYoneticisi:
    def __init__(self):
        self.gorevler: list[Gorev] = []
        self.dosya_yolu = "gorevler.json"
    
    def kaydet(self) -> None:
        with open(self.dosya_yolu, "w", encoding="utf-8") as f:
            json.dump(self.gorevler, f, ensure_ascii=False, indent=4)

    def gorev_ekle(self, baslik: str, sure: int) -> None:

        yeni_gorev: Gorev = {
            "id": len(self.gorevler) + 1,
            "baslik": baslik,
            "tamamlandi": False,
            "sure": sure
        }
        self.gorevler.append(yeni_gorev)
        self.kaydet()
        
    def gorev_sil(self, gorev_id: int) -> None:
        bulunan_gorev = None
        for g in self.gorevler:
            if g["id"] == gorev_id:
                bulunan_gorev = g
                break

        # Görev bulunamazsa hatayı fırlatıyoruz
        if bulunan_gorev is None:
            raise GorevBulunamadiHatasi(f"Silinmek istenen ID'si {gorev_id} olan görev bulunamadı!")

        self.gorevler.remove(bulunan_gorev)
        self.kaydet()
        print(f"🗑️ Görev {gorev_id} silindi: {bulunan_gorev['baslik']}")

    async def gorev_calistir(self, gorev_id: int) -> None:
        bulunan_gorev = None
        for g in self.gorevler:
            if g["id"] == gorev_id:
                bulunan_gorev = g
                break

        if bulunan_gorev is None:
            raise GorevBulunamadiHatasi(f"ID'si {gorev_id} olan görev bulunamadı!")

        print(f"⏳ Görev {gorev_id} çalıştırılıyor: {bulunan_gorev['baslik']}...")
        
        # Asenkron bekleme yapıyoruz (Görevin kendi süresi kadar)
        await asyncio.sleep(bulunan_gorev["sure"])

        # Görevi tamamlandı yapıp kaydediyoruz
        bulunan_gorev["tamamlandi"] = True
        self.kaydet()
        print(f"✔️ Görev {gorev_id} tamamlandı: {bulunan_gorev['baslik']}")

    def gorev_listele(self) -> None:
        if not self.gorevler:
            print("📭 Listede henüz görev yok.")
            return
        
        print("\n📋 === MEVCUT GÖREVLER ===")
        for g in self.gorevler:
            durum = "✔️ Tamamlandı" if g["tamamlandi"] else "⏳ Bekliyor"
            print(f"[{g['id']}] {g['baslik']} - {g['sure']} sn - {durum}")
        print("==========================\n")

    def gorevleri_say(self) -> int:
        sayi = 0
        for s in self.gorevler:
            if s["tamamlandi"] == True:
                sayi += 1
        return sayi

    def tamamlanmamis_gorevleri_say(self) -> int:
        sayi = 0
        for s in self.gorevler:
            if s["tamamlandi"] == False:
                sayi += 1
        return sayi