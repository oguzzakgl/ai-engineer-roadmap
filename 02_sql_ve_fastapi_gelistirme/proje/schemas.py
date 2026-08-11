from pydantic import BaseModel, Field


class KategoriBase(BaseModel):
    ad: str = Field(min_length=2, max_length=50)

class KategoriCreate(KategoriBase):
    pass
class KategoriResponse(KategoriBase):
    id: int

    class Config:
        from_attributes = True


# --- PROMPT ŞEMALARI ---

class PromptBase(BaseModel):
    baslik: str = Field(min_length=3, max_length=100, description="Prompt başlığı")
    prompt_metni: str = Field(min_length=10, description="Prompt içeriği")

class PromptCreate(PromptBase):
    kategori_id: int  # Hangi kategoriye ait olacağını belirtiyoruz.

class PromptResponse(PromptBase):
    id: int
    begeni_sayisi: int
    kategori_id: int

    class Config:
        from_attributes = True
