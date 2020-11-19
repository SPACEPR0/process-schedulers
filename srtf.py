import sys
from collections import deque

#Clase básica de un proceso
class Proceso:
    #Se construye a partir de un id y los periodos de CPU que necesita
    def __init__(self, id, periodos, tiempo_llegada):
        self.__id = id
        self.__periodos = periodos
        self.__tiempo_espera = 0
        self.__tiempo_llegada = 0

    # Este método suma una unidad al tiempo de espera del proceso
    def actualizar_tiempo_espera(self):
        self.__tiempo_espera += 1

    # Este método resta una unidad a los periodos de cpu del proceso
    def actualizar_periodos(self):
        self.__periodos -= 1

    # Este método regresa el tiempo de llegada del proceso
    def obtener_tiempo_llegada(self):
        return self.__tiempo_llegada

    # Este método regresa los periodos restantes del proceso
    def obtener_periodos_restantes(self):
        return self.__periodos

    # Este método regresa el tiempo de espera del proceso
    def obtener_tiempo_espera(self):
        return self.__tiempo_espera

    # Este método regresa el Id del proceso
    def obtener_id(self):
        return self.__id

    # La comparación de procesos se realiza por su tiempo restante
    def __lt__(self, otro):
        return self.__periodos < otro.obtener_periodos_restantes()

    def __le__(self, otro):
        return self.__periodos <= otro.obtener_periodos_restantes()

 #Se lee la info de los procesos del archivo de texto
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

        # actualiza periodos
        proceso_actual.actualizar_periodos()

        # Procesos que no se están ejecutando
        for p in cola_listos[1:]:
            p.actualizar_tiempo_espera()

        t += 1

        if proceso_actual.obtener_periodos_restantes() == 0:
            print("Proceso:", proceso_actual.obtener_id(), end=" ")
            print("terminó en el tiempo:", t, end=" ")
            print("Con tiempo de espera de:", proceso_actual.obtener_tiempo_espera())
            print("---------------------------------------------------")
            # Se saca de la cola de procesos
            terminados.append(heapq.heappop(cola_listos))
    else:
        t += 1
