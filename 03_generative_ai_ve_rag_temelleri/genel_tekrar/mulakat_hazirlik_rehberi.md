# 🎯 TEKNİK MÜLAKAT HAZIRLIK REHBERİ (AI & BACKEND ENGINEER)

Bu döküman, teknik mülakatlarda (özellikle AI Product Engineer rollerinde) en çok sorulan soruları, bu soruların arkasındaki gerçek mühendislik nedenlerini ve mülakatçıyı etkileyecek profesyonel cevapları barındırır.

---

## 🧠 BÖLÜM 1: YAPAY ZEKA VE RAG (RETRIEVAL-AUGMENTED GENERATION) MİMARİSİ

### Soru 1: RAG (Retrieval-Augmented Generation) nedir ve neden ihtiyaç duyarız?
*   **Mülakatçı neyi test ediyor?** Yapay zekanın sınırlarını bilip bilmediğinizi ve dış veri kaynaklarını modele nasıl güvenle besleyeceğinizi anlayıp anlamadığınızı.
*   **Nokta Atışı Cevap:** 
    > "Büyük Dil Modelleri (LLM) sadece kendi eğitildikleri genel verileri bilirler ve şirketlerin özel dökümanlarına veya güncel verilere erişimleri yoktur. Ayrıca bilmedikleri konularda uydurma (halüsinasyon) cevaplar verebilirler. 
    > RAG, kullanıcının sorusuyla ilgili en alakalı belgeleri (PDF, Word vb.) önce bir veritabanından bulup çıkartır, ardından bu belgeleri soruyla birlikte LLM'e bağlam (context) olarak besler. Böylece model uydurmadan, tamamen gerçek belgelere dayanarak doğru ve güncel cevaplar üretir."

### Soru 2: Belgeleri veritabanına kaydederken neden "Chunking" (parçalama) yapıyoruz?
*   **Mülakatçı neyi test ediyor?** Token maliyeti kontrolü, model bağlam penceresi (context window) limitleri ve anlamsal gürültü azaltma bilginizi.
*   **Nokta Atışı Cevap:**
    > "Bunun üç temel nedeni var:
    > 1. **Bağlam Penceresi ve Maliyet:** 500 sayfalık bir PDF'in tamamını her soruda LLM'e göndermek çok yüksek API maliyetine ve yavaş cevap sürelerine (latency) neden olur.
    > 2. **Alaka Düzeyi:** Tüm dökümanı göndermek modele 'gürültü' yaratır. Biz sadece sorunun cevabını içeren paragrafları (örneğin ~800 karakterlik parçaları) göndererek odaklanmayı artırırız.
    > 3. **Kelime Bütünlüğü:** Parçalama yaparken kelimelerin ortadan kesilmemesine dikkat ederiz ki vektör benzerliği hesaplanırken kelimenin anlamı kaybolmasın."

### Soru 3: Vektör Embedding (Vektör Temsili) nedir?
*   **Mülakatçı neyi test ediyor?** Yapay zekanın metinleri nasıl matematiksel koordinatlara dönüştürdüğünü bilip bilmediğinizi.
*   **Nokta Atışı Cevap:**
    > "Embedding, kelimelerin veya paragrafların anlamsal karşılıklarının yapay zeka modelleri tarafından çok boyutlu (örneğin Gemini Embedding v2 ile 3072 boyutlu) birer ondalık sayı listesine (vektöre) dönüştürülmesidir. 
    > Bu sayede anlamsal olarak birbirine benzeyen metinler (Örn: 'otomobil' ve 'araba') bu çok boyutlu uzayda geometrik olarak birbirine çok yakın koordinatlarda yer alırlar."

---

## 🗄️ BÖLÜM 2: VERİTABANI VE SQL GÜVENLİĞİ

### Soru 4: Klasik kelime araması (LIKE sorgusu) ile Vektör Araması (Cosine Similarity) arasındaki fark nedir?
*   **Mülakatçı neyi test ediyor?** Semantik (anlamsal) arama ile anahtar kelime eşleşmesi arasındaki farkı anlayıp anlamadığınızı.
*   **Nokta Atışı Cevap:**
    > "Klasik `LIKE '%kelime%'` araması sadece harf harfe eşleşme arar. Kullanıcı 'araba' yazdıysa ve dökümanda sadece 'otomobil' geçiyorsa sonucu bulamaz.
    > Vektör araması (Kosinüs Benzerliği) ise harflere değil anlama bakar. İki metnin embedding vektörleri arasındaki açının kosinüsünü hesaplar. Böylece kullanıcı 'otomobil' yazsa bile 'araba' veya 'taşıt' geçen paragrafı en alakalı sonuç olarak getirebilir."

### Soru 5: Text-to-SQL (Yapay zekaya SQL yazdırma) uygulamalarında veritabanı güvenliğini nasıl sağlarsınız?
*   **Mülakatçı neyi test ediyor?** Üretim ortamında (production) veri güvenliğini nasıl koruyacağınızı ve SQL Injection risklerini nasıl azaltacağınızı.
*   **Nokta Atışı Cevap:**
    > "Yapay zekanın ürettiği SQL sorgularını doğrudan veritabanında çalıştırmak büyük risk taşır. Bunu engellemek için 3 katmanlı güvenlik uygularım:
    > 1. **Read-Only DB Yetkisi:** Uygulamanın SQL çalıştırdığı veritabanı kullanıcısına sadece okuma (`SELECT`) yetkisi veririm. Böylece yapay zeka kazara `DELETE` veya `DROP` üretse bile veritabanı bunu reddeder.
    > 2. **Kod Seviyesinde Filtreleme:** Python kodunda çalıştırılacak SQL string'ini kontrol edip içinde 'DROP', 'DELETE', 'TRUNCATE' gibi kelimeler geçiyorsa işlemi durdururum.
    > 3. **Prompt Guardrails:** Prompt içinde modele sadece veri okuma sorguları üretebileceğini kesin bir dille kural olarak belirtirim."

---

## 🕸️ BÖLÜM 3: API TASARIMI VE YAZILIM PRENSİPLERİ

### Soru 6: Pydantic şemaları (BaseModel) neden kullanılır?
*   **Mülakatçı neyi test ediyor?** Veri doğrulama, tip güvenliği ve API sözleşmesi (API contract) konusundaki tecrübenizi.
*   **Nokta Atışı Cevap:**
    > "Pydantic, dışarıdan gelen verileri otomatik olarak doğrulamamızı (validation) ve tip güvenliği (type safety) sağlamamızı sağlar. 
    > Örneğin bir endpoint `stok: int` bekliyorsa ve kullanıcı metin gönderdiyse, kodumuz hata vermeden önce Pydantic bunu yakalar ve kullanıcıya düzgün bir hata mesajı döner. Ayrıca Gemini'den Structured Output (Yapılandırılmış Çıktı) alırken modelin belirlediğimiz JSON şemasına kesin olarak uymasını garanti eder."

### Soru 7: early return (Erken Dönüş) prensibi nedir ve neden önemlidir?
*   **Mülakatçı neyi test ediyor?** Clean Code (Temiz Kod) yazma alışkanlığınızı ve kod okunabilirliğine verdiğiniz önemi.
*   **Nokta Atışı Cevap:**
    > "Erken dönüş, bir fonksiyonda hata veya özel durumlar varsa, bunları fonksiyonun en başında kontrol edip `return` or `raise` ile hemen sonlandırma prensibidir. 
    > Bu sayede iç içe geçmiş (nested) `if-else` bloklarının yarattığı karmaşıklığı ('Arrow Anti-Pattern') engelleriz. Kod yukarıdan aşağıya düz ve okunabilir bir şekilde akar."

---

## 🚀 BÖLÜM 4: GELİŞMİŞ RAG VE LLMOPS SORULARI (YENİ KAYNAKLAR)

### Soru 8: RAG sistemlerinde "Reranking" (Yeniden Sıralama) nedir ve neden gereklidir? (Cross-Encoder vs Bi-Encoder)
*   **Mülakatçı neyi test ediyor?** Arama doğruluğunu artırma (Precision) ve gelişmiş arama mimarileri bilginizi.
*   **Nokta Atışı Cevap:**
    > "Vektör veritabanları (Bi-Encoder mimarisi), milyonlarca dökümanı hızlıca taramak için metinleri bağımsız vektörlere çevirir ve benzerlik hesaplar. Bu işlem çok hızlıdır ama anlamsal ince detayları kaçırabilir.
    > Reranking aşamasında, ilk aramada dönen en alakalı örn: 20 dökümanı alıp, soru ile dökümanı aynı anda işleyen daha güçlü bir modele (Cross-Encoder) sokarız. Bu model, soru ile döküman arasındaki ilişkiyi kelime kelime karşılaştırarak en alakalı ilk 3-5 belgeyi yeniden sıralar. Bu sayede LLM'e giden bağlamın kalitesi ve doğruluğu en üst düzeye çıkar."

### Soru 9: Üretim ortamındaki (production) bir LLM uygulamasında maliyet ve gecikmeyi düşürmek için "Semantic Cache" (Anlamsal Önbellek) nasıl kullanılır?
*   **Mülakatçı neyi test ediyor?** LLMOps tecrübenizi, API maliyet kontrolü ve performans iyileştirme yöntemlerini.
*   **Nokta Atışı Cevap:**
    > "Klasik önbellekler (Redis vb.) birebir aynı anahtarı arar. Kullanıcı 'İzin politikası nedir?' yazdıktan sonra 'Bana izin politikasını anlat' yazarsa klasik önbellek bunu kaçırır ve LLM'e tekrar istek atar.
    > Semantic Cache (Anlamsal Önbellek) ise gelen sorunun embedding'ini alıp daha önce sorulmuş ve önbelleğe alınmış sorularla benzerlik kontrolü yapar. Eğer benzerlik eşiği (örn: 0.95 üstü) çok yüksekse, LLM'e hiç gitmeden önbellekteki cevabı milisaniyeler içinde döner. Bu hem maliyeti %80'e kadar düşürür hem de gecikmeyi 0'a indirir."

### Soru 10: RAG başarısını ölçmek için kullanılan "Ragas" metrikleri (Faithfulness ve Answer Relevance) nelerdir?
*   **Mülakatçı neyi test ediyor?** RAG değerlendirme (evaluation) metotları ve halüsinasyon ölçüm bilgilerinizi.
*   **Nokta Atışı Cevap:**
    > "RAG sistemlerinin kalitesini ölçmek için Ragas kütüphanesinin iki temel metriğini kullanırız:
    > 1. **Faithfulness (Doğruluk/Güvenilirlik):** LLM'in ürettiği cevabın, veritabanından çekilen kaynak paragraflara ne kadar sadık olduğunu ölçer. Eğer cevapta kaynakta olmayan bir iddia varsa, faithfulness skoru düşer (yani halüsinasyon vardır).
    > 2. **Answer Relevance (Cevap Alakası):** Üretilen cevabın, kullanıcının sorduğu soruya ne kadar doğrudan hitap ettiğini ölçer. Cevap uzun ve doğru olsa bile, asıl soruyu geçiştiriyorsa bu skor düşer."
