def calcular_metricas(procesos):
    resultados = []
    total_espera = 0
    total_retorno = 0

    for p in procesos:
        espera = p.inicio - p.llegada
        retorno = p.fin - p.llegada

        total_espera += espera
        total_retorno += retorno

        resultados.append({
            "nombre": p.nombre,
            "llegada": p.llegada,
            "duracion": p.duracion,
            "inicio": p.inicio,
            "fin": p.fin,
            "espera": espera,
            "retorno": retorno
        })

    promedio_espera = total_espera / len(procesos)
    promedio_retorno = total_retorno / len(procesos)

    return resultados, promedio_espera, promedio_retorno