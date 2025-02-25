import pytest
from PySide6.QtWidgets import QApplication
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sqlite3

from proyecto import Proyecto


@pytest.fixture(scope='session')  # Instancia para todos los métodos
def app_instance():
    app = QApplication([])  # Creamos una instancia de QApplication
    yield app  # Proporciona la aplicación para todos los tests
    app.quit()  # Cierra la app después de todos los tests


@pytest.fixture()
def window(app_instance): # Crea una instancia de la ventana para cada test
    window = Proyecto()
    window.show()
    return window


@pytest.fixture
def db_connection(): # Crea una conexión a la base de datos antes del test y la cierra después
    conn = sqlite3.connect("proyecto.db")
    yield conn  # Proporciona la conexión a los tests
    conn.close()


def contar_usuarios(conn): # Cuenta cuántos usuarios hay en la tabla
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    return cursor.fetchone()[0]


def test_registrar(window, db_connection):
    conn = db_connection  # Hago la conexión a la base de datos

    # Cuento los usuarios antes de registrar
    usuarios_antes = contar_usuarios(conn)

    # Creo el usuario nuevo
    window.textoCorreo.setText('nuevo_usuario@example.com')
    window.textoPass.setText('password123')
    window.sexoHombre.setChecked(True)

    # Ejecutar el registro del usuario
    window.registrar()

    # Cuento los usuarios después de registrar al nuevo usuario
    usuarios_despues = contar_usuarios(conn)

    # Verifico que el número de usuarios aumentó en 1
    assert usuarios_despues == usuarios_antes + 1, "El usuario no se registró correctamente"