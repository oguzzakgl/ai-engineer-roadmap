# faz2/proje/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import database
import models
import schemas
import crud

# Veritabanında tabloları otomatik oluşturuyoruz
models.Base.metadata.create_all(bind=database.engine)

# FastAPI uygulamamızı başlatıyoruz
app = FastAPI(title="Yapay Zeka Prompt Kütüphanesi API")

@app.post("/categories",response_model=schemas.KategoriResponse, status_code=201)
def kategori_ekle(kategori: schemas.KategoriCreate, db: Session = Depends(database.get_db)):
    mevcut_kategoriler = crud.get_kategoriler(db)
    for k in mevcut_kategoriler:
        if k.ad.lower() == kategori.ad.lower():
            raise HTTPException(status_code=400, detail="Bu kategori zaten mevcut!")

    return crud.create_kategori(db=db, kategori=kategori)

@app.get("/categories", response_model=list[schemas.KategoriResponse])
def list_kategoriler(db: Session = Depends(database.get_db)):
    return crud.get_kategoriler(db)

    
@app.post("/promptlar", response_model=schemas.PromptResponse, status_code=201)
def prompt_ekle(prompt: schemas.PromptCreate, db: Session = Depends(database.get_db)):
    kategori_var = db.query(models.KategoriTablosu).filter(models.KategoriTablosu.id == prompt.kategori_id).first()
    
    if not kategori_var:
        raise HTTPException(status_code=400, detail="Kategori bulunamadı!")
    else:
        return crud.create_prompt(db=db, prompt=prompt)


@app.get("/promptlar", response_model=list[schemas.PromptResponse])
def promptlari_listele(
    kategori_id: int = None, 
    search: str = None, 
    db: Session = Depends(database.get_db)
):
    return crud.get_promptlar(db, kategori_id, search)

@app.patch("/promptlar/{id}/like", response_model=schemas.PromptResponse)
def prompt_begen(id: int, db: Session = Depends(database.get_db)):
    db_prompt = crud.like_prompt(db=db, prompt_id=id)
    if not db_prompt:
        raise HTTPException(status_code=404, detail="Prompt bulunamadı!")
    return db_prompt

@app.delete("/promptlar/{id}")
def prompt_sil(id: int, db: Session = Depends(database.get_db)):
    silindi = crud.delete_prompt(db=db, prompt_id=id)
    if not silindi:
        raise HTTPException(status_code=404, detail="Prompt bulunamadı!")
    return {"mesaj": "Prompt başarıyla silindi"}