# =====================================================================
# 📂 GENEL TEKRAR - schemas_tekrar.py
# =====================================================================
# Bu dosyada Pydantic şemalarını tanımlayacağız.
# Kılavuz olarak pratik/syntax_rehberi.py 2. bölümü kullanabilirsiniz.

from pydantic import BaseModel, Field

# 1. Chat İstek Şeması (ChatIstekRequest)
# Kullanıcının gönderdiği soruyu doğrular.
# Sütunlar:
#   - soru: str (Kullanıcının yazdığı mesaj)
# =====================================================================
# KODUNUZU BURAYA YAZIN:

class ChatIstekRequest(BaseModel):
    soru:str=Field(description="Kullanıcının yazdığı mesaj")


# 2. Chat Yanıt Şeması (ChatCevapResponse)
# Sunucunun (FastAPI) döneceği veriyi şekillendirir.
# Sütunlar:
#   - niyet: str ("BELGE_ARAMA" veya "VERITABANI_ANALIZ")
#   - cevap: str (Gemini'nin yazdığı analiz özeti veya RAG cevabı)
#   - sql_sorgusu: str | None = None (Eğer SQL çalıştıysa sorgu metni, opsiyonel)
#   - tablo_verisi: list[dict] | None = None (Eğer SQL çalıştıysa dönen satırlar, opsiyonel)
#   - kaynaklar: list[str] | None = None (Eğer RAG çalıştıysa kullanılan PDF paragraf kaynakları, opsiyonel)
# =====================================================================
# KODUNUZU BURAYA YAZIN:

class ChatYanıtResponse(BaseModel):
    niyet: str = Field(description="Değerler: BELGE_ARAMA veya VERITABANI_ANALIZ") 
    cevap: str=Field(description="Yapay zekanın ürettiği analiz veya cevap metni")
    sql_sorgusu: str | None= None
    tablo_verisi: list[dict] | None= None
    kaynaklar: list[str] | None= None