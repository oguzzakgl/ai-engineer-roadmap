document.addEventListener('DOMContentLoaded', () => {
    const taskForm = document.getElementById('task-form');
    const newTaskInput = document.getElementById('new-task-input');
    const taskList = document.getElementById('task-list');

    // Görev ekleme fonksiyonu
    const addTask = (taskText) => {
        if (taskText.trim() === '') {
            return;
        }

        const listItem = document.createElement('li');
        listItem.classList.add('task-item');

        const taskSpan = document.createElement('span');
        taskSpan.classList.add('task-text');
        taskSpan.textContent = taskText;

        const taskActionsDiv = document.createElement('div');
        taskActionsDiv.classList.add('task-actions');

        const completeButton = document.createElement('button');
        completeButton.classList.add('complete-button');
        completeButton.textContent = 'Tamamla';
        completeButton.setAttribute('aria-label', 'Görevi tamamla');

        const deleteButton = document.createElement('button');
        deleteButton.classList.add('delete-button');
        deleteButton.textContent = 'Sil';
        deleteButton.setAttribute('aria-label', 'Görevi sil');

        taskActionsDiv.appendChild(completeButton);
        taskActionsDiv.appendChild(deleteButton);

        listItem.appendChild(taskSpan);
        listItem.appendChild(taskActionsDiv);

        taskList.appendChild(listItem);
    };

    // Form submit olay dinleyicisi
    taskForm.addEventListener('submit', (event) => {
        event.preventDefault(); // Sayfanın yeniden yüklenmesini engelle

        const taskText = newTaskInput.value;
        addTask(taskText);
        newTaskInput.value = ''; // Input alanını temizle
        newTaskInput.focus(); // Input alanına odaklan
    });

    // Görev listesi için olay dinleyicisi (delegasyon)
    taskList.addEventListener('click', (event) => {
        const target = event.target;

        // Tamamlama butonu tıklaması
        if (target.classList.contains('complete-button')) {
            const listItem = target.closest('.task-item');
            if (listItem) {
                listItem.classList.toggle('completed'); // 'completed' sınıfını ekle/kaldır
            }
        }

        // Silme butonu tıklaması
        if (target.classList.contains('delete-button')) {
            const listItem = target.closest('.task-item');
            if (listItem) {
                listItem.remove(); // Görevi DOM'dan kaldır
            }
        }
    });
});