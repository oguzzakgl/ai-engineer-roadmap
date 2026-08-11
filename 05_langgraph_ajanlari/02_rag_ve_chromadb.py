# 05_langgraph_ajanlari/02_rag_ve_chromadb.py
"""
FAZ 5 - RAG (RETRIEVAL-AUGMENTED GENERATION) BİLGİ TAZELEME VE PRATİK ÇALIŞMASI
------------------------------------------------------------------------------
Amaç: PDF dökümanını yükleme, metni parçalama, Gemini embeddings ile 
vektörleştirip ChromaDB'ye yazma ve RAG araması yapma adımlarını sıfırdan yazıp kavramak.
"""

import os
from dotenv import load_dotenv

# LangChain RAG & Vektör Bileşenleri
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# API Anahtarı Ayarı
if "GEMINI_API_KEY" in os.environ and "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",)
embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2")
parser = StrOutputParser()

# =====================================================================
# 📁 ADIM 1: PDF YÜKLEME, PARÇALAMA VE INDEKSLEME (RAG PIPELINE)
# =====================================================================
# Görev: Verilen PDF dosyasını okuyup ChromaDB retriever nesnesini dönen fonksiyonu yaz.
# Fonksiyon ismi fiille başlasın (örn: hazirla_rag_veritabanini).

def hazirla_rag_veritabanini(pdf_yolu: str):
    """
    1. PyPDFLoader ile PDF dosyasını yükle.
    2. RecursiveCharacterTextSplitter (chunk_size=400, chunk_overlap=40) ile metinleri parçala.
    3. GoogleGenerativeAIEmbeddings (model="gemini-embedding-2") tanımla.
    4. Chroma.from_documents() kullanarak geçici veya kalıcı veritabanına indeksle.
    5. as_retriever(search_kwargs={"k": 2}) ile arama getirici nesnesini döndür.
    """
    # Kodu sen yazacaksın
    loader = PyPDFLoader(pdf_yolu)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=40)
    docs = splitter.split_documents(docs)

    vector_db = Chroma.from_documents(documents=docs, embedding=embeddings)
    retriever = vector_db.as_retriever(search_kwargs={"k": 2})
    return retriever


# =====================================================================
# 🧠 ADIM 2: RAG SORU-CEVAP ZİNCİRİ
# =====================================================================
# Görev: Retriever ve soru parametrelerini alıp bağlama göre cevap üreten fonksiyonu yaz.
# Fonksiyon ismi fiille başlasın (örn: sor_soruyu_rag_ile).

def sor_soruyu_rag_ile(retriever, soru: str) -> str:
    """
    1. ChatGoogleGenerativeAI (gemini-2.5-flash) tanımla.
    2. Prompt şablonu oluştur. Sistem: "Aşağıdaki bağlama göre soruyu yanıtla: {context}"
       Kullanıcı: "Soru: {soru}"
    3. RAG zincirini kur. İpuçları:
       - bağlamı retriever'dan okumak için: {"context": retriever, "soru": RunnablePassthrough()}
       - zincir yapısı: context_hazirlayici | prompt | llm | StrOutputParser()
    4. invoke({input: soru}) veya invoke(soru) ile çalıştır ve string yanıtı dön.
    """
    # Kodu sen yazacaksın
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Aşağıdaki bağlama göre soruyu yanıtla:\n\n{context}"),
        ("user", "Soru: {soru}")
    ])

    context_hazirlayici = {"context": retriever, "soru": RunnablePassthrough()}

    zincir = context_hazirlayici | prompt | llm | parser
    return zincir.invoke(soru)


if __name__ == "__main__":
    print("📚 RAG Tekrar Çalışması Başlatılıyor...\n")
    
    # Reborn klasörünün ana dizinindeki test PDF'i
    pdf_yolu = "../sirket_mevzuati.pdf"
    
    # Veritabanını hazırla
    retriever = hazirla_rag_veritabanini(pdf_yolu)
    
    # Soruyu sor
    cevap = sor_soruyu_rag_ile(retriever, "yıllık izin kaç gün")
    
    print("\n--- RAG CEVABI ---")
    print(cevap)
