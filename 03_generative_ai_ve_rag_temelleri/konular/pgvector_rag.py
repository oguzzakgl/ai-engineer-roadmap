# faz3/konular/pgvector_rag.py
import math
from google import genai
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# 1. Gemini elçimizi başlatıyoruz.
client = genai.Client()

# 2. Neon PostgreSQL Bağlantı Adresimiz
DATABASE_URL = "postgresql+psycopg2://neondb_owner:npg_tIU6WbK5ysYA@ep-noisy-shadow-ayl4dhke-pooler.c-5.us-east-2.aws.neon.tech/neondb?sslmode=require"

# 3. Veritabanı bağlantı motorunu oluşturuyoruz.
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# ---------------------------------------------------------------------
# 🛠️ 1. ADIM: VERİTABANI ALTYAPISINI HAZIRLAMA (DDL)
# ---------------------------------------------------------------------

print("[DB] Veritabanı hazırlanıyor...")
# Bulutta 'vector' eklentisini aktif ediyoruz.
session.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))

# Vektörleri saklayacağımız 'rehber' tablosunu oluşturuyoruz.
# koordinat sütunu VECTOR(3072) tipinde olacak (gemini-embedding-2 boyutu).
session.execute(text("""
    CREATE TABLE IF NOT EXISTS rehber (
        id SERIAL PRIMARY KEY,
        icerik TEXT,
        koordinat VECTOR(3072)
    );
"""))
session.commit()
print("[DB] pgvector eklentisi ve 'rehber' tablosu hazır.")


# ---------------------------------------------------------------------
# 🛠️ 2. ADIM: VERİLERİ VEKTÖRLEŞTİRİP DB'YE EKLEME (INSERT)
# ---------------------------------------------------------------------

# Gemini'den embedding alan yardımcı fonksiyonumuz
def vektor_al(metin: str):
    response = client.models.embed_content(
        model='gemini-embedding-2',
        contents=metin
    )
    return response.embeddings[0].values

# Tablo boş mu kontrol ediyoruz. Boşsa verileri dolduracağız.
kayit_sayisi = session.execute(text("SELECT COUNT(*) FROM rehber;")).scalar()

if kayit_sayisi == 0:
    print("\n[DB] Tablo boş, veriler vektörleştirilip ekleniyor...")
    
    bilgi_tabani = [
        "Şirketimizde mesai saatleri hafta içi sabah 09:00 ile akşam 18:00 arasındadır.",
        "Yıllık izin talepleri en az 2 hafta önceden insan kaynakları sisteminden yapılmalıdır.",
        "Ofis mutfağındaki tüm yiyecek ve içecekler çalışanlar için ücretsizdir.",
        "Sunucu şifreleri ve API anahtarları asla Slack veya WhatsApp gibi platformlardan paylaşılamaz."
    ]
    
    for satir in bilgi_tabani:
        # Satırın 3072 adet sayısını alıyoruz.
        vektor = vektor_al(satir)
        
        # pgvector kütüphanesi sayı listesini string formatında (örn: '[0.1, -0.2, ...]') kabul eder.
        # Python'da listeyi str() içine almak tam da bu formatı verir!
        vektor_str = str(vektor)
        
        # Veritabanına kaydetme sorgusu
        session.execute(
            text("INSERT INTO rehber (icerik, koordinat) VALUES (:icerik, :koordinat);"),
            {"icerik": satir, "koordinat": vektor_str}
        )
    session.commit()
    print("[DB] Tüm veriler başarıyla buluta yüklendi!")
else:
    print(f"\n[DB] Tabloda zaten {kayit_sayisi} adet kayıt var. Ekleme adımı atlandı.")


# ---------------------------------------------------------------------
# 🔍 3. ADIM: ANLAMSAL ARAMA (RETRIEVAL)
# ---------------------------------------------------------------------

def en_alakali_dokumani_veritabanindan_bul(kullanici_sorusu: str) -> str:
    print(f"\n[RAG] Soru için vektör alınıyor: '{kullanici_sorusu}'")
    soru_vektoru = vektor_al(kullanici_sorusu)
    soru_vektoru_str = str(soru_vektoru)
    
    print("[RAG] PostgreSQL (pgvector) üzerinde Kosinüs Benzerliği sorgusu çalıştırılıyor...")
    # <=> Kosinüs mesafesini ölçer. En düşük mesafeli (en yakın) olan 1 kaydı çekeriz.
    sorgu = text("""
        SELECT icerik, koordinat <=> :soru_vektoru AS mesafe 
        FROM rehber 
        ORDER BY mesafe ASC 
        LIMIT 1;
    """)
    
    sonuc = session.execute(sorgu, {"soru_vektoru": soru_vektoru_str}).fetchone()
    
    if sonuc:
        alakali_metin, mesafe = sonuc
        # Kosinüs benzerliği skoru = 1 - Kosinüs mesafesi
        benzerlik_skoru = 1.0 - mesafe
        print(f"[RAG] Buluttan gelen en alakalı metin (Benzerlik Skoru: {benzerlik_skoru:.4f}):")
        print(f"--> '{alakali_metin}'")
        return alakali_metin
    return ""


# ---------------------------------------------------------------------
# 🚀 4. ADIM: ZENGİNLEŞTİRİLMİŞ ÜRETİM (RAG GENERATION)
# ---------------------------------------------------------------------

def rag_cevap_uret(soru: str):
    # 1. Veritabanından en alakalı bilgiyi çek
    kaynak_bilgi = en_alakali_dokumani_veritabanindan_bul(soru)
    
    # 2. Prompt'u zenginleştir
    zenginlestirilmis_prompt = f"""
Sana bir soru ve bu soruya cevap bulabilmen için bir kaynak bilgi verilecek.
Lütfen SADECE sana verilen kaynak bilgiyi kullanarak soruyu cevapla.

KAYNAK BİLGİ:
{kaynak_bilgi}

SORU:
{soru}
"""
    
    print("\n[RAG] Zenginleştirilmiş prompt Gemini'ye gönderiliyor...")
    response = client.models.generate_content(
        model='gemini-3.5-flash',
        contents=zenginlestirilmis_prompt
    )
    
    print("\n--- BULUT VERİTABANI DESTEKLİ GEMINI CEVABI ---")
    print(response.text)


# Deneme Sorusu
soru = "Şirkette mesailer saat kaçta başlayıp kaçta bitiyor?"
rag_cevap_uret(soru)

# Oturumu kapatıyoruz
session.close()
