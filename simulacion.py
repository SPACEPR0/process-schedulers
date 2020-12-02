from calendarizadores import rr, srtf
from proceso import Proceso
import argparse
import matplotlib.pyplot as plt
import statistics

# Esta función lee la información de los procesos  del archivo de texto y
# regresa una lista con los objetos de tipo Proceso ya creados.
def obtener_procesos(archivo):
    procesos = [p.strip().split(',') for p in open(archivo,'r').readlines()]
    return [Proceso(p[0], int(p[1]), int(p[2])) for p in procesos]
###############################################################################

# Esta función crea la tabla con los resultados de la calendarización y la
# guarda como "tabla_algoritmo.jpg"
# -----PARAMETROS-----
# resultado: Diccionario que regresa el calendarizador
# algoritmo: Nombre del algoritmo, se usa para nombrar la imagen (rr o srtf)
def crear_tabla(resultado, algoritmo):
    # ------------------------SE ACOMODAN LOS DATOS PARA LA TABLA------------------
    # Se construye la primer columna de la tabla (El header)
    data = [["ID", "CPU Burst", "T. Llegada", "T. Respuesta", "T. Salida",
            "T. Retorno", "T. Espera"]]

    # Se construyen los renglones de la tabla de acuerdo a la info de los procesos
    # después de que se calendarizaron
    for i in range(len(resultado["ids"])):
        renglon = []
        renglon.append(resultado["ids"][i])
        renglon.append(resultado["cpu_bursts"][i])
        renglon.append(resultado["ts_llegada"][i])
        renglon.append(resultado["ts_respuesta"][i])
        renglon.append(resultado["ts_salida"][i])
        renglon.append(resultado["ts_retorno"][i])
        renglon.append(resultado["ts_espera"][i])
        data.append(renglon)

    # Se crea la última columna en donde estarán los promedios y se agrega a la 
    # tabla
    promedios = ["Promedios", "-", "-", 
                format(statistics.mean(resultado['ts_respuesta']), ".2f"),
                "-", 
                format(statistics.mean(resultado['ts_retorno']), ".2f"),
                format(statistics.mean(resultado['ts_espera']), ".2f")]
    data.append(promedios)

    # --------------------- SE CREA LA TABLA Y SE LE DA FORMATO -------------------

    # Se obtiene 4 colores iguales (gris) para cada celda del header
    colores_header = [(.5,.5,.5) for i in range(len(data[0]))]

    # Se construye la tabla con matplotlib
    table = plt.table(cellText=data[1:], colLabels=data[0], loc="center",
            rowLoc="center", colColours=colores_header)

    # El texto de las celdas del header se ponen blancas
    header_cells = [table[(0,i)] for i in range(len(data[0]))]
    for cell in header_cells:
        cell.get_text().set_color("white")

    # Se obtienen las renglones de la tabla alternados para colorearlos de gris
    # alternadamente (uno sí, uno no, ...)
    gray_cells = [table[(i,j)] for i in range(2,len(resultado["ids"])+1, 2) for j in range(len(data[0]))]
    for cell in gray_cells:
        cell.set_facecolor((.8, .8, .8, .5))

    # Se obtiene las celdas de la columna de las medias para colorearlas de otro
    # color (verde)
    means_row = [table[(len(resultado["ids"])+1, i)] for i in range(len(data[0]))]
    for cell in means_row:
        cell.get_text().set_fontweight("bold")
        cell.set_facecolor((.65,.74,.58))

    # Se quitan los ejes a la tabla y se guarda como imagen .jpg
    plt.axis("off")
    plt.savefig(f"tabla_{algoritmo}.jpg", bbox_inches="tight", dpi=150)
    # Se "limpia" la figura para evitar que se sobreescriba en usos posteriores
    # de esta función
    plt.clf()
###############################################################################


# Esta función crea el diagrama de ejecución de los procesos en formato
# html
# -----PARÁMETROS-----
# resultado: diccionario que regresa el algoritmo de calendarización
def crear_diagrama_ejecucion(resultado):
    # Cada renglón del diagrama es una tabla. Más o menos 19 se ven bien en el
    # documento. Con este contador vamos a contar cuándot cuadritos llevamos
    # para saber si debemos crear un nuevo renglón (nueva tabla)
    contador = 0

    # Esta variable corresponde a la creación de la tabla en donde se indican los
    # tiempo
    tiempos = "<table border=\"0\" width=\"95%\" style=\"table-layout: fixed;margin: 0px auto;\"><tbody><tr><td align=\"center\"><b>t:</b></td>"

    # Esta variable corresponde a la creación de la tabla en donde se indican los
    # procesos
    orden = "<table border=\"1\" width=\"95%\" style=\"table-layout: fixed;margin: 0px auto;\"><tbody><tr><td bgcolor=\"#DDDDDD\" align=\"center\"><span style=\"font-size: small;\">CPU</span></td>"

    # En esta variable vamos a almacenar el diagrama completo que se va a construir
    # por partes.
    diagrama = ""

    # Comienza a crearse el diagrama
    for i in range(resultado['t']):
        # Mientras no haya 19 cuadritos en el renglón actual, se siguen metiendo
        # tiempos a la tabla de tiempos y procesos a la tabla de procesos
        if contador < 20:
            tiempos += f"<td align=\"left\"><span style=\"font-size: small;\">&nbsp;{i}</span></td>"
            orden += f"<td align=\"center\">{resultado['orden'][i]}</td>"
            contador += 1

        # Cuando ya tengamos 19 cuadritos, entonces agregamos a cada tabla su fin y
        # las agregamos al diagrama
        else:
            tiempos += "</tr></tbody></table>"
            orden += "</tbody></table>"
            diagrama = diagrama + tiempos +  orden + "<br>"

            tiempos = "<table border=\"0\" width=\"95%\" style=\"table-layout: fixed;margin: 0px auto;\"><tbody><tr><td align=\"center\"><b>t:</b></td>"
            orden = "<table border=\"1\" width=\"95%\" style=\"table-layout: fixed;margin: 0px auto;\"><tbody><tr><td bgcolor=\"#DDDDDD\" align=\"center\"><span style=\"font-size: small;\">CPU</span></td>"
            tiempos += f"<td align=\"left\"><span style=\"font-size: small;\">&nbsp;{i}</span></td>"
            orden += f"<td align=\"center\">{resultado['orden'][i]}</td>"

            contador = 0

    # Para que el diagrama no se vea feo cuando la última tabla tenga menos de 19
    # cuadritos, se acompletan con espacios y tiempos de relleno
    for _ in range(20 - contador):
        tiempos += "<td align=\"left\"><span style=\"font-size: small;\">&nbsp;-</span></td>"
        orden += "<td align=\"center\">-</td>"

    # Al final se cierran todas las tablas y se agrega el último trozo al diagrama
    tiempos += "</tr></tbody></table>"
    orden += "</tbody></table>"
    diagrama = diagrama + tiempos +  orden + "<br>"

    return diagrama
###############################################################################

# Esta función crea el archivo html final. Puede crearse para un solo algoritmo
# o para ambos.
# -----PARÁMETROS-----
# algoritmos: lista con los nombres de los algoritmos (rr o srtf)
# diagramas: lista con los diagramas de ejecución de los diagramas
#            (resultados de la función crear_diagrama_ejecucion())
# cambios_contexto: lista con el número de cambios de contexto
# grafica: Nombre de la imagen que contiene la gráfica comparativa

def crear_html(algoritmos, diagramas, cambios_contexto, grafica=None):
    # Se lee la plantilla del header
    html_file = open("header.html", 'r').read()

    # Por cada algoritmo dado se agregará su tabla y su diagrama de ejecución
    for i in range(len(algoritmos)):
        # Se lee la plantilla
        html_file += open("plantilla_tabla_y_diagrama.html", 'r').read()
        # Se pone un encabezado y se lee la tabla desde la imagen correspondiente
        if algoritmos[i] == "rr":
            html_file = html_file.replace("{calendarizador}", "ROUND ROBIN")
            html_file = html_file.replace("{tabla}", "tabla_rr.jpg")
            
        else:
            html_file = html_file.replace("{calendarizador}", "SHORTEST REMAINING TIME FIRST")
            html_file = html_file.replace("{tabla}", "tabla_srtf.jpg")
        
        # Se agrega el diagrama de ejecución
        html_file = html_file.replace("{diagrama}", diagramas[i])
        # Se escribe el número de cambios de contexto
        html_file = html_file.replace("{cambios_contexto}", str(cambios_contexto[i]))
        # Se agrega un espacio en blanco
        html_file += "<br><br>"
    
    # Si nos dan una gráfica comparativa, entonces se lee la plantilla
    # correspondiente y se agrega la imagen.
    if grafica:
        html_file += open("plantilla_tabla_y_diagrama.html", 'r').read()
        html_file = html_file.replace("{grafica}", grafica)

    # Se crea el archivo y se guarda
    file = open("resultados.html", 'w')
    file.write(html_file)
    file.close()

# /////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////

parser = argparse.ArgumentParser(description=
                                 "Este script corre los algoritmos de calendarización")

parser.add_argument("-a", "--algoritmo", help="Algoritmo de calendarización"+
                    " a correr. Puede ser rr, srtf u all.", metavar="", type=str)
parser.add_argument("-p", "--procesos", help="Archivo de texto que contiene los procesos.",
                    metavar = "", type=str)
parser.add_argument("-q", "--quantum", help="Tamaño del quantum en caso de correr round robin.",
                    metavar="", type=int)

args = parser.parse_args()


# Se obtienen los valores necesarios para correr el calendarizador
algoritmo = args.algoritmo
archivo_procesos = args.procesos
quantum = args.quantum

#Se corre el algoritmo deseado
resultado = None
if algoritmo == "rr":
    if not quantum:
        print("No se ha especificado el tamaño del quantum")
    else:
        print("ROUND ROBIN\n")
        resultado_rr = rr(obtener_procesos(archivo_procesos), quantum)
        crear_tabla(resultado_rr, "rr")
        diagrama_rr = crear_diagrama_ejecucion(resultado_rr)
        crear_html(["rr"], [diagrama_rr], [resultado_rr['cambios_contexto']])

elif algoritmo == "srtf":
    print("SHORTEST REMAINING TIME FIRST\n")
    resultado_srtf = srtf(obtener_procesos(archivo_procesos))
    crear_tabla(resultado_srtf, "srtf")
    diagrama_srtf = crear_diagrama_ejecucion(resultado_srtf)
    crear_html(["srtf"], [diagrama_srtf], [resultado_srtf['cambios_contexto']])

elif algoritmo == "all":
    if not quantum:
        print("No se ha especificado el tamaño del quantum")
    else:
        resultado_rr = rr(obtener_procesos(archivo_procesos), quantum)
        crear_tabla(resultado_rr, "rr")
        diagrama_rr = crear_diagrama_ejecucion(resultado_rr)

        resultado_srtf = srtf(obtener_procesos(archivo_procesos))
        crear_tabla(resultado_srtf, "srtf")
        diagrama_srtf = crear_diagrama_ejecucion(resultado_srtf)

        crear_html(["rr", "srtf"], 
                    [diagrama_rr, diagrama_srtf], 
                    [resultado_rr['cambios_contexto'], 
                    resultado_srtf['cambios_contexto']])
else:
    print("El algoritmo", algoritmo, "no está implementado.")


