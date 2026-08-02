# faz3/proje_pdf_chat/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. BULUT VERİTABANI ADRESİMİZ (Neon PostgreSQL)
# Bu URL, buluttaki veritabanımıza güvenli şekilde bağlanmamızı sağlayan adrestir.
DATABASE_URL = "postgresql+psycopg2://neondb_owner:npg_tIU6WbK5ysYA@ep-noisy-shadow-ayl4dhke-pooler.c-5.us-east-2.aws.neon.tech/neondb?sslmode=require"

# 2. BAĞLANTI MOTORU (Engine)
# Python ile PostgreSQL veritabanı arasında veri taşıyacak olan ana otobanı (bağlantıyı) kurar.
engine = create_engine(DATABASE_URL)

# 3. OTURUM FABRİKASI (Sessionmaker)
# Veritabanında okuma/yazma işlemleri yapacak olan "geçici oturumları (işçileri)" üreten fabrikadır.
# autocommit=False: Biz onay vermeden (commit) verileri veritabanına kaydetmez.
# autoflush=False: Gereksiz yere veritabanına sorgu gönderip yormaz.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. TABLOLARIN ORTAK ATASI (Base Class)
# models.py'de yazacağımız tüm tablolar bu sınıftan türeyecek. Bu sayede SQLAlchemy
# hangi sınıfların veritabanında birer tabloya dönüşeceğini otomatik anlar.
Base = declarative_base()

# 5. FASTAPI İÇİN VERİTABANI OTURUM YÖNETİCİSİ (Dependency)
# Bu fonksiyon FastAPI endpoint'lerinde (API kapılarında) kullanılır.
# Her istek geldiğinde veritabanı oturumu açar (yield db), işlem bitince
# bağlantıyı güvenli bir şekilde kapatır (db.close()). Böylece bağlantı sızıntısı olmaz.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
