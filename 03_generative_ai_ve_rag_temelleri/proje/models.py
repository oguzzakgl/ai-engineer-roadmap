# faz2/proje/models.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base  # database.py'de tanımladığımız Base'i import ediyoruz

class KategoriTablosu(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    ad = Column(String, unique=True, nullable=False, index=True)

    # İlişki: Bir kategorinin birden fazla prompt'u olabilir.
    # cascade="all, delete-orphan" -> Kategori silinirse, ona bağlı promptlar da otomatik silinir.
    promptlar = relationship("PromptTablosu", back_populates="kategori", cascade="all, delete-orphan")


class PromptTablosu(Base):
    __tablename__ = "promptlar"

    id = Column(Integer, primary_key=True, index=True)
    baslik = Column(String, nullable=False)
    prompt_metni = Column(Text, nullable=False)
    begeni_sayisi = Column(Integer, default=0)
    
    # Yabancı Anahtar (Foreign Key): Hangi kategoriye ait olduğunu belirtir.
    kategori_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)

    # İlişki: Her prompt sadece tek bir kategoriye aittir.
    kategori = relationship("KategoriTablosu", back_populates="promptlar")
