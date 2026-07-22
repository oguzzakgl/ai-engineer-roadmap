# =====================================================================
# 🔵 FAZ 2 - KONU 2.1: HTTP & REST PRENSİPLERİ (ÇALIŞMA NOTLARI)
# =====================================================================

# ---------------------------------------------------------------------
# 🚀 1. HTTP Metotları (Request Methods)
# ---------------------------------------------------------------------
# GET    -> Sunucudan veri okumak için kullanılır (Gövdesi yoktur).
# POST   -> Sunucuda yeni veri oluşturmak için kullanılır (Payload/JSON taşır).
# PUT    -> Sunucudaki veriyi tamamen güncellemek için kullanılır.
# PATCH  -> Sunucudaki verinin sadece belirli bir kısmını güncellemek için kullanılır.
# DELETE -> Sunucudaki veriyi silmek için kullanılır.


# ---------------------------------------------------------------------
# 📊 2. HTTP Durum Kodları (Status Codes)
# ---------------------------------------------------------------------
# 2xx (Başarılı İşlemler):
#   - 200 OK      -> İşlem başarıyla tamamlandı.
#   - 201 Created -> Yeni kaynak başarıyla oluşturuldu.
#
# 4xx (İstemci / Hatalı İstek Hataları):
#   - 400 Bad Request  -> İstek hatalı veya eksik veri içeriyor.
#   - 401 Unauthorized -> Kimlik doğrulama başarısız (API Key/Token eksik).
#   - 403 Forbidden    -> Yetki yetersiz (Giriş yapılmış ama izni yok).
#   - 404 Not Found    -> Aranan kaynak veya sayfa bulunamadı.
#
# 5xx (Sunucu Hataları):
#   - 500 Internal Server Error -> Sunucu tarafında Python kodu patladı.
#   - 503 Service Unavailable   -> Sunucu yoğun veya bakımda.


# ---------------------------------------------------------------------
# 📨 3. Headers (Başlıklar) ve Payload (Gövde)
# ---------------------------------------------------------------------
# Headers (Meta Veriler):
#   - Content-Type: application/json -> Gönderilen/alınan verinin JSON olduğunu belirtir.
#   - Authorization: Bearer <token>  -> API anahtarını taşır.
#
# Payload / Body (Asıl Veri):
#   - Genellikle JSON biçimindeki verinin kendisidir.
#   - Örnek: {"soru": "Python nedir?", "sure": 10}
