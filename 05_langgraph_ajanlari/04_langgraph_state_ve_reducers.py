# 05_langgraph_ajanlari/04_langgraph_state_ve_reducers.py
"""
FAZ 5 - LANGGRAPH STATE MANAGEMENT VE REDUCER DERİNLEŞME PRATİĞİ
------------------------------------------------------------------------------
Bu çalışmada, LangGraph'teki State (Durum) güncellemelerinin arka planını,
verilerin birbirini ezmesini engellemeyi (Reducer) ve mesaj listelerini yönetmeyi
derinlemesine öğreneceğiz.

ÖĞRENECEĞİMİZ KRİTİK KAVRAMLAR:
1. Override (Varsayılan Davranış): Bir düğüm dict döndüğünde, var olan anahtarı tamamen ezer.
2. Reducer (Annotated[List, add]): Listelerin veya verilerin üstüne ekleme (append) yapılmasını sağlar.
3. Özel Reducer Fonksiyonları: Kendi belirlediğimiz kurallara göre state birleştirme.
"""

import os
from typing import Annotated, TypedDict
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END

# API Key Kontrolleri
if "GEMINI_API_KEY" in os.environ and "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]


# =====================================================================
# 🧠 KONU 1: REDUCER MANTIĞI VE OVERSIGHT ENGELLEME
# =====================================================================
# Normalde LangGraph'te bir State anahtarı güncellendiğinde eski değer silinir, yeni değer yazılır.
# Ancak listelerde (örn: loglar veya mesaj geçmişi) eski veriyi koruyup yeniyi EKLEMEK (append) isteriz.
# Bunun için 'operator.add' veya özel bir reducer fonksiyonu kullanırız.

def ekle_yeni_veri(eski_liste: list, yeni_liste: list) -> list:
    """
    Bu bizim ÖZEL REDUCER fonksiyonumuzdur.
    LangGraph bu anahtarı güncellerken eski değer ile yeni değeri bu fonksiyona parametre olarak gönderir.
    Biz de bu fonksiyonda verileri nasıl birleştireceğimizi belirleriz.
    """
    # E-posta listesi veya log birleştirme mantığı:
    if eski_liste is None:
        eski_liste = []
    if yeni_liste is None:
        yeni_liste = []
    
    # İki listeyi birleştirip benzersiz (unique) elemanları döndürelim:
    return list(set(eski_liste + yeni_liste))


# =====================================================================
# 📋 ADIM 1: STATE TANIMLAMA
# =====================================================================
# Görev: Annotated kullanarak 'gunluk_loglar' listesine 'ekle_yeni_veri' reducer'ını bağla.
# 'islem_adedi' ise düz bir integer olsun (her adımda güncellenen/ezilen değer).

class KurumsalState(TypedDict):
    islem_adedi: int
    # Annotated[Tip, Reducer_Fonksiyonu] formatında yazmalısın:
    gunluk_loglar: Annotated[list[str], ekle_yeni_veri]


# =====================================================================
# 🤖 ADIM 2: DÜĞÜM FONKSİYONLARI (NODES)
# =====================================================================
# Görev: İki farklı düğüm yaz. 
# - Birincisi log listesine ['Adım 1 Başladı'] eklesin, islem_adedi=1 yapsın.
# - İkincisi log listesine ['Adım 2 Tamamlandı'] eklesin, islem_adedi=2 yapsın.
# reducer sayesinde listeler birleşecek, islem_adedi ise ezilecek (en son 2 olacak).

def adim_bir_calistir(state: KurumsalState) -> dict:
    return {"islem_adedi": 1, "gunluk_loglar": ["Adım 1 Başladı"]}


def adim_iki_calistir(state: KurumsalState) -> dict:
    return {"islem_adedi": 2, "gunluk_loglar": ["Adım 2 Tamamlandı"]}


# =====================================================================
# 🏗️ ADIM 3: GRAPH KURULUMU
# =====================================================================
# Görev: Düğümleri ekle, düz bağlantıyı kur (adım_bir -> adım_iki -> END) ve compile et.

def kur_kurumsal_grafigi():
    # Kodu sen yazacaksın
    workflow = StateGraph(KurumsalState)
    workflow.add_node("adim_bir", adim_bir_calistir)
    workflow.add_node("adim_iki", adim_iki_calistir)
    workflow.add_edge("adim_bir", "adim_iki")
    workflow.add_edge("adim_iki", END)
    workflow.set_entry_point("adim_bir")
    return workflow.compile()


if __name__ == "__main__":
    print("🧠 LangGraph State & Reducer Derinleşme Çalışması Başlatılıyor...\n")
    # Test Etme Alanı
    app = kur_kurumsal_grafigi()
    baslangic = {"islem_adedi": 0, "gunluk_loglar": ["Sistem Başlatıldı"]}
    sonuc = app.invoke(baslangic)
    print("\n--- NİHAİ STATE ---")
    print(sonuc)

