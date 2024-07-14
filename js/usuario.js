document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevenir el envío del formulario por defecto

            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            if (!username || !password) {
                alert('Por favor, complete todos los campos.');
                return;
            }

            fetch('https://docs.google.com/spreadsheets/d/e/2PACX-1vRU_17ow0jVNY1-YwQmhI5poo6q5pCjxispUmAwNsRzCycd3GTBSs8LRnp7H7a7bD59A14jnZ_rA2SO/pub?gid=0&single=true&output=csv')
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Error en la red');
                    }
                    return response.text(); // Convertir respuesta a texto
                })
                .then(data => {
                    const parsedData = processDataFromCSV(data); // Convertir CSV a objeto JavaScript

                    const user = parsedData.find(user => user.username === username && user.password === password);
                    if (user) {
                        console.log("Usuario encontrado:", user); // Verificación del usuario encontrado
                        localStorage.setItem('loggedInUser', JSON.stringify(user)); // Almacenar usuario en localStorage

                        switch (user.role.toLowerCase()) {
                            case 'administrador':
                                window.location.href = '../html/admin.html';
                                break;
                            case 'psicologo':
                                window.location.href = '../html/psicologos.html';
                                break;
                            case 'enfermeria':
                                window.location.href = '../html/enfermeria.html';
                                break;
                            case 'estudiante':
                                window.location.href = '../html/estudiantes.html';
                                break;
                            default:
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

    // Evento para manejar el historial del navegador
    window.addEventListener('popstate', function(event) {
        if (!localStorage.getItem('loggedInUser')) {
            window.location.href = 'index.html';
        }
    });

    // Función para convertir datos CSV en objeto JavaScript
    function processDataFromCSV(csvData) {
        const lines = csvData.split('\n');
        const headers = lines[0].split(',');
        const result = [];

        for (let i = 1; i < lines.length; i++) {
            const obj = {};
            const currentLine = lines[i].split(',');

            for (let j = 0; j < headers.length; j++) {
                obj[headers[j].trim()] = currentLine[j]?.trim();
            }

            result.push(obj);
        }

        return result;
    }
});

    // Cargar datos del Google Sheet para cada rol
    loadTableData('https://docs.google.com/spreadsheets/d/e/2PACX-1vTHT19rI2EPRnxrKldsHajplHhvxgTdX_tWFwg85h4MgN2BQuJT5mlVFaJmYofJuTIZAKGKANKkCDpF/pub?gid=1689042652&single=true&output=csv', '#psicologos-table tbody');
    loadTableData('https://docs.google.com/spreadsheets/d/e/2PACX-1vTHT19rI2EPRnxrKldsHajplHhvxgTdX_tWFwg85h4MgN2BQuJT5mlVFaJmYofJuTIZAKGKANKkCDpF/pub?gid=582985098&single=true&output=csv', '#enfermeria-table tbody');
    loadTableData('https://docs.google.com/spreadsheets/d/e/2PACX-1vTHT19rI2EPRnxrKldsHajplHhvxgTdX_tWFwg85h4MgN2BQuJT5mlVFaJmYofJuTIZAKGKANKkCDpF/pub?gid=1727120283&single=true&output=csv', '#estudiantes-table tbody');
    loadTableData('https://docs.google.com/spreadsheets/d/e/2PACX-1vRU_17ow0jVNY1-YwQmhI5poo6q5pCjxispUmAwNsRzCycd3GTBSs8LRnp7H7a7bD59A14jnZ_rA2SO/pub?gid=0&single=true&output=csv', '#admin-table tbody');
    
   // Get the elements
const loginForm = document.getElementById('login-form');
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const limpiarBtn = document.getElementById('limpiarBtn');

// Add event listener to the Limpiar button
limpiarBtn.addEventListener('click', () => {
    // Clear the input fields
    usernameInput.value = '';
    passwordInput.value = '';
});
    

