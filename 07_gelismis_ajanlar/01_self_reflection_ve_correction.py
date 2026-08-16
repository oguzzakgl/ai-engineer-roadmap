# 07_gelismis_ajanlar/01_self_reflection_ve_correction.py
"""
🧠 FAZ 6 - ADIM 1: GELİŞMİŞ AJANLAR - SELF-REFLECTION & SELF-CORRECTION
------------------------------------------------------------------------------
NEDİR?
Ajanların (AI Agents) geleneksel yapay zekalardan en büyük farkı, kararlar alabilmesi 
ve eylemlerinin sonuçlarına göre davranışlarını düzeltebilmesidir. 

"Self-Correction (Kendi Kendini Düzeltme)" döngüsü şu şekilde çalışır:
1. Üretim (Generation): Ajan, kendisine verilen talimata göre bir iş yapar (Örn: Python kodu yazar).
2. Eylem (Action/Execution): Yazılan kod veya üretilen eylem bir araç (tool/interpreter) 
   aracılığıyla çalıştırılır.
3. Denetleme (Reflection): Kod çalışırken hata alırsa (Örn: IndexError, SyntaxError), 
   ajan bu hata çıktısını alır ve "Ben nerede hata yaptım?" diye düşünerek hatayı analiz eder.
4. Düzeltme (Correction): Hata analizine göre kodu yeniden yazar ve tekrar çalıştırır.
   Bu süreç, kod hatasız çalışana veya maksimum deneme sınırına ulaşılana kadar tekrarlanır.

---
ÖDEV GÖREVİNİZ:
- calis_ve_duzelt() fonksiyonunun içini doldurarak, LLM'in yazdığı hatalı kodu 
  hata mesajına bakarak otomatik olarak düzeltmesini sağlayan döngüyü (reflection loop) kodlayın.
"""

import os
import sys
import io
from dotenv import load_dotenv
load_dotenv()

# API Key Kontrolü
if "GEMINI_API_KEY" in os.environ and "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Ajan beyni olarak kullanacağımız LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.0)


# =====================================================================
# 📋 BOILERPLATE: Python Kodunu Arka Planda Çalıştıran Güvenli Araç
# =====================================================================
def python_kodu_calistir(kod_metni: str) -> tuple[bool, str]:
    """
    Gelen Python kodunu exec() kullanarak çalıştırır.
    Dönen sonuç: (Başarılı Mı: bool, Çıktı Veya Hata Mesajı: str)
    """
    # print çıktılarını yakalamak için stdout'u yönlendiriyoruz
    eski_stdout = sys.stdout
    yeni_stdout = io.StringIO()
    sys.stdout = yeni_stdout
    
    basarili = True
    cikti = ""
    
    # Kodun başındaki ve sonundaki markdown işaretlerini temizleme
    kod_temiz = kod_metni.replace("```python", "").replace("```", "").strip()
    
    try:
        # Kodu çalıştır
        exec(kod_temiz, {})
        cikti = yeni_stdout.getvalue()
    except Exception as e:
        basarili = False
        # Hata tipini ve mesajını yakala
        import traceback
        cikti = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
    finally:
        # stdout'u eski haline getir
        sys.stdout = eski_stdout
        
    return basarili, cikti


# =====================================================================
# 🔥 GÖREV: SELF-CORRECTION (DÜZELTME) DÖNGÜSÜ
# =====================================================================
def calis_ve_duzelt(talimat: str, max_deneme: int = 3) -> str:
    """
    Görev: LLM'e verilen talimata göre Python kodu yazdırın.
    Kodu python_kodu_calistir() ile çalıştırın.
    Eğer hata alırsa, hatayı LLM'e geri besleyerek (reflection) kodu düzeltmesini isteyin.
    Başarılı olana kadar max_deneme sayısı kadar bu döngüyü sürdürün.
    
    İpuçları:
    - Adım 1: LLM'e ilk kodu yazdıracak bir prompt oluşturun (Sadece saf python kodu dönmeli).
    - Adım 2: Bir for/while döngüsü kurun (max_deneme kadar dönecek).
    - Adım 3: Kodu çalıştırın. Başarılıysa doğrudan kodu ve çıktıyı döndürün.
    - Adım 4: Hata aldıysa, LLM'e "Hatalı Kod" ve "Hata Mesajı" verilerini gönderen 
      yeni bir "düzeltme promptu" ile yeni kod isteyin. Döngüyü devam ettirin.
    """
    kod_uretme_promptu = ChatPromptTemplate.from_template(
        "Sana verilen talimata uygun bir Python kodu yaz.\n"
        "Kurallar:\n"
        "- Sadece Python kodu yaz, açıklama ekleme.\n"
        "- Kod blokları (```python) kullanabilirsin.\n\n"
        "Talimat: {talimat}\n"
        "Python Kodu:"
    )
    
    duzeltme_promptu = ChatPromptTemplate.from_template(
        "Yazdigin Python kodu calisirken hata aldi.\n"
        "Lutfen kodu incele ve hatayi gidererek kodu yeniden yaz.\n\n"
        "Hatali Kod:\n{hatali_kod}\n\n"
        "Alinan Hata:\n{hata_mesaji}\n\n"
        "Kurallar:\n"
        "- Sadece duzeltilmis Python kodunu yaz, aciklama ekleme.\n"
        "Duzeltilmis Python Kodu:"
    )
    
    # 1. İlk kod üretimi
    zincir = kod_uretme_promptu | llm | StrOutputParser()
    kod = zincir.invoke({"talimat": talimat})
    
    # 2. Hata düzeltme (reflection) döngüsü
    for deneme in range(max_deneme):
        print(f"\n👉 [Deneme {deneme + 1}/{max_deneme}] Kod çalıştırılıyor...")
        print(f"--- Çalıştırılacak Kod ---\n{kod}\n-------------------------")
        
        basarili, sonuc = python_kodu_calistir(kod)
        
        if basarili:
            print("✅ Kod başarıyla çalıştı!")
            return f"EĞİTİM BAŞARILI!\n\nKod:\n{kod}\n\nÇıktı:\n{sonuc}"
        else:
            # Hata tipini alıp ekrana basıyoruz
            hata_tipi = sonuc.splitlines()[0] if sonuc else "UnknownError"
            print(f"❌ Hata Alındı: {hata_tipi}")
            
            # Eğer son deneme hakkındaysak yeni kod istemeye gerek yok
            if deneme == max_deneme - 1:
                break
                
            print("🔍 Ajan hatayı inceliyor ve kodu düzeltiyor (Reflection)...")
            duzeltme_zinciri = duzeltme_promptu | llm | StrOutputParser()
            kod = duzeltme_zinciri.invoke({
                "hatali_kod": kod,
                "hata_mesaji": sonuc
            })
            
    return "Maksimum deneme sayısına ulaşıldı, kod düzeltilemedi."


# =====================================================================
# 🧪 TEST VE DOĞRULAMA ALANI
# =====================================================================
# Çalıştırmak için: $env:PYTHONIOENCODING="utf-8"; py 07_gelismis_ajanlar/01_self_reflection_ve_correction.py
# =====================================================================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🤖 TEST: SELF-CORRECTION AJAN DÖNGÜSÜ BAŞLIYOR")
    print("="*60)
    
    # ⚠️ Kasıtlı olarak hata üretecek zorlu bir talimat veriyoruz.
    # LLM ilk yazdığında büyük ihtimalle 6. elemana erişirken IndexError alacak.
    zorlu_talimat = (
        "5 elemanli bir liste olustur. Liste elemanlari: [10, 20, 30, 40, 50] olsun. "
        "Daha sonra bu listenin 6. elemanini (indeks 5) ekrana print etmeye calis. "
        "Eger hata alirsan hatayi yakalamak yerine kodun dogal olarak hata fırlatmasına izin ver."
    )
    
    print(f"Ajan Talimatı:\n{zorlu_talimat}\n")
    
    sonuc = calis_ve_duzelt(zorlu_talimat, max_deneme=3)
    print(sonuc)
    print("\n" + "="*60)
