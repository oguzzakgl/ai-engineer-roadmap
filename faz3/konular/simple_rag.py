# faz3/konular/simple_rag.py
import math
from google import genai
from google.genai import types

# Gemini elçimizi başlatıyoruz.
client = genai.Client()

# ---------------------------------------------------------------------
# 📚 BİLGİ DOKÜMANLARIMIZ (SIMÜLE EDİLMİŞ VERİTABANI)
# ---------------------------------------------------------------------
# Şirketimizin kurallarını içeren bilgi tabanı. 
# Gemini bu bilgileri ezbere bilmez. Bunlar bizim özel verilerimizdir.
bilgi_tabani = [
    "Şirketimizde mesai saatleri hafta içi sabah 09:00 ile akşam 18:00 arasındadır.",
    "Yıllık izin talepleri en az 2 hafta önceden insan kaynakları sisteminden yapılmalıdır.",
    "Ofis mutfağındaki tüm yiyecek ve içecekler çalışanlar için ücretsizdir.",
    "Sunucu şifreleri ve API anahtarları asla Slack veya WhatsApp gibi platformlardan paylaşılamaz."
]


# ---------------------------------------------------------------------
# 🛠️ YARDIMCI HESAPLAMA FONKSİYONLARI
# ---------------------------------------------------------------------

# Gemini'den 3072 boyutlu embedding alan fonksiyonumuz
def vektor_al(metin: str):
    response = client.models.embed_content(
        model='gemini-embedding-2',
        contents=metin
    )
    return response.embeddings[0].values

# İki vektör arasındaki anlamsal yakınlığı hesaplayan Kosinüs Benzerliği fonksiyonumuz
def kosinus_benzerligi(vektor_a, vektor_b):
    dot_product = sum(a * b for a, b in zip(vektor_a, vektor_b))
    magnitude_a = math.sqrt(sum(a * a for a in vektor_a))
    magnitude_b = math.sqrt(sum(b * b for b in vektor_b))
    if not magnitude_a or not magnitude_b:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)


# ---------------------------------------------------------------------
# 🔍 1. ADIM: RETRIEVAL (BİLGİ GETİRME)
# ---------------------------------------------------------------------
# Kullanıcının sorduğu soruya en yakın dokümanı bilgi tabanından buluyoruz.
def en_alakali_dokumani_bul(kullanici_sorusu: str) -> str:
    print(f"\n[RAG] 1. Adım: Soru için vektör alınıyor: '{kullanici_sorusu}'")
    soru_vektoru = vektor_al(kullanici_sorusu)
    
    en_yuksek_skor = -1.0
    en_alakali_metin = ""
    
    print("[RAG] 2. Adım: Bilgi tabanındaki tüm satırlarla anlamsal yakınlık hesaplanıyor...")
    for satir in bilgi_tabani:
        satir_vektoru = vektor_al(satir)
        benzerlik = kosinus_benzerligi(soru_vektoru, satir_vektoru)
        
        # Eğer bu satır, şu ana kadar bulduğumuz en yakın satırsa, kaydet
        if benzerlik > en_yuksek_skor:
            en_yuksek_skor = benzerlik
            en_alakali_metin = satir
            
    print(f"[RAG] Bulunan en alakalı satır (Skor: {en_yuksek_skor:.4f}):")
    print(f"--> '{en_alakali_metin}'")
    return en_alakali_metin


# ---------------------------------------------------------------------
# 🚀 2. ve 3. ADIM: AUGMENTED GENERATION (ZENGİNLEŞTİRİLMİŞ ÜRETİM)
# ---------------------------------------------------------------------
# Bulduğumuz bilgiyi prompt içerisine yerleştirip Gemini'ye cevaplatıyoruz.
def rag_cevap_uret(soru: str):
    # 1. Bilgiyi getir (Retrieve)
    kaynak_bilgi = en_alakali_dokumani_bul(soru)
    
    # 2. Prompt'u zenginleştir (Augment)
    # Gemini'ye diyoruz ki: "Sana verdiğim KAYNAK BİLGİ dışına çıkma."
    zenginlestirilmis_prompt = f"""
Sana bir soru ve bu soruya cevap bulabilmen için bir kaynak bilgi verilecek.
Lütfen SADECE sana verilen kaynak bilgiyi kullanarak soruyu cevapla. Kaynak bilgide olmayan hiçbir şeyi uydurma.

KAYNAK BİLGİ:
{kaynak_bilgi}

SORU:
{soru}
"""
    
    print("\n[RAG] 3. Adım: Zenginleştirilmiş prompt Gemini'ye gönderiliyor...")
    
    # 3. Yanıtı üret (Generate)
    response = client.models.generate_content(
        model='gemini-3.5-flash',
        contents=zenginlestirilmis_prompt
    )
    
    print("\n--- GEMINI'NİN RAG CEVABI ---")
    print(response.text)


# Deneme sorumuzu soruyoruz
soru = "Ofiste acıkırsam dolaptan bir şeyler yiyebilir miyim, ücretli mi?"
rag_cevap_uret(soru)
