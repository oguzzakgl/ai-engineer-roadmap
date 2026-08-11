# faz4_langchain/proje_langchain_assistant/pdf_processor_langchain.py
"""
LANGCHAIN ILE PDF ISLEME VE PARÇALAMA (CHUNKİNG)
-----------------------------------------------------------------------
🔄 FAZ 3 KARŞILIĞI: 
Bu dosya, Faz 3'teki `faz3/proje_sql_chat/pdf_processor.py` dosyasında yazdığımız
`pdf_metnini_oku()` (20 satır) ve `metni_parcalara_bol()` (52 satır) fonksiyonlarının
toplam 72 satırlık karmaşık kodunun YERİNE GEÇER.
-----------------------------------------------------------------------
"""

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def pdf_islem_langchain(pdf_dosya_yolu: str) -> list[Document]:
    """
    LangChain kullanarak bir PDF dosyasını okur ve akıllıca parçalara ayırır.
    """
    print(f"📄 [LangChain] PDF Yükleniyor: {pdf_dosya_yolu}")
    
    # -----------------------------------------------------------------
    # 🔄 FAZ 3 KARŞILIĞI: faz3/pdf_processor.py -> pdf_metnini_oku() (Sayfa döngüsü)
    # PyPDFLoader tüm sayfaları tek adımda okur.
    # -----------------------------------------------------------------
    loader = PyPDFLoader(pdf_dosya_yolu)
    sayfalar = loader.load()
    
    print(f"✅ [LangChain] Toplam {len(sayfalar)} sayfa okundu.")
    
    # -----------------------------------------------------------------
    # 🔄 FAZ 3 KARŞILIĞI: faz3/pdf_processor.py -> metni_parcalara_bol() (52 satırlık döngü)
    # RecursiveCharacterTextSplitter paragraf, cümle ve kelime sınırlarına göre otomatik böler.
    # -----------------------------------------------------------------
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    parcalanmis_dokumanlar = text_splitter.split_documents(sayfalar)
    
    print(f"✂️ [LangChain] PDF {len(parcalanmis_dokumanlar)} anlamlı parçaya bölündü.")
    
    return parcalanmis_dokumanlar


if __name__ == "__main__":
    print("PDF İşleyici LangChain Modülü Hazır!")
