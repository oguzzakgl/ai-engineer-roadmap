# faz3/konular/agent_intro.py
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from google import genai

# 1. Gemini elçimizi başlatıyoruz.
client = genai.Client()

# ---------------------------------------------------------------------
# 🕸️ 1. ADIM: ORTAK HAFIZA (STATE) TANIMI
# ---------------------------------------------------------------------
class AgentState(TypedDict):
    soru: str      # Kullanıcının gönderdiği talep/soru
    analiz: str    # Analist düğümünün yazacağı teknik analiz
    karar: str     # Karar verici düğümün vereceği karar ("ONAY" veya "RED")
    cevap: str     # Cevap üretici düğümün yazacağı teknik cevap (eğer onaylandıysa)


# ---------------------------------------------------------------------
# 🕸️ 2. ADIM: DÜĞÜMLERİ (NODES) TANIMLAMA
# ---------------------------------------------------------------------

# A. Analiz Düğümü (Analist Node)
def analist_dugumu(state: AgentState):
    print("\n[Node: Analist] Gelen talep inceleniyor...")
    
    prompt = f"""
Sana gelen talebin bir yazılım/backend konusu olup olmadığını analiz et.
Eğer yazılım konusuysa neden backend ile alakalı olduğunu 1 cümleyle açıkla.
Eğer yazılım dışı bir konuysa bunun yazılım dışı olduğunu belirt.

TALEP:
{state['soru']}
"""
    response = client.models.generate_content(
        model='gemini-3.5-flash',
        contents=prompt
    )
    return {"analiz": response.text}


# B. Karar Düğümü (Decision Node)
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
    
    karar_sonucu = response.text.strip().upper()
    return {"karar": karar_sonucu}


# C. Cevap Düğümü (Answer Node)
def cevap_dugumu(state: AgentState):
    print("\n[Node: Cevap Üretici] Kullanıcıya teknik cevap hazırlanıyor...")
    
    prompt = f"""
Sana sorulan yazılım/backend sorusuna detaylı, açıklayıcı ve örnek içeren teknik bir yanıt hazırla.

SORU:
{state['soru']}
"""
    response = client.models.generate_content(
        model='gemini-3.5-flash',
        contents=prompt
    )
    return {"cevap": response.text}


# 🧭 3. ADIM: YÖNLENDİRİCİ (ROUTER) FONKSİYON
# Neden? Karar kutusundan çıkınca ONAY ise cevaba, RED ise çıkışa (END) yönlendirmek için.
def karar_yonlendirici(state: AgentState):
    if state["karar"] == "ONAY":
        return "cevap_kutusu"
    else:
        return END


# ---------------------------------------------------------------------
# 🕸️ 4. ADIM: AKIŞ ŞEMASINI OLUŞTURMA (BUILD GRAPH)
# ---------------------------------------------------------------------

workflow = StateGraph(AgentState)

# Düğümleri ekliyoruz
workflow.add_node("analist_kutusu", analist_dugumu)
workflow.add_node("karar_kutusu", karar_dugumu)
workflow.add_node("cevap_kutusu", cevap_dugumu)

# Başlangıç ve düz yolları bağlıyoruz
workflow.add_edge(START, "analist_kutusu")
workflow.add_edge("analist_kutusu", "karar_kutusu")

# 🌟 KOŞULLU YOL (Conditional Edge):
# Karar kutusundan sonra 'karar_yonlendirici' fonksiyonunun sonucuna göre yol seç.
# Eğer ONAY dönerse 'cevap_kutusu'na gidecek, RED dönerse END'e gidecek.
workflow.add_conditional_edges(
    "karar_kutusu",
    karar_yonlendirici
)

# Cevap kutusu bittikten sonra doğrudan çıkışa bağla
workflow.add_edge("cevap_kutusu", END)

# Derle
app = workflow.compile()


# ---------------------------------------------------------------------
# 🚀 5. ADIM: AJANI ÇALIŞTIRMA (INVOKE)
# ---------------------------------------------------------------------
if __name__ == "__main__":
    
    # SENARYO 1: Yazılım Sorusu (ONAYLANMALI ve cevaplanmalı)
    print("\n================ SENARYO 1 (Yazılım Konusu) ================")
    durum_1 = {"soru": "Veritabanında sorguları hızlandırmak için nasıl indeks eklerim?"}
    nihai_sonuc_1 = app.invoke(durum_1)
    
    print("\n=== SENARYO 1 RAPORU ===")
    print("Karar Sonucu:", nihai_sonuc_1.get("karar"))
    print("Yazılan Cevap:", nihai_sonuc_1.get("cevap"))

    # SENARYO 2: Yazılım Dışı Soru (REDDEDİLMELİ ve cevap üretilmemeli)
    print("\n================ SENARYO 2 (Yazılım Dışı) ================")
    durum_2 = {"soru": "Çilekli kek nasıl yapılır, malzemeleri nelerdir?"}
    nihai_sonuc_2 = app.invoke(durum_2)
    
    print("\n=== SENARYO 2 RAPORU ===")
    print("Karar Sonucu:", nihai_sonuc_2.get("karar"))
    print("Yazılan Cevap:", nihai_sonuc_2.get("cevap")) # Bunun 'None' veya boş kalmasını bekliyoruz!
