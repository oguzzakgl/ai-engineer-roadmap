# 07_gelismis_ajanlar/02_hierarchical_multi_agent.py
"""
🧠 FAZ 6 - ADIM 2: HİYERARŞİK ÇOKLU AJAN MİMARİLERİ (HIERARCHICAL MULTI-AGENT)
------------------------------------------------------------------------------
NEDİR?
Büyük ve karmaşık görevleri tek bir ajana yaptırmak yerine, işleri uzmanlaşmış 
alt ajanlara (Workers) dağıtan ve bu süreci yöneten bir "Yönetici Ajan" (Supervisor) 
kurgusudur.

Bu çalışmada, senin önerdiğin "Vanilla JS ile Web Sitesi Üretme" senaryosunu simüle ediyoruz:
1. Yönetici Ajan (Supervisor): Kullanıcının fikrini alır. Önce HTML Ajanına görev verir, 
   gelen HTML kodunu inceler, ardından CSS Ajanına görev verir ve son olarak "Bitti" diyerek sonlandırır.
2. HTML Uzmanı (Worker): Sadece temiz ve semantik bir index.html içeriği üretir.
3. CSS Uzmanı (Worker): Gelen HTML içeriğine uygun, modern ve şık bir style.css hazırlar.
4. JS Uzmanı (Worker): Web sitesinin butonlarını ve özellikleri çalıştıran app.js hazırlar.

---
ÖDEV GÖREVİNİZ:
- TODO alanlarını doldurarak; Supervisor'ın state'i (durumu) yönetmesini, 
  sırasıyla HTML, CSS ve JS uzmanlarını çağırarak dosyaları oluşturmasını sağlayın.
"""

import os
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
# 📂 BOILERPLATE: Dosyaları Yerel Disk üzerine Kaydetme Aracı (Tool)
# =====================================================================
def dosyaya_yaz(dosya_adi: str, icerik: str):
    """
    Belirtilen dosya adına gelen içeriği yazar (HTML/CSS/JS dosyaları oluşturmak için).
    """
    klasor = "uretilen_website"
    if not os.path.exists(klasor):
        os.makedirs(klasor)
        
    yol = os.path.join(klasor, dosya_adi)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(icerik.strip())
    print(f"💾 Dosya başarıyla kaydedildi: {yol}")


# =====================================================================
# 🤖 UZMAN AJANLARIN PROMPT ŞABLONLARI
# =====================================================================
html_uzmani_prompt = ChatPromptTemplate.from_template(
    "Sen uzman bir Frontend HTML tasarımcısısın.\n"
    "Kullanıcının istediği web sitesi fikrine uygun, sadece temiz ve semantik bir HTML5 kodu yaz.\n"
    "Kurallar:\n"
    "- Kodun içinde `<link rel='stylesheet' href='style.css'>` ve `<script src='app.js' defer></script>` etiketlerinin olduğundan emin ol.\n"
    "- Sadece HTML kodu yaz, açıklama veya markdown dışı metin ekleme.\n\n"
    "İstenen Web Sitesi Fikri: {fikir}\n"
    "HTML Kodu:"
)

css_uzmani_prompt = ChatPromptTemplate.from_template(
    "Sen uzman bir CSS stilistisin.\n"
    "Sana verilen HTML koduna ve bu HTML'e dinamik olarak eleman ekleyen JavaScript (app.js) koduna uygun, "
    "kullanıcının '{fikir}' isteğini tamamlayan modern, şık ve duyarlı (responsive) bir style.css içeriği yaz.\n"
    "Kurallar:\n"
    "- JavaScript kodunu incele! JS içinde `document.createElement` veya `classList.add` ile dinamik oluşturulan "
    "TÜM elemanları, sınıfları (class) ve butonları (örn: .task-item, .complete-btn, .delete-btn, .completed, .completed-text vb.) bul.\n"
    "- Bu dinamik elemanlara harika, modern retro-futuristik buton/liste stilleri ekle. Asla varsayılan çirkin tarayıcı buton stili kalmasın.\n"
    "- Renkler uyumlu, yazı tipleri modern olsun.\n"
    "- Sadece CSS kodu yaz, açıklama veya markdown dışı metin ekleme.\n\n"
    "Mevcut HTML Kodu:\n{html_kodu}\n\n"
    "Dinamik JS Kodu:\n{js_kodu}\n"
    "CSS Kodu:"
)

js_uzmani_prompt = ChatPromptTemplate.from_template(
    "Sen uzman bir JavaScript yazılımcısısın.\n"
    "Kullanıcının talep ettiği fikir: {fikir}\n\n"
    "Bu fikir doğrultusunda üretilen HTML kodu aşağıdadır:\n{html_kodu}\n\n"
    "Görevin:\n"
    "- Yukarıdaki HTML kodunu dikkatlice analiz et. Etkileşimli elemanları (butonlar, inputlar, divler) ve bunların ID/Class isimlerini bul.\n"
    "- Bu HTML elemanlarını seçerek, kullanıcının istediği web uygulamasını tam fonksiyonel çalışır hale getirecek JavaScript kodunu yaz.\n"
    "- HTML'de olmayan ID'leri veya elemanları kullanma. Sadece HTML'de var olan elemanları seç.\n"
    "- Sadece saf JavaScript kodu yaz, açıklama veya markdown dışı metin ekleme.\n\n"
    "JavaScript Kodu:"
)


# =====================================================================
# 👑 GÖREV: HIYERARŞİK MULTI-AGENT ORKESTRASYONU
# =====================================================================
def web_sitesi_uret_ve_yonet(fikir: str):
    """
    Görev (Orkestrasyon Sırası):
    1. HTML Ajanı -> index.html yazar.
    2. JS Ajanı -> app.js yazar (Dinamik class/butonları belirler).
    3. CSS Ajanı -> style.css yazar (Hem HTML hem JS verilerini okuyarak eksiksiz tasarım yapar).
    """
    print(f"\n🚀 [Yönetici] İş akışı başlatıldı. Talep: '{fikir}'")
    
    # 1. HTML Ajanı tetikleniyor
    print("\n✍️ [Yönetici] HTML Uzmanı çalıştırılıyor...")
    html_zinciri = html_uzmani_prompt | llm | StrOutputParser()
    html_kodu = html_zinciri.invoke({"fikir": fikir})
    
    # Clean-up (kod bloklarını temizleme)
    html_kodu_temiz = html_kodu.replace("```html", "").replace("```", "").strip()
    dosyaya_yaz("index.html", html_kodu_temiz)
    
    # 2. JS Ajanı tetikleniyor (Dinamik ve Genel Amaçlı)
    print("\n⚡ [Yönetici] JS Uzmanı çalıştırılıyor...")
    js_zinciri = js_uzmani_prompt | llm | StrOutputParser()
    js_kodu = js_zinciri.invoke({
        "fikir": fikir,
        "html_kodu": html_kodu_temiz
    })
    
    # Clean-up
    js_kodu_temiz = js_kodu.replace("```javascript", "").replace("```js", "").replace("```", "").strip()
    dosyaya_yaz("app.js", js_kodu_temiz)
    
    # 3. CSS Ajanı tetikleniyor (JS ve HTML'i birlikte okuyor!)
    print("\n🎨 [Yönetici] CSS Uzmanı çalıştırılıyor...")
    css_zinciri = css_uzmani_prompt | llm | StrOutputParser()
    css_kodu = css_zinciri.invoke({
        "fikir": fikir,
        "html_kodu": html_kodu_temiz,
        "js_kodu": js_kodu_temiz
    })
    
    # Clean-up
    css_kodu_temiz = css_kodu.replace("```css", "").replace("```", "").strip()
    dosyaya_yaz("style.css", css_kodu_temiz)
    
    print("\n🎉 [Yönetici] Proje tamamlandı! Dosyalar 'uretilen_website/' klasörüne kaydedildi.")


# =====================================================================
# 🧪 TEST ALANI
# =====================================================================
if __name__ == "__main__":
    # Ajanlardan yapmasını istediğimiz modern web sitesi fikri
    site_fikri = (
        "Retro-futuristik tarzda, koyu arka plana sahip, şık bir To-Do List. "
        "Kullanıcı görevlerini ekleyebilsin, silsin ve tamamlananları işaretleyebilsin."
    )
    
    web_sitesi_uret_ve_yonet(site_fikri)
