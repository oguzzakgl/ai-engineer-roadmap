# faz4_langchain/01_langchain_giris.py
import os
from dotenv import load_dotenv

# 1. LangChain İthalatları (Imports)
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# Gemini API Anahtarı Kontrolü (LangChain GOOGLE_API_KEY veya GEMINI_API_KEY bekler)
if "GEMINI_API_KEY" in os.environ and "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]


# =====================================================================
# 🎯 1. MODELİ TANIMLAMA (ChatGoogleGenerativeAI)
# =====================================================================
# Gemini modelimizi LangChain standartlarında başlatıyoruz.
# temperature=0.2 -> Mantıksal ve tutarlı cevaplar için.
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2
)

# =====================================================================
# 🎯 2. PROMPT ŞABLONUNU TANIMLAMA (ChatPromptTemplate)
# =====================================================================
# Sistem talimatı ve kullanıcı girdisini şablon olarak hazırlıyoruz.
# {konu} ve {uzmanlik} dışarıdan dinamik olarak beslenecek değişkenlerdir.
prompt = ChatPromptTemplate.from_messages([
    ("system", "Sen {uzmanlik} alanında uzmanlaşmış kıdemli bir mühendissin. Cevaplarını Türkçe, öz ve teknik terimlerle ver."),
    ("user", "{konu} hakkında bana bilgi ver.")
])

# =====================================================================
# 🎯 3. ÇIKTI AYRIŞTIRICI (StrOutputParser)
# =====================================================================
# Modelden dönen ham cevaptan sadece metin kısmını kırpan ayrıştırıcı.
parser = StrOutputParser()

# =====================================================================
# 🎯 4. ZİNCİRİ (CHAIN) KURMA (LCEL Yapısı)
# =====================================================================
# Pipe (|) operatörü ile veriyi soldan sağa akıtıyoruz:
# Prompt ➔ LLM ➔ StrOutputParser
zincir = prompt | llm | parser

# =====================================================================
# 🎯 5. ZİNCİRİ ÇALIŞTIRMA (.invoke)
# =====================================================================
if __name__ == "__main__":
    # .invoke() metoduna şablonumuzdaki değişkenleri sözlük (dict) olarak veriyoruz
    sonuc = zincir.invoke({
        "uzmanlik": "Yapay Zeka Mimarisi",
        "konu": "RAG (Retrieval-Augmented Generation) nedir ve neden kullanılır?"
    })
    
    print("--- LANGCHAIN ZİNCİR ÇIKTISI ---")
    print(sonuc)
