import sqlite3


# CONECTAR LA BASE DE DATOS
def conectar():
    return sqlite3.connect("proyecto.db")


# CREAR TABLA USUARIOS
def crear_tabla_usuarios():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            correo TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            genero TEXT NOT NULL
        )
    ''')

    conexion.commit()
    conexion.close()


# REGISTRAR UN USUARIO
def registrar_usuario(correo, password, genero):
    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute("INSERT INTO usuarios (correo, password, genero) VALUES (?, ?, ?)",
                       (correo, password, genero))
        conexion.commit()
        conexion.close()
        return True  # Usuario registrado con éxito
    except sqlite3.IntegrityError:
        return False  # Usuario ya registrado


# VERIFICAR LOGIN DE USUARIO
def verificar_usuario(correo, password):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE correo = ? AND password = ?", (correo, password))
    usuario = cursor.fetchone()
    conexion.close()

    return usuario is not None  # Devuelve True si existe, False si no existe

