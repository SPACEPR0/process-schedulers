import heapq
from proceso import Proceso

def srtf(procesos):
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

            # Se establece el tiempo de respuesta del proceso actual
            proceso_actual.establecer_tiempo_respuesta(t)

            # Actualiza periodos
            proceso_actual.actualizar_periodos_restantes()

            # Procesos que no se están ejecutando
            for p in cola_listos[1:]:
                p.actualizar_tiempo_espera()

            t += 1

            if proceso_actual.obtener_periodos_restantes() == 0:
                # Se establece el tiempo de salida
                proceso_actual.establecer_tiempo_salida(t)
                # Se establece el tiempo de retorno. Para calcularo, es
                # necesario que el tiempo de salida ya se haya establecido
                proceso_actual.establecer_tiempo_retorno()

                print("Proceso:", proceso_actual.obtener_id(), end=" ")
                print("terminó en el tiempo:", t, end=" ")
                print("Con tiempo de espera de:", proceso_actual.obtener_tiempo_espera())
                print("---------------------------------------------------")
                # Se saca de la cola de procesos
                terminados.append(heapq.heappop(cola_listos))
        else:
            t += 1
# -----------------------------------------------------------------------------

def rr(procesos, q):
    # Esta función obtiene los nuevos procesos que van llegando en cada tiempo
    # t y los va agrega a la cola
    def obtener_nuevos_procesos(procesos, t):
        # Se obtienen los procesos nuevos
        nuevos = [p for p in procesos if p.obtener_tiempo_llegada() == t]
        # Se eliminan de la lista de procesos los que hemos obtenido
        for p in nuevos:
            procesos.remove(p)

        return nuevos

    # Esta variable almacenará el proceso que está siendo atendido en el CPU
    proceso_actual = None

    # Esta variable representa el tiempo
    t = 0

    # Esta variable lleva la cuenta de los cambios de contexto realizados.
    # Inicia en -1 para no contar el falso cambio de contexto del primer proceso
    cambios_contexto = -1

    # Se obtienen los procesos que llegan en el tiempo 0
    cola = obtener_nuevos_procesos(procesos, 0)

    # Esta variable representa la cola de terminados
    terminados = []

    while True:
        #Si hay cola, entonces se toma el siguiente proceso
        if cola:
            cambios_contexto += 1
            proceso_actual = cola.pop(0)
            # Si el proceso actual no tiene asignado un tiempo de respuesta
            # significa que el 't' actual corresponde a su primera vez en el cpu,
            # por lo tanto, el tiempo de respuesta se establece
            if proceso_actual.obtener_tiempo_respuesta() == None:
                proceso_actual.establecer_tiempo_respuesta(t)

        # Si no hay cola y el cpu está desocupado, pero existen procesos,
        # entonces los esperamos
        elif procesos and proceso_actual == None:
            t += 1
            # Se obtienen los procesos que llegaron en el tiempo actual
            cola.extend(obtener_nuevos_procesos(procesos, t))
            continue
        # Si hay procesos (o no) pero el cpu está ocupado, entonces seguimos
        # atendiendo al proceso
        elif proceso_actual != None:
            pass
        else: #Si la cola y lista de procesos están vacíos, además el cpu está libre, se termina.
            break

        # Bandera que indica si el proceso debe agregarse a la cola una vez que se
        # haya atendido
        proceso_termino = False

        # Comienza a contar el quantum.
        for i in range(q):
            # Se actualiza el tiempo, el cpu burst del proceso actual y los tiempos
            # de espera de los procesos en la cola
            t += 1
            proceso_actual.actualizar_periodos_restantes()
            for p in cola:
                p.actualizar_tiempo_espera()

            # Se obtienen los procesos que llegaron en el tiempo actual
            cola.extend(obtener_nuevos_procesos(procesos, t))

            # Si el cpu burst del proceso actual llegó a cero, entonces ya no
            # necesita el cpu y este se libera
            if proceso_actual.obtener_periodos_restantes() == 0:
                proceso_termino = True
                # Se establece el tiempo de salida
                proceso_actual.establecer_tiempo_salida(t)
                # Se establece el tiempo de retorno. Para calcularo, es
                # necesario que el tiempo de salida ya se haya establecido
                proceso_actual.establecer_tiempo_retorno()

                terminados.append(proceso_actual)
                proceso_actual = None
                break

        # Si el proceso no terminó después de su turno, entonces se revisa si hay
        # otro proceso esperando en la cola; si no, continúa en el cpu
        if not proceso_termino:
            # Si hay cola significa que ocurrirá un cambio de contexto
            # porque un proceso diferente entrará al cpu
            if cola:
                cola.append(proceso_actual)
    
    # Se escribe un csv con los resultados de la corrida
    archivo = open('resultados_rr.csv', 'w')
    archivo.write("id,cpu_burst,t_llegada,t_respuesta,t_salida,t_retorno,t_espera\n")
    for p in terminados:
        Id = p.obtener_id()
        cpu_burst = str(p.obtener_cpu_burst())
        t_llegada = str(p.obtener_tiempo_llegada())
        t_respuesta = str(p.obtener_tiempo_respuesta())
        t_salida = str(p.obtener_tiempo_salida())
        t_retorno = str(p.obtener_tiempo_retorno())
        t_espera = str(p.obtener_tiempo_espera())
        resultado = (Id+','+cpu_burst+','+t_llegada+','+t_respuesta+','+t_salida+
                    ','+t_retorno+','+t_espera+'\n')
        archivo.write(resultado)

    archivo.write(str(cambios_contexto))
    archivo.close()
