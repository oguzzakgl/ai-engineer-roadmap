# modeller.py
# Bu dosyaya Hata Sınıfları ve Tip Tanımlarını sen yazacaksın.
from typing import TypedDict

class GorevBulunamadiHatasi(Exception):
    """Sistemde aranan görev ID'si bulunamadığında fırlatılır."""
    pass


class Gorev(TypedDict):
    id: int
    baslik: str
    tamamlandi: bool
    sure: int