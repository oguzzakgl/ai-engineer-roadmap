# faz3/proje_sql_chat/schemas.py
from pydantic import BaseModel, Field
from typing import Optional

# =====================================================================
# 🎯 TODO 6: PDF DOSYA YANIT ŞEMASINI YAZIN (PDFDosyaResponse)
# =====================================================================
# (Referans: faz3/proje_pdf_chat/schemas.py içindeki PDFDosyaResponse şeması.)
# =====================================================================
class PDFDosyaResponse(BaseModel):
    id: int = Field(ge=0, description="PDF dosyasının veritabanındaki benzersiz kimlik numarası")
    dosya_adi: str = Field(min_length=1, max_length=255, description="Yüklenen PDF dosyasının adı")

    class Config:
        from_attributes = True
    

# =====================================================================
# 🎯 TODO 7: SOHBET İSTEK ŞEMASINI YAZIN (ChatSoruRequest)
# =====================================================================
# (Referans: faz3/proje_pdf_chat/schemas.py içindeki ChatSoruRequest şeması.)
# =====================================================================
class ChatSoruRequest(BaseModel):
    soru: str = Field(min_length=3, description="PDF içeriğine sorulacak soru metni")

# =====================================================================
# 🎯 TODO 8: BİRLEŞİK SOHBET CEVAP ŞEMASINI OLUŞTURUN (ChatCevapResponse)
# =====================================================================
# Bu şema, yapay zekanın cevabını, niyetini ve cevabın türüne göre (SQL veya PDF)
# döneceği ek verileri (grafik verileri, SQL sorgusu veya PDF paragrafları) taşır.
#
# Alanlar:
# - niyet: Cevabın türünü belirtir (String, örn: "BELGE_ARAMA" veya "VERITABANI_ANALIZ")
# - cevap: Yapay zekanın kullanıcıya yazdığı açıklayıcı cevap (String)
# - kaynaklar: Eğer niyet "BELGE_ARAMA" ise, kullanılan PDF paragraf listesi (Optional list[str])
# - sql_sorgusu: Eğer niyet "VERITABANI_ANALIZ" ise, çalıştırılan SQL sorgusu (Optional str)
# - tablo_verisi: Eğer niyet "VERITABANI_ANALIZ" ise, SQL sorgusunun veritabanından getirdiği
#   ham satırların sözlük (dict) formatındaki listesi. Grafik çizmek için JS'e gönderilir (Optional list[dict])
# =====================================================================

class ChatCevapResponse(BaseModel):
    niyet: str = Field(..., description="Cevabın türünü belirtir (BELGE_ARAMA veya VERITABANI_ANALIZ)")
    cevap: str = Field(..., description="Yapay zekanın kullanıcıya yazdığı açıklayıcı cevap")
    kaynaklar: Optional[list[str]] = Field(None, description="Cevabın oluşturulmasında kanıt olarak kullanılan PDF paragraf listesi")
    sql_sorgusu: Optional[str] = Field(None, description="Çalıştırılan SQL sorgusu")
    tablo_verisi: Optional[list[dict]] = Field(None, description="SQL sorgusunun veritabanından getirdiği ham satırların sözlük formatındaki listesi")
