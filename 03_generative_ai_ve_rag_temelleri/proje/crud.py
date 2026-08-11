# faz2/proje/crud.py
from sqlalchemy.orm import Session
import models
import schemas

# --- KATEGORİ CRUD İŞLEMLERİ ---

# 1. Tüm Kategorileri Getir (Read)
def get_kategoriler(db: Session):
    return db.query(models.KategoriTablosu).all()

# 2. Yeni Kategori Ekle (Create)
def create_kategori(db: Session, kategori: schemas.KategoriCreate):
    db_kategori = models.KategoriTablosu(ad=kategori.ad)
    db.add(db_kategori)
    db.commit()
    db.refresh(db_kategori)  # Veritabanının verdiği ID'yi nesneye yükler
    return db_kategori


# --- PROMPT CRUD İŞLEMLERİ ---

# 3. Promptları Listele (Filtreleme ve Arama Destekli)
def get_promptlar(db: Session, kategori_id: int = None, search: str = None):
    sorgu = db.query(models.PromptTablosu)
    
    # Eğer kategori_id gönderildiyse filtrele
    if kategori_id is not None:
        sorgu = sorgu.filter(models.PromptTablosu.kategori_id == kategori_id)
        
    # Eğer arama kelimesi gönderildiyse başlıkta veya prompt metninde ara
    if search:
        sorgu = sorgu.filter(
            (models.PromptTablosu.baslik.ilike(f"%{search}%")) |
            (models.PromptTablosu.prompt_metni.ilike(f"%{search}%"))
        )
        
    return sorgu.all()

# 4. Yeni Prompt Ekle (Create)
def create_prompt(db: Session, prompt: schemas.PromptCreate):
    db_prompt = models.PromptTablosu(
        baslik=prompt.baslik,
        prompt_metni=prompt.prompt_metni,
        kategori_id=prompt.kategori_id
    )
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt

# 5. Prompt Beğen (Update)
def like_prompt(db: Session, prompt_id: int):
    db_prompt = db.query(models.PromptTablosu).filter(models.PromptTablosu.id == prompt_id).first()
    if db_prompt:
        db_prompt.begeni_sayisi += 1
        db.commit()
        db.refresh(db_prompt)
    return db_prompt

# 6. Prompt Sil (Delete)
def delete_prompt(db: Session, prompt_id: int):
    db_prompt = db.query(models.PromptTablosu).filter(models.PromptTablosu.id == prompt_id).first()
    if db_prompt:
        db.delete(db_prompt)
        db.commit()
        return True
    return False
