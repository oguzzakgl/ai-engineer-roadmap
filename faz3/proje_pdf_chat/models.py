# faz3/proje_pdf_chat/models.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base  # database.py'deki Base sınıfını içe aktarıyoruz

# =====================================================================
# 📂 1. TABLO: PDF DOSYA BİLGİLERİ (pdf_dosyalari)
# =====================================================================
# Bu tablo, sisteme yüklenen her bir PDF dosyasının üst bilgilerini saklar.
# İçinde PDF'in ham metin parçaları olmaz, sadece dosyanın kimlik kartıdır.
class PDFDosyaTablosu(Base):
    __tablename__ = "pdf_dosyalari"

    # id: Her dosyaya veritabanı tarafından otomatik atanan benzersiz numara (1, 2, 3...)
    id = Column(Integer, primary_key=True, index=True)
    
    # dosya_adi: Yüklenen PDF dosyasının bilgisayardaki adı (örn: "kullanim_kilavuzu.pdf")
    dosya_adi = Column(String, nullable=False)

    # paragraflar: Bu dosya ile paragraflar tablosu arasındaki "ilişki" (relationship) köprüsüdür.
    # cascade="all, delete-orphan": Eğer bu dosya silinirse, ona ait tüm paragraf kayıtları da otomatik silinir.
    paragraflar = relationship("PDFParagrafTablosu", back_populates="pdf", cascade="all, delete-orphan")


# =====================================================================
# 📂 2. TABLO: PDF METİN PARÇALARI VE VEKTÖRLERİ (pdf_paragraflar)
# =====================================================================
# Bu tablo, PDF'ten kırptığımız 800 karakterlik küçük metinleri ve bu metinlerin
# yapay zeka tarafından üretilen anlamsal koordinatlarını (vektörlerini) saklar.
class PDFParagrafTablosu(Base):
    __tablename__ = "pdf_paragraflar"

    # id: Her bir metin paragrafına atanan benzersiz kayıt numarası
    id = Column(Integer, primary_key=True, index=True)
    
    # pdf_id: Bu paragrafın hangi PDF dosyasına ait olduğunu gösteren yabancı anahtar (Foreign Key).
    # ondelete="CASCADE": Bağlı olduğu dosya silindiğinde bu satırın da silinmesini veritabanı seviyesinde garanti eder.
    pdf_id = Column(Integer, ForeignKey("pdf_dosyalari.id", ondelete="CASCADE"), nullable=False)
    
    # metin_icerigi: PDF'ten koparılan ham metin paragrafı (Örn: "Şirket çalışma saatleri sabah 9'da başlar.")
    metin_icerigi = Column(Text, nullable=False)
    
    # embedding: Bu paragrafın Gemini ile üretilen 3072 boyutlu vektör koordinatlarının metin (string) hali.
    # Örn: "[0.012, -0.045, ... 3072 tane sayı]"
    embedding = Column(Text, nullable=True)

    # pdf: Bu paragrafın ait olduğu PDFDosyaTablosu kaydına ters köprü oluşturur.
    pdf = relationship("PDFDosyaTablosu", back_populates="paragraflar")
