# 02_sql_ve_fastapi_gelistirme/proje/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Yeni pythonDev veritabanı adresimiz
DATABASE_URL = "postgresql+psycopg2://neondb_owner:npg_tIU6WbK5ysYA@ep-noisy-shadow-ayl4dhke-pooler.c-5.us-east-2.aws.neon.tech/neondb?sslmode=require"

# 2. Bağlantı motorunu kuruyoruz
engine = create_engine(DATABASE_URL)

# 3. Oturum fabrikası
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Tablo modellerimiz için Base sınıfı
Base = declarative_base()

# 5. FastAPI için Dependency (Bağımlılık) Fonksiyonu
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
