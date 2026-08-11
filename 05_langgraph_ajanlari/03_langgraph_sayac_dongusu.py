# 05_langgraph_ajanlari/03_langgraph_sayac_dongusu.py
"""
FAZ 5 - LANGGRAPH BİLGİ TAZELEME VE PRATİK ÇALIŞMASI
---------------------------------------------------
Amaç: LangGraph StateGraph, TypedDict State, Nodes, Edges, 
ve Conditional Routing mekanizmalarını sıfırdan kurup çalıştırmak.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END

# =====================================================================
# 📋 ADIM 1: STATE (DURUM) YAPISI
# =====================================================================
# Görev: Bir adet 'sayac' (int) ve 'mesaj' (str) barındıran
# TypedDict sınıfı tanımla. Sınıf adı "TekrarState" olsun.

class TekrarState(TypedDict):
    # Kodu sen yazacaksın
    sayac: int
    mesaj: str

# =====================================================================
# 🤖 ADIM 2: DÜĞÜM FONKSİYONLARI (NODES)
# =====================================================================
# Görev: State alan ve güncellenmiş alanları sözlük olarak dönen düğüm fonksiyonlarını yaz.
# Fonksiyon isimleri fiille başlasın (örn: arttir_sayaci, ekle_mesaji).

def arttir_sayaci(state: TekrarState) -> dict:
    """
    State içindeki 'sayac' değerini 1 artırır ve geriye güncel sayacı dönen dict verir.
    """
    # Kodu sen yazacaksın
    return {"sayac": state["sayac"] + 1}


def ekle_mesaji(state: TekrarState) -> dict:
    """
    Mesajı günceller (Örn: "Döngü adımı çalıştı") ve geriye dict döner.
    """
    # Kodu sen yazacaksın
    return {"mesaj": "Döngü adımı çalıştı"}


# =====================================================================
# 🚦 ADIM 3: KOŞULLU YÖNLENDİRİCİ (CONDITIONAL ROUTER)
# =====================================================================
# Görev: Sayaç 3'e ulaştığında akışı bitiren (END), aksi halde 'arttir_sayaci' düğümüne 
# geri yönlendiren router fonksiyonunu yaz.
# Fonksiyon ismi fiille başlasın (örn: kontrol_et_donguyu).

def kontrol_et_donguyu(state: TekrarState) -> str:
    """
    Sayaç değerine bakar:
    - Eğer sayaç >= 3 ise END döner.
    - Değilse, tekrar arttırma düğümüne gitmesi için o düğümün adını (örn: "sayac_arttirici") döner.
    """
    # Kodu sen yazacaksın
    if state["sayac"] >= 3:
        return END
    else:
        return "sayac_arttirici"


# =====================================================================
# 🏗️ ADIM 4: GRAPH KURULUMU
# =====================================================================
# Görev: Düğümleri ekleyen, bağlantıları (edges) kuran ve grafiği compile eden fonksiyonu yaz.
# Fonksiyon ismi fiille başlasın (örn: kur_grafigi).

def kur_grafigi():
    """
    1. StateGraph(TekrarState) nesnesini başlat.
    2. add_node ile düğümleri ekle.
    3. set_entry_point ile giriş noktasını ayarla.
    4. add_edge ile düğümleri düz bağla (Örn: sayac_arttirici -> mesaj_ekleyici).
    5. add_conditional_edges ile koşullu yönlendirmeyi ekle.
    6. compile() edip derlenmiş uygulamayı döndür.
    """
    # Kodu sen yazacaksın
    workflow = StateGraph(TekrarState) # baslat
    workflow.add_node("sayac_arttirici", arttir_sayaci) # dugum ekle
    workflow.add_node("mesaj_ekleyici", ekle_mesaji) # dugum ekle
    
    # Giriş noktasını ayarlıyoruz (Grafik nereden başlayacak?)
    workflow.set_entry_point("sayac_arttirici") # giris
    
    # Arttırıcıdan sonra doğrudan mesaj ekleyiciye git (Düz bağ)
    workflow.add_edge("sayac_arttirici", "mesaj_ekleyici") # duz baglantilar
    
    # Mesaj ekleyiciden sonra KOŞULA bak: END mi yoksa başa (sayac_arttirici) mı?
    workflow.add_conditional_edges("mesaj_ekleyici", kontrol_et_donguyu) # kosullu baglanti
    
    return workflow.compile()



if __name__ == "__main__":
    print("🕸️ LangGraph Tekrar Çalışması Başlatılıyor...\n")
    app = kur_grafigi()
    baslangic = {"sayac": 0, "mesaj": "Başladı"}
    for adim in app.stream(baslangic):
        print(adim)
