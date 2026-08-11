## 2026-08-11 06:05 - Faz 5: İleri Düzey RAG Başlangıcı (Query Translation)

### YAPILANLAR:
- [06_ileri_duzey_rag_sistemleri/01_query_translation_ve_decomposition.py](file:///c:/Users/ouz/Desktop/ai-engineer-roadmap/06_ileri_duzey_rag_sistemleri/01_query_translation_ve_decomposition.py) - Multi-Query, döküman tekilleştirme ve Query Decomposition pratik kodu ve test senaryosu başarıyla oluşturuldu.

### KARARLAR:
- Karmaşık veya genel sorgularda arama başarısını artırmak için LLM ile sorgu zenginleştirme (Query Translation) ve çok adımlı sorgu parçalama (Decomposition) mimarileri pratik edildi.

---

## 2026-08-11 02:41 - Faz 6: Arize Phoenix İzlenebilirlik Entegrasyonu ve Ajan Testi

### YAPILANLAR:
- [careerAsistant/main.py](file:///c:/Users/ouz/Desktop/reborn/careerAsistant/main.py) - Arize Phoenix OpenTelemetry izleme ve LangChainInstrumentor entegrasyonu tamamlandı.
- [careerAsistant/main.py](file:///c:/Users/ouz/Desktop/reborn/careerAsistant/main.py) - Windows terminallerindeki Türkçe karakter kodlama (cp1254 UnicodeEncodeError) hatasını aşmak için terminal çıktıları ASCII/UTF-8 uyumlu hale getirildi.
- Standalone Arize Phoenix sunucusu arka planda başarıyla ayağa kaldırıldı (`http://localhost:6006`).
- CV-İş İlanı analizi, eksik beceriler ve kişiselleştirilmiş yol haritası üreten LangGraph akışı izleme aktifken başarıyla çalıştırıldı ve sonuçlar ekrana basıldı.

### KARARLAR:
- Windows loopback (IPv6) ve veritabanı migrasyon yavaşlığından kaynaklanan timeout sorunlarını engellemek için Phoenix sunucusunun kod içerisinde `launch_app` ile değil, MLOps standartlarında bağımsız bir servis olarak arka planda çalıştırılması kararlaştırıldı.

### NOTLAR:
- Phoenix paneline `http://localhost:6006` üzerinden erişilebilir ve az önce çalışan LangGraph akışının tüm LLM ve RAG çağrıları görsel olarak izlenebilir.

## 2026-08-11 00:55 - Faz 5: LangChain, RAG ve LangGraph Pratiklerinin Tamamlanması

### YAPILANLAR:
- [faz5_langgraph/langchain_tekrar.py](file:///c:/Users/ouz/Desktop/reborn/faz5_langgraph/langchain_tekrar.py) - Pydantic Output Parser ile yapılandırılmış çıktı veren teknoloji analiz zinciri başarıyla kodlandı ve test edildi.
- [faz5_langgraph/rag_tekrar.py](file:///c:/Users/ouz/Desktop/reborn/faz5_langgraph/rag_tekrar.py) - ChromaDB ve PDF loader ile RAG boru hattı kuruldu. LCEL ile context_hazirlayici köprüsü kurularak test edildi.
- [faz5_langgraph/langgraph_tekrar.py](file:///c:/Users/ouz/Desktop/reborn/faz5_langgraph/langgraph_tekrar.py) - StateGraph üzerinde sayaç döngüsü ve koşullu çıkış kapısı (conditional edges) mantığı kurularak grafik başarıyla çalıştırıldı.
- [faz5_langgraph/özgeçmiş_taslağı.md](file:///c:/Users/ouz/Desktop/reborn/faz5_langgraph/özgeçmiş_taslağı.md) - Girişim planları doğrultusunda ATS uyumlu modern AI Developer CV şablonu hazırlandı.
- [faz5_langgraph/girişim_planı.md](file:///c:/Users/ouz/Desktop/reborn/faz5_langgraph/girişim_planı.md) - Otonom kurumsal asistan (Nova OS) ürün vizyonu ve departmanlar arası otonom paslaşma mimarisi belgelendirildi.

### KARARLAR:
- Tekrarlı llm/parser tanımlamalarından kaçınmak için global nesne tanımlama yaklaşımı (DRY prensibi) benimsendi.
- Döngüsel grafiklerde kilitlenmeyi önlemek için koşullu çıkış kapılarının (add_conditional_edges) düğüm çıkışlarına doğru konumlandırılması sağlandı.

### NOTLAR:
- Temel pratikler başarıyla tamamlandığı için proje bir sonraki adım olan çoklu ajan (multi-agent) mimarilerine hazır hale geldi.
