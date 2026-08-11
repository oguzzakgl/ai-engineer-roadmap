# faz5_langgraph/proje_kurumsal_multi_agent/main.py
"""
KURUMSAL ÇOKLU AJAN SİSTEMİ - TEST VE ÇALIŞTIRMA MODÜLÜ
------------------------------------------------------
Kullanıcıdan iş talebini alan ve LangGraph akışını başlatan CLI arayüzü.
"""

# Graph içindeki derlenmiş akışı (app) çağıracağız
# from graph import app

def main():
    """
    Sistemi başlatan ana fonksiyon.
    
    Öğrenilecek Adımlar:
    1. Kullanıcıdan input() ile kurumsal talebi al.
       (Örn: "Mevcut çalışan sayısını getir" veya "ali@gmail.com adresine mail at")
    2. KurumsalState modeline uygun başlangıç durumunu hazırla.
    3. app.stream() veya app.invoke() ile akışı başlat.
    4. Adım çıktılarını ve en son 'ajan_yaniti' sonucunu ekrana yazdır.
    """
    print("====================================================")
    print("🏢 AKILLI KURUMSAL ÇOKLU AJAN ASİSTANI (LANGGRAPH) 🏢")
    print("====================================================\n")
    
    sorgu = input("Yapmak istediğiniz işlemi yazın: ").strip()
    if not sorgu:
        print("Geçersiz işlem girdisi.")
        return
        
    baslangic_durumu = {
        "sorgu": sorgu,
        "yonlendirilen_ajan": "",
        "ajan_yaniti": "",
        "islem_gecmisi": []
    }
    
    print(f"\n🚀 İşlem başlatılıyor: '{sorgu}'...\n")
    
    # 📌 3. LangGraph akışını invoke veya stream et (Kodu sen yazacaksın)
    # try:
    #     for adim in app.stream(baslangic_durumu):
    #         for dugum_adi, guncel_state in adim.items():
    #             print(f"\n📍 [{dugum_adi.upper()}] Adımı Tamamlandı.")
    #             if "ajan_yaniti" in guncel_state and guncel_state["ajan_yaniti"]:
    #                 print(f"\n📢 AJAN YANITI: {guncel_state['ajan_yaniti']}")
    # except Exception as e:
    #     print(f"Akış sırasında hata oluştu: {e}")


if __name__ == "__main__":
    main()
