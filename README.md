# 🎓 AI Engineer Roadmap & Workspace

Bu depo, Python temellerinden başlayarak SQL, FastAPI, LLM entegrasyonları, RAG (Retrieval-Augmented Generation) sistemleri ve son olarak LangGraph tabanlı çoklu ajan (Multi-Agent) mimarilerine uzanan AI Engineering gelişim yolculuğumu içermektedir.

## 🗂️ Çalışma Yapısı ve Konular

Depo, adım adım öğrenilen konulara ve pratik çalışmalara göre sıralanmıştır:

1.  **`00_syntax_ve_temel_pratikler`**
    *   Python sınıfları (OOP), RAG için akıllı metin parçalama (chunking), cosine similarity matrisleri, temel SQL ve FastAPI denemeleri.
2.  **`01_python_ve_asenkron_programlama`**
    *   Gelişmiş Python konuları: Hata yönetimi, JSON manipülasyonu, asenkron programlama (`asyncio`) ve tip ipuçları (type hinting).
3.  **`02_sql_ve_fastapi_gelistirme`**
    *   Pydantic veri doğrulama modelleri, Neon Postgres entegrasyonu, SQLAlchemy ORM ile CRUD işlemleri ve kurumsal FastAPI geliştirme.
4.  **`03_generative_ai_ve_rag_temelleri`**
    *   Gemini API entegrasyonları, pgvector ile vektör veritabanları, function calling (araç çağırma) ve döküman tabanlı RAG (PDF/SQL Chat) projeleri.
5.  **`04_langchain_yapisi`**
    *   Langchain kütüphanesi kullanarak RAG boru hatları, araç tanımları (Tools), hafıza (Memory) yönetimi ve sınav koçu gibi asistan projeleri.
6.  **`05_langgraph_ajanlari`**
    *   LangGraph ile döngüsel grafikler (cyclic graphs), state yönetimi ve custom reducer'lar, otonom ReAct ajan mimarisi ve multi-agent paslaşma simülasyonları.
7.  **`careerAsistant`** (💼 Ana Portföy Projesi)
    *   **AI Career Assistant & Job Matcher**: Adayın CV'sini (RAG) ve iş ilanını analiz edip Pydantic formatında yapılandırılmış uyuşma raporu üreten ve Phoenix Tracing entegrasyonlu modern Streamlit arayüzüne sahip otonom ajan sistemi.

---

## 🛠️ Temel Teknolojiler

*   **Diller & Frameworkler:** Python 3.13+, FastAPI, Streamlit, SQLAlchemy, Pydantic
*   **AI / Ajan Mimarileri:** LangGraph, LangChain, Gemini API (gemini-2.5-flash)
*   **Veritabanları:** Neon (PostgreSQL), ChromaDB, pgvector
*   **Gözlemlenebilirlik (MLOps):** Arize Phoenix, OpenTelemetry

---

*Bu çalışma alanı, modern LLM uygulama geliştirme, yapay zeka ajanları ve MLOps standartlarına uyum sağlamak üzere tasarlanmıştır.*
