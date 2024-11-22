document.getElementById('registerForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Останавливаем обычную отправку формы

    const formData = new FormData(this);  // Получаем данные из формы

    // Получаем CSRF-токен из cookies
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch('/register/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken,  // Добавляем CSRF-токен в заголовок
        }
    })
    .then(response => response.json())  // Обрабатываем ответ сервера
    .then(data => {
        if (data.status === 'success') {
            // Можно здесь обновить интерфейс или показать сообщение об успешной регистрации
            alert('Registration successful!');
        } else {
            alert('Registration failed: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred during registration.');
    });
});



document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault(); 

    const formData = new FormData(this); 

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch('/auth/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken, 
        }
    })
    .then(response => response.json()) 
    .then(data => {
        console.log(data); 
        if (data.status === 'success') {
            alert('Login successful!');
            window.location.href = '/main/'; 
        } else {
            alert('Login failed: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred during login.');
    });
});
