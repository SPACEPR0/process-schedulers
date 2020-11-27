#Clase básica de un proceso
class Proceso:
    #Se construye a partir de un id y los periodos de CPU que necesita
    def __init__(self, Id, tiempo_llegada, cpu_burst):
        self.__id = Id
        self.__cpu_burst = cpu_burst
        self.__periodos_restantes = cpu_burst
        self.__tiempo_llegada = tiempo_llegada
        self.__tiempo_respuesta = None
        self.__tiempo_salida = None
        self.__tiempo_retorno = None
        self.__tiempo_espera = 0


    # Este método resta una unidad a los periodos de cpu del proceso
    def actualizar_periodos_restantes(self):
        self.__periodos_restantes -= 1

    # Este método establece el tiempo de respuesta
    def establecer_tiempo_respuesta(self, t_primera_vez_cpu):
        self.__tiempo_respuesta = t_primera_vez_cpu - self.__tiempo_llegada

    # Este método establece el tiempo de salida
    def establecer_tiempo_salida(self, t):
        self.__tiempo_salida = t

    # Este método establece el tiempo de retorno
    def establecer_tiempo_retorno(self):
        self.__tiempo_retorno = self.__tiempo_salida - self.__tiempo_llegada

    # Este método suma una unidad al tiempo de espera del proceso
    def actualizar_tiempo_espera(self):
        self.__tiempo_espera += 1


   # Este método regresa el Id del proceso
    def obtener_id(self):
        return self.__id

    # Este método regresa el cpu burst del proceso
    def obtener_cpu_burst(self):
        return self.__cpu_burst

    # Este método regresa los periodos restantes
    def obtener_periodos_restantes(self):
        return self.__periodos_restantes

    # Este método regresa el tiempo de llegada del proceso
    def obtener_tiempo_llegada(self):
        return self.__tiempo_llegada

    # Este método regresa el tiempo de respuesta
    def obtener_tiempo_respuesta(self):
        return self.__tiempo_respuesta

    # Este método regresa el tiempo de salida
    def obtener_tiempo_salida(self):
        return self.__tiempo_salida

    # Este método regresa el tiempo de retorno
    def obtener_tiempo_retorno(self):
        return self.__tiempo_retorno

    # Este método regresa el tiempo de espera del proceso
    def obtener_tiempo_espera(self):
        return self.__tiempo_espera

    # La Comparación de procesos se realiza por su tiempo restante
    def __lt__(self, otro):
        return self.__periodos_restantes < otro.obtener_periodos_restantes()

#-----------------------------------------------------------------------------
