# faz5_langgraph/proje_kurumsal_multi_agent/db_config.py
"""
KURUMSAL ÇOKLU AJAN SİSTEMİ - DATABASE BAĞLANTISI VE ARAÇLARI
-------------------------------------------------------------
Neon PostgreSQL veritabanına bağlanır ve SQL Ajanı için sorgulama aracı sunar.
"""

import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_core.tools import tool

load_dotenv()

# Veritabanı Bağlantı URI'si
DATABASE_URL = os.getenv("DATABASE_URL")

# LangChain SQLDatabase nesnesi ilklendirilir
db = SQLDatabase.from_uri(DATABASE_URL)

@tool
def sorgula_veritabanini(sql_sorgusu: str) -> str:
    """
    Verilen SQL sorgusunu veritabanında çalıştırır ve sonuçları döner.
    """
    # Referans: faz4_langchain/proje_langchain_sifirdan/sql_agent.py dosyasındaki db.run() kullanımını incele.
    try:
        # SQL sorgusunu çalıştırıp çıktıyı döndür
        # return db.run(sql_sorgusu)
        return "Sorgu çıktısı buraya gelecek (Kodu sen yazacaksın)"
    except Exception as e:
        return f"Sorgu çalıştırılırken hata oluştu: {e}"
