# 06_ileri_duzey_rag_sistemleri/03_graph_rag_temelleri.py
"""
🧠 FAZ 5 - ADIM 3: İLERİ DÜZEY RAG - MINI GRAPHRAG (BİLGİ GRAFİKLERİ)
------------------------------------------------------------------------------
NEDİR?
Standart RAG (Vector Search) verileri düz metin parçaları olarak saklar. Eğer aradığınız 
bilgi birbiriyle dolaylı yoldan ilişkili iki ayrı dökümandaysa, standart RAG bu zinciri 
takip edip doğru çıkarımı yapamaz. Buna "Multi-Hop" (Çok Adımlı) akıl yürütme problemi denir.

GraphRAG bu sorunu dökümanları bir Bilgi Grafiğine (Knowledge Graph) dönüştürerek çözer:
1. Düğümler (Nodes / Entities): Nesneler, kişiler, teknolojiler veya kavramlar.
   Örn: "Oğuz Kaan", "LangGraph", "Gemini".
2. Kenarlar (Edges / Relationships): Düğümleri birbirine bağlayan eylemler veya ilişkiler.
   Örn: "Oğuz Kaan" --[geliştirdi]--> "AI Career Assistant"
        "AI Career Assistant" --[kullanır]--> "LangGraph"

Kullanıcı "Oğuz Kaan hangi teknolojileri kullanan projeler yaptı?" diye sorduğunda, 
grafikte "Oğuz Kaan" düğümünden yola çıkıp tüm bağlı komşu düğümleri (1. ve 2. derece ilişkileri) 
gezerek (Graph Traversal) tüm zinciri çözeriz.

---
ÖDEV GÖREVLERİNİZ:
- Görev 1: ilişkileri_ve_varliklari_cikar() -> LLM kullanarak metinden (entity_1, relationship, entity_2) üçlülerini çıkartın.
- Görev 2: grafik_uzerinde_ara() -> Python sözlüğü (dict) olarak kurulan grafik ağında dolaylı (2. derece) ilişkileri arayıp bulun.
"""

import os
import json
from dotenv import load_dotenv
load_dotenv()

# API Key Kontrolü
if "GEMINI_API_KEY" in os.environ and "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Rerank yapmak için kullanacağımız LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.0)

# 📋 BOILERPLATE: Test Bilgi Havuzumuz (ChromaDB yerine grafik oluşturmak için kullanacağız)
ornek_cumleler = [
    "Oguz Kaan, AI Career Assistant adinda bir otonom proje gelistirmistir.",
    "AI Career Assistant projesi, verileri analiz etmek icin LangGraph ajan mimarisini kullanir.",
    "LangGraph ajan mimarisi, yapay zeka beyni olarak Gemini modeline bağlanir."
]


# =====================================================================
# 🔥 GÖREV 1: METİNDEN İLİŞKİ VE VARLIK ÇIKARMA (LLM Entity Extraction)
# =====================================================================
def ilişkileri_ve_varliklari_cikar(metin: str) -> list[dict]:
    """
    Görev: Gelen metni inceleyin ve içindeki özneleri (entity_1), aralarındaki eylemi (relationship) 
    ve nesneyi (entity_2) tespit ederek JSON formatında çıkartın.
    
    Beklenen Çıktı Formatı (JSON):
    [
      {"entity_1": "Oguz Kaan", "relationship": "gelistirdi", "entity_2": "AI Career Assistant"}
    ]
    
    İpuçları:
    - Bir ChatPromptTemplate oluşturun. LLM'e sadece saf bir JSON listesi dönmesini, 
      kod blokları (```json) veya ekstra metinler yazmamasını söyleyin.
    - JSON çıktısının parse edilebilmesi için json.loads() kullanın. Hata durumunda boş liste dönün.
    """
    # TODO: Kodunuzu buraya yazın
    return []


# =====================================================================
# 🔥 GÖREV 2: GRAFİK ÜZERİNDE MULTI-HOP ARAMA (Graph Traversal)
# =====================================================================
def grafik_uzerinde_ara(baslangic_dugumu: str, grafik: list[dict]) -> list[str]:
    """
    Görev: Verilen başlangıç düğümünden (Örn: "Oguz Kaan") yola çıkarak grafiği tarayın.
    Sadece 1. derece ilişkileri değil, onlara bağlı olan 2. derece ilişkileri de (Multi-Hop) yakalayın.
    Bulduğunuz tüm ilişkileri açıklayıcı cümleler olarak liste halinde geriye döndürün.
    
    Girdi `grafik` formatı:
    [
      {"entity_1": "Oguz Kaan", "relationship": "gelistirdi", "entity_2": "AI Career Assistant"},
      {"entity_1": "AI Career Assistant", "relationship": "kullanir", "entity_2": "LangGraph"}
    ]
    
    İpuçları:
    - 1. Derece İlişkiler: entity_1 değeri `baslangic_dugumu` ile eşleşen ilişkilerdir.
      Örn: "Oguz Kaan gelistirdi AI Career Assistant" -> Buradaki entity_2 (AI Career Assistant) artık yeni bir arama hedefidir.
    - 2. Derece İlişkiler: Bulduğunuz entity_2 değerlerinin de entity_1 olarak kullanıldığı yeni ilişkilerdir.
      Örn: "AI Career Assistant kullanir LangGraph"
    - Benzersiz ilişkileri listelemek için bir döngü kurun.
    """
    bulunan_ilişkiler = []
    ziyaret_edilen_dugumler = set([baslangic_dugumu.lower().strip()])
    ziyaret_edilecek_dugumler = [baslangic_dugumu.lower().strip()]
    
    # TODO: Grafik üzerinde gezinme (Graph Traversal) mantığını kodlayın.
    # 1. derece ve 2. derece bağlantıları bularak açıklayıcı metinler (Örn: 'X -> Y -> Z') üretin.
    
    return bulunan_ilişkiler


# =====================================================================
# 🧪 TEST VE DOĞRULAMA ALANI
# =====================================================================
# Çalıştırmak için: $env:PYTHONIOENCODING="utf-8"; py 06_ileri_duzey_rag_sistemleri/03_graph_rag_temelleri.py
# =====================================================================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🕸️ TEST: MINI GRAPHRAG BİLGİ GRAFİĞİ OLUŞTURMA")
    print("="*60)
    
    bilgi_grafigi = []
    
    # Adım 1: Cümlelerden varlıkları çıkarıp ortak grafiği kuruyoruz
    for cumle in ornek_cumleler:
        print(f"Cümleden varlıklar çıkarılıyor: '{cumle}'")
        iliskiler = ilişkileri_ve_varliklari_cikar(cumle)
        bilgi_grafigi.extend(iliskiler)
        
    print("\nOluşturulan Bilgi Grafiği (Knowledge Graph):")
    print(json.dumps(bilgi_grafigi, indent=2, ensure_ascii=False))
    
    print("\n" + "="*60)
    print("🧪 TEST: MULTI-HOP SORGULAMA (Arama: Oguz Kaan)")
    print("="*60)
    
    hedef = "Oguz Kaan"
    sonuclar = grafik_uzerinde_ara(hedef, bilgi_grafigi)
    
    print(f"'{hedef}' için bulunan 1. ve 2. Derece Akış Zinciri:")
    for s in sonuclar:
        print(f"  🔗 {s}")
        
    print("\n" + "="*60)
