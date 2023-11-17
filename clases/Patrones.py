from PyQt6 import uic, QtWidgets
import re
from clases.Mensaje import Mensaje


# iniciar aplicacion
app = QtWidgets.QApplication([])


resultados = []


class Patrones:
    def __init__(self):
        self.variables = {}
        self.fracciones = []
        self.patron_declaracion = r'^\s*([a-zA-Z_]\w*)\s*$'
        self.patron_texto = r'"[^"]*"'
        self.patron_entero = r'(?<![\d.])[-+]?\b\d+\b(?![\d.])'
        self.patron_real = r'\b\d+\.\d+\b'

        self.ventana_captura = uic.loadUi("./vistas/capturar.ui")

        self.variables_texto = {}
        self.variables_entero = {}
        self.variables_real = {}
        self.error = 0

    def abrir_ventana(self, mensaje):
        self.ventana_captura.show()
        self.ventana_captura.label_mensaje.setText(
            mensaje)
        self.ventana_captura.btn_aceptar.clicked.connect(
            lambda: self.ventana_captura.hide())

    def ft(self, nombre_variable, tipo_variable):

        self.ventana_captura.hide()
        valor = self.ventana_captura.txt_captura.toPlainText()

        if tipo_variable == 'texto':
            self.variables_texto[nombre_variable] = valor

            print(self.variables_texto)
        self.ventana_captura.txt_captura.setPlainText('')

    def set_variables_texto(self, valor):
        self.variables_texto = valor

    def es_declaracion_valida(self, declaracion):
        return bool(self.expresion_regular.match(declaracion))

    # Función para verificar si una cadena tiene varias palabras
    def leer_lineas(self, lineas,  ejecutar=False):

        for linea in lineas:

            partes = linea.split()

            if len(partes) == 1 and ejecutar:

                patron_mensaje = r"Mensaje\.Texto\((\"[^\"]*\")\)"
                # Patrón para capturar el nombre en la expresión
                patron_mensaje_sin_comillas = r'Mensaje\.Texto\((\w+)\)'
                mensaje = re.findall(patron_mensaje, linea)

                if len(mensaje) > 0:

                    self.abrir_ventana(Mensaje.Texto(mensaje[0]))
                else:
                    # Buscar la expresión y capturar el nombre
                    match = re.search(patron_mensaje_sin_comillas, linea)
                    # print(match)
                    if match:
                        self.eliminar_error()
                        nombre_variable = match.group(1)
                        if nombre_variable in self.variables_texto:
                            self.eliminar_error()
                            self.abrir_ventana(
                                str(self.variables_texto[nombre_variable]))
                        elif nombre_variable in self.variables_entero:
                            self.eliminar_error()
                            self.abrir_ventana(
                                str(self.variables_entero[nombre_variable]))

                        elif nombre_variable in self.variables_real:
                            self.eliminar_error()
                            self.abrir_ventana(
                                str(self.variables_real[nombre_variable]))
                        else:
                            self.crear_error()
                    else:
                        self.crear_error()

            # declarar variables
            if len(partes) > 1:
                nombre = partes[0]
                tipo = partes[1]
                if tipo == "Texto":
                    es_correcta = bool(self.expresion_regular(
                        self.patron_declaracion).match(nombre.strip()))

                    if (not es_correcta):
                        self.crear_error()
                    else:

                        self.variables_texto[nombre] = None

                    # asignar valores texto
                    if len(self.variables_texto) > 0:
                        self.variables_texto[nombre] = None
                elif tipo == "Entero":
                    es_correcta = bool(self.expresion_regular(
                        self.patron_declaracion).match(nombre.strip()))
                    if (not es_correcta):
                        self.crear_error()
                    else:
                        self.variables_entero[nombre] = None

                    # asignar valores entero
                    if len(self.variables_entero) > 0:
                        self.variables_entero[nombre] = None

                elif tipo == "Real":
                    es_correcta = bool(self.expresion_regular(
                        self.patron_declaracion).match(nombre.strip()))
                    if (not es_correcta):
                        self.crear_error()

                    else:
                        self.variables_real[nombre] = None

                    # asignar valores entero
                    if len(self.variables_real) > 0:
                        self.variables_real[nombre] = None
                elif tipo == '=':

                    try:

                        if nombre in self.variables_texto:
                            valor_variable = ''
                            if len(partes) > 3:
                                for i, despues_espacio in enumerate(partes):
                                    if i > 1:
                                        valor_variable = valor_variable+despues_espacio+' '
                            else:
                                valor_variable = partes[2]
                            coincidencias = re.findall(
                                self.patron_texto, valor_variable.strip())
                            valor_texto = ''
                            # print(coincidencias)
                            for texto in coincidencias:
                                valor_texto = texto
                                # print(texto)

                            if len(valor_texto) > 0:
                                self.variables_texto[nombre] = valor_texto.strip(
                                    '"')

                            p = r"Captura.Texto"
                            leer = re.findall(p, partes[2])
                            if len(leer) > 0 and ejecutar:

                                self.abrir_ventana(nombre, 'texto')
                        elif nombre in self.variables_entero:

                            coincidencias = re.findall(
                                self.patron_entero, partes[2].strip())
                            numero_entero = ''
                            for numero in coincidencias:
                                numero_entero = numero_entero+numero
                            numero_entero = int(numero_entero)

                            if numero_entero <= 0 or numero_entero > 0:
                                self.variables_entero[nombre] = partes[2]
                            p = r"Captura.Entero"
                            leer = re.findall(p, partes[2])
                            if len(leer) > 0 and ejecutar:

                                self.abrir_ventana(nombre, 'texto')
                        elif nombre in self.variables_real:

                            coincidencias = re.findall(
                                self.patron_real, partes[2].strip())
                            print(coincidencias)
                            numero_real = ''
                            for numero in coincidencias:
                                numero_real = numero_real+numero
                            numero_real = float(numero_real)

                            if numero_real <= 0 or numero_real > 0:
                                self.variables_real[nombre] = numero_real
                            p = r"Captura.Real"
                            leer = re.findall(p, partes[2])
                            if len(leer) > 0 and ejecutar:

                                self.abrir_ventana(nombre, 'texto')

                    except Exception as e:

                        f'Error: {e}'
                else:
                    self.crear_error()
            elif linea.strip():
                resultados.append('Error de sintaxis: ' + linea)

    def expresion_regular(self, patron):
        return re.compile(patron)

    def crear_error(self):
        self.error = self.error + 1

    def eliminar_error(self):
        self.error = self.error - 1
