document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    const messageDiv = document.getElementById('message');
    const limpiarBtn = document.getElementById('limpiarBtn');

    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        axios.post('http://127.0.0.1:3000/login', { // Asegúrate de usar la URL correcta del backend
            username: username,
            password: password
        })
        .then(function (response) {
            if (response.data.success) {
                messageDiv.innerHTML = `<div class="alert alert-success">Bienvenido, ${response.data.username}. Tu rol es: ${response.data.role}</div>`;
                
                switch(response.data.role) {
                    case 'admin':
                        window.location.href = 'html/admin.html';  // Ruta correcta para admin
                        break;
                    case 'estudiante':
                        window.location.href = 'html/estudiante.html';  // Ruta correcta para estudiante
                        break;
                    case 'enfermera':
                        window.location.href = 'html/enfermeria.html';  // Ruta correcta para enfermera
                        break;
                    case 'psicologo':
                        window.location.href = 'html/psicologos.html';  // Ruta correcta para psicologo
                        break;
                    default:
                        console.error('Rol desconocido:', response.data.role);
                        messageDiv.innerHTML += '<div class="alert alert-warning">Rol no reconocido. Contacte al administrador.</div>';
                }
            } else {
                messageDiv.innerHTML = '<div class="alert alert-danger">Usuario o contraseña incorrectos</div>';
            }
        })
        .catch(function (error) {
            console.error('Error:', error);
            messageDiv.innerHTML = '<div class="alert alert-danger">Error al intentar iniciar sesión</div>';
        });
        
    });

    limpiarBtn.addEventListener('click', function() {
        loginForm.reset();
        messageDiv.innerHTML = '';
    });
});

function togglePassword() {
    const passwordInput = document.getElementById('password');
    const togglePasswordIcon = document.getElementById('togglePassword');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        togglePasswordIcon.classList.replace('fa-eye', 'fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        togglePasswordIcon.classList.replace('fa-eye-slash', 'fa-eye');
    }
}

