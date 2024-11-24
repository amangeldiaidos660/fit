document.addEventListener('DOMContentLoaded', () => {
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) {
            return decodeURIComponent(parts.pop().split(';').shift());
        }
        return null; 
    }


    const responseData = getCookie('responseData');

    if (responseData) {
        try {
            const data = JSON.parse(responseData);

            if (data.user_id) {
                console.log('User ID:', data.user_id);
                localStorage.setItem('user_id', data.user_id);
            } else {
                console.error('User ID не найден в cookie');
            }
        } catch (error) {
            console.error('Ошибка при разборе данных из cookie:', error);
        }
    } else {
        console.log('Cookie с именем "responseData" не найдено.');
    }





    const accountTab = document.getElementById('account-tab');
    accountTab.addEventListener('click', () => {
        fetch('/user_data/')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const userInfo = document.getElementById('userInfo');
                    userInfo.innerHTML = `
                        <p><strong>Email:</strong> ${data.user.email}</p>
                        <p><strong>Логин:</strong> ${data.user.login}</p>
                        <p><strong>Имя:</strong> ${data.user.name}</p>
                    `;
                } else {
                    console.error('Ошибка:', data.message);
                    alert('Не удалось загрузить данные пользователя.');
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
                alert('Произошла ошибка при загрузке данных.');
            });
    });


    
    const getCSRFToken = () => {
        return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    };

    logoutButton.addEventListener('click', () => {
        fetch('/logout/', {
            method: 'POST',
            credentials: 'include',
            headers: {
                'X-CSRFToken': getCSRFToken(),
            },
        })
            .then(response => response.json())
            .then(data => {
                console.log('Ответ сервера:', data);
                if (data.status === 'success') {
                    document.cookie = "responseData=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
                    window.location.replace('/');
                } else {
                    console.error('Ошибка при выходе:', data.message);
                    alert('Не удалось завершить сессию.');
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
                alert('Произошла ошибка при выходе.');
            });
    });
    
});
