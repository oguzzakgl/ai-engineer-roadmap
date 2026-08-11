# faz5_langgraph/proje_kurumsal_multi_agent/agents.py
"""
KURUMSAL ÇOKLU AJAN SİSTEMİ - AJAN MANTIKLARI
---------------------------------------------
Bu dosya Router, SQL Agent ve CRM Agent taslaklarını barındırır.
"""

import os
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# LangChain & LangGraph kütüphaneleri
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_community.agent_toolkits import create_sql_agent
from langgraph.prebuilt import create_react_agent

# Proje bileşenleri
from state import KurumsalState
from tools import gonder_eposta_bildirimi
from db_config import db, sorgula_veritabanini

load_dotenv()

# API Anahtarı Ayarı
if "GEMINI_API_KEY" in os.environ and "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]


# =====================================================================
# 📋 PYDANTIC ŞEMASI: ROUTER KARARI
# =====================================================================

class AjanYonlendirmesi(BaseModel):
    """
    Router ajanın karar şeması. Kullanıcının talebini en uygun uzman ajana yönlendirir.
    """
    yonlendirilecek_ajan: str = Field(
        description="Eğer talep veritabanı, ürün listeleri, çalışan sayıları gibi SQL verileri içeriyorsa 'SQL'; "
                    "Eğer e-posta gönderimi, bildirim veya genel müşteri işlemleri içeriyorsa 'CRM' döndür."
    )
    gerekce: str = Field(
        description="Neden bu ajanı seçtiğine dair kısa, tek cümlelik gerekçe."
    )


# =====================================================================
# 🤖 1. YÖNLENDİRİCİ AJAN (ROUTER AGENT)
# =====================================================================

def yonlendir_sorguyu(state: KurumsalState) -> dict:
    """
    Kullanıcının state['sorgu'] alanındaki girdisini okur.
    AjanYonlendirmesi şemasına göre 'SQL' veya 'CRM' kararı verip state'i günceller.
    
    Öğrenilecek Adımlar:
    1. ChatGoogleGenerativeAI ve PydanticOutputParser(pydantic_object=AjanYonlendirmesi) tanımla.
    2. Prompt şablonunu oluştur.
    3. Zinciri kurup çalıştır (invoke).
    4. Geriye state'deki 'yonlendirilen_ajan' alanını güncelleyecek dict dön.
    """
    print("\n--- [ROUTER] Talep Yönlendiriliyor ---")
    
    # Referans: faz4_langchain/proje_langchain_assistant/intent_router.py dosyasını incele.
    
    return {
        "yonlendirilen_ajan": "SQL",  # Veya "CRM" (Kodu sen yazacaksın)
        "islem_gecmisi": state.get("islem_gecmisi", []) + ["[Router] Talep yönlendirildi."]
    }


# =====================================================================
# 🤖 2. SQL UZMANI AJAN (SQL AGENT - ReAct)
# =====================================================================

def calistir_sql_ajanini(state: KurumsalState) -> dict:
    """
    Kullanıcı talebini alır:
    1. `create_sql_agent` fonksiyonunu kullanarak veritabanına bağlı bir SQL Ajanı oluşturur.
    2. Ajanı invoke ederek SQL sorgusu üretmesini, çalıştırmasını ve yanıt vermesini sağlar.
    3. Üretilen yanıtı state'deki 'ajan_yaniti' alanına kaydeder.
    """
    print("\n--- [SQL AGENT] Veritabanı Sorgulanıyor ---")
    
    # Referans: faz4_langchain/proje_langchain_sifirdan/sql_agent.py dosyasını incele.
    
    return {
        "ajan_yaniti": "Veritabanı sorgu sonucu buraya gelecek (Kodu sen yazacaksın)",
        "islem_gecmisi": state.get("islem_gecmisi", []) + ["[SQL Agent] Veritabanı sorgulandı."]
    }


# =====================================================================
# 🤖 3. CRM UZMANI AJAN (CRM AGENT - ReAct)
# =====================================================================

def calistir_crm_ajanini(state: KurumsalState) -> dict:
    """
    Kullanıcı talebini alır:
    1. CRM ajanı için kullanılacak araçları (`gonder_eposta_bildirimi`) listeler.
    2. `create_react_agent` (veya normal zincir) ile LLM ve e-posta aracını bağlar.
    3. Ajanı çalıştırıp e-posta gönderim sürecini işletir.
    4. Sonucu state'deki 'ajan_yaniti' alanına yazar.
    """
    print("\n--- [CRM AGENT] Müşteri İşlemleri Yapılıyor ---")
    
    # İpucu: 
    # model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    # araclar = [gonder_eposta_bildirimi]
    # crm_agent = create_react_agent(model, tools=araclar)
    # sonuc = crm_agent.invoke({"messages": [("user", state["sorgu"])]})
    
    return {
        "ajan_yaniti": "CRM işlem sonucu buraya gelecek (Kodu sen yazacaksın)",
        "islem_gecmisi": state.get("islem_gecmisi", []) + ["[CRM Agent] Bildirim/İşlem yapıldı."]
    }
