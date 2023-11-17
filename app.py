from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QLineEdit, QTextBrowser
from clases.Patrones import Patrones
# iniciar app

app = QApplication([])

p = Patrones()

# cargar archivos
IDE = uic.loadUi("./vistas/ide.ui")
tablero = IDE.plainTextEdit
tablero.textChanged.connect(lambda: abrir_ide(tablero.toPlainText()))


resultados = []


def abrir_ide(tt):
    codigo = tablero.toPlainText()
    lineas = codigo.split(";")
    p.leer_lineas(lineas)


def ejecutar():
    codigo = tablero.toPlainText()
    lineas = codigo.split(";")
    p.leer_lineas(lineas, True)
    # print(lineas)


# boton
IDE.pushButton.clicked.connect(ejecutar)

# Ejecutable
IDE.show()
app.exec()
