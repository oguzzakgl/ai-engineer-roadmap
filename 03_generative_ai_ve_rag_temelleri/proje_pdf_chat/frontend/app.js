// =====================================================================
// 🌐 API BAĞLANTI AYARLARI
// =====================================================================
const API_URL = ""; // Sunucu ile aynı porttan çalışacağı için boş bırakabiliriz.

// DOM Elemanlarını Seçiyoruz (HTML üzerindeki etiketler)
const fileInput = document.getElementById("pdf-file");
const dropZone = document.getElementById("drop-zone");
const filesList = document.getElementById("files-list");
const uploadStatus = document.getElementById("upload-status");
const chatForm = document.getElementById("chat-form");
const userQuestionInput = document.getElementById("user-question");
const chatMessages = document.getElementById("chat-messages");
const sendBtn = document.getElementById("send-btn");

// =====================================================================
// 🚀 UYGULAMA BAŞLANGICI (SAYFA YÜKLENDİĞİNDE)
// =====================================================================
document.addEventListener("DOMContentLoaded", () => {
    // Sayfa açıldığında daha önce veritabanına yüklenmiş dosyaları listele
    dosyalariYukle();
});

// =====================================================================
// 📁 DOSYALARI LİSTELEME FONKSİYONU
// =====================================================================
async function dosyalariYukle() {
    try {
        const response = await fetch(`${API_URL}/files`);
        if (!response.ok) throw new Error("Dosya listesi çekilemedi.");
        
        const files = await response.json();
        
        // Eğer veritabanında dosya yoksa boş liste mesajı göster
        if (files.length === 0) {
            filesList.innerHTML = `<li class="empty-list">Henüz belge yüklenmedi.</li>`;
            return;
        }

        // Gelen dosyaları listeye dönüştürerek ekrana bas
        filesList.innerHTML = files.map(file => `
            <li>📄 ${file.dosya_adi}</li>
        `).join("");

    } catch (error) {
        console.error("Hata:", error);
    }
}

// =====================================================================
// ⬆️ PDF DOSYASI YÜKLEME SÜRECİ
// =====================================================================
fileInput.addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (file) pdfYukle(file);
});

async function pdfYukle(file) {
    // Arayüzde yükleniyor durumu
    uploadStatus.textContent = "Yükleniyor ve vektörleşiyor...";
    uploadStatus.className = "status-msg status-loading";
    
    // HTTP Multipart Form Data hazırlığı (Dosya göndermek için)
    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch(`${API_URL}/upload-pdf`, {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.detail || "Yükleme hatası.");
        }

        // Başarılı durumu
        uploadStatus.textContent = "Yükleme başarıyla tamamlandı!";
        uploadStatus.className = "status-msg status-success";
        
        // Dosya listesini hemen güncelle
        dosyalariYukle();

    } catch (error) {
        // Hatalı durumu
        uploadStatus.textContent = error.message;
        uploadStatus.className = "status-msg status-error";
    }
}

// =====================================================================
// 💬 SOHBET / RAG SÜRECİ (SORU SORMA)
// =====================================================================
chatForm.addEventListener("submit", async (e) => {
    e.preventDefault(); // Sayfanın yenilenmesini engeller

    const soru = userQuestionInput.value.trim();
    if (!soru) return;

    // 1. Kullanıcının sorusunu ekrana mesaj kabarcığı olarak ekle
    mesajEkle(soru, "user");
    userQuestionInput.value = ""; // Girdi alanını temizle

    // 2. Yapay zeka cevap verirken butonları geçici kilitle ve yükleniyor ikonu göster
    sendBtn.disabled = true;
    const loadingMessageId = mesajEkle("Düşünüyor...", "ai system-msg");

    try {
        // 3. API'ye soruyu gönderiyoruz
        const response = await fetch(`${API_URL}/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ soru: soru })
        });

        // Geçici "Düşünüyor..." mesajını sil
        loadingMessageId.remove();

        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.detail || "Cevap üretilirken bir hata oluştu.");
        }

        const data = await response.json();

        // 4. Yapay zekanın cevabını ve kaynaklarını ekrana bas
        mesajEkle(data.cevap, "ai", data.kaynaklar);

    } catch (error) {
        loadingMessageId.remove();
        mesajEkle(error.message, "ai system-msg");
    } finally {
        sendBtn.disabled = false;
        userQuestionInput.focus();
    }
});

// =====================================================================
// 🛠️ EKRANA MESAJ BALONU EKLEME YARDIMCISI (DOM HELPER)
// =====================================================================
function mesajEkle(metin, gonderen, kaynaklar = []) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `${gonderen}-message`;
    
    // Mesaj metnini güvenli şekilde ekle (satır atlamalarını koru)
    messageDiv.innerHTML = `<p>${metin.replace(/\n/g, "<br>")}</p>`;

    // Eğer yapay zeka cevabıysa ve kaynak paragraflar varsa, "Citations/Kaynak" alanını oluştur
    if (gonderen === "ai" && kaynaklar.length > 0) {
        const citationsDiv = document.createElement("div");
        citationsDiv.className = "citations-container";

        // Tıklanabilir başlık
        const citationsTitle = document.createElement("div");
        citationsTitle.className = "citations-title";
        citationsTitle.innerHTML = "📖 Yararlanılan Kaynak Paragrafları Göster/Gizle";
        
        // Kaynakların listesi (başlangıçta gizli)
        const citationsList = document.createElement("div");
        citationsList.className = "citations-list";
        citationsList.style.display = "none";
        
        citationsList.innerHTML = kaynaklar.map(k => `
            <div class="citation-card">"... ${k} ..."</div>
        `).join("");

        // Tıklandığında açılıp kapanma aksiyonu (Toggle)
        citationsTitle.addEventListener("click", () => {
            citationsList.style.display = citationsList.style.display === "none" ? "block" : "none";
        });

        citationsDiv.appendChild(citationsTitle);
        citationsDiv.appendChild(citationsList);
        messageDiv.appendChild(citationsDiv);
    }

    chatMessages.appendChild(messageDiv);
    
    // Mesajlar eklendikçe ekranı en aşağı kaydır (Auto Scroll)
    chatMessages.scrollTop = chatMessages.scrollHeight;

    return messageDiv; // Geçici yükleniyor mesajını silebilmek için div referansını dönüyoruz
}
