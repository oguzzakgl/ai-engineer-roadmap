# 05_langgraph_ajanlari/01_langchain_temelleri.py
"""
FAZ 5 - LANGCHAIN BİLGİ TAZELEME VE PRATİK ÇALIŞMASI
---------------------------------------------------
Amaç: LCEL (LangChain Expression Language), prompt şablonu, 
Gemini model entegrasyonu ve Pydantic yapılandırılmış çıktı almayı sıfırdan yazarak pekiştirmek.
"""

import os
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# LangChain Bileşenleri
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

# API Anahtarı Ayarı
if "GEMINI_API_KEY" in os.environ and "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]


# =====================================================================
# 📋 ADIM 1: PYDANTIC ÇIKTI ŞEMASI TANIMLAMA
# =====================================================================
# Görev: LLM'den kesinlikle JSON formatında alacağımız yapıyı tanımlayan
# Pydantic modelini kur. Model adı "TeknolojiAnalizi" olsun.
# Alanlar:
# - teknoloji_adi (str): Teknolojinin adı
# - populerlik_skoru (int): 1-10 arası popülerlik puanı
# - kullanim_alanlari (list[str]): En yaygın kullanıldığı 3 alan
# - gelecek_yorumu (str): Geleceğine dair tek cümlelik yorum

class TeknolojiAnalizi(BaseModel):
    # Kodu sen yazacaksın
    teknoloji_adi: str = Field(description="Teknolojinin adı")
    populerlik_skoru: int = Field(description="1-10 arası popülerlik puanı")
    kullanim_alanlari: list[str] = Field(description="En yaygın kullanıldığı 3 alan")
    gelecek_yorumu: str = Field(description="Geleceğine dair tek cümlelik yorum")
    


# =====================================================================
# 🧠 ADIM 2: TEKNOLOJİ ANALİZ ZİNCİRİ FONKSİYONU
# =====================================================================
# Görev: Kullanıcının girdiği teknolojiyi analiz eden ve Pydantic modeli dönen fonksiyonu yaz.
# Fonksiyon ismi fiille başlasın (örn: analiz_et_teknolojiyi).

def analiz_et_teknolojiyi(teknoloji: str) -> TeknolojiAnalizi:
    """
    1. ChatGoogleGenerativeAI (gemini-2.5-flash) tanımla.
    2. PydanticOutputParser'ı TeknolojiAnalizi sınıfı ile ilklendir.
    3. ChatPromptTemplate oluştur. İçinde sistem ve kullanıcı mesajları olsun.
       Format yönergelerini {format_instructions} olarak prompta ekle.
    4. zincir = prompt | llm | parser yapısını kur.
    5. zincir.invoke() ile çalıştır ve sonucu döndür.
    """
    # Kodu sen yazacaksın
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",)

    parser = PydanticOutputParser(pydantic_object=TeknolojiAnalizi) 
    
    prompt = ChatPromptTemplate.from_template(
        """
        Sen bir teknoloji analiz uzmanısın.
        
        Kullanıcının sorduğu şu teknoloji hakkında detaylı bir analiz yap: {teknoloji}
        
        Uyman gereken JSON format yönergeleri aşağıdadır:
        {format_instructions}
        """
    )
    
    zincir = prompt | llm | parser
    sonuc = zincir.invoke({
        "teknoloji": teknoloji, # Burada doğru anahtarla gönderiyoruz
        "format_instructions": parser.get_format_instructions()
    })
    return sonuc    

if __name__ == "__main__":
    # Test Etme Alanı
    print("🤖 LangChain Tekrar Çalışması Başlatılıyor...\n")
    sonuc = analiz_et_teknolojiyi("python")
    print(sonuc)
