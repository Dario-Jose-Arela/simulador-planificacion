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
def srt(procesos):
    tiempo_actual = 0
    completados = 0
    n = len(procesos)

    timeline = []

    while completados < n:
        disponibles = [p for p in procesos if p.llegada <= tiempo_actual and p.restante > 0]

        if not disponibles:
            timeline.append("idle")
            tiempo_actual += 1
            continue

        # Elegir el de menor tiempo restante
        proceso = min(disponibles, key=lambda p: p.restante)

        # Si es la primera vez que entra
        if proceso.restante == proceso.duracion:
            proceso.inicio = tiempo_actual

        proceso.restante -= 1
        timeline.append(proceso.nombre)

        tiempo_actual += 1

        if proceso.restante == 0:
            proceso.fin = tiempo_actual
            completados += 1

    return procesos, timeline
def rr(procesos, quantum=2):
    tiempo_actual = 0
    cola = []
    timeline = []
    procesos = sorted(procesos, key=lambda p: p.llegada)

    i = 0
    n = len(procesos)

    while cola or i < n:
        # Agregar procesos que llegaron
        while i < n and procesos[i].llegada <= tiempo_actual:
            cola.append(procesos[i])
            i += 1

        if not cola:
            timeline.append("idle")
            tiempo_actual += 1
            continue

        proceso = cola.pop(0)

        if proceso.restante == proceso.duracion:
            proceso.inicio = tiempo_actual

        tiempo_ejecucion = min(quantum, proceso.restante)

        for _ in range(tiempo_ejecucion):
            proceso.restante -= 1
            timeline.append(proceso.nombre)
            tiempo_actual += 1

            # Llegan nuevos procesos
            while i < n and procesos[i].llegada <= tiempo_actual:
                cola.append(procesos[i])
                i += 1

        if proceso.restante > 0:
            cola.append(proceso)
        else:
            proceso.fin = tiempo_actual

    return procesos, timeline