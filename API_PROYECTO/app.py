from flask import Flask, request, jsonify, session, redirect, url_for
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
from werkzeug.security import generate_password_hash, check_password_hash

# initializations
app = Flask(__name__)
CORS(app)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'proyecto'
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"0

# Ruta para iniciar sesión
@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.json['username']
        password = request.json['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        if user and check_password_hash(user[2], password):
            session['username'] = user[1]
            session['role'] = user[3]
            return jsonify({"informacion": "Inicio de sesión exitoso", "role": user[3]})
        else:
            return jsonify({"informacion": "Usuario o contraseña incorrectos"}), 401
    except Exception as e:
        print(e)
        return jsonify({"informacion": e})

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return jsonify({"informacion": "Sesión cerrada exitosamente"})

# Ruta para obtener el rol del usuario actual
@app.route('/getRole')
def getRole():
    if 'username' in session:
        return jsonify({"username": session['username'], "role": session['role']})
    else:
        return jsonify({"informacion": "No hay usuario logueado"})

# Ruta para administradores
@app.route('/admin')
def admin():
    if 'role' in session and session['role'] == 'admin':
        return jsonify({"informacion": "Bienvenido, administrador"})
    return jsonify({"informacion": "Acceso denegado"}), 403

# Ruta para psicólogos
@app.route('/psicologo')
def psicologo():
    if 'role' in session and session['role'] == 'psicologo':
        return jsonify({"informacion": "Bienvenido, psicólogo"})
    return jsonify({"informacion": "Acceso denegado"}), 403

# Ruta para enfermeros
@app.route('/enfermero')
def enfermero():
    if 'role' in session and session['role'] == 'enfermero':
        return jsonify({"informacion": "Bienvenido, enfermero"})
    return jsonify({"informacion": "Acceso denegado"}), 403

# Función para verificar si el usuario es un administrador
def is_admin():
    if 'role' in session and session['role'] == 'admin':
        return True
    return False

# Ruta para agregar un nuevo usuario, solo para administradores
@app.route('/add_user', methods=['POST'])
def add_user():
    if not is_admin():
        return jsonify({"informacion": "Acceso denegado. Solo administradores."}), 403
    
    try:
        nombre = request.json['nombre']
        identificacion = request.json['identificacion']
        correo = request.json['correo']
        telefono = request.json['telefono']
        funcion = request.json['funcion']
        username = request.json['username']
        password = request.json['password']
        rol = request.json['rol']  # El rol del nuevo usuario

        hashed_password = generate_password_hash(password)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios (nombre, identificacion, correo, telefono, funcion, username, password, rol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                    (nombre, identificacion, correo, telefono, funcion, username, hashed_password, rol))
        mysql.connection.commit()
        return jsonify({"informacion": "Usuario agregado exitosamente"})
    
    except Exception as e:
        print(e)
        return jsonify({"informacion": "Error al agregar usuario", "error": str(e)}), 500

# Ruta para consultar todos los registros
@app.route('/getAll')
def getAll():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM contacts')
        rv = cur.fetchall()
        cur.close()
        payload = []
        content = {}
        for result in rv:
            content = {'id': result[0], 'fullname': result[1], 'phone': result[2], 'email': result[3]}
            payload.append(content)
            content = {}
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion": e})

# Ruta para consultar por parámetro
@app.route('/getAllById/<id>')
def getAllById(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM contacts WHERE id = %s', (id,))
        rv = cur.fetchall()
        cur.close()
        payload = []
        content = {}
        for result in rv:
            content = {'id': result[0], 'fullname': result[1], 'phone': result[2], 'email': result[3]}
            payload.append(content)
            content = {}
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion": e})

# Ruta para crear un registro
@app.route('/add_contact', methods=['POST'])
def add_contact():
    try:
        if request.method == 'POST':
            fullname = request.json['fullname']  # nombre
            phone = request.json['phone']        # telefono
            email = request.json['email']        # email
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)", (fullname, phone, email))
            mysql.connection.commit()
            return jsonify({"informacion": "Registro exitoso"})
    except Exception as e:
        print(e)
        return jsonify({"informacion": e})

# Ruta para actualizar
@app.route('/update/<id>', methods=['PUT'])
def update_contact(id):
    try:
        fullname = request.json['fullname']
        phone = request.json['phone']
        email = request.json['email']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE contacts
        SET fullname = %s,
            email = %s,
            phone = %s
        WHERE id = %s
        """, (fullname, email, phone, id))
        mysql.connection.commit()
        return jsonify({"informacion": "Registro actualizado"})
    except Exception as e:
        print(e)
        return jsonify({"informacion": e})

# Ruta para eliminar
@app.route('/delete/<id>', methods=['DELETE'])
def delete_contact(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM contacts WHERE id = %s', (id,))
        mysql.connection.commit()
        return jsonify({"informacion": "Registro eliminado"})
    except Exception as e:
        print(e)
        return jsonify({"informacion": e})

# Iniciar la aplicación
if __name__ == "__main__":
    app.run(port=3000, debug=True)
