# 06_ileri_duzey_rag_sistemleri/01_query_translation_ve_decomposition.py
"""
🧠 FAZ 5 - ADIM 1: İLERİ DÜZEY RAG (QUERY TRANSLATION & DECOMPOSITION)
------------------------------------------------------------------------------
NEDİR?
1. Query Translation (Multi-Query): Kullanıcı bazen arama motorunun veya vektör DB'nin 
   anlayacağı doğru kelimeleri kullanamaz. Bu durumda, LLM'e kullanıcının sorusunu 
   farklı açılardan 3-4 alternatif cümleyle yeniden yazdırırız. Tüm bu alternatiflerle 
   vektör DB'de arama yapar, çıkan dökümanları tekilleştirip LLM'e bağlam olarak veririz.
   Böylece döküman kaçırma riski minimize edilir.

2. Query Decomposition (Sorguyu Alt Parçalara Bölme): Kullanıcı karmaşık veya iki şeyi 
   karşılaştıran bir soru sorduğunda (Örn: "FastAPI ile Flask arasındaki farklar nelerdir?"), 
   vektör DB tek bir sorguyla doğru dökümanları getiremez. LLM'e bu soruyu "FastAPI nedir?" 
   ve "Flask nedir?" gibi 2 basit alt soruya böldürürüz. Ayrı ayrı arama yapıp bağlamları birleştiririz.

---
ÖDEV GÖREVLERİNİZ:
- Görev 1: uret_alternatif_sorgular() -> LLM kullanarak gelen soruyu 3 alternatif soruya genişletin.
- Görev 2: dökümanlari_tekillestir() -> Farklı sorgulardan dönen aynı dökümanların kopyalarını temizleyin.
- Görev 3: sorguyu_alt_parcalara_bol() -> Karmaşık karşılaştırmalı soruyu 2 basit alt soruya bölün.
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

# 📋 BOILERPLATE: Test Veritabanı Kurulumu (Bu kısma dokunmanıza gerek yok)
print("1. Geçici ChromaDB yükleniyor ve örnek veriler indeksleniyor...")
ornek_dokümanlar = [
    Document(page_content="Oğuz Kaan, FastAPI kullanarak yüksek performanslı asenkron API'ler geliştirmiştir.", metadata={"id": 1}),
    Document(page_content="PostgreSQL, Neon DB ve SQLAlchemy kullanarak ilişkisel veritabanları ve CRUD işlemleri yapmıştır.", metadata={"id": 2}),
    Document(page_content="LangGraph kullanarak otonom çoklu ajan (multi-agent) mimarileri üzerine çalışmalar yapmıştır.", metadata={"id": 3}),
    Document(page_content="Yapay zeka modellerini Docker konteynerleri içine alarak lokalde test etmiştir.", metadata={"id": 4}),
    Document(page_content="Arize Phoenix ve OpenTelemetry ile LLM tracing entegrasyonu kurmuştur.", metadata={"id": 5})
]

embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2")
vectorstore = Chroma.from_documents(ornek_dokümanlar, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# Değerlendirme için LLM Tanımı
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.0)


# =====================================================================
# 🔥 GÖREV 1: MULTI-QUERY GENERATOR (Sorgu Çeşitlendirme)
# =====================================================================
def uret_alternatif_sorgular(orijinal_sorgu: str) -> list[str]:
    """
    Görev: Kullanıcının girdiği orijinal soruyu, vektör aramada performansı artırmak 
    için LLM kullanarak 3 farklı alternatif cümle ile yeniden yazdırın.
    
    İpuçları:
    - Bir ChatPromptTemplate oluşturun. LLM'e rol verip her bir alternatif soruyu 
      yeni bir satırda yazmasını söyleyin.
    - LLM çıktısını StrOutputParser() ile parse edin.
    - Dönen metni satır bazlı ayırıp (.split('\n')) boş satırları temizleyin.
    - Listenin sonuna orijinal sorgunun kendisini de eklemeyi unutmayın!
    """
    prompt = ChatPromptTemplate.from_template(
    "Sen bir arama asistanısın. Kullanıcının verdiği soruyu "
    "vektör veritabanında aratmak üzere 3 farklı alternatif cümleyle yeniden yaz.\n"
    "Kurallar:\n"
    "- Her alternatif soruyu yeni bir satırda yaz.\n"
    "- Başına numara (1, 2, 3) veya işaret koyma.\n\n"
    "Kullanıcı Sorusu: {soru}\n"
    "Alternatif Sorgular:"
)
    
    chain = prompt | llm | StrOutputParser()
    
    yanit = chain.invoke({"soru": orijinal_sorgu})

    sorgular = [s.strip() for s in yanit.split('\n') if s.strip()]

    sorgular.append(orijinal_sorgu)

    return sorgular


# =====================================================================
# 🔥 GÖREV 2: DOCUMENT UNIQUIFICATION (Döküman Tekilleştirme)
# =====================================================================
def dökümanlari_tekillestir(döküman_listesi: list[Document]) -> list[Document]:
    """
    Görev: Çoklu aramalar sonucunda dönen ham döküman listesinde, aynı içeriğe sahip
    dökümanların kopyalarını (kullanıcıya gereksiz veri gitmemesi için) temizleyin.
    
    İpuçları:
    - Bir set() kullanarak daha önce eklediğiniz page_content değerlerini takip edin.
    - Liste içindeki her dökümanın page_content değerini kontrol edip sadece benzersiz olanları 
      yeni bir döküman listesine ekleyin.
    """
    gorulenler = set()
    yeni_liste = []
    for doc in döküman_listesi:
        if doc.page_content not in gorulenler:
            gorulenler.add(doc.page_content)
            yeni_liste.append(doc)
    return yeni_liste


# =====================================================================
# 🔥 GÖREV 3: QUERY DECOMPOSITION (Sorgu Parçalama)
# =====================================================================
def sorguyu_alt_parcalara_bol(karmaşik_sorgu: str) -> list[str]:
    """
    Görev: Karşılaştırmalı veya çok adımlı karmaşık bir soruyu alıp, vektör DB'de 
    ayrı ayrı aranabilecek 2 adet bağımsız basit alt soruya bölün.
    
    İpuçları:
    - LLM'e karmaşık soruyu girdi olarak verip, 2 alt soruyu yeni satırlarda 
      dönmesini isteyen bir ChatPromptTemplate yazın.
    - Çıktıyı parse edin ve satırlara bölerek bir liste olarak döndürün.
    """
    prompt = ChatPromptTemplate.from_template(
    """
    Sen bir soru analizörüsün. Aşağıdaki karmaşık soruyu, vektör veritabanında 
    ayrı ayrı aranabilecek 2 adet bağımsız basit alt soruya ayır.

    Kurallar:
    - Her alt soruyu yeni bir satırda yaz.
    - Basit ve anlaşılır cümleler kullan.
    - Karşılaştırma veya çok adımlı mantığı koru ama sorguları sadeleştir.

    Karmaşık Soru: {soru}
    Alt Sorular:
    """
)
    chain = prompt | llm | StrOutputParser()

    yanit = chain.invoke({"soru": karmaşik_sorgu})
    
    alt_sorgular = [s.strip() for s in yanit.split('\n') if s.strip()]
    
    return alt_sorgular


# =====================================================================
# 🧪 TEST VE DOĞRULAMA ALANI (Çalıştırıp sonuçları görün)
# =====================================================================
# Çalıştırmak için: $env:PYTHONIOENCODING="utf-8"; py 06_ileri_duzey_rag_sistemleri/01_query_translation_ve_decomposition.py
# =====================================================================
if __name__ == "__main__":
    print("\n" + "="*50)
    print("🧪 TEST 1: MULTI-QUERY VE TEKİLLEŞTİRME TESTİ")
    print("="*50)
    
    test_sorgu = "Oğuz'un veritabanları ile ilgili ne tecrübesi var?"
    print(f"Orijinal Sorgu: {test_sorgu}\n")
    
    alternatifler = uret_alternatif_sorgular(test_sorgu)
    print("Üretilen Alternatif Sorgular:")
    for i, s in enumerate(alternatifler, 1):
        print(f"  {i}. {s}")
        
    toplam_dökümanlar = []
    for sorgu in alternatifler:
        docs = retriever.invoke(sorgu)
        toplam_dökümanlar.extend(docs)
        
    print(f"\nToplam dönen ham döküman sayısı: {len(toplam_dökümanlar)}")
    
    tekil_sonuclar = dökümanlari_tekillestir(toplam_dökümanlar)
    print(f"Tekilleştirilmiş döküman sayısı: {len(tekil_sonuclar)}")
    print("\nBulunan Bağlamlar (Contexts):")
    for doc in tekil_sonuclar:
        print(f"  - {doc.page_content}")
        
    print("\n" + "="*50)
    print("🧪 TEST 2: QUERY DECOMPOSITION TESTİ")
    print("="*50)
    
    karsilastirmali_sorgu = "Oğuz Kaan'ın API geliştirme deneyimi ile otonom ajan deneyimi arasındaki farklar nelerdir?"
    print(f"Karmaşık Soru: {karsilastirmali_sorgu}\n")
    
    alt_sorular = sorguyu_alt_parcalara_bol(karsilastirmali_sorgu)
    print("Alt Sorulara Bölünmüş Hali:")
    for i, s in enumerate(alt_sorular, 1):
        print(f"  {i}. {s}")
        
    print("\nHer bir alt soru için arama sonuçları:")
    for s in alt_sorular:
        docs = retriever.invoke(s)
        print(f"\n-> Sorgu: '{s}'")
        for doc in docs:
            print(f"   * {doc.page_content}")
            
    print("\n" + "="*50)
