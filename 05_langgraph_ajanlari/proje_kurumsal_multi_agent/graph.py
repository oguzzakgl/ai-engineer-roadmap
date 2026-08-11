# faz5_langgraph/proje_kurumsal_multi_agent/graph.py
"""
KURUMSAL ÇOKLU AJAN SİSTEMİ - GRAPH MODÜLÜ
------------------------------------------
StateGraph nesnesini kurar ve Router'ın kararına göre SQL veya CRM ajanını tetikler.
"""

from langgraph.graph import StateGraph, END

# Durum ve Ajan fonksiyonlarımız
from state import KurumsalState
from agents import yonlendir_sorguyu, calistir_sql_ajanini, calistir_crm_ajanini


# =====================================================================
# 🚦 KOŞULLU YÖNLENDİRİCİ (CONDITIONAL ROUTER)
# =====================================================================

def degerlendir_ve_yonlendir(state: KurumsalState) -> str:
    """
    State içindeki 'yonlendirilen_ajan' değerine bakar ve akışı yönlendirir.
    
    Öğrenilecek Adımlar:
    1. state['yonlendirilen_ajan'] değerini oku.
    2. Değer 'SQL' ise 'sql_uzmani' düğümüne yönlendir.
    3. Değer 'CRM' ise 'crm_uzmani' düğümüne yönlendir.
    4. Geçersiz bir durum varsa END dön.
    """
    print("\n--- [ROUTER DEĞERLENDİRME] Akış Yönü Seçiliyor ---")
    
    # 📌 Dönüş değeri hedef düğümün adı olmalıdır ("sql_uzmani" veya "crm_uzmani")
    # return "sql_uzmani"
    
    return END # Kodu sen yazacaksın
    

# =====================================================================
# 🏗️ STATEGRAPH KURULUMU
# =====================================================================

# 1. StateGraph nesnesini KurumsalState ile başlatıyoruz
workflow = StateGraph(KurumsalState)

# 2. Düğümleri (Nodes) ekliyoruz
workflow.add_node("yonlendirici", yonlendir_sorguyu)
workflow.add_node("sql_uzmani", calistir_sql_ajanini)
workflow.add_node("crm_uzmani", calistir_crm_ajanini)

# 3. Akış yollarını (Edges) kuruyoruz
workflow.set_entry_point("yonlendirici")

# Koşullu Yönlendirme: 'yonlendirici' çalıştıktan sonra 'degerlendir_ve_yonlendir' ile ayrım yap
workflow.add_conditional_edges(
    "yonlendirici",
    degerlendir_ve_yonlendir
)

# Düz Geçişler: Uzman ajanlar işlerini bitirince doğrudan sonlanırlar (END)
workflow.add_edge("sql_uzmani", END)
workflow.add_edge("crm_uzmani", END)

# 4. Grafiği derliyoruz (Compile)
app = workflow.compile()
