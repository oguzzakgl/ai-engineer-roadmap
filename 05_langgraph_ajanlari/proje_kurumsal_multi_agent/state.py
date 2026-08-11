# faz5_langgraph/proje_kurumsal_multi_agent/state.py
"""
KURUMSAL ÇOKLU AJAN SİSTEMİ - STATE (DURUM) MODÜLÜ
--------------------------------------------------
Ajanların ortak durumunu ve veri iletimini sağlayan TypedDict tanımı.
"""

from typing import TypedDict, List, Dict, Any

class KurumsalState(TypedDict):
    """
    Tüm düğümlerin erişebileceği durum yapısı.
    """
    # Kullanıcının girdiği ilk talep / soru
    sorgu: str
    
    # Router'ın karar verdiği hedef uzman ajan ('SQL' veya 'CRM')
    yonlendirilen_ajan: str
    
    # Uzman ajanın ürettiği nihai yanıt metni
    ajan_yaniti: str
    
    # Grafik boyunca yapılan işlemlerin listesi (Loglama amaçlı)
    islem_gecmisi: List[str]
