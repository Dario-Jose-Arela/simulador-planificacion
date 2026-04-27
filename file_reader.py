import csv
from process import Proceso

def leer_procesos(ruta):
    procesos = []

    try:
        with open(ruta, newline='') as archivo:
            lector = csv.reader(archivo)
            next(lector)  # saltar encabezado

            for fila in lector:
                if len(fila) != 3:
                    print("Fila inválida:", fila)
                    continue

                nombre, llegada, duracion = fila
                procesos.append(Proceso(nombre, llegada, duracion))

    except FileNotFoundError:
        print("Error: archivo no encontrado")

    return procesos