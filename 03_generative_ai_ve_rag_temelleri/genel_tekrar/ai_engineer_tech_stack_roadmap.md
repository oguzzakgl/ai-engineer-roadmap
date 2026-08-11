# 🗺️ AI ENGINEER TEKNOLOJİ & ÖĞRENİM YOL HARİTASI

Abra Partners ve benzeri kurumsal firmaların AI Engineer ilanlarında aradığı, junior seviyeden başlayıp ileri seviyeye giden teknoloji stack listesi.

---

## Seviye 1: Temel Backend & Veritabanı (Mevcut Durum: %90 Tamamlandı) 🧱
Yapay zeka uygulamalarının dış dünyaya açıldığı ve verilerin saklandığı altyapı katmanı.

*   **Python:** Yapay zeka ve veri biliminin ana dili.
*   **FastAPI:** Hızlı, asenkron ve Pydantic tip doğrulamalı API backend çatısı.
*   **PostgreSQL & pgvector:** Kurumsal ilişkisel veriler ile vektör embedding verilerini aynı veritabanında saklama standardı.
*   **SQLAlchemy:** Python nesneleriyle veritabanı yönetimi (ORM).

---

## Seviye 2: RAG & Vektör Arama Mantığı (Mevcut Durum: %90 Tamamlandı) 📂
Belgeler içerisinden anlamsal arama yapma ve LLM bağlamını genişletme mantığı.

*   **Embedding Modelleri:** Metinleri anlamsal koordinat vektörlerine çeviren sistemler (Gemini Embedding, OpenAI text-embedding).
*   **Chunking (Parçalama):** Belgeleri anlam kaybı olmadan küçük parçalara bölme stratejileri.
*   **Kosinüs Benzerliği (Cosine Distance):** Soru vektörü ile döküman vektörleri arasındaki anlamsal mesafeyi ölçme formülü.
*   **Prompt Engineering:** LLM'e bağlamı (context) ve kuralları doğru aktarma sanatı.

---

## Seviye 3: Hazır AI Frameworks & Vektör Veritabanları (Gelecek Adım) 🤖
Uygulamaları daha hızlı prototiplemek için kullanılan kütüphaneler.

*   **LangChain:** LLM zincirleri, RAG bileşenleri ve ajanları bağlayan en popüler ekosistem.
*   **LlamaIndex:** Veri yükleme, dizinleme ve RAG odaklı optimize edilmiş veri kütüphanesi.
*   **ChromaDB / Pinecone / Weaviate:** pgvector alternatifi olan, hızlı ayağa kalkan özel vektör veritabanları.

---

## Seviye 4: Gelişmiş Ajanlar (Agentic AI) & Protokoller 🚀
Yapay zekanın karar verme, planlama ve araç kullanma yetenekleri.

*   **Function Calling (Araç Kullanımı):** Modelin, kullanıcının sorusuna göre doğru Python fonksiyonunu çalıştırma kararı alması.
*   **AI Agents (Çoklu Ajanlar - CrewAI / LangGraph):** Belirli görevleri paylaşan işbirlikçi yapay zeka ajanları.
*   **MCP (Model Context Protocol):** Modellerin yerel sistemlerle (veritabanı, dosyalar) güvenli iletişim kurmasını sağlayan yeni açık standart.

---

## Seviye 5: Altyapı & Dağıtım (Production Ready) 🐳
Uygulamanın sunucuya taşınması ve versiyon yönetimi.

*   **Docker:** Uygulamayı kütüphaneleriyle birlikte paketleyip her ortamda aynı çalışmasını sağlayan konteyner teknolojisi.
*   **Git & GitHub:** Versiyon kontrolü, ekip çalışması ve portfolyo sunumu.
*   **CI/CD Temelleri:** Kod güncellendiğinde testlerin otomatik çalışması.
