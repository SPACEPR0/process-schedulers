#Clase básica de un proceso
class Proceso:
    #Se construye a partir de un id y los periodos de CPU que necesita
    def __init__(self, Id, tiempo_llegada, cpu_burst):
        self.__id = Id
        self.__tiempo_llegada = tiempo_llegada
        self.__cpu_burst = cpu_burst
        self.__tiempo_espera = 0

    # Este método suma una unidad al tiempo de espera del proceso
    def actualizar_tiempo_espera(self):
        self.__tiempo_espera += 1

    # Este método resta una unidad a los periodos de cpu del proceso
    def actualizar_cpu_burst(self):
        self.__cpu_burst -= 1

    # Este método regresa los periodos restantes del proceso
    def obtener_cpu_burst(self):
        return self.__cpu_burst

    # Este método regresa el tiempo de espera del proceso
    def obtener_tiempo_espera(self):
        return self.__tiempo_espera

    # Este método regresa el Id del proceso
    def obtener_id(self):
        return self.__id

    # Este método regresa el tiempo de llegada del proceso
    def obtener_tiempo_llegada(self):
        return self.__tiempo_llegada

    # La Comparación de procesos se realiza por su tiempo restante
    def __lt__(self, otro):
        return self.__cpu_burst < otro.obtener_cpu_burst()

#-----------------------------------------------------------------------------
