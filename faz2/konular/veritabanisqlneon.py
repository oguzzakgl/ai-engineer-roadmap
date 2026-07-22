from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Bağlantı Adresimiz (Yeni pythonDev Projesi)
DATABASE_URL = "postgresql+psycopg2://neondb_owner:npg_tIU6WbK5ysYA@ep-noisy-shadow-ayl4dhke-pooler.c-5.us-east-2.aws.neon.tech/neondb?sslmode=require"

# 2. Veritabanı Motorunu (Engine) Oluşturuyoruz
engine = create_engine(DATABASE_URL)

# 3. Tablo şablonları için ana sınıf (Base)
Base = declarative_base()

# 4. Görev Tablomuzu Sınıf Olarak Tanımlıyoruz
class GorevTablosu(Base):
    __tablename__ = "gorevler"  # Veritabanındaki tablo adı

    id = Column(Integer, primary_key=True, autoincrement=True)
    baslik = Column(String, nullable=False)
    tamamlandi = Column(Boolean, default=False)

# 5. Tabloları veritabanında otomatik oluştur (Yoksa oluşturur)
Base.metadata.create_all(engine)

# 6. Sorgu gönderebilmek için Session (Oturum) Sınıfı
SessionLocal = sessionmaker(bind=engine)


# 🚀 EKLEYECEĞİNİZ YENİ KISIM BURADAN BAŞLIYOR:

# A. Tezgahtarı çağırıyoruz (Oturum açtık)
session = SessionLocal()

# B. Yeni bir görev nesnesi oluşturuyoruz (Create)
yeni_gorev = GorevTablosu(baslik="Bulut Veritabanı Öğren", tamamlandi=False)

# C. Sepete ekle ve kaydet
session.add(yeni_gorev)
session.commit()
print("Yeni gorev buluta basariyla eklendi!")

# D. Buluttaki tüm görevleri çekip listeliyoruz (Read)
tum_gorevler = session.query(GorevTablosu).all()

print("\n--- BULUTTAKİ GÖREVLER ---")
for g in tum_gorevler:
    durum = "Tamamlandi" if g.tamamlandi else "Bekliyor"
    print(f"[{g.id}] {g.baslik} - {durum}")

# E. Oturumu kapatıyoruz
session.close()
