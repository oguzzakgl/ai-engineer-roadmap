# 05_langgraph_ajanlari/05_react_ajan_mimarisi.py
"""
FAZ 5 - REACT AGENT VE TOOL CALLING (ARAÇ KULLANIMI) DERİNLEŞME PRATİĞİ
------------------------------------------------------------------------------
Bu çalışmada, yapay zekanın (LLM) dış dünyayla konuşmasını sağlayan araç çağrıları (Tool Calls)
ve ReAct (Düşün-Eyleme Geç-Gözlemle) döngüsünün LangGraph üzerindeki uygulamasını pratik edeceğiz.

ÖĞRENECEĞİMİZ KRİTİK KAVRAMLAR:
1. @tool dekoratörü: Standart Python fonksiyonlarını LLM'in anlayacağı araçlara dönüştürme.
2. Docstring Önemi: LLM'in aracı ne zaman ve nasıl kullanacağını anlaması için açıklama yazma.
3. create_react_agent: LangGraph'in otonom karar veren hazır ajan yapısı.
"""

import os
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

# Env yükle
load_dotenv()

# API Key Kontrolleri
if "GEMINI_API_KEY" in os.environ and "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]


# =====================================================================
# 🛠️ ADIM 1: ARAÇLARIN (TOOLS) TANIMLANMASI
# =====================================================================
# Görev: LLM'in matematik yapması ve veritabanı araması için kullanacağı 2 araç yaz.
# İpucu: @tool dekoratörünü kullan ve fonksiyonun ne işe yaradığını docstring olarak yaz (LLM burayı okur!).

@tool
def hesapla_toplam(a: int, b: int) -> int:
    """İki tam sayıyı toplar ve sonucu döndürür. Matematiksel işlemler için bu aracı kullan."""
    # Kodu sen yazacaksın
    pass


@tool
def ara_veritabaninda(sorgu: str) -> str:
    """Veritabanında müşteri veya ürün araması yapar. Hukuk, veritabanı veya bilgi sorgularında bu aracı kullan."""
    # Kodu sen yazacaksın
    # Mock (sahte) bir veri döndürebilirsin (örn: "Müşteri Ali Yılmaz: Bakiye 500 TL")
    pass


# =====================================================================
# 🤖 ADIM 2: LLM VE RE-ACT AJANININ KURULMASI
# =====================================================================
# Görev: gemini-2.5-flash modelini tanımla, araçları listeye ekle ve create_react_agent ile ajanı kur.

def kur_react_ajanini():
    # Kodu sen yazacaksın
    # 1. llm = ChatGoogleGenerativeAI(...)
    # 2. araclar = [...]
    # 3. return create_react_agent(llm, tools=araclar)
    pass


if __name__ == "__main__":
    print("🤖 ReAct Agent (Tool Calling) Derinleşme Çalışması Başlatılıyor...\n")
    # Test Etme Alanı
    # ajan = kur_react_ajanini()
    
    # Test 1 (Matematik Sorusu): "15 ile 27'yi toplar mısın?"
    # print("--- TEST 1 ---")
    # response = ajan.invoke({"messages": [("user", "15 ile 27 sayılarının toplamı kaçtır?")]})
    # print(response["messages"][-1].content)
    
    # Test 2 (Veri Sorgusu): "Ali Yılmaz kimdir?"
    # print("\n--- TEST 2 ---")
    # response = ajan.invoke({"messages": [("user", "Veritabanında Ali Yılmaz araması yapar mısın?")]})
    # print(response["messages"][-1].content)
