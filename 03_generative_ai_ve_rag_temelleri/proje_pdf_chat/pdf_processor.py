# faz3/proje_pdf_chat/pdf_processor.py
from pypdf import PdfReader
from google import genai
from sqlalchemy.orm import Session
from models import PDFDosyaTablosu, PDFParagrafTablosu

# 1. Gemini elçimizi başlatıyoruz.
# embed_content API çağrıları için bu nesneyi kullanacağız.
client = genai.Client()

# =====================================================================
# 📂 1. İŞLEM: PDF'TEN HAM METNİ SÖKMEK (pdf_metnini_oku)
# =====================================================================
# Girdi: file_path (Dosyanın bilgisayardaki geçici yolu)
# Çıktı: PDF'in tüm sayfalarındaki metinlerin birleştirilmiş hali (string)
def pdf_metnini_oku(file_path: str) -> str:
    tum_metin = ""
    # PDF dosyasını okumak üzere açıyoruz
    reader = PdfReader(file_path)
    
    # PDF'in tüm sayfalarını tek tek dolaşıyoruz
    for page in reader.pages:
        # Sayfadaki okunabilir karakterleri söküyoruz
        metin = page.extract_text()
        if metin:
            # Metni ve sayfa geçişini belirtmek için bir alt satır ekleyerek birleştiriyoruz
            tum_metin += metin + "\n"
            
    return tum_metin


# =====================================================================
# 📂 2. İŞLEM: METNİ KÜÇÜK PARÇALARA BÖLMEK (metni_parcalara_bol)
# =====================================================================
# Girdi: metin (bütün PDF metni), chunk_size (hedef paragraf uzunluğu - 800 harf)
# Çıktı: Kelimelerin bölünmediği 800'er karakterlik metin parçaları listesi (list[str])
def metni_parcalara_bol(metin: str, chunk_size: int = 800) -> list[str]:
    # 1. Metni kelimelerine ayırıyoruz (kelimelerin ortadan bölünmemesi için)
    words = metin.split()
    
    # 2. Sonuçta elde edeceğimiz paragrafların ekleneceği ana liste
    parcalar = []
    
    # 3. Aktif olarak kelimeleri biriktirdiğimiz geçici sepet (poşet)
    current_chunk = []
    
    # 4. Sepetteki kelimelerin toplam harf/karakter uzunluğu sayacı
    current_length = 0

    # 5. Tüm kelimeleri sırayla döngüye sokuyoruz
    for word in words:
        # Kelimeyi sepete ekle
        current_chunk.append(word)
        # Kelimenin harf sayısını ve 1 adet boşluk karakterini sayaca ekle
        current_length += len(word) + 1 
        
        # Eğer sepetin toplam karakter uzunluğu belirlenen limiti (800) geçtiyse:
        if current_length >= chunk_size:
            # Sepetteki kelimeleri aralarına boşluk koyarak birleştir ve listeye paragraf olarak ekle
            parcalar.append(" ".join(current_chunk))
            # Yeni paragraf için sepeti boşalt
            current_chunk = []
            # Sayacı sıfırla
            current_length = 0

    # 6. Döngü bittiğinde sepette kalan son kelimeleri de son bir parça olarak ekle
    if current_chunk:
        parcalar.append(" ".join(current_chunk))
        
    # 7. Oluşan tüm paragrafların listesini geri dön
    return parcalar


# =====================================================================
# 📂 3. İŞLEM: PARÇALARIN ANLAMSAL VEKTÖRLERİNİ ALMAK (parca_vektorlerini_uret)
# =====================================================================
# Girdi: parcalar (Az önce böldüğümüz metin paragraflarının listesi)
# Çıktı: Her paragrafın 3072 adet ondalık sayıdan oluşan koordinat listesi (list[list[float]])
def parca_vektorlerini_uret(parcalar: list[str]) -> list[list[float]]:
    # Gemini embed_content API'sine tüm listeyi tek seferde gönderiyoruz.
    # Bu sayede her paragraf için ayrı ayrı istek atıp zaman kaybetmeyiz (Batching).
    response = client.models.embed_content(
        model="gemini-embedding-2",
        contents=parcalar
    )
    # Gelen cevaptan her bir embedding koordinat dizisini (.values) çekiyoruz
    return [e.values for e in response.embeddings]


# =====================================================================
# 📂 4. ANA İŞLEM: PDF SÜRECİNİ YÖNETME VE VERİTABANINA YAZMA (pdf_dosyasini_isle)
# =====================================================================
# Girdi: file_path (Dosya yolu), dosya_adi (Dosya adı), db (Veritabanı bağlantısı)
# Çıktı: Veritabanına kaydedilen PDF dosyasının üst bilgi nesnesi
def pdf_dosyasini_isle(file_path: str, dosya_adi: str, db: Session) -> PDFDosyaTablosu:
    # 1. Adım: Veritabanına dosya adını kaydedip yeni bir dosya kaydı oluşturuyoruz
    yeni_pdf = PDFDosyaTablosu(dosya_adi=dosya_adi)
    db.add(yeni_pdf)
    db.commit() # Veri tabanına kaydet
    db.refresh(yeni_pdf) # Veritabanının bu dosyaya verdiği otomatik ID'yi (yeni_pdf.id) Python'a yükle

    pdf_id = yeni_pdf.id

    # 2. Adım: PDF dosyasını okuyup tüm metni tek bir string yapıyoruz
    tum_metin = pdf_metnini_oku(file_path)

    # 3. Adım: Dev metni kelime bölünmelerine dikkat ederek 800 karakterlik parçalara bölüyoruz
    parcalar = metni_parcalara_bol(tum_metin)

    # 4. Adım: Parçaların tamamını Gemini'ye gönderip 3072 boyutlu vektörlerini alıyoruz
    vektorler = parca_vektorlerini_uret(parcalar)

    # 5. Adım: Her paragraf metnini ve onun vektör koordinatlarını tek tek DB'ye kaydediyoruz
    # zip() kullanarak paragraf metnini ve o paragrafa ait vektör koordinatını eşleştiriyoruz
    for metin, vektor in zip(parcalar, vektorler):
        yeni_paragraf = PDFParagrafTablosu(
            pdf_id=pdf_id, 
            metin_icerigi=metin, 
            # Veritabanı sütunumuz Text olduğu için sayı listesini string'e çevirip kaydediyoruz
            embedding=str(vektor) 
        )
        db.add(yeni_paragraf)

    # 6. Adım: Tüm paragrafları veritabanına onaylıyoruz (commit)
    db.commit()
    
    return yeni_pdf
