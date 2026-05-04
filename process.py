class Proceso:
    def __init__(self, nombre, llegada, duracion):
        self.nombre = nombre
        self.llegada = int(llegada)
        self.duracion = int(duracion)
        self.restante = self.duracion

        # Se calcularán después
        self.inicio = 0
        self.fin = 0

    def __str__(self):
        return f"{self.nombre} (Llegada: {self.llegada}, Duración: {self.duracion})"