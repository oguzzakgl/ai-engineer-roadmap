# faz4_langchain/proje_langchain_assistant/main_langchain.py
"""
LANGCHAIN İLE KURUMSAL AI DATA ASSISTANT MAIN SERVER
-----------------------------------------------------------------------
🔄 FAZ 3 KARŞILIĞI: 
Bu dosya, Faz 3'teki `faz3/proje_sql_chat/main.py` (210 satırlık ham backend)
dosyasının YERİNE GEÇER. 

Tüm karmaşık mantık LangChain modüllerine dağıtıldığı için bu dosya 
son derece temiz, okuması kolay ve sürdürülebilirdir (Clean Code).
-----------------------------------------------------------------------
"""

import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# LangChain Modüllerimizi İthal Ediyoruz
from pdf_processor_langchain import pdf_islem_langchain
from vector_store_langchain import vektor_veritabani_olustur_langchain, varolan_veritabanini_yukle
from intent_router_langchain import niyet_analizi_yap_langchain
from rag_chain import rag_sohbet_zinciri_kur

load_dotenv()

app = FastAPI(title="LangChain Corporate AI Data Assistant", version="2.0")

# Önbellekteki Vektör Veritabanı ve RAG Zinciri Referansı
GLOBAL_VECTORSTORE = None
GLOBAL_RAG_CHAIN = None

# Girdi ve Çıktı Pydantic Şemaları
class ChatSoruRequest(BaseModel):
    soru: str

class ChatCevapResponse(BaseModel):
    niyet: str
    gerekce: str
    cevap: str
    kaynaklar: list[str] = []


@app.on_event("startup")
def baslangic_ayarlari():
    """Sunucu başlarken varolan ChromaDB veritabanı varsa yükler."""
    global GLOBAL_VECTORSTORE, GLOBAL_RAG_CHAIN
    if os.path.exists("./chroma_db"):
        print("⚡ [Startup] Varolan ChromaDB veritabanı yükleniyor...")
        GLOBAL_VECTORSTORE = varolan_veritabanini_yukle("./chroma_db")
        GLOBAL_RAG_CHAIN = rag_sohbet_zinciri_kur(GLOBAL_VECTORSTORE)
        print("✅ [Startup] LangChain RAG Zinciri hazır!")


@app.post("/upload-pdf")
def pdf_yukle_langchain(file: UploadFile = File(...)):
    """PDF dosyasını yükler, LangChain ile parçalar ve ChromaDB'ye indeksler."""
    global GLOBAL_VECTORSTORE, GLOBAL_RAG_CHAIN
    
    # 1. Dosyayı geçici olarak diske kaydet
    temp_path = f"./temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        # 🔄 FAZ 3 KARŞILIĞI: pdf_processor.py -> pdf_metnini_oku + metni_parcalara_bol
        dokumanlar = pdf_islem_langchain(temp_path)
        
        # 🔄 FAZ 3 KARŞILIĞI: pdf_processor.py -> parca_vektorlerini_uret + SQL Insert
        GLOBAL_VECTORSTORE = vektor_veritabani_olustur_langchain(dokumanlar, db_dizin="./chroma_db")
        
        # 🔄 FAZ 3 KARŞILIĞI: main.py -> RAG zincirini hazırlama
        GLOBAL_RAG_CHAIN = rag_sohbet_zinciri_kur(GLOBAL_VECTORSTORE)
        
        return {
            "mesaj": "PDF dosyası LangChain ile başarıyla işlendi ve ChromaDB'ye kaydedildi.",
            "toplam_parca": len(dokumanlar)
        }
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


@app.post("/chat", response_model=ChatCevapResponse)
def sohbet_langchain(request: ChatSoruRequest):
    """
    Kullanıcı sorusunu alır:
    1. LangChain ile Niyet Analizi yapar.
    2. Niyete göre RAG Zincirini çalıştırır.
    """
    global GLOBAL_RAG_CHAIN
    
    # -----------------------------------------------------------------
    # 🔄 FAZ 3 KARŞILIĞI: main.py içindeki 40 satırlık manuel JSON prompt temizleme
    # -----------------------------------------------------------------
    karar = niyet_analizi_yap_langchain(request.soru)
    print(f"🎯 [LangChain Router] Niyet: {karar.niyet} | Gerekçe: {karar.gerekce}")
    
    if karar.niyet == "BELGE_ARAMA":
        if not GLOBAL_RAG_CHAIN:
            raise HTTPException(status_code=400, detail="Henüz veritabanına bir PDF yüklenmedi!")
            
        # -----------------------------------------------------------------
        # 🔄 FAZ 3 KARŞILIĞI: main.py içindeki ham RAG arama ve prompt birleştirme
        # LangChain .invoke() tek adımda arar, birleştirir ve cevabı üretir.
        # -----------------------------------------------------------------
        rag_sonuc = GLOBAL_RAG_CHAIN.invoke({"input": request.soru})
        
        # Kullanılan kaynak paragraflar
        kaynak_metinler = [doc.page_content for doc in rag_sonuc.get("context", [])]
        
        return ChatCevapResponse(
            niyet=karar.niyet,
            gerekce=karar.gerekce,
            cevap=rag_sonuc.get("answer", ""),
            kaynaklar=kaynak_metinler
        )
    else:
        # VERITABANI_ANALIZ durumu
        return ChatCevapResponse(
            niyet=karar.niyet,
            gerekce=karar.gerekce,
            cevap="Veritabanı Analiz (SQL) isteği tespit edildi.",
            kaynaklar=[]
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
