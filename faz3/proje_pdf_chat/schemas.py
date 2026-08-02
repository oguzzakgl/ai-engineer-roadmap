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
    pass # TODO: Burayı doldur.


# =====================================================================
# 🎯 TODO 4: SOHBET SORU İSTEK ŞEMASI
# =====================================================================
# Kullanıcının PDF hakkında soru sorarken göndereceği veri formatı.
# Sınıf adı: ChatSoruRequest
# Alanlar:
# - soru: str (Kullanıcının yazdığı soru metni. min_length=3 olsun)
# =====================================================================
class ChatSoruRequest(BaseModel):
    pass # TODO: Burayı doldur.


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
    pass # TODO: Burayı doldur.
