# 06_ileri_duzey_rag_sistemleri/04_neo4j_baglantisi.py
"""
🕸️ FAZ 5: İLERİ DÜZEY RAG - NEO4J & PYTHON BAĞLANTISI
------------------------------------------------------------------------------
BU ADIMDA NE YAPIYORUZ?
Daha önce Python listeleri ile simüle ettiğimiz Grafik veri yapısını, 
şimdi buluttaki gerçek bir Neo4j veritabanına bağlayarak fiziksel olarak inşa ediyoruz!

ADIMLAR:
1. https://neo4j.com/cloud/platform/auradb/ adresine gidin.
2. Ücretsiz bir hesap açın ve "AuraDB Free" veritabanı oluşturun (Instance tipi: Blank Database).
3. Veritabanı açıldığında size verilen:
   - Connection URI (Şununla başlar: neo4j+s://...)
   - Username (Genellikle: neo4j)
   - Password (Size verilen özel şifre)
   bilgilerini bilgisayarınızdaki .env dosyasına ekleyin:
     NEO4J_URI=neo4j+s://your-instance-id.databases.neo4j.io
     NEO4J_USERNAME=neo4j
     NEO4J_PASSWORD=your-generated-password

---
ÖDEV GÖREVİNİZ:
- TODO alanlarını doldurarak; Python üzerinden Neo4j veritabanına bağlanın, 
  "Oguz Kaan" ve "FastAPI" düğümlerini (Nodes) ve aralarındaki "KULLANIR" ilişkisini (Relationship)
  Cypher sorgusuyla oluşturup veritabanına kaydedin.
"""

import os
from dotenv import load_dotenv
load_dotenv()

# neo4j kütüphanesini import ediyoruz
# Not: Eğer hata alırsanız terminalde şu komutla kurun: pip install neo4j
from neo4j import GraphDatabase

# Bağlantı bilgilerini .env'den okuyoruz
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

def veritabanina_baglan():
    """
    Neo4j veritabanına bağlantı sürücüsünü (driver) oluşturur ve döner.
    """
    if not NEO4J_URI or not NEO4J_PASSWORD:
        raise ValueError("Lütfen .env dosyasında NEO4J_URI ve NEO4J_PASSWORD alanlarını tanımlayın!")
        
    # TODO: GraphDatabase.driver() kullanarak veritabanı sürücüsünü oluşturun ve döndürün.
    # driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
    # return driver
    pass

def iliskiyi_kaydet(driver, e1: str, iliski: str, e2: str):
    """
    Parametre olarak gelen e1, iliski ve e2 değerlerini kullanarak 
    Neo4j veritabanına MERGE sorgusu gönderir ve kaydeder.
    
    Örnek sorgu yapısı:
    MERGE (a:Varlik {name: 'Oguz Kaan'})
    MERGE (b:Varlik {name: 'FastAPI'})
    MERGE (a)-[r:KULLANIR]->(b)
    """
    # Cypher sorgumuzu hazırlıyoruz
    # NOT: İlişki (Relationship) tipleri dinamik olarak değişkenden geçilirken 
    # Cypher syntax kuralları gereği {relationship} parametresi doğrudan string yerine 
    # sorgu metnine yerleştirilmelidir: -[r:{iliski}]->
    sorgu = f"""
    MERGE (a:Varlik {{name: $e1}})
    MERGE (b:Varlik {{name: $e2}})
    MERGE (a)-[r:{iliski}]->(b)
    """
    
    # TODO: driver.session() kullanarak bir veritabanı oturumu açın 
    # ve session.run(sorgu, e1=e1, e2=e2) komutuyla sorguyu çalıştırın.
    pass

# =====================================================================
# 🧪 TEST ALANI
# =====================================================================
if __name__ == "__main__":
    try:
        driver = veritabanina_baglan()
        print("⚡ Neo4j Veritabanına başarıyla bağlanıldı!")
        
        # Test ilişkisi kaydediyoruz
        iliskiyi_kaydet(driver, "Oguz Kaan", "KULLANIR", "FastAPI")
        print("✅ İlişki veritabanına başarıyla yazıldı!")
        
        driver.close()
    except Exception as e:
        print(f"❌ Hata Oluştu: {e}")
