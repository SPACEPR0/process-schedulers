import sys
import heapq
from proceso import Proceso

# Se lee la info de los procesos del archivo de texto
procesos = [p.strip().split(',') for p in open(sys.argv[1],'r').readlines()]

# Se construye cada proceso y se ordenan respecto a tiempo de llegada
procesos = [Proceso(p[0], int(p[1]), int(p[2])) for p in procesos]
procesos.sort(key = lambda p: p.obtener_tiempo_llegada())

# Esta variable representa el tiempo
t = 0

# Esta variable representa la cola de listos
cola_listos = []

# Esta variable representa la cola de terminados
terminados = []

# Hasta que la cola quede vacía y ya no haya procesos
while procesos or cola_listos:
    # Obtener todos los que llegan al proceso en dicho tiempo
    while (procesos and t == procesos[0].obtener_tiempo_llegada()):
        heapq.heappush(cola_listos, procesos.pop(0))

    if cola_listos:
        # El proceso actual siempre será el que tenga menor tiempo restante
        proceso_actual = cola_listos[0]

        # Actualiza periodos
        proceso_actual.actualizar_cpu_burst()

        # Procesos que no se están ejecutando
        for p in cola_listos[1:]:
            p.actualizar_tiempo_espera()

        t += 1

        if proceso_actual.obtener_cpu_burst() == 0:
            print("Proceso:", proceso_actual.obtener_id(), end=" ")
            print("terminó en el tiempo:", t, end=" ")
            print("Con tiempo de espera de:", proceso_actual.obtener_tiempo_espera())
            print("---------------------------------------------------")
            # Se saca de la cola de procesos
            terminados.append(heapq.heappop(cola_listos))
    else:
        t += 1
