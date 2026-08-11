# faz4_langchain/proje_langchain_assistant/intent_router_langchain.py
"""
LANGCHAIN ILE NIYET ANALİZİ (INTENT ROUTING)
-----------------------------------------------------------------------
🔄 FAZ 3 KARŞILIĞI: 
Bu dosya, Faz 3'teki `faz3/proje_sql_chat/main.py` içindeki:
- Prompt içine 'BANA SADECE JSON DÖN' yazıp,
- Gemini'den gelen cevaptan ```json kelimelerini string temizleme (replace/strip) ile silip,
- Manuel json.loads() ile Python sözlüğüne çevirmeye çalıştığımız 40 satırlık kodun YERİNE GEÇER.
-----------------------------------------------------------------------
"""

import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

# Gemini API anahtarı kontrolü
if "GEMINI_API_KEY" in os.environ and "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]


# -----------------------------------------------------------------
# 🔄 FAZ 3 KARŞILIĞI: faz3/schemas.py -> Pydantic Şemaları
# -----------------------------------------------------------------
class NiyetKarari(BaseModel):
    niyet: str = Field(description="Karar türü: 'BELGE_ARAMA' veya 'VERITABANI_ANALIZ'")
    gerekce: str = Field(description="Bu kararın alınma nedeni")


def niyet_analizi_yap_langchain(soru: str) -> NiyetKarari:
    """
    Kullanıcının sorusunu alır ve LangChain LCEL zinciri ile niyet analizi yapıp Pydantic nesnesi döner.
    """
    # -----------------------------------------------------------------
    # 🔄 FAZ 3 KARŞILIĞI: main.py içindeki genai.Client().models.generate_content()
    # -----------------------------------------------------------------
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.0)
    
    # -----------------------------------------------------------------
    # 🔄 FAZ 3 KARŞILIĞI: main.py içindeki manuel json.loads() ve string temizlikleri
    # PydanticOutputParser yapay zekaya format talimatı üretir ve çıktıyı doğrulayıp Pydantic nesnesi yapar.
    # -----------------------------------------------------------------
    parser = PydanticOutputParser(pydantic_object=NiyetKarari)
    
    system_prompt = """
    Sen kurumsal bir AI yönlendirici asistanısın. Kullanıcı sorularını sınıflandırmakla görevlisin.
    
    Sınıflandırma Kuralları:
    1. 'VERITABANI_ANALIZ': Eğer soru şirket sayısal verileri, izin günleri, maaşlar, çalışan bilgileri veya istatistikler ile ilgiliyse bu niyeti seç.
    2. 'BELGE_ARAMA': Eğer soru şirket mevzuatları, izin politikası kuralları, dökümanlar veya nasıl yapılır rehberleri ile ilgiliyse bu niyeti seç.
    
    Uyman Gereken Çıktı Formatı:
    {format_instructions}
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "Kullanıcı Sorusu: {soru}")
    ])
    
    # -----------------------------------------------------------------
    # 🔄 FAZ 3 KARŞILIĞI: Manuel akış yerine Pipe (|) operatörü ile tek zincir (LCEL)
    # -----------------------------------------------------------------
    router_chain = prompt | llm | parser
    
    karar: NiyetKarari = router_chain.invoke({
        "soru": soru,
        "format_instructions": parser.get_format_instructions()
    })
    
    return karar


if __name__ == "__main__":
    test_sorusu = "Şirket yıllık izin politikasına göre kaç gün mazeret iznim var?"
    print(f"❓ Test Sorusu: {test_sorusu}")
    sonuc = niyet_analizi_yap_langchain(test_sorusu)
    print(f"🎯 Karar Niyeti: {sonuc.niyet}")
    print(f"💡 Gerekçe: {sonuc.gerekce}")
