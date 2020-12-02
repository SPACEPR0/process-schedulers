from calendarizadores import rr, srtf
from proceso import Proceso
import argparse
import dash
import graficas

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Esta función lee la información de los procesos  del archivo de texto y
# regresa una lista con los objetos de tipo Proceso ya creados.
def obtener_procesos(archivo):
    procesos = [p.strip().split(',') for p in open(archivo,'r').readlines()]
    return [Proceso(p[0], int(p[1]), int(p[2])) for p in procesos]

# /////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////

parser = argparse.ArgumentParser(description=
                                 "Este script corre los algoritmos de calendarización")

parser.add_argument("-a", "--algoritmo", help="Algoritmo de calendarización"+
                    " a correr. Puede ser rr, srtf u all.", metavar="", type=str)
parser.add_argument("-p", "--procesos", help="Archivo de texto que contiene los procesos.",
                    metavar = "", type=str, default="procesos.txt")
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
        app.layout = graficas.layout_uni(resultado_rr, "Round Robin", quantum)
        app.run_server(debug=True)

elif algoritmo == "srtf":
    print("SHORTEST REMAINING TIME FIRST\n")
    resultado_srtf = srtf(obtener_procesos(archivo_procesos))
    app.layout = graficas.layout_uni(resultado_srtf, "Shortest Remaining Time First")
    app.run_server(debug=True)

elif algoritmo == "all":
    if not quantum:
        print("No se ha especificado el tamaño del quantum")
    else:
        resultado_rr = rr(obtener_procesos(archivo_procesos), quantum)
        resultado_srtf = srtf(obtener_procesos(archivo_procesos))
        app.layout = graficas.layout_all(resultado_srtf, resultado_rr, quantum)
        app.run_server(debug=True)
else:
    print("El algoritmo", algoritmo, "no está implementado.")