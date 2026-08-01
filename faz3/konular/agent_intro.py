# faz3/konular/agent_intro.py
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from google import genai

# 1. Gemini elçimizi başlatıyoruz.
client = genai.Client()

# ---------------------------------------------------------------------
# 🕸️ 1. ADIM: ORTAK HAFIZA (STATE) TANIMI
# ---------------------------------------------------------------------
# Neden? Düğümlerin (Nodes) kendi aralarında bilgi paylaşması için.
# Her düğüm bu defteri okuyabilir ve hücreleri güncelleyebilir.
class AgentState(TypedDict):
    soru: str      # Kullanıcının gönderdiği talep/soru
    analiz: str    # Analist düğümünün yazacağı teknik analiz
    karar: str     # Karar verici düğümün vereceği karar ("ONAY" veya "RED")


# ---------------------------------------------------------------------
# 🕸️ 2. ADIM: DÜĞÜMLERİ (NODES) TANIMLAMA
# ---------------------------------------------------------------------

# A. Analiz Düğümü (Analist Node)
# Neden? Soruyu alıp teknik açıdan analiz etmek için.
def analist_dugumu(state: AgentState):
    print("\n[Node: Analist] Gelen talep inceleniyor...")
    
    prompt = f"""
Sana gelen talebin bir yazılım/backend konusu olup olmadığını analiz et.
Eğer yazılım konusuysa neden backend ile alakalı olduğunu 1 cümleyle açıkla.
Eğer yazılım dışı bir konuysa (yemek, spor, magazin vb.) bunun yazılım dışı olduğunu belirt.

TALEP:
{state['soru']}
"""
    response = client.models.generate_content(
        model='gemini-3.5-flash',
        contents=prompt
    )
    
    # Ortak hafızadaki 'analiz' alanını güncelleyerek geriye dönüyoruz.
    return {"analiz": response.text}


# B. Karar Düğümü (Decision Node)
# Neden? Analistin yazdığı analize bakıp nihai kararı (ONAY/RED) vermek için.
def karar_dugumu(state: AgentState):
    print("\n[Node: Karar Verici] Yapılan analiz incelenip karar veriliyor...")
    
    prompt = f"""
Önündeki analiz raporunu oku.
Eğer rapor bunun bir yazılım/backend konusu olduğunu söylüyorsa sadece "ONAY" kelimesini dön.
Eğer rapor bunun yazılım dışı bir konu olduğunu söylüyorsa sadece "RED" kelimesini dön.

ANALİZ RAPORU:
{state['analiz']}
"""
    response = client.models.generate_content(
        model='gemini-3.5-flash',
        contents=prompt
    )
    
    # Ortak hafızadaki 'karar' alanını güncelleyerek geriye dönüyoruz.
    # .strip() ile gereksiz boşlukları temizliyoruz.
    karar_sonucu = response.text.strip().upper()
    return {"karar": karar_sonucu}


# ---------------------------------------------------------------------
# 🕸️ 3. ADIM: GRAF AKIŞ ŞEMASINI OLUŞTURMA (BUILD GRAPH)
# ---------------------------------------------------------------------

# A. Ortak hafıza şablonumuzla bir StateGraph başlatıyoruz.
workflow = StateGraph(AgentState)

# B. Düğümlerimizi (Python fonksiyonlarını) grafa ekliyoruz.
workflow.add_node("analist_kutusu", analist_dugumu)
workflow.add_node("karar_kutusu", karar_dugumu)

# C. Kenarları (Edges) yani yolları çiziyoruz.
# START -> analist_kutusu -> karar_kutusu -> END
workflow.add_edge(START, "analist_kutusu")
workflow.add_edge("analist_kutusu", "karar_kutusu")
workflow.add_edge("karar_kutusu", END)

# D. Grafı derleyip çalışabilir (executable) hale getiriyoruz.
app = workflow.compile()


# ---------------------------------------------------------------------
# 🚀 4. ADIM: AJANI ÇALIŞTIRMA (INVOKE)
# ---------------------------------------------------------------------

# Ajanımıza başlangıç state'i (sorusu) vererek çalıştırıyoruz.
baslangic_durumu = {"soru": "Veritabanında sorguları hızlandırmak için nasıl indeks eklerim?"}

print("=== AJAN ÇALIŞTIRILIYOR ===")
nihai_sonuc = app.invoke(baslangic_durumu)

print("\n=== AJANIN NİHAİ RAPORU ===")
print("Soru:", nihai_sonuc["soru"])
print("\nAnalist Raporu:", nihai_sonuc["analiz"])
print("\nKarar Sonucu:", nihai_sonuc["karar"])
