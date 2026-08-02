## [2026-08-02 - 05:13] - Faz 3: GenAI Entegrasyonu & Capstone PDF Chatbot

### YAPILANLAR:
- 3.2 & 3.3 Vektörleştirme (Embeddings), pgvector RAG entegrasyonu tamamlandı (faz3/konular/embeddings.py, similarity_test.py, simple_rag.py, pgvector_rag.py).
- 3.4 AI Ajanları & LangGraph Akış Yönetimi (State, Nodes, Edges, Routers) tamamlandı (faz3/konular/agent_intro.py).
- Gemini API ile interaktif terminal sohbet oturumu pratiği yapıldı (faz3/konular/canli_sohbet.py).
- Faz 3 Capstone Projesi: Akıllı PDF Asistanı (RAG + pgvector + FastAPI + Premium Glassmorphism UI) dosyaları oluşturuldu ve tamamlandı (faz3/proje_pdf_chat/).
  - models.py, schemas.py, database.py, crud.py, pdf_processor.py ve main.py yazıldı.
  - static/index.html ile şık, modern bir karanlık mod chat arayüzü tasarlandı.

### KARARLAR:
- Vektör tabanlı anlamsal aramayı (Semantic Search) Neon PostgreSQL bulut veritabanında pgvector eklentisiyle (<=> operatorü) çalıştırma kararı alındı.
- Büyük PDF dosyalarının işlenmesi sırasında sunucunun yorulmaması için kelime bazlı akıllı parçalama (chunking) algoritması tercih edildi.

### NOTLAR:
- Projeyi çalıştırmak için terminalden `cd faz3/proje_pdf_chat` dizinine gidip `uvicorn main:app --reload` komutu girilmelidir.

---

## [2026-07-23 - 01:05] - Faz 2: Web, API, Veri Yönetimi & Test

### YAPILANLAR:
- Faz 2 (Web, API, Veri Yönetimi & Test) süreci başlatıldı.
- 2.1 HTTP & REST Prenipleri çalışma notları dosyası oluşturuldu (faz2/konular/http_rest.py).
- 2.2 Pydantic (v2) veri doğrulama konusu tamamlandı (faz2/konular/pydantic_giris.py).
- 2.3 FastAPI temel web sunucusu ve yerel JSON entegrasyonu tamamlandı (faz2/konular/fastapigiris.py).
- 2.4 SQL & Veritabanı (PostgreSQL) bulut bağlantısı ve temel CRUD işlemleri tamamlandı (faz2/konular/veritabanisqlneon.py).
- 2.4 Ham SQL (Raw SQL) pratik çalışma dosyası oluşturuldu (faz2/konular/sql_temelleri.py).
- Faz 2 Tekrar ödevi dosyası oluşturuldu ve tamamlandı (faz2/tekrar/faz2_tekrar.py).
- Faz 3 (Yapay Zeka Uygulama Geliştirme) süreci başlatıldı.
- 3.1 LLM API Entegrasyonu, Structured Outputs ve Function Calling pratikleri yapıldı (faz3/konular/gemini_giris.py, structured_output.py, function_calling.py).
- Faz 3 Tekrar ödevi başarıyla tamamlandı (faz3/tekrar/faz3_tekrar.py).









### KARARLAR:
- Faz 1'deki interaktif öğretim ve kullanıcının kendi elleriyle yazma modeli Faz 2'de de sürdürülecek.

### NOTLAR:
- İlk konu: 2.1 HTTP & REST Prensipleri.

---

## [2026-07-22 - 23:04] - Faz 1: Python İleri Temelleri & Git/GitHub


### YAPILANLAR:
- Proje başlangıcı yapıldı ve seviye tespit testi tamamlandı.
- Faz 1 (Python İleri Temelleri & Git/GitHub) süreci başlatıldı.

### KARARLAR:
- Kullanıcı talebi doğrultusunda anlatım ve öğretim interaktif olarak teorik/örnek üzerinden yürütülecek; kullanıcı "kodunu yaz" demediği sürece çalışma alanına kod dosyası yazılmayacak.

### NOTLAR:
- 1.1 Tüm konu anlatım ve pratik dosyaları faz1/konular/ klasöründe toplandı (typehinting.py, dosya_islemleri.py, json_islemleri.py, hata_yonetimi.py, asenkron.py).
- 1.3 Faz 1 Capstone Projesi (Async Task Manager & JSON Logger) başarıyla tamamlandı. Kullanıcı tarafından tamamlanan/tamamlanmamış görev sayaçları yazıldı ve test edildi.



- 1.2 Git & GitHub repository başlatıldı ve ilk commit/push https://github.com/oguzzakgl/pythonDev.git adresine yapıldı.




