from calendarizadores import rr, srtf
from proceso import Proceso
import argparse
import matplotlib.pyplot as plt
import statistics

parser = argparse.ArgumentParser(description=
                                 "Este script corre los algoritmos de calendarización")

parser.add_argument("-a", "--algoritmo", help="Algoritmo de calendarización"+
                    " a correr. Puede ser rr, srtf u all.", metavar="", type=str)
parser.add_argument("-p", "--procesos", help="Archivo de texto que contiene los procesos.",
                    metavar = "", type=str)
parser.add_argument("-q", "--quantum", help="Tamaño del quantum en caso de correr round robin.",
                    metavar="", type=int)

args = parser.parse_args()

# Esta función lee la información de los procesos  del archivo de texto y
# regresa una lista con los objetos de tipo Proceso ya creados.
def obtener_procesos(archivo):
    procesos = [p.strip().split(',') for p in open(archivo,'r').readlines()]
    return [Proceso(p[0], int(p[1]), int(p[2])) for p in procesos]


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
        resultado = rr(obtener_procesos(archivo_procesos), quantum)

elif algoritmo == "srtf":
    print("SHORTEST REMAINING TIME FIRST\n")
    srtf(obtener_procesos(archivo_procesos))

elif algoritmo == "all":
    print("SHORTEST REMAINING TIME FIRST\n")
    srtf(obtener_procesos(archivo_procesos))
    print("\nROUND ROBIN\n")
    if not quantum:
        print("No se ha especificado el tamaño del quantum")
    else:
        rr(obtener_procesos(archivo_procesos), quantum)

else:
    print("El algoritmo", algoritmo, "no está implementado.")

# Por el momento, nadamás está implementado para cuando se ejecute sólo Round Robin

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

# Se obtiene 5 colores iguales (gris) para cada celda del header
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
plt.savefig("tabla.jpg", bbox_inches="tight", dpi=150)

# ---SE CREA UN HTML CON LA TABLA Y EL DIAGRAMA DE EJECUCIÓN DE LOS PROCESOS---

# Cada renglón del diagrama es una tabla. Más o menos 20 se ven bien en el
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
    # Mientras no haya 20 cuadritos en el renglón actual, se siguen metiendo
    # tiempos a la tabla de tiempos y procesos a la tabla de procesos
    if contador < 20:
        tiempos += f"<td align=\"left\"><span style=\"font-size: small;\">&nbsp;{i}</span></td>"
        orden += f"<td align=\"center\">{resultado['orden'][i]}</td>"
        contador += 1

    # Cuando ya tengamos 20 cuadritos, entonces agregamos a cada tabla su fin y
    # las agregamos al diagrama
    else:
        tiempos += "</tr></tbody></table>"
        orden += "</tbody></table>"
        diagrama = diagrama + tiempos +  orden + "<br>"

        tiempos = "<table border=\"0\" width=\"95%\" style=\"table-layout: fixed;margin: 0px auto;\"><tbody><tr><td align=\"center\"><b>t:</b></td>"
        orden = "<table border=\"1\" width=\"95%\" style=\"table-layout: fixed;margin: 0px auto;\"><tbody><tr><td bgcolor=\"#DDDDDD\" align=\"center\"><span style=\"font-size: small;\">CPU</span></td>"
        tiempos += f"<td align=\"left\"><span style=\"font-size: small;\">&nbsp;{i}</span></td>"
        orden += f"<td align=\"center\">{resultado['orden'][i]}</td>"

        contador = 1

# Para que el diagrama no se vea feo cuando la última tabla tenga menos de 20
# cuadritos, se acompletan con espacios y tiempos de relleno
for _ in range(20 - contador):
    tiempos += "<td align=\"left\"><span style=\"font-size: small;\">&nbsp;-</span></td>"
    orden += "<td align=\"center\">-</td>"

# Al final se cierran todas las tablas y se agrega el último trozo al diagrama
tiempos += "</tr></tbody></table>"
orden += "</tbody></table>"
diagrama = diagrama + tiempos +  orden + "<br>"

# Vamos a crear un HTML con una cadena de texto. Aquí se le da formato
# a este archivo y agregamos la tabla y el diagrama en donde convenga
text = f'''
<head>
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
</head>
<div class="jumbotron text-center">
  <h1>CALENDARIZADOR ROUND ROBIN</h1>
</div>

<div class="container", style="margin:auto;">
    <img src="tabla.jpg" alt="tabla", style="display:block;margin:auto;">
   
</div>

<div class="container">
    <h2> Diagrama de ejecución</h2>
    {diagrama}   
    <h5> Cambios de contexto: {resultado['cambios_contexto']}</h5>
</div>
'''

# Se crea el archivo y se guarda
file = open("sample.html", 'w')
file.write(text)
file.close()
