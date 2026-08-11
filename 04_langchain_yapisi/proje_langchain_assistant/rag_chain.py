# faz4_langchain/proje_langchain_assistant/rag_chain.py
"""
LANGCHAIN ILE RAG SOHBET VE DÖKÜMAN ARAMA (RETRIEVAL CHAIN)
-----------------------------------------------------------------------
🔄 FAZ 3 KARŞILIĞI: 
Bu dosya, Faz 3'teki `faz3/proje_sql_chat/main.py` ve `crud.py` içindeki:
1. `pdf_paragraf_ara_vektorle()` (Veritabanından vektörle arama)
2. Paragrafları birleştirip prompt'a yapıştırma
3. Gemini'ye istek atıp cevabı döndürme
toplam 45 satırlık kodun YERİNE GEÇER.
-----------------------------------------------------------------------
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

load_dotenv()

# Gemini API anahtarı kontrolü
if "GEMINI_API_KEY" in os.environ and "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]


def rag_sohbet_zinciri_kur(vectorstore: Chroma):
    """
    LangChain VectorStore nesnesini alır ve otomatik RAG zincirini kurar.
    """
    # -----------------------------------------------------------------
    # 🔄 FAZ 3 KARŞILIĞI: main.py içindeki Gemini Chat Client
    # -----------------------------------------------------------------
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)
    
    # -----------------------------------------------------------------
    # 🔄 FAZ 3 KARŞILIĞI: crud.py -> pdf_paragraf_ara_vektorle()
    # vectorstore.as_retriever() tek satırda arama motoruna dönüşür. (k=3 en yakın 3 döküman)
    # -----------------------------------------------------------------
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    # -----------------------------------------------------------------
    # 🔄 FAZ 3 KARŞILIĞI: main.py içindeki RAG Prompt Metni
    # {{context}} değişkenine veritabanından çekilen paragraflar otomatik gömülür!
    # -----------------------------------------------------------------
    system_prompt = (
        "Sen kurumsal bir bilgi asistanısın. Aşağıda sana verilen kurumsal döküman bağlamını (context) "
        "kullanarak kullanıcının sorusuna doğru, öz ve nazik bir dille cevap ver.\n"
        "Eğer verilen dökümanlarda sorunun cevabı yoksa, bilmediğini nazikçe belirt.\n\n"
        "Kurumsal Bağlam (Context):\n{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])
    
    # -----------------------------------------------------------------
    # 🔄 FAZ 3 KARŞILIĞI: Dökümanları birleştirme + LLM'e gönderme zinciri
    # -----------------------------------------------------------------
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    
    # -----------------------------------------------------------------
    # 🔄 FAZ 3 KARŞILIĞI: Arama Motoru + LLM Birleşik RAG Zinciri
    # -----------------------------------------------------------------
    rag_chain = create_retrieval_chain(retriever, combine_docs_chain)
    
    return rag_chain


if __name__ == "__main__":
    print("RAG Sohbet LangChain Modülü Hazır!")
