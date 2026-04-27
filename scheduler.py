def fcfs(procesos):
    # Ordenar por tiempo de llegada
    procesos.sort(key=lambda p: p.llegada)

    tiempo_actual = 0

    for p in procesos:
        # Si el CPU está libre, avanzar el tiempo
        if tiempo_actual < p.llegada:
            tiempo_actual = p.llegada

        p.inicio = tiempo_actual
        p.fin = tiempo_actual + p.duracion

        tiempo_actual = p.fin

    return procesos
def spn(procesos):
    tiempo_actual = 0
    completados = []
    pendientes = procesos[:]

    while pendientes:
        # Procesos que ya llegaron
        disponibles = [p for p in pendientes if p.llegada <= tiempo_actual]

        if not disponibles:
            tiempo_actual += 1
            continue

        # Elegir el de menor duración
        proceso = min(disponibles, key=lambda p: p.duracion)
        pendientes.remove(proceso)

        proceso.inicio = tiempo_actual
        proceso.fin = tiempo_actual + proceso.duracion

        tiempo_actual = proceso.fin
        completados.append(proceso)

    return completados