# faz3/proje_pdf_chat/schemas.py
from pydantic import BaseModel, Field

# =====================================================================
# 📂 1. ŞEMA: PDF DOSYASI YANIT FORMATI (PDFDosyaResponse)
# =====================================================================
# Bir PDF dosyası sisteme yüklendiğinde ya da listelendiğinde kullanıcıya
# döneceğimiz verilerin sınırlarını çizer. (Güvenlik için gereksiz alanları gizler).
class PDFDosyaResponse(BaseModel):
    # ge=0: ID değerinin 0 veya daha büyük bir tam sayı olması gerektiğini garanti eder.
    id: int = Field(ge=0, description="PDF dosyasının veritabanındaki benzersiz kimlik numarası")
    
    # min_length=1: Dosya adının boş olamayacağını doğrular.
    dosya_adi: str = Field(min_length=1, max_length=255, description="Yüklenen PDF dosyasının adı")
   
    class Config:
        # from_attributes = True (Eski adıyla orm_mode):
        # FastAPI'nin veritabanından dönen ham SQL nesnesini (PDFDosyaTablosu)
        # otomatik olarak bu Pydantic formatına dönüştürmesini sağlar.
        from_attributes = True


# =====================================================================
# 📂 2. ŞEMA: SOHBET SORU İSTEK FORMATI (ChatSoruRequest)
# =====================================================================
# Kullanıcı PDF hakkında soru sorarken göndereceği JSON verisini denetler.
# Örn: {"soru": "Şirket mesaileri kaçta başlıyor?"}
class ChatSoruRequest(BaseModel):
    # min_length=3: Kullanıcının en az 3 karakterli mantıklı bir soru sormasını zorunlu kılar.
    soru: str = Field(min_length=3, description="PDF içeriğine sorulacak soru metni")


# =====================================================================
# 📂 3. ŞEMA: SOHBET CEVAP YANIT FORMATI (ChatCevapResponse)
# =====================================================================
# Yapay zekanın ürettiği cevabı ve bu cevabı verirken veritabanından bulduğu
# kanıt/kaynak paragrafları paket halinde kullanıcıya dönmemizi sağlar.
class ChatCevapResponse(BaseModel):
    # cevap: Yapay zekanın (Gemini) ürettiği nihai metin.
    cevap: str = Field(min_length=1, description="Yapay zekanın kaynaklara dayanarak ürettiği cevap")
    
    # kaynaklar: Cevabın doğruluğunu kanıtlayan, veritabanından çekilen paragraf listesi.
    kaynaklar: list[str] = Field(description="Cevabın oluşturulmasında kanıt olarak kullanılan metin parçaları")
