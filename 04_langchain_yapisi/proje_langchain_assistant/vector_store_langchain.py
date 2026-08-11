# faz4_langchain/proje_langchain_assistant/vector_store_langchain.py
"""
LANGCHAIN ILE VEKTÖR VERİTABANI VE EMBEDDING (ChromaDB + Gemini)
-----------------------------------------------------------------------
🔄 FAZ 3 KARŞILIĞI: 
Bu dosya, Faz 3'teki:
1. `pdf_processor.py` -> `parca_vektorlerini_uret()` (15 satır - Gemini API toplu istek)
2. `crud.py` -> `pdf_paragraf_ara_vektorle()` (20 satır - Ham SQL CAST(AS vector) sorgusu)
toplam 35 satırlık kodun YERİNE GEÇER.
-----------------------------------------------------------------------
"""

import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

# Gemini API anahtarı kontrolü
if "GEMINI_API_KEY" in os.environ and "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]


def vektor_veritabani_olustur_langchain(dokumanlar: list[Document], db_dizin: str = "./chroma_db") -> Chroma:
    """
    LangChain döküman listesini alır, Gemini ile vektörleştirir ve ChromaDB'ye kaydeder.
    """
    print("🧠 [LangChain] Gemini Embedding modeli başlatılıyor...")
    
    # -----------------------------------------------------------------
    # 🔄 FAZ 3 KARŞILIĞI: pdf_processor.py -> client.models.embed_content()
    # -----------------------------------------------------------------
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    
    print(f"💾 [LangChain] {len(dokumanlar)} döküman ChromaDB yerel veritabanına indeksleniyor...")
    
    # -----------------------------------------------------------------
    # 🔄 FAZ 3 KARŞILIĞI: crud.py -> PDFParagrafTablosu veritabanına kaydetme + CAST işlemi
    # Chroma.from_documents hem API'ye istek atar hem de diskte saklar.
    # -----------------------------------------------------------------
    vectorstore = Chroma.from_documents(
        documents=dokumanlar,
        embedding=embeddings,
        persist_directory=db_dizin
    )
    
    print(f"✅ [LangChain] Vektör veritabanı başarıyla oluşturuldu ve '{db_dizin}' klasörüne kaydedildi.")
    return vectorstore


def varolan_veritabanini_yukle(db_dizin: str = "./chroma_db") -> Chroma:
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    vectorstore = Chroma(
        persist_directory=db_dizin,
        embedding_function=embeddings
    )
    return vectorstore


if __name__ == "__main__":
    print("Vector Store LangChain Modülü Hazır!")
