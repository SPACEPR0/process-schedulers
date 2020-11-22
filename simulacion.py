from calendarizadores import rr, srtf
from proceso import Proceso
import argparse

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
if algoritmo == "rr":
    if not quantum:
        print("No se ha especificado el tamaño del quantum")
    else:
        print("ROUND ROBIN\n")
        rr(obtener_procesos(archivo_procesos), quantum)

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

