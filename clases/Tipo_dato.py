class Entero:
    def captura(self):
        while True:
            valor = input("Ingrese un valor de tipo Entero: ")
            try:
                valor = int(valor)
                return valor
            except ValueError:
                print("El valor ingresado no es un Entero válido. Inténtelo de nuevo.")


class Real:
    def captura(self):
        while True:
            valor = input("Ingrese un valor de tipo Real: ")
            try:
                valor = float(valor)
                return valor
            except ValueError:
                print("El valor ingresado no es un Real válido. Inténtelo de nuevo.")


def capturar_valor(capturar):

    r = capturar.captura()

    return r
