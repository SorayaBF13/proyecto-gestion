import sys

from PySide6.QtGui import QPixmap, Qt

from databaseClientes import crear_tabla_clientes, registrar_cliente, obtener_clientes

from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QApplication, QLineEdit, QPushButton, \
    QTableWidgetItem, QTableWidget, QMessageBox


# CLASE
class VentanaClientes(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
                    QMainWindow {
                        background-image: url('images/bgwhite.jpg');
                        background-repeat: no-repeat;
                        background-position: center;
                        background-size: 100%, 100%;
                        
                    }
                """)

        crear_tabla_clientes()

        # VENTANA
        self.setWindowTitle("Gestión de Clientes")
        self.setGeometry(700, 300, 400, 500)

        # WIDGET
        self.widget = QWidget()


        # LAYOUT
        self.layout = QVBoxLayout()
        self.layout.setSpacing(9)  # Ajusta el espaciado entre widgets

        # WIDGETS DE LA INTERFAZ

            # IMAGEN LOGIN
        self.imagenRegistro = QLabel(self)
        self.imagenRegistro.setPixmap(QPixmap("src/images/registro.png"))
        self.imagenRegistro.setScaledContents(True)
        self.imagenRegistro.setFixedSize(250, 100)  # Define un tamaño fijo para la imagen
        self.layout.addWidget(self.imagenRegistro, alignment=Qt.AlignCenter)

            # CAMPOS DE ENTRADA
        self.nombre = QLineEdit(self)
        self.layout.addWidget(self.nombre)
        self.nombre.setPlaceholderText("Introduzca nombre cliente")

        self.apellido = QLineEdit(self)
        self.layout.addWidget(self.apellido)
        self.apellido.setPlaceholderText("Introduzca apellido cliente")

        self.telefono = QLineEdit(self)
        self.layout.addWidget(self.telefono)
        self.telefono.setPlaceholderText("Introduzca teléfono cliente")

        self.correo = QLineEdit(self)
        self.layout.addWidget(self.correo)
        self.correo.setPlaceholderText("Introduzca correo cliente")

        self.direccion = QLineEdit(self)
        self.layout.addWidget(self.direccion)
        self.direccion.setPlaceholderText("Introduzca dirección cliente")



            # BOTÓN INSERTAR CLIENTE
        self.button_guardar = QPushButton("Guardar Cliente")
        self.button_guardar.setStyleSheet("""
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
        self.button_guardar.clicked.connect(self.registrar_cliente)
        self.layout.addWidget(self.button_guardar)

            # BOTÓN LIMPIAR
        self.button_limpiar = QPushButton("Limpiar campos")
        self.button_limpiar.setStyleSheet("""
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
        self.button_limpiar.clicked.connect(self.limpiar_campos)
        self.layout.addWidget(self.button_limpiar)

            # BOTÓN VER CLIENTES
        self.button_clientes = QPushButton("Ver clientes")
        self.button_clientes.setStyleSheet("""
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
        self.button_clientes.clicked.connect(self.cargar_clientes)
        self.layout.addWidget(self.button_clientes)

        # Crear la tabla para mostrar los datos de los clientes
        self.table_widget = QTableWidget(self)
        self.layout.addWidget(self.table_widget)


        # UNIÓN WIDGET Y LAYOUT
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def registrar_cliente(self):
        # Obtener los valores de los campos
        nombre = self.nombre.text()
        apellido = self.apellido.text()
        telefono = self.telefono.text()
        correo = self.correo.text()
        direccion = self.direccion.text()

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

        # Verificar si los campos no están vacíos
        if nombre and apellido and telefono and correo and direccion:
            # Registrar el cliente en la base de datos
            if registrar_cliente(nombre, apellido, telefono, correo, direccion):
                msg.setWindowTitle("Éxito")
                msg.setText("Usuario registrado correctamente")
                msg.setIcon(QMessageBox.Information)

        else:
            msg.setWindowTitle("Error")
            msg.setText("Rellene todos los campos")
            msg.setIcon(QMessageBox.Critical)


        # Aplica el estilo al QMessageBox
        msg.setStyleSheet(estilo_qmessagebox)

    # Mostrar el mensaje
        msg.exec()

    def limpiar_campos(self):
        self.nombre.setText("")
        self.apellido.setText("")
        self.telefono.setText("")
        self.correo.setText("")
        self.direccion.setText("")

    def cargar_clientes(self):
        # Obtener los clientes desde la base de datos
        clientes = obtener_clientes()

        # Limpiar la tabla antes de llenarla
        self.table_widget.setRowCount(0)

        # Configurar el número de columnas (5 campos)
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(['ID', 'Nombre', 'Apellido', 'Teléfono', 'Correo'])

        # Llenar la tabla con los datos obtenidos
        for row, cliente in enumerate(clientes):
            self.table_widget.insertRow(row)
            for col, data in enumerate(cliente):
                self.table_widget.setItem(row, col, QTableWidgetItem(str(data)))

        # Ajustar el tamaño de las columnas
        self.table_widget.resizeColumnsToContents()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VentanaClientes()
    window.show()
    sys.exit(app.exec())