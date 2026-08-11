# 06_ileri_duzey_rag_sistemleri/02_reranking_ve_cross_encoder.py
"""
🧠 FAZ 5 - ADIM 2: İLERİ DÜZEY RAG - RERANKING (YENİDEN SIRALAMA)
------------------------------------------------------------------------------
NEDİR?
Vektör veritabanları (Chroma, pgvector) arama yaparken "Bi-Encoder" mantığı kullanır.
Yani dökümanları ve soruyu ayrı ayrı vektörlere çevirir, aralarındaki açıya (Cosine Similarity) 
bakar. Bu işlem milisaniyeler sürer, çok hızlıdır ama her zaman "en derin ilişkileri" yakalayamaz.

"Reranking (Yeniden Sıralama)" ise bu sürece ikinci bir aşama ekler:
1. Geri Getirme Aşaması (Retrieval): Vektör DB'den hızlıca geniş bir liste (Örn: 10 döküman) çekilir.
2. Puanlama Aşaması (Reranking): Çekilen dökümanlar ve kullanıcının sorusu bir "Cross-Encoder" modeline 
   veya akıllı bir LLM'e verilir. Bu model soru ile dökümanı kelime kelime, derinlemesine karşılaştırarak 
   0 ile 10 arası bir alaka puanı verir.
3. Filtreleme Aşaması: En yüksek puanı alan ilk 3 döküman seçilerek ana LLM'e (Gemini) beslenir.

AVANTAJLARI:
- Vektör DB'nin kaçırdığı detaylı dökümanları yukarı taşır (Daha yüksek doğruluk).
- LLM'e giden bağlam (context) kalitesini artırır, böylece model gereksiz verileri okumakla vakit kaybetmez.

---
ÖDEV GÖREVLERİNİZ:
- Görev 1: gemini_ile_dokumanlari_puanla() -> Gemini'ı bir Reranker olarak kullanarak her dökümana 0-10 arası bir alaka puanı verdirin.
- Görev 2: rerank_dokumanlari() -> Puanlanan dökümanları büyükten küçüğe sıralayıp en iyi ilk N dökümanı filtreleyin.
"""

import os
from dotenv import load_dotenv
load_dotenv()

# API Key Kontrolü
if "GEMINI_API_KEY" in os.environ and "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 📋 BOILERPLATE: Test Verileri ve Geçici Veritabanı Kurulumu
print("1. Geçici veritabanı yükleniyor ve aday yetkinlik dökümanları indeksleniyor...")
ornek_dokümanlar = [
    Document(page_content="Aday Python programlama dilinde 5 yıl deneyimlidir. FastAPI ve Django projeleri geliştirmiştir.", metadata={"id": 1}),
    Document(page_content="Aday sadece temel düzeyde Python bilmektedir, projelerinde genellikle JavaScript kullanmıştır.", metadata={"id": 2}),
    Document(page_content="Aday veritabanı optimizasyonları, SQL sorguları yazma ve PostgreSQL konusunda uzmandır.", metadata={"id": 3}),
    Document(page_content="Aday makine öğrenmesi modelleri ve veri analitiği üzerine çalışmıştır, derin öğrenme tecrübesi vardır.", metadata={"id": 4}),
    Document(page_content="Adayın Python deneyimi sadece veri analizi kütüphaneleri (pandas, numpy) ile sınırlıdır, web backend bilmez.", metadata={"id": 5})
]

embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2")
vectorstore = Chroma.from_documents(ornek_dokümanlar, embeddings)
# Geniş bir havuz çekmek için retriever arama sınırını (k) 5 olarak ayarlıyoruz
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# Rerank yapmak için kullanacağımız LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.0)


# =====================================================================
# 🔥 GÖREV 1: GEMINI ILE DÖKÜMANLARI PUANLAMA
# =====================================================================
def gemini_ile_dokumanlari_puanla(soru: str, dokumanlar: list[Document]) -> list[tuple[Document, float]]:
    """
    Görev: Gelen döküman listesindeki her dökümanı kullanıcının sorusuna göre 
    Gemini kullanarak 0.0 ile 10.0 arasında puanlayın.
    
    İpuçları:
    - Bir ChatPromptTemplate oluşturun. LLM'e bir hakem rolü verin.
    - Promptta LLM'den dökümanı incelemesini ve soruyla alakasını 0 ile 10 arasında 
      sadece bir sayı (float) olarak dönmesini isteyin. Ekstra açıklama yapmamasını belirtin.
    - Bir for döngüsüyle her dökümanı tek tek LLM'e gönderip puan alın.
    - Hata almamak için LLM çıktısını float'a çevirmeyi deneyin (try/except ile hata durumunda 0.0 verin).
    - Geriye (Document, puan) ikililerinden (tuple) oluşan bir liste döndürün.
    """
    puanlanmis_list = []
    
    # TODO: Kodunuzu buraya yazın
    
    return puanlanmis_list


# =====================================================================
# 🔥 GÖREV 2: SIRALAMA VE FİLTRELEME (Reranking)
# =====================================================================
def rerank_dokumanlari(puanlanmis_dokumanlar: list[tuple[Document, float]], top_n: int = 2) -> list[Document]:
    """
    Görev: Puanlanmış döküman listesini puanlarına göre büyükten küçüğe sıralayın 
    ve en yüksek puanlı ilk top_n adet dökümanı geriye liste olarak döndürün.
    
    İpuçları:
    - Python'ın sorted() fonksiyonunu kullanın. Sıralama anahtarı (key) olarak 
      puanı (yani tuple'ın 2. elemanını) belirtin: key=lambda x: x[1]
    - Büyükten küçüğe sıralama için reverse=True parametresini ekleyin.
    - Sıralanan listeden sadece Document nesnelerini çıkarıp ilk top_n elemanı dilimleyin (slicing).
    """
    # TODO: Kodunuzu buraya yazın
    return []


# =====================================================================
# 🧪 TEST VE DOĞRULAMA ALANI
# =====================================================================
# Çalıştırmak için: $env:PYTHONIOENCODING="utf-8"; py 06_ileri_duzey_rag_sistemleri/02_reranking_ve_cross_encoder.py
# =====================================================================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🧪 TEST: RERANKER (YENİDEN SIRALAMA) TESTİ")
    print("="*60)
    
    test_soru = "FastAPI ve web backend projelerinde deneyimli uzman Python geliştiricisi arıyoruz."
    print(f"Kullanıcı İhtiyacı / Soru: '{test_sorgu}'\n")
    
    # Adım 1: Standart Vektör Araması ile geniş havuzu çekelim (k=5)
    ham_dokümanlar = retriever.invoke(test_soru)
    print("--- STANDART VEKTÖR ARAMASI SONUÇLARI (ChromaDB Sıralaması) ---")
    for i, doc in enumerate(ham_dokümanlar, 1):
        print(f"  {i}. [ID: {doc.metadata['id']}] {doc.page_content[:80]}...")
        
    print("\n--- GEMINI ILE RERANKING BAŞLIYOR ---")
    # Adım 2: Çekilen dökümanları Gemini ile puanlayalım
    puanlanmis = gemini_ile_dokumanlari_puanla(test_soru, ham_dokümanlar)
    
    print("\nLLM Puanlama Sonuçları:")
    for doc, puan in puanlanmis:
         print(f"  * [ID: {doc.metadata['id']}] Puan: {puan:.1f}/10.0 -> {doc.page_content[:60]}...")
         
    # Adım 3: Yeniden sıralayıp en iyi ilk 2 dökümanı seçelim
    reranked_dokümanlar = rerank_dokumanlari(puanlanmis, top_n=2)
    
    print("\n--- RERANKED (YENİDEN SIRALANMIŞ) NİHAİ EN İYİ 2 DÖKÜMAN ---")
    for i, doc in enumerate(reranked_dokümanlar, 1):
         print(f"  🏆 {i}. [ID: {doc.metadata['id']}] {doc.page_content}")
         
    print("\n" + "="*60)
