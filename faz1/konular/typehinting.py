isim = "oguz"
yas = 19

isim2: str = "oguz"
yas2: int = 19

def topla(a: int, b: int) -> int:
    return a + b


def birlesim(a: str, b: str) -> str:
    return f"{a} - {b}"

print(birlesim("oguz","akgul"))


sayilar: list[int] = [1, 2, 3, 4]
isimler: list[str] = ["oguz", "ali", "ayse"]


ogrenci_notlari: dict[str, int] = {
    "oguz": 90,
    "ali": 85
}


telefon: str | None = None


def kumascinsi(cins: str | None = None) -> str | None:
    if cins is None:
        return "kumas cinsi belirtilmedi"
    return f"Bu bir {cins} kumaştır."

print(kumascinsi("ipek"))
print(kumascinsi())