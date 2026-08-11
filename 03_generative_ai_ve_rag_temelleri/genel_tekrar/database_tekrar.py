# =====================================================================
# 📂 GENEL TEKRAR - database_tekrar.py
# =====================================================================
# Bu dosyada Neon PostgreSQL veritabanımıza bağlantı ayarlarını kuracağız.
# Kılavuz olarak pratik/syntax_rehberi.py dosyasını kullanabilirsiniz.

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. DATABASE_URL değişkenini tanımlayın (Neon DB Bağlantı Adresi)
# İPUCU: Neon PostgreSQL adresinizi string olarak buraya yazın.
DATABASE_URL = "postgresql+psycopg2://neondb_owner:npg_tIU6WbK5ysYA@ep-noisy-shadow-ayl4dhke-pooler.c-5.us-east-2.aws.neon.tech/neondb?sslmode=require"

# 2. create_engine kullanarak SQLAlchemy motorunu oluşturun.
# İPUCU: engine = create_engine(DATABASE_URL)
engine = create_engine(DATABASE_URL)  # <-- Burayı tamamlayın!

# 3. sessionmaker kullanarak oturum (SessionLocal) fabrikasını kurun.
# İPUCU: bind=engine parametresini vermeyi unutmayın.
SessionLocal = sessionmaker(bind=engine)  # <-- Burayı tamamlayın!

# 4. Tablolarımızın miras alacağı Base sınıfını declarative_base() ile tanımlayın.
# İPUCU: Base = declarative_base()
Base = declarative_base()  # <-- Burayı tamamlayın!


# 5. FastAPI rotalarında kullanacağımız get_db jeneratör fonksiyonunu yazın.
# İPUCU: 
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
# =====================================================================
# KODUNUZU BURAYA YAZIN:

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
