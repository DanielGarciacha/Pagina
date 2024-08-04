// Espera a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    const apiUrl = 'http://127.0.0.1:3000';

    // Función para cargar la lista de citas
    function loadUserList() {
        console.log("Cargando lista de citas..."); // Log de inicio
        axios.get(`http://127.0.0.1:3000/getAll_psi`)
            .then(response => {
                console.log("Datos recibidos:", response.data); // Log de datos recibidos
                const tableBody = document.querySelector('#dataTable');
                tableBody.innerHTML = ''; // Limpiar el contenido previo
                response.data.forEach(user => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${user.nombre_apellidos}</td>
                        <td>${user.correo}</td>
                        <td>${user.genero}</td>
                        <td>${user.motivo}</td>
                        <td>${user.fecha_reserva}</td>
                        <td>${user.hora_reserva}</td>
                        <td>${user.sede}</td>
                        <td>${user.user_id}</td>
                        <td>
                            <button class="btn btn-warning btn-sm" onclick="editUser(${user.user_id})">Editar</button>
                            <button class="btn btn-danger btn-sm" onclick="deleteUser(${user.user_id})">Eliminar</button>
                        </td>
                    `;
                    tableBody.appendChild(row);
                });
            })
            .catch(error => {
                console.error('Error fetching user list:', error);
            });
    }

    // Llama a la función para cargar la lista de citas al cargar la página
    loadUserList();
});
