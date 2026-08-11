# faz4_langchain/konular/sohbet_hafizasi.py
"""
LANGCHAIN CONVERSATIONAL MEMORY (SOHBET HAFIZASI)
--------------------------------------------------
LLM'lere oturum kimliği (session_id) bazında geçmiş konuşmaları 
hatırlatma yeteneği kazandırır.
"""

import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

load_dotenv()

# API Anahtarı Kontrolü
if "GEMINI_API_KEY" in os.environ and "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]
elif not os.environ.get("GOOGLE_API_KEY"):
    raise ValueError("GEMINI_API_KEY or GOOGLE_API_KEY environment variable is not set!")



# =====================================================================
# 🧠 OTURUM DEPOSU (SESSION STORE)
# =====================================================================
# Her session_id (örn: "kullanici_1") için ayrı bir Sohbet Geçmişi tutan sözlük
store = {}

def get_session_history(session_id: str):
    """
    Verilen session_id için var olan sohbet geçmişini döner, 
    yoksa yeni bir InMemoryChatMessageHistory oluşturur.
    """
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


# =====================================================================
# 🧩 ZİNCİR VE HAFIZA ENTEGRASYONU
# =====================================================================

def hafizali_bot_olustur():
    # 1. ChatGoogleGenerativeAI sınıfından model nesnesi oluşturup 'llm' değişkenine atadık
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
    
    # 2. ChatPromptTemplate ve MessagesPlaceholder ile prompt oluşturup 'prompt' değişkenine atadık
    # MessagesPlaceholder(variable_name="history") geçmiş konuşmaları buraya enjekte eder.
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Sen yardımcı ve kibar bir AI Asistanısın."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    
    # 3. Pipe (|) ile temel zinciri kurup 'chain' değişkenine atadık
    chain = prompt | llm
    
    # 4. RunnableWithMessageHistory ile hafızalı zinciri kurup 'with_history_chain' değişkenine atadık
    with_history_chain = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history"
    )
    
    return with_history_chain


if __name__ == "__main__":
    # hafizali_bot_olustur() fonksiyonunu çağırıp hafızalı zinciri 'bot' değişkenine atadık
    bot = hafizali_bot_olustur()
    
    # Oturum Kimliği (Session ID) belirledik
    config = {"configurable": {"session_id": "oguz_oturumu"}}
    
    # 1. Soru
    print("--- 1. SORU ---")
    cevap1 = bot.invoke({"input": "Merhaba! Ben Oğuz. Bilgisayar Mühendisiyim."}, config=config)
    print("Bot:", cevap1.content)
    
    # 2. Soru (Hafıza Testi)
    print("\n--- 2. SORU (HAFIZA TESTİ) ---")
    cevap2 = bot.invoke({"input": "Benim adım neydi ve mesleğim nedir?"}, config=config)
    print("Bot:", cevap2.content)
