
# =====================================================================
# 📂 GENEL TEKRAR - crud_tekrar.py
# =====================================================================
# Bu dosyada veritabanı işlemlerini yürütecek fonksiyonları yazacağız.
# Kılavuz olarak pratik/syntax_rehberi.py 4. bölümü kullanabilirsiniz.

from sqlalchemy.orm import Session
from sqlalchemy import text

# 1. Dinamik SQL Çalıştırıcı Fonksiyon (dinamik_sql_calistir)
# Parametreler: db (Session), sql_sorgusu (str)
# Görevi:
#   - Gelen sql_sorgusu'nu text() ile sarmalayarak çalıştır: db.execute(text(sql_sorgusu))
#   - Sonuçları fetchall() ile çek.
#   - SQLAlchemy Row nesnelerini dict(row._mapping) kullanarak birer sözlüğe (dict) çevir.
#   - Sözlüklerin listesini döndür.
#
# İPUCU:
# def dinamik_sql_calistir(db: Session, sql_sorgusu: str) -> list[dict]:
#     result = db.execute(text(sql_sorgusu))
#     return [dict(row._mapping) for row in result.fetchall()]
# =====================================================================
# KODUNUZU BURAYA YAZIN:

def dinamik_sql_calistir(db:Session, sql_sorgusu:str) -> list[dict]:
    sorgu = text(sql_sorgusu)

    sonuc = db.execute(sorgu).fetchall()

    kolonlar = list(sonuc[0]._mapping.keys()) if sonuc else []

    veriler = [dict(row._mapping) for row in sonuc]

    return veriler