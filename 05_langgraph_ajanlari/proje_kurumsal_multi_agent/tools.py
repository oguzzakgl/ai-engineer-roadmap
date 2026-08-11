# faz5_langgraph/proje_kurumsal_multi_agent/tools.py
"""
KURUMSAL ÇOKLU AJAN SİSTEMİ - MÜŞTERİ İLETİŞİM ARAÇLARI (TOOLS)
--------------------------------------------------------------
CRM Ajanı tarafından kullanılacak LangChain @tool decorated e-posta gönderme aracı.
"""

from langchain_core.tools import tool

@tool
def gonder_eposta_bildirimi(alici_eposta: str, konu: str, icerik: str) -> str:
    """
    Belirtilen alıcıya, konu ve içerik ile e-posta gönderimi simüle eder.
    
    Öğrenilecek Adımlar:
    1. Eski projedeki `eposta_gonder` aracını referans al.
    2. E-postanın kime, hangi konuyla ve içerikle gönderildiğini terminale yazdır (print).
    3. Geriye başarılı olduğuna dair açıklayıcı bir metin dön.
    """
    # Referans: faz4_langchain/proje_langchain_assistant/email_tool.py dosyasındaki eposta_gonder tool'unu incele.
    
    print(f"\n📧 [SIMULATOR] E-Posta Gönderiliyor...")
    print(f"   Kime: {alici_eposta}")
    print(f"   Konu: {konu}")
    print(f"   İçerik: {icerik}\n")
    
    return f"E-posta başarıyla {alici_eposta} adresine gönderildi."
