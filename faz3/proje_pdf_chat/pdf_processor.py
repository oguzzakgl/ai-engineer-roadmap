# faz3/proje_pdf_chat/pdf_processor.py
from pypdf import PdfReader
from google import genai
from sqlalchemy.orm import Session
from models import PDFDosyaTablosu, PDFParagrafTablosu

# 1. Gemini elçimizi başlatıyoruz.
client = genai.Client()

# =====================================================================
# 🎯 TODO 6: PDF'TEN HAM METNİ AYIKLAMA (TEXT EXTRACTION)
# =====================================================================
# Verilen PDF dosya yolundaki metinleri sayfa sayfa okuyup birleştiren fonksiyon.
# Girdi: file_path (str)
# Çıktı: Tüm PDF'in birleşik metin içeriği (str)
# İpucu:
# reader = PdfReader(file_path)
# for page in reader.pages:
#     text += page.extract_text()
# =====================================================================
def pdf_metnini_oku(file_path: str) -> str:
    tum_metin = ""
    reader=PdfReader(file_path)
    for page in reader.pages:
        tum_metin += page.extract_text()
    return tum_metin


# =====================================================================
# 🎯 TODO 7: METNİ KÜÇÜK PARÇALARA BÖLME (CHUNKING)
# =====================================================================
# PDF metnini, yapay zekanın rahat okuması için 500-1000 karakterlik 
# mantıklı parçalara ayıran fonksiyon.
# Girdi: metin (str), chunk_size (int = 800)
# Çıktı: Parçalara ayrılmış metin listesi (list[str])
# İpucu:
# Metni satır sonlarına (\n) göre bölüp, kelime kelime ekleyerek 
# 800 karaktere ulaştığında listeye ekleyen basit bir döngü yazabilirsin.
# Veya en basitinden metni doğrudan 800 karakterlik dilimlere bölebilirsin.
# =====================================================================
def metni_parcalara_bol(metin: str, chunk_size: int = 800) -> list[str]:
    # 1. Metni kelimelerine ayırıyoruz (kelimelerin ortadan bölünmemesi için)
    words = metin.split()
    
    # 2. Sonuçta elde edeceğimiz paragrafların ekleneceği liste
    parcalar = []
    
    # 3. Aktif olarak kelimeleri biriktirdiğimiz geçici sepet
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
            # Sepetteki kelimeleri aralarına boşluk koyarak birleştir ve listeye ekle
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
# 🎯 TODO 8: PARÇALARIN EMBEDDING KOORDİNATLARINI ÜRETME
# =====================================================================
# Elde ettiğimiz her bir metin parçasının Gemini ile 3072 boyutlu vektörünü çıkarır.
# Girdi: parcalar (list[str])
# Çıktı: Vektörlerin listesi (list[list[float]])
# İpucu:
# client.models.embed_content(model="gemini-embedding-2", contents=parcalar)
# =====================================================================
def parca_vektorlerini_uret(parcalar: list[str]) -> list[list[float]]:
    vektorler = []
    # TODO: Gemini modelini kullanarak her bir parçanın embedding vektörünü al.
    return vektorler


# =====================================================================
# 🎯 TODO 9: TÜM PDF SÜRECİNİ YÖNETME VE DB'YE KAYDETME (MASTER PROCESS)
# =====================================================================
# PDF dosyasını okuyup, parçalayıp, vektörlerini alıp DB'ye kaydeden ana fonksiyon.
# Girdi: file_path (str), dosya_adi (str), db (Session)
# Çıktı: PDFDosyaTablosu nesnesi (veritabanından dönen kayıt)
# İş Akışı:
# 1. Yeni bir PDFDosyaTablosu kaydı oluşturup db'ye ekle ve commit et (id'sini almak için).
# 2. pdf_metnini_oku() ile metni çıkar.
# 3. metni_parcalara_bol() ile parçala.
# 4. parca_vektorlerini_uret() ile tüm parçaların vektörlerini al.
# 5. Her bir parçayı PDFParagrafTablosu modeliyle (pdf_id, metin_icerigi, embedding) DB'ye kaydet.
#    (Vektörü DB'de text olarak saklayacağımız için embedding=str(vektor) şeklinde kaydetmelisin!)
# 6. db.commit() et ve oluşturduğun dosya nesnesini dön.
# =====================================================================
def pdf_dosyasini_isle(file_path: str, dosya_adi: str, db: Session) -> PDFDosyaTablosu:
    # TODO: Yukarıdaki iş akışını uygulayarak verileri veritabanına kaydet.
    pass
