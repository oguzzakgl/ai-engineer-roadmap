# faz3/proje_pdf_chat/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Bulut Neon PostgreSQL bağlantı adresimiz
DATABASE_URL = "postgresql+psycopg2://neondb_owner:npg_tIU6WbK5ysYA@ep-noisy-shadow-ayl4dhke-pooler.c-5.us-east-2.aws.neon.tech/neondb?sslmode=require"

# Bağlantı motorunu kuruyoruz
engine = create_engine(DATABASE_URL)

# Oturum fabrikası
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tablo modellerimiz için Base sınıfı
Base = declarative_base()

# FastAPI endpoint'lerinde veritabanı oturumu açıp kapatacak yardımcı fonksiyon (Dependency)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
