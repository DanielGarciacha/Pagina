document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            // Verifica la conexión al JSON
            fetch('https://danielgarciacha.github.io/Taller/user.json')
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Error en la red');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log("Datos del JSON:", data); // Verificación del JSON

                    const user = data.users.find(user => user.username === username && user.password === password);
                    if (user) {
                        console.log("Usuario encontrado:", user); // Verificación del usuario

                        // Redirigir según el rol del usuario
                        if (user.role === 'admin') {
                            window.location.href = 'admin.html';
                        } else if (user.role === 'psicologo') {
                            window.location.href = 'psicologos.html';
                        } else if (user.role === 'enfermeria') {
                            window.location.href = './html/enfermeria.html';
                        } else if (user.role === 'estudiante') {
                            window.location.href = 'estudiantes.html';
                        } else {
                            console.error('Rol de usuario no reconocido:', user.role);
                            alert('Rol de usuario no reconocido');
                        }
                    } else {
                        alert('Usuario o contraseña incorrectos');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('No se pudo conectar con el servidor');
                });
        });
    }
});




