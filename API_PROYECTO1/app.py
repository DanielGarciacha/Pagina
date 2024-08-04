from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
import mysql.connector

app = Flask(__name__)
CORS(app)

# Configuración de conexión a MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mi_base_datos' #cambiar a TU base de datos para que todo corra y funcione de manera acorde
mysql = MySQL(app)
app.secret_key = "mysecretkey"


# Rutas de mi API para gráfico
@app.route("/getAllUsers", methods=["GET"])
def consultar():
    if request.method == "GET": 
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM user")
            resultado = cur.fetchall()
            cur.close()
            print(f"Resultado de la consulta: {resultado}")
            tabla = []
            for fila in resultado:
                print(fila)
                if len(fila) == 8:  # Asegúrate de que la tupla tiene 8 elementos
                    contenido = {
                        "id": fila[0],
                        "nombre": fila[1],
                        "identificacion": fila[2],
                        "correo": fila[3],
                        "telefono": fila[4],
                        "username": fila[5],
                        "password": fila[6],
                        "rol": fila[7]
                    }
                    tabla.append(contenido)
                else:
                    print(f"Fila con datos insuficientes: {fila}")
            return jsonify(tabla)
        except Exception as error:
            print("Error al obtener los usuarios \n", error)
            return jsonify({"mensaje": str(error)}), 500
        
        
# Ruta para grafica de cantidad de citas en psicologia
@app.route("/getcitaspsicologias", methods=["GET"])
def get_psychology_appointments():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*) AS total FROM citas")
        resultado = cur.fetchone()
        cur.close()
        total_appointments = resultado[0] if resultado else 0
        return jsonify({"total": total_appointments})
    except Exception as error:
        return jsonify({"mensaje": str(error)}), 500

# Ruta para grafica de cantidad de citas en enfermeria
@app.route("/getcitasenfermeria", methods=["GET"])
def get_nursing_appointments():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*) AS total FROM citas_enfermeria")
        resultado = cur.fetchone()
        cur.close()
        total_appointments = resultado[0] if resultado else 0
        return jsonify({"total": total_appointments})
    except Exception as error:
        return jsonify({"mensaje": str(error)}), 500
    
# Ruta para consultar todos los registros(ADMIN)
@cross_origin()
@app.route('/getAll', methods=['GET'])
def getAll():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM user')  # Cambiado a 'user'
        rv = cur.fetchall()
        cur.close()
        payload = []
        for result in rv:
            content = {
                'id': result[0], 
                'nombre': result[1], 
                'identificacion': result[2], 
                'correo': result[3], 
                'telefono': result[4], 
                'username': result[5], 
                'password': result[6], 
                'rol': result[7]
            }
            payload.append(content)
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)})
    
    
# Ruta para consultar todos los registros(PSICOLOGO)
@app.route('/getAll_psi', methods=['GET'])
def get_all_psi():
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT estudiante_id, Nombre_Completo, Correo, Genero, motivo, fecha, hora, sede
            FROM citas
            WHERE Nombre_Completo IS NOT NULL AND Nombre_Completo != ''
        """)
        rv = cur.fetchall() 
        cur.close()
        
        payload = []
        for result in rv:
            content = {
                'user_id': result[0],
                'nombre_apellidos': result[1] or "No especificado", 
                'correo': result[2] or "No especificado",
                'genero': result[3] or "No especificado",
                'motivo': result[4] or "No especificado",
                'fecha_reserva': result[5].strftime('%Y-%m-%d') if result[5] else "No especificado",
                'hora_reserva': result[6].strftime('%H:%M:%S') if result[6] else "No especificado",
                'sede': result[7] or "No especificado"
            }
            payload.append(content)
        return jsonify(payload)
    except Exception as e:
        print(f"Error en get_all_psi: {str(e)}")
        return jsonify({"error": str(e)}), 500


#  consultar por parámetro
@cross_origin()
@app.route('/getAllById/<id>', methods=['GET'])
def getAllById(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM user WHERE id = %s', (id,))
        rv = cur.fetchall()
        cur.close()
        payload = []
        for result in rv:
            content = {
                'id': result[0], 
                'nombre': result[1], 
                'identificacion': result[2], 
                'correo': result[3], 
                'telefono': result[4], 
                'username': result[5], 
                'password': result[6], 
                'rol': result[7]
            }
            payload.append(content)
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)})

#  crear un registro
@cross_origin()
@app.route('/add_contact', methods=['POST'])
def add_contact():
    try:
        if request.method == 'POST':
            nombre = request.json['nombre']
            identificacion = request.json['identificacion']
            correo = request.json['correo']
            telefono = request.json['telefono']
            username = request.json['username']
            password = request.json['password']
            rol = request.json['rol']
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO user (nombre, identificacion, correo, telefono, username, password, rol)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (nombre, identificacion, correo, telefono, username, password, rol))
            mysql.connection.commit()
            cur.close()
            return jsonify({"informacion": "Registro exitoso"})
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)})

# actualizar un registro
@app.route('/update/<int:id>', methods=['PUT'])
@cross_origin()
def update_contact(id):
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        identificacion = data.get('identificacion')
        correo = data.get('correo')
        telefono = data.get('telefono')
        username = data.get('username')
        password = data.get('password')
        rol = data.get('rol')

        # Validación básica de datos
        if not all([nombre, identificacion, correo, telefono, username, password, rol]):
            return jsonify({"informacion": "Todos los campos son requeridos"}), 400

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE user
            SET nombre = %s,
                identificacion = %s,
                correo = %s,
                telefono = %s,
                username = %s,
                password = %s,
                rol = %s
            WHERE id = %s
        """, (nombre, identificacion, correo, telefono, username, password, rol, id))
        mysql.connection.commit()
        cur.close()
        
        return jsonify({"informacion": "Usuario actualizado correctamente"})
    
    except Exception as e:
        print(e)
        return jsonify({"informacion": "Error al actualizar el usuario", "error": str(e)}), 500

# eliminar un registro
@cross_origin()
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_contact(id):
    try:
        print(f"Intentando eliminar usuario con ID: {id}")
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM user WHERE id = %s', (id,))
        mysql.connection.commit()
        cur.close()
        print(f"Usuario con ID {id} eliminado correctamente")
        return jsonify({"informacion": "Usuario eliminado correctamente"})
    except Exception as e:
        print(f"Error al eliminar usuario con ID {id}: {e}")
        return jsonify({"informacion": "Error al eliminar usuario", "error": str(e)}), 500

@cross_origin()
@app.route('/citas', methods=['POST'])
def citas():
    try:
        if request.method == 'POST':
            motivo = request.json.get('motivo')
            fecha_reserva = request.json.get('fecha')
            hora_reserva = request.json.get('hora')
            sede = request.json.get('sede')
            identificacion = request.json.get('identificacion')

            if not identificacion:
                return jsonify({"informacion": "Identificación no proporcionada"}), 400

            try:
                identificacion = int(identificacion)
            except ValueError:
                return jsonify({"informacion": "Identificación inválida"}), 400

            cur = mysql.connection.cursor()

            # Verificar valor de identificación
            print(f"Identificación recibida: {identificacion}")

            cur.execute("SELECT identificacion, Nombre_Completo, Correo, Genero FROM estudiante WHERE identificacion = %s", (identificacion,))
            estudiante = cur.fetchone()

            # Verificar resultado de la consulta
            print(f"Resultado de la consulta: {estudiante}")

            if not estudiante:
                cur.close()
                return jsonify({"informacion": "Estudiante no encontrado"}), 404

            id_estudiante, nombre, email, genero = estudiante

            cur.execute("""
                INSERT INTO citas (estudiante_id, motivo, fecha, hora, sede, Nombre_Completo, Correo, Genero)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (id_estudiante, motivo, fecha_reserva, hora_reserva, sede, nombre, email, genero))

            mysql.connection.commit()
            cur.close()

            return jsonify({"informacion": "Cita registrada exitosamente"})

    except Exception as e:
        print(e)
        return jsonify({"informacion": f"Error interno del servidor: {str(e)}"}), 500

@app.route('/citas_enfermeria', methods=['POST'])
def citas_enfermeria():
    try:
        if request.method == 'POST':
            motivo = request.json.get('motivo')
            fecha_reserva = request.json.get('fecha')
            hora_reserva = request.json.get('hora')
            sede = request.json.get('sede')
            identificacion = request.json.get('identificacion')

            # Verificación de datos recibidos
            print("Datos recibidos:", motivo, fecha_reserva, hora_reserva, sede, identificacion)

            if not identificacion:
                return jsonify({"informacion": "Identificación no proporcionada"}), 400

            cur = mysql.connection.cursor()  # Acceder al cursor de la conexión
            print("Conexión a la base de datos establecida.")

            # Ajustamos la consulta SQL para coincidir con la estructura de la tabla
            cur.execute("SELECT identificacion, Nombre_Completo, Correo, Genero FROM estudiante WHERE identificacion = %s", (identificacion,))
            estudiante = cur.fetchone()
            print("Datos del estudiante:", estudiante)

            if not estudiante:
                cur.close()
                return jsonify({"informacion": "Estudiante no encontrado"}), 404

            id_estudiante, nombre, email, genero = estudiante

            cur.execute("""
                INSERT INTO citas_enfermeria (estudiante_id, motivo, fecha, hora, sede, Nombre_Completo, Correo, Genero)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (id_estudiante, motivo, fecha_reserva, hora_reserva, sede, nombre, email, genero))

            mysql.connection.commit()  # Hacer commit en la conexión
            cur.close()
            print("Cita registrada exitosamente.")
            return jsonify({"informacion": "Cita registrada exitosamente"})

    except Exception as e:
        print("Error interno del servidor:", e)
        return jsonify({"informacion": f"Error interno del servidor: {str(e)}"}), 500



@app.route('/registrar_recomendacion_ef', methods=['POST'])
def registrar_recomendacion_ef():
    try:
        data = request.get_json()
        id_enfermero = data.get('id_enfermero')
        id_estudiante = data.get('id_estudiante')
        fecha_recomendacion = data.get('fecha_recomendacion')
        recomendacion = data.get('recomendacion')

        # Validar que todos los datos requeridos estén presentes
        if not all([id_enfermero, id_estudiante, fecha_recomendacion, recomendacion]):
            return jsonify({'message': 'Faltan datos requeridos'}), 400

        # Validar tipos de datos
        if not (isinstance(id_enfermero, int) and isinstance(id_estudiante, int)):
            return jsonify({'message': 'ID de enfermero y estudiante deben ser números enteros'}), 400

        cur = mysql.connection.cursor()

        # Verificar si el enfermero existe
        check_enfermero_sql = "SELECT COUNT(*) FROM enfermero WHERE identificacion = %s"
        cur.execute(check_enfermero_sql, (id_enfermero,))
        if cur.fetchone()[0] == 0:
            cur.close()
            return jsonify({'message': 'El enfermero especificado no existe en la base de datos'}), 400

        # Verificar si el estudiante existe
        check_estudiante_sql = "SELECT COUNT(*) FROM estudiante WHERE identificacion = %s"
        cur.execute(check_estudiante_sql, (id_estudiante,))
        if cur.fetchone()[0] == 0:
            cur.close()
            return jsonify({'message': 'El estudiante especificado no existe en la base de datos'}), 400

        # Insertar la recomendación
        insert_sql = """
        INSERT INTO recomendaciones_enfermeria (id_enfermero, id_estudiante, fecha_recomendacion, recomendacion)
        VALUES (%s, %s, %s, %s)
        """
        values = (id_enfermero, id_estudiante, fecha_recomendacion, recomendacion)
        cur.execute(insert_sql, values)
        mysql.connection.commit()
        cur.close()
        
        return jsonify({'message': 'Recomendación registrada exitosamente'})
    except IntegrityError as e:
        mysql.connection.rollback()
        return jsonify({'message': f'Error de integridad de datos: {str(e)}'}), 400
    except Exception as err:
        mysql.connection.rollback()
        return jsonify({'message': f'Error inesperado: {str(err)}'}), 500
    

@app.route('/registrar_recomendacion_ps', methods=['POST'])
def registrar_recomendacion_ps():
    try:
        data = request.get_json()
        id_psicologo = data.get('id_psicologo')
        id_estudiante = data.get('id_estudiante')
        fecha_recomendacion = data.get('fecha_recomendacion')
        recomendacion = data.get('recomendacion')

        # Validar que todos los datos requeridos estén presentes
        if not all([id_psicologo, id_estudiante, fecha_recomendacion, recomendacion]):
            return jsonify({'message': 'Faltan datos requeridos'}), 400

        # Validar tipos de datos
        if not (isinstance(id_psicologo, int) and isinstance(id_estudiante, int)):
            return jsonify({'message': 'ID de psicólogo y estudiante deben ser números enteros'}), 400

        print(f"Datos recibidos - Psicólogo: {id_psicologo}, Estudiante: {id_estudiante}")

        cur = mysql.connection.cursor()

        # Verificar si el psicólogo existe
        check_psicologo_sql = "SELECT COUNT(*) FROM psicologo WHERE identificacion = %s"
        cur.execute(check_psicologo_sql, (id_psicologo,))
        psicologo_count = cur.fetchone()[0]
        print(f"Resultados de búsqueda de psicólogo: {psicologo_count}")
        if psicologo_count == 0:
            cur.close()
            return jsonify({'message': 'El psicólogo especificado no existe en la base de datos'}), 400

        # Verificar si el estudiante existe
        check_estudiante_sql = "SELECT COUNT(*) FROM estudiante WHERE identificacion = %s"
        cur.execute(check_estudiante_sql, (id_estudiante,))
        estudiante_count = cur.fetchone()[0]
        print(f"Resultados de búsqueda de estudiante: {estudiante_count}")
        if estudiante_count == 0:
            cur.close()
            return jsonify({'message': 'El estudiante especificado no existe en la base de datos'}), 400

        # Insertar la recomendación
        insert_sql = """
        INSERT INTO recomendaciones_psicologia (id_psicologo, id_estudiante, fecha_recomendacion, recomendacion)
        VALUES (%s, %s, %s, %s)
        """
        values = (id_psicologo, id_estudiante, fecha_recomendacion, recomendacion)
        cur.execute(insert_sql, values)
        mysql.connection.commit()
        cur.close()
        
        return jsonify({'message': 'Recomendación registrada exitosamente'})
    except IntegrityError as e:
        mysql.connection.rollback()
        return jsonify({'message': f'Error de integridad de datos: {str(e)}'}), 400
    except Exception as err:
        mysql.connection.rollback()
        return jsonify({'message': f'Error inesperado: {str(err)}'}), 500


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Nombre de usuario y contraseña son requeridos'}), 400
        
        cur = mysql.connection.cursor()
        query = 'SELECT * FROM usuarios WHERE username = %s AND password = %s'
        cur.execute(query, (username, password))
        user = cur.fetchone()
        cur.close()
        
        if user:
            # Guardar el nombre de usuario y el rol en la sesión
            session['username'] = user[1]
            session['role'] = user[3]
            return jsonify({
                'success': True,
                'username': user[1],
                'role': user[3]
            })
        else:
            return jsonify({'success': False, 'message': 'Usuario o contraseña incorrectos'}), 401

    except Exception as e:
        print(f'Error en /login: {e}')
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/admin')
def admin():
    return render_template('html/admin.html')

@app.route('/bienestar')
def bienestar():
    return render_template('html/bienestar.html')

@app.route('/enfermeria')
def enfermeria():
    # Verificar si el usuario está autenticado y tiene el rol 
    if 'role' in session and session['role'] == 'enfermera':
        return render_template('html/enfermeria.html')
    else:
        return redirect('/')  # Redirige a la página de inicio si no está autenticado o no tiene el rol 

@app.route('/estudiante')
def estudiantes():
    return render_template('html/estudiantes.html')

@app.route('/formed')
def formed():
    return render_template('html/FORMED.html')

@app.route('/formpsi')
def formpsi():
    return render_template('html/formpsi.html')

@app.route('/graficos')
def graficos():
    return render_template('html/Graficos.html')

@app.route('/psicologos')
def psicologos():
    return render_template('html/psicologos.html')


# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)
