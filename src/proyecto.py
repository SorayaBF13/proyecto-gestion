import sys
import sqlite3
from database import crear_tabla_usuarios, registrar_usuario, verificar_usuario
from clientes import VentanaClientes
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QCheckBox, \
    QMessageBox, QApplication


# CLASE
class Proyecto (QMainWindow):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QMainWindow {
                background-image: url('images/bgwhite.jpg');
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            }
        """)

        crear_tabla_usuarios()

        # VENTANA
        self.setWindowTitle("Proyecto")
        self.setGeometry(700, 300, 400, 500)

        # WIDGET
        self.widget = QWidget()

        # LAYOUT
        self.layout = QVBoxLayout()
        self.layout.setSpacing(9)  # Ajusta el espaciado entre widgets

        # WIDGETS DE LA INTERFAZ

            # IMAGEN LOGIN
        self.imagenLogin = QLabel(self)
        self.imagenLogin.setPixmap(QPixmap("src/images/login.png"))
        self.imagenLogin.setScaledContents(True)
        self.imagenLogin.setFixedSize(200, 250)  # Define un tamaño fijo para la imagen
        self.layout.addWidget(self.imagenLogin, alignment=Qt.AlignCenter)

            # CORREO
        self.textoCorreo = QLineEdit(self)
        self.layout.addWidget(self.textoCorreo)
        self.textoCorreo.setPlaceholderText("Introduzca su correo")

            # PASS
        self.textoPass = QLineEdit(self)
        self.layout.addWidget(self.textoPass)
        self.textoPass.setPlaceholderText("Introduzca su contraseña")
        self.textoPass.setEchoMode(QLineEdit.Password)

            # BOTÓN LOGIN
        self.buttonIniciar = QPushButton("Iniciar Sesión")
        self.buttonIniciar.setStyleSheet("""
                QPushButton {
                        background-color: #03a6e7;
                        color: white;
                        border-radius: 5px;
                        padding: 5px;
                            }
                QPushButton:hover {
                        background-color: #5E81AC;
                            }
        """
                                         )
        self.layout.addWidget(self.buttonIniciar)
        self.buttonIniciar.clicked.connect(self.saludo)


            # BOTÓN REGISTRARSE
        self.buttonRegistro = QPushButton("Registrarse")
        self.buttonRegistro.setStyleSheet("""
            QPushButton {
                background-color: #03a6e7;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #5E81AC;
            }
        """)
        self.layout.addWidget(self.buttonRegistro)
        self.buttonRegistro.clicked.connect(self.registrar)

            # BOTÓN LIMPIAR
        self.buttonLimpiar = QPushButton("Reiniciar")
        self.buttonLimpiar.setStyleSheet("""
                QPushButton {
                        background-color: #03a6e7;
                        color: white;
                        border-radius: 5px;
                        padding: 5px;
                        }
                QPushButton:hover {
                        background-color: #5E81AC;
                        }
                """)

        self.layout.addWidget(self.buttonLimpiar)
        self.buttonLimpiar.clicked.connect(self.reset)

            # LAYOUT PARA CHECKBOX
        layout_checkbox = QHBoxLayout()

            # TEXTO SEXO:
        self.textoSexo = QLabel("Seleccione género:",self)
        self.textoSexo.setStyleSheet("""
                QLabel {                    
                        color: #5E81AC; 
                        font-size: 13px;
                        font-family: "Arial"; 
                        font-weight: bold; 
                        }                                            
                """)

        layout_checkbox.addWidget(self.textoSexo)


            # CHECKSBOX
        self.sexoMujer = QCheckBox("Mujer", self)
        self.sexoMujer.setStyleSheet("""
                        QCheckBox {                    
                                color: #5E81AC; 
                                font-size: 13px;
                                font-family: "Arial"; 
                                font-weight: bold; 
                                }                                            
                        """)
        layout_checkbox.addWidget(self.sexoMujer)

        self.sexoHombre = QCheckBox("Hombre", self)
        self.sexoHombre.setStyleSheet("""
                        QCheckBox {                    
                                color: #5E81AC; 
                                font-size: 13px;
                                font-family: "Arial"; 
                                font-weight: bold; 
                                }                                            
                        """)
        layout_checkbox.addWidget(self.sexoHombre)

            # Unión del HLayout al principal
        self.layout.addLayout(layout_checkbox)

        # UNIÓN WIDGET Y LAYOUT
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def saludo(self):
        correo = self.textoCorreo.text().strip()
        password = self.textoPass.text().strip()

        msg = QMessageBox(self)

        # Estilos generales para el QMessageBox
        estilo_qmessagebox = """
        QMessageBox {
            background-image: url('images/bgwhite.jpg');
            background-repeat: no-repeat;
            background-position: center;
            background-size: cover;
        }
        QLabel {
            color: #5E81AC; /* Color del texto */
            font-size: 14px;
            font-family: "Arial"; /* Tipo de letra */
            font-weight: bold; /* Negrita */
        }
        QPushButton {
            background-color: #03a6e7;
            color: 5E81AC;
            border-radius: 5px;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #5E81AC;
        }
        """

        # Validación: Verificar si los campos están vacíos
        if not correo or not password:
            msg.setWindowTitle("Error")
            msg.setText("Faltan datos")
            msg.setIcon(QMessageBox.Critical)
        else:
            # Verificar usuario en la base de datos
            if verificar_usuario(correo, password):
                msg.setWindowTitle("Bienvenida")
                msg.setText(f"Bienvenido {correo}" if self.sexoHombre.isChecked() else f"Bienvenida {correo}")
                self.open_clientes_window()

            else:
                msg.setWindowTitle("Error")
                msg.setText("Usuario o contraseña incorrectos")
                msg.setIcon(QMessageBox.Critical)

        # Aplica el estilo al QMessageBox
        msg.setStyleSheet(estilo_qmessagebox)

        # Muestra el QMessageBox
        msg.exec()

    def reset(self):
        self.textoCorreo.setText("")
        self.textoPass.setText("")

    def open_clientes_window(self):
        # Cierra la ventana de login
        self.close()

        # Abre la ventana de gestión de clientes
        self.ventana_clientes = VentanaClientes()
        self.ventana_clientes.show()

    def registrar(self):
        correo = self.textoCorreo.text().strip()
        password = self.textoPass.text().strip()
        genero = "Hombre" if self.sexoHombre.isChecked() else "Mujer"

        msg = QMessageBox(self)


        if not correo or not password:
            msg.setWindowTitle("Error")
            msg.setText("Faltan datos para registrarse")
            msg.setIcon(QMessageBox.Critical)
        else:
            if registrar_usuario(correo, password, genero):
                msg.setWindowTitle("Éxito")
                msg.setText("Usuario registrado correctamente")

            else:
                msg.setWindowTitle("Error")
                msg.setText("El correo ya está registrado")
                msg.setIcon(QMessageBox.Critical)

        msg.exec()


# EJECUCIÓN
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Proyecto()
    window.show()
    sys.exit(app.exec())