# faz3/proje_sql_chat/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# =====================================================================
# 🎯 TODO 1: VERİTABANI BAĞLANTI AYARLARINI YAPIN
# =====================================================================
# Adım 1: DATABASE_URL değişkenini tanımlayın.
# (Referans: faz3/proje_pdf_chat/database.py dosyasındaki DATABASE_URL'i birebir kullanabilirsiniz.)
#
# Adım 2: create_engine() fonksiyonunu kullanarak bağlantı motorunu (engine) oluşturun.
# (Referans: faz3/proje_pdf_chat/database.py içindeki engine tanımı.)
#
# Adım 3: sessionmaker() ile SessionLocal oturum fabrikasını kurun.
# (Referans: faz3/proje_pdf_chat/database.py içindeki SessionLocal tanımı.)
#
# Adım 4: declarative_base() ile Base sınıfını oluşturun.
# (Referans: faz3/proje_pdf_chat/database.py içindeki Base tanımı.)
#
# Adım 5: get_db() dependency (oturum yönetim) fonksiyonunu yazın.
# (Referans: faz3/proje_pdf_chat/database.py içindeki get_db fonksiyonu.)
# =====================================================================
