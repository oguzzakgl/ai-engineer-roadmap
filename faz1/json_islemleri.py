import json

# Elimizdeki Python Sözlüğü (dict)
kullanici: dict = {
    "ad": "oguz",
    "yas": 20,
    "sehir": "istanbul"
}

# =========================================================
# 1. json.dumps() -> SADECE METNE (STRING) ÇEVİRİR
# (Dosya ile işi yoktur, sadece değişken olarak tutarsın)
# =========================================================
json_metni: str = json.dumps(kullanici, ensure_ascii=False, indent=4)

print("--- 1. json.dumps() ÇIKTISI ---")
print(json_metni)
print("Veri Tipi:", type(json_metni))  # <class 'str'> (Düz metin)


# =========================================================
# 2. json.dump() -> ÇEVİRİR VE DOĞRUDAN DOSYAYA YAZAR
# (Açık olan dosyaya otomatik olarak veriyi basar)
# =========================================================
with open("kullanici.json", "w", encoding="utf-8") as f:
    json.dump(kullanici, f, ensure_ascii=False, indent=4)

print("\n--- 2. json.dump() ÇIKTISI ---")
print("kullanici.json dosyası oluşturuldu ve veri içine yazıldı!")
