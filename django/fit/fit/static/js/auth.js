document.getElementById('registerForm').addEventListener('submit', function(event) {
    event.preventDefault();  

    const formData = new FormData(this);  


    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch('/register/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken,  
        }
    })
    .then(response => response.json())  
    .then(data => {
        if (data.status === 'success') {
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
