# 03_generative_ai_ve_rag_temelleri/proje_sql_chat/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# =====================================================================
# 🎯 TODO 1: VERİTABANI BAĞLANTI AYARLARINI YAPIN
# =====================================================================
# Adım 1: DATABASE_URL değişkenini tanımlayın.
# (Referans: faz3/proje_pdf_chat/database.py dosyasındaki DATABASE_URL'i birebir kullanabilirsiniz.)
DATABASE_URL = "postgresql+psycopg2://neondb_owner:npg_tIU6WbK5ysYA@ep-noisy-shadow-ayl4dhke-pooler.c-5.us-east-2.aws.neon.tech/neondb?sslmode=require"

# Adım 2: create_engine() fonksiyonunu kullanarak bağlantı motorunu (engine) oluşturun.
# (Referans: faz3/proje_pdf_chat/database.py içindeki engine tanımı.)
engine = create_engine(DATABASE_URL)

# Adım 3: sessionmaker() ile SessionLocal oturum fabrikasını kurun.
# (Referans: faz3/proje_pdf_chat/database.py içindeki SessionLocal tanımı.)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Adım 4: declarative_base() ile Base sınıfını oluşturun.
# (Referans: faz3/proje_pdf_chat/database.py içindeki Base tanımı.)
Base = declarative_base()

# Adım 5: get_db() dependency (oturum yönetim) fonksiyonunu yazın.
# (Referans: faz3/proje_pdf_chat/database.py içindeki get_db fonksiyonu.)
# =====================================================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
