# =====================================================================
# 📂 GENEL TEKRAR - main_tekrar.py
# =====================================================================
# Bu dosya uygulamanın ana sunucu dosyasıdır.
# RAG ve SQL yönlendirmesini burada yapacağız.

import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from google import genai
from pydantic import BaseModel, Field

# Diğer dosyalarımızı içe aktaralım
import database_tekrar as database
import schemas_tekrar as schemas
import crud_tekrar as crud

# 1. Gemini istemcisini (Client) tanımlayın.
API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)

# 2. FastAPI uygulamasını başlatın
app = FastAPI()

# 3. Niyet Analizi için Pydantic Structured Output Şeması
# Yapay zekanın dönmesini istediğimiz JSON yapısı
class NiyetAnalizi(BaseModel):
    niyet: str = Field(
        description="Soru döküman araması mı yoksa veritabanı analizi mi? Değerler: 'BELGE_ARAMA' veya 'VERITABANI_ANALIZ'")


# 4. Sohbet Asistanı Endpoint'i (POST /chat)
# Parametre olarak schemas.ChatIstekRequest almalı, db bağlantısını çekmeli.
# Geriye schemas.ChatCevapResponse dönmeli.
# =====================================================================
# ADIM ADIM İÇ YAPISI (Tamamlamanız gereken kısım):
#
# Adım 4a: Niyet Analizi Yapma (Intent Routing)
# Gemini'ye structured output ile kullanıcının sorusunu gönderin.
# Hangi niyet olduğuna karar versin (BELGE_ARAMA veya VERITABANI_ANALIZ).
#
# Adım 4b: Niyet VERITABANI_ANALIZ ise:
#   - Gemini'ye tablolarımızın şemasını ve kolonlarını anlatan promptu verip SQL ürettirin.
#   - crud.dinamik_sql_calistir(db, sql_sorgusu) ile SQL'i çalıştırın.
#   - Dönen tablo verilerini tekrar Gemini'ye yorumlatıp cevap üretin.
#   - schemas.ChatCevapResponse olarak yanıtı dönün.
#
# Adım 4c: Niyet BELGE_ARAMA ise:
#   - (Şimdilik mock edebilir veya doğrudan döküman araması yanıtı dönebilirsiniz).
# =====================================================================

# ENDPOINT KODUNU BURAYA YAZIN:

@app.post("/chat")
def sohbet_endpoint():
    niyet 

# 5. Statik Frontend Dosyalarını Mount Etme (app.mount)
# 'frontend' klasörünü StaticFiles ile '/' dizinine bağlayın.
# =====================================================================
# KODUNUZU BURAYA YAZIN:
