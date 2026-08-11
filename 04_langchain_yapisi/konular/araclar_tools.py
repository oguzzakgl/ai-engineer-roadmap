# faz4_langchain/konular/araclar_tools.py
"""
LANGCHAIN ÖZEL ARAÇLAR (CUSTOM TOOLS)
------------------------------------
Python fonksiyonlarını '@tool' decorator'ü ile LLM'lerin kullanabileceği 
akıllı araçlara dönüştürme.
"""

import os
from dotenv import load_dotenv

from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# API Anahtarı Kontrolü
if "GEMINI_API_KEY" in os.environ and "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]
elif not os.environ.get("GOOGLE_API_KEY"):
    raise ValueError("GEMINI_API_KEY or GOOGLE_API_KEY environment variable is not set!")


# =====================================================================
# 🛠️ 1. ÖZEL PYTHON ARAÇLARI (TOOLS) TANIMLAMA
# =====================================================================

@tool
def hesap_makinesi(sayi1: float, sayi2: float, islem: str) -> float:
    """
    İki sayı arasında matematiksel işlem yapar.
    islem parametresi: 'topla', 'cikar', 'carp', 'bol' olabilir.
    """
    if islem == "topla":
        return sayi1 + sayi2
    elif islem == "cikar":
        return sayi1 - sayi2
    elif islem == "carp":
        return sayi1 * sayi2
    elif islem == "bol":
        return sayi1 / sayi2 if sayi2 != 0 else 0.0
    return 0.0


@tool
def hava_durumu_getir(sehir: str) -> str:
    """
    Belirtilen şehrin canlı hava durumu bilgisini getirir.
    sehir parametresi: Şehir adı (örn: 'İstanbul', 'Ankara', 'İzmir')
    """
    sehir_norm = sehir.lower()
    if "istanbul" in sehir_norm:
        return "İstanbul'da hava 24°C ve güneşli."
    elif "ankara" in sehir_norm:
        return "Ankara'da hava 18°C ve parçalı bulutlu."
    elif "izmir" in sehir_norm:
        return "İzmir'de hava 29°C ve sıcak."
    return f"{sehir} için hava durumu bilgisi: 22°C ve açık."


# =====================================================================
# 🧩 LLM İLE ARAÇLARI BAĞLAMA (TOOL BINDING)
# =====================================================================

if __name__ == "__main__":
    # 1. ChatGoogleGenerativeAI sınıfından model nesnesi oluşturup 'llm' değişkenine atadık
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.0)
    
    # 2. Hazırladığımız araçları bir liste halinde tanımlayıp 'araclar' değişkenine atadık
    araclar = [hesap_makinesi, hava_durumu_getir]
    
    # 3. .bind_tools() metodu ile modelimize araçları bağlayıp 'llm_with_tools' değişkenine atadık
    llm_with_tools = llm.bind_tools(araclar)
    
    # -----------------------------------------------------------------
    # TEST 1: Hava Durumu Aracı Tetikleme
    # -----------------------------------------------------------------
    print("--- TEST 1: Hava Durumu Sorusu ---")
    soru1 = "İzmir'de bugün hava nasıl?"
    yanit1 = llm_with_tools.invoke(soru1)
    
    print("[Modelin Cagirmak Istedigi Arac (Tool Calls)]:")
    for call in yanit1.tool_calls:
        print(f"-> Arac Adi: {call['name']} | Parametreler: {call['args']}")
        
    # -----------------------------------------------------------------
    # TEST 2: Hesap Makinesi Aracı Tetikleme
    # -----------------------------------------------------------------
    print("\n--- TEST 2: Matematiksel Hesap Sorusu ---")
    soru2 = "4587 sayısı ile 982 sayısını çarp."
    yanit2 = llm_with_tools.invoke(soru2)
    
    print("[Modelin Cagirmak Istedigi Arac (Tool Calls)]:")
    for call in yanit2.tool_calls:
        print(f"-> Arac Adi: {call['name']} | Parametreler: {call['args']}")

