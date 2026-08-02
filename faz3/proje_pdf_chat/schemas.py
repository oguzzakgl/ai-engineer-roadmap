# faz3/proje_pdf_chat/schemas.py
from pydantic import BaseModel, Field

# =====================================================================
# 🎯 TODO 3: PDF DOSYASI YANIT ŞEMASI
# =====================================================================
# Dosya başarıyla yüklendiğinde kullanıcıya döneceğimiz veri formatı.
# Sınıf adı: PDFDosyaResponse
# Alanlar:
# - id: int (Veritabanındaki ID'si)
# - dosya_adi: str (Dosyanın adı)
# (from_attributes = True eklemeyi unutma, çünkü DB modelinden veri okuyacak)
# =====================================================================
class PDFDosyaResponse(BaseModel):
    id: int = Field(ge=0, description="PDF ID'si")
    dosya_adi: str = Field(min_length=1, max_length=255, description="PDF dosyasının adı")
   
    class Config:
        from_attributes = True

# =====================================================================
# 🎯 TODO 4: SOHBET SORU İSTEK ŞEMASI
# =====================================================================
# Kullanıcının PDF hakkında soru sorarken göndereceği veri formatı.
# Sınıf adı: ChatSoruRequest
# Alanlar:
# - soru: str (Kullanıcının yazdığı soru metni. min_length=3 olsun)
# =====================================================================
class ChatSoruRequest(BaseModel):
    soru: str = Field(min_length=3, description="PDF dosyasına sorulacak soru")


# =====================================================================
# 🎯 TODO 5: SOHBET CEVAP YANIT ŞEMASI
# =====================================================================
# Yapay zekanın kullanıcıya vereceği cevap ve kaynak bilgileri.
# Sınıf adı: ChatCevapResponse
# Alanlar:
# - cevap: str (Yapay zekanın ürettiği teknik yanıt)
# - kaynaklar: list[str] (Cevabın oluşturulmasında kullanılan kaynak paragraflar)
# =====================================================================
class ChatCevapResponse(BaseModel):
    cevap: str = Field(min_length=1, description="Yapay zekanın ürettiği yanıt")
    kaynaklar: list[str] = Field(description="Cevabın oluşturulmasında kullanılan kaynak paragraflar")
