# 🗺️ AI Developer & Advanced LLM Engineer Öğrenme Yol Haritası

Bu döküman, Python temellerinden başlayarak SQL, FastAPI, RAG sistemleri, LangGraph otonom çoklu ajan mimarileri ve ileri düzey LLM mühendisliği (Fine-Tuning, Serving, GraphRAG) konularında gelişim yol haritamı ve ilerlememi gösterir.

---

## 🟢 FAZ 1: Python İleri Temelleri & Git/GitHub
> *Amaç: Kodlama altyapısını güçlendirmek ve versiyon kontrolünü öğrenmek.*

- [x] **Type Hinting (Tip Belirteçleri):** Python `typing` modülü, `str`, `int`, `List`, `Dict`, `Optional`. (Klasör: `01_python_ve_asenkron_programlama`)
- [x] **Dosya İşlemleri & JSON:** `with open()`, JSON serialization/deserialization. (Klasör: `01_python_ve_asenkron_programlama`)
- [x] **Hata Yönetimi (Exception Handling):** `try...except...finally`, özel Hata sınıfları. (Klasör: `01_python_ve_asenkron_programlama`)
- [x] **Asenkron Python (`asyncio`):** `async` / `await` anahtar kelimeleri, non-blocking I/O mantığı. (Klasör: `01_python_ve_asenkron_programlama`)
- [x] **Git Temelleri & GitHub:** `git init`, `git add`, `git commit`, `git push`, branch yönetimi ve uzak depo eşleme. (Klasör: `ai-engineer-roadmap`)

---

## 🔵 FAZ 2: Web, API, Veri Yönetimi & Test
> *Amaç: AI servislerini dış dünyaya sunacak backend mimarisini kurmak.*

- [x] **HTTP & REST Prensipleri:** GET, POST, PUT, DELETE metotları, Status Code'lar ve Payload yapısı. (Klasör: `02_sql_ve_fastapi_gelistirme`)
- [x] **Pydantic (v2):** Data Validation, `BaseModel`, `Field` ve Tip Güvenliği şemaları. (Klasör: `02_sql_ve_fastapi_gelistirme`)
- [x] **FastAPI Geliştirme:** Asenkron endpoint'ler, Dependency Injection (`Depends`) ve Swagger/OpenAPI. (Klasör: `02_sql_ve_fastapi_gelistirme`)
- [x] **SQL & Veritabanı (PostgreSQL):** SQLAlchemy ORM entegrasyonu, Neon Postgres veritabanı, CRUD işlemleri. (Klasör: `02_sql_ve_fastapi_gelistirme`)
- [x] **pytest ile Test Otomasyonu:** Unit testler, FastAPI TestClient ile endpoint testleri. (Klasör: `00_syntax_ve_temel_pratikler`)

---

## 🟣 FAZ 3: Yapay Zeka Uygulama Geliştirme (GenAI Stack)
> *Amaç: LLM'leri uygulamaya entegre etmek ve RAG mimarilerini kurmak.*

- [x] **LLM API Entegrasyonu & Structured Outputs:** Gemini API, LangChain entegrasyonu, Pydantic ile garantili JSON çıktısı alma. (Klasör: `03_generative_ai_ve_rag_temelleri`)
- [x] **Vektör Veritabanları & Embedding:** Cosine similarity matrisleri, ChromaDB entegrasyonu, Google Embeddings. (Klasör: `03_generative_ai_ve_rag_temelleri`)
- [x] **RAG (Retrieval-Augmented Generation):** PDFLoader ile döküman okuma, Recursive metin parçalama ve RAG sorgu zincirleri. (Klasör: `03_generative_ai_ve_rag_temelleri` & `04_langchain_yapisi`)
- [x] **Agent Orchestration (LangGraph):** StateGraph üzerinde durum yönetimi, döngüsel yapılar, ReAct ajanları ve çoklu ajan paslaşması. (Klasör: `05_langgraph_ajanlari`)
- [x] **Ana Portföy Projesi (Career Assistant):** Streamlit kullanıcı arayüzü, RAG tabanlı CV analizi, uyuşma raporu ve yol haritası üreten otonom LangGraph ajanı. (Klasör: `careerAssistant`)

---

## 🟡 FAZ 4: Bulut Servisleri, Docker & Production
> *Amaç: AI uygulamasını konteynerleştirip bulut ortamına taşımak.*

- [ ] **Docker ile Konteynerleştirme:** Dockerfile ve Docker Compose ile FastAPI ve Streamlit uygulamalarını container imajı yapma.
- [ ] **Azure Bulut Servisleri:** Azure App Service / Container Apps üzerinde API ve Streamlit canlı yayını.
- [x] **AI Observability & Monitoring:** Arize Phoenix ve OpenTelemetry entegrasyonu ile LLM çağrılarını, token maliyetlerini ve ajan adımlarını canlı izleme. (Port: `6006`)

---

## 🚀 FAZ 5: İleri Düzey RAG & Bilgi Grafikleri (Advanced RAG)
> *Amaç: Üretim ortamlarında RAG arama kalitesini ve çıkarım yeteneğini en üst düzeye çıkarmak.*

- [ ] **Query Translation & Decomposition:** Kullanıcı sorusunu analiz edip alt sorgulara bölme ve paralel arama yapma (Query Rewrite).
- [ ] **Reranking:** Cohere Reranker veya BGE Reranker entegrasyonu ile en alakalı dökümanları yukarı taşıyarak LLM bağlam kalitesini artırma.
- [ ] **Microsoft GraphRAG:** Dökümanlardaki varlıkları (entities) ve ilişkileri çıkarıp Neo4j veya benzeri grafik veritabanlarında Bilgi Grafiği (Knowledge Graph) oluşturarak ilişkisel RAG yapma.

---

## 🧠 FAZ 6: Gelişmiş Ajan Tasarım Kalıpları & Bellek (Advanced Agents)
> *Amaç: Kendi kendini denetleyen ve uzun vadeli hafızaya sahip üst düzey ajan sistemleri kurmak.*

- [ ] **Self-Reflection & Self-Correction:** Ajanın ürettiği çıktıyı (örneğin yazdığı SQL sorgusunu veya kodu) kendisinin çalıştırıp hata alırsa otomatik olarak düzeltmesi (Self-Correction/Reflection döngüleri).
- [ ] **Hierarchical Multi-Agent Architectures:** Bir "Yönetici Ajan" (Supervisor Node) tasarlayarak işleri uzman alt ajanlara (Raporcu, Analist, Yazılımcı) dağıtma ve yönetme.
- [ ] **Long-Term Semantic Memory:** Kullanıcı tercihlerini ve geçmiş konuşmaları PostgreSQL/ChromaDB üzerinde vektörel olarak saklayıp gelecekteki sohbetlerde otomatik hatırlama.

---

## 💾 FAZ 7: Yerel Model Servis Etme & Nicemleme (Local LLMs & Serving)
> *Amaç: Açık kaynaklı modelleri yerel sunucularda yüksek performansla çalıştırmak ve optimize etmek.*

- [ ] **Ollama & Llama.cpp:** Llama-3, Mistral, Gemma gibi modelleri tamamen yerel (local) bilgisayarda çalıştırma ve API olarak sunma.
- [ ] **Quantization (Nicemleme) Teknolojileri:** Büyük modelleri GGUF, AWQ ve GPTQ formatlarına sıkıştırarak VRAM tüketimini azaltma mantığı.
- [ ] **vLLM (High-Throughput Serving):** Üretim ortamlarında (production) binlerce eşzamanlı isteği karşılamak için "PagedAttention" tabanlı vLLM sunucu mimarisi kurma.

---

## ⚙️ FAZ 8: Model İnce Ayar (Fine-Tuning & Customization)
> *Amaç: Açık kaynaklı bir modeli kendi özel veri setimizle eğiterek belirli bir alanda uzmanlaştırmak.*

- [ ] **Dataset Hazırlama & Veri Temizleme:** Alpaca ve ShareGPT formatında LLM eğitim setleri hazırlama, tokenizasyon süreçleri.
- [ ] **LoRA & QLoRA:** Düşük donanımlarda model eğitebilmek için Parametre Verimli İnce Ayar (PEFT) tekniklerini uygulama.
- [ ] **Supervised Fine-Tuning (SFT) & DPO:** SFTTrainer ve Direct Preference Optimization kullanarak modeli insan tercihlerine göre hizalama.
- [ ] **Unsloth Entegrasyonu:** Llama-3 eğitimi süreçlerini 2 kat daha hızlı ve %80 daha az hafıza kullanımıyla gerçekleştirme.

---

## 🔒 FAZ 9: LLM Güvenliği & Guardrails (LLM Security)
> *Amaç: Ajan ve LLM sistemlerini manipülasyonlara ve zararlı girdilere karşı korumak.*

- [ ] **NeMo Guardrails & Llama Guard:** LLM giriş ve çıkışlarına güvenlik duvarı kurarak prompt injection ve uygunsuz içerik üretimini engelleme.
- [ ] **Prompt Injection & Jailbreak Defenses:** Sistem talimatlarını koruma yöntemleri ve LLM güvenlik açığı testleri (Red-Teaming).
