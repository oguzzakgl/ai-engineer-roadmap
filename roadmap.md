# 🗺️ AI Developer (GenAI Engineer) Öğrenme Yol Haritası

## 📌 Kullanıcı Başlangıç Seviyesi Tespiti
- **Mevcut Bilgiler:** Değişkenler, Fonksiyonlar, If/Else Koşulları, Döngüler, Temel Class Yapısı (OOP).
- **Hedef:** Junior AI Application / GenAI Developer.

---

## 🟢 FAZ 1: Python İleri Temelleri & Git/GitHub
> *Amaç: Kodlama altyapısını güçlendirmek ve versiyon kontrolünü öğrenmek.*

### 1.1 Python İleri Konuları
- [ ] **Type Hinting (Tip Belirteçleri):** Python `typing` modülü, `str`, `int`, `List`, `Dict`, `Optional`.
- [ ] **Dosya İşlemleri & JSON:** `with open()`, JSON serialization/deserialization.
- [ ] **Hata Yönetimi (Exception Handling):** `try...except...finally`, özel Hata sınıfları (Custom Exceptions).
- [ ] **Asenkron Python (`asyncio`):** `async` / `await` anahtar kelimeleri, non-blocking I/O mantığı.

### 1.2 Versiyon Kontrol (Git & GitHub)
- [ ] **Git Temelleri:** `git init`, `git add`, `git commit`, `git status`, `git log`.
- [ ] **GitHub & Branch Yönetimi:** `git push`, `git pull`, `git branch`, `git merge`, Pull Request (PR) süreçleri.

---

## 🔵 FAZ 2: Web, API, Veri Yönetimi & Test
> *Amaç: AI servislerini dış dünyaya sunacak backend mimarisini kurmak.*

### 2.1 HTTP & REST Prensipleri
- [ ] **HTTP Metodları:** `GET`, `POST`, `PUT`, `DELETE`, `PATCH`.
- [ ] **HTTP Status Code'lar:** 2xx (Başarılı), 4xx (İstemci Hatası), 5xx (Sunucu Hatası).
- [ ] **Headers & Payload:** Request/Response gövdesi, JSON formatı, Authorization header'ları.

### 2.2 Pydantic (v2)
- [ ] **Data Validation & Schemas:** Pydantic `BaseModel`, `Field`, `field_validator`.
- [ ] **Type Safety:** Çevresel değişkenler için `pydantic-settings` kullanımı.

### 2.3 FastAPI
- [ ] **API Geliştirme:** Asenkron endpoint'ler (`@app.get`, `@app.post`).
- [ ] **Dependency Injection:** FastAPI `Depends` mekanizması.
- [ ] **Swagger / OpenAPI:** Otomatik dokümantasyon üretimi ve API testi.

### 2.4 SQL & Veritabanı (PostgreSQL)
- [ ] **İlişkisel Veritabanı Mantığı:** Tablolar, Primary Key, Foreign Key, İlişkiler (1-N, N-N).
- [ ] **SQL Sorguları:** `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `JOIN`, `WHERE`.
- [ ] **ORM Kullanımı:** SQLAlchemy 2.0 veya SQLModel ile veritabanı etkileşimi.

### 2.5 pytest ile Test Otomasyonu
- [ ] **Unit Tests:** Fonksiyon ve iş mantığı testleri.
- [ ] **Integration Tests:** FastAPI `TestClient` / `AsyncClient` ile endpoint testleri.
- [ ] **Mocking:** Dış servisleri taklit etme (`unittest.mock` / `pytest-mock`).

---

## 🟣 FAZ 3: Yapay Zeka Uygulama Geliştirme (GenAI Stack)
> *Amaç: LLM'leri uygulamaya entegre etmek ve RAG mimarilerini kurmak.*

### 3.1 LLM API Entegrasyonu & Prompt Mühendisliği
- [ ] **LLM API Çağrıları:** OpenAI, Anthropic, Gemini API kütüphaneleri.
- [ ] **Structured Outputs:** Pydantic modelleri ile garanti JSON formatlı LLM çıktıları alma.
- [ ] **Function Calling / Tool Use:** LLM'lerin dış fonksiyonları ve API'leri tetiklemesi.
- [ ] **Prompt Security:** Prompt Injection engelleme, PII verilerini gizleme.

### 3.2 Vektör Veritabanları & Embedding
- [ ] **Embedding Kavramı:** Metinlerin matris karşılıkları, embedding modelleri (OpenAI, Cohere, BGE).
- [ ] **Vektör Arama:** Cosine Similarity, Dot Product, HNSW indeksleme.
- [ ] **Vector DBs:** PostgreSQL eklentisi `pgvector`, Qdrant veya ChromaDB.

### 3.3 RAG (Retrieval-Augmented Generation) Mimarisi
- [ ] **Chunking Stratejileri:** Metin bölme (Recursive, Semantic chunking).
- [ ] **Hybrid Search:** Vektör arama + BM25 keyword araması birleşimi.
- [ ] **Reranking:** Cohere / BGE Reranker ile sonuçların yeniden sıralanması.

### 3.4 Agent Frameworks & Orchestration
- [ ] **LangChain / LangGraph:** Multi-agent iş akışları ve durum yönetimi.
- [ ] **LlamaIndex:** Doküman odaklı arama ve RAG pipelines.

---

## 🔴 FAZ 4: Bulut Servisleri, Docker & Production
> *Amaç: AI uygulamasını konteynerleştirip bulut ortamına taşımak.*

### 4.1 Docker ile Konteynerleştirme
- [ ] **Dockerfile & Docker Compose:** Python / FastAPI uygulamalarını container imajı yapma.
- [ ] **Local & Prod Eşitlemesi:** Bağımlılıkları ve çalışma ortamını izole etme.

### 4.2 Azure Bulut Servisleri
- [ ] **Azure App Service / Container Apps:** API ve AI servislerini canlıya alma.
- [ ] **Azure OpenAI Service:** Kurumsal LLM modellerini çalıştırma.
- [ ] **Azure Key Vault:** Hassas API anahtarlarını saklama.

### 4.3 AI Observability & Monitoring
- [ ] **LangSmith / Phoenix:** Token kullanımı, maliyet hesabı ve LLM çağrılarını izleme.
