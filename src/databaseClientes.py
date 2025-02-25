import sqlite3

# CONECTAR A LA BASE DE DATOS
def conectar():
    return sqlite3.connect("proyecto.db")


# CREAR TABLA CLIENTES
def crear_tabla_clientes():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            telefono TEXT NOT NULL,
            correo TEXT NOT NULL,
            direccion TEXT NOT NULL
        )
    ''')

    conexion.commit()
    conexion.close()


# REGISTRAR UN CLIENTE
def registrar_cliente(nombre, apellido, telefono, correo, direccion):
    # Verificar que ningún campo esté vacío
    if not nombre.strip() or not apellido.strip() or not telefono.strip() or not correo.strip() or not direccion.strip():
        return False  # Devuelve False si algún campo está vacío

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute("INSERT INTO clientes (nombre, apellido, telefono, correo, direccion) VALUES (?, ?, ?, ?, ?)",
                       (nombre, apellido, telefono, correo, direccion))
        conexion.commit()
        return True  # Devuelve True si el registro está bien
    except sqlite3.IntegrityError:
        return False  # Devuelve False si hay un error de integridad, como duplicados
    finally:
        conexion.close()


# OBTENER CLIENTES
def obtener_clientes():
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM clientes")  # SQL para obtener todos los clientes
            clientes = cursor.fetchall()  # Obtener todos los resultados
            conexion.close()
            return clientes
        except sqlite3.IntegrityError as e:
            print(f"Error al obtener clientes: {e}")
            conexion.close()
            return []


