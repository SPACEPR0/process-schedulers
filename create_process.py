import argparse
import numpy as np
from numpy import asarray, savetxt
from numpy.random import normal, randint


parser = argparse.ArgumentParser(description=
                                 "Este script genera un archivo .txt con n procesos (ids, tiempo de llegada y cpu burst)")
parser.add_argument("-a", "--archivo", help="Nombre del archivo donde escribir los procesos" + 
                    ", de no ser especificado se escribira en procesos.txt", metavar="", type=str, default="procesos.txt")

parser.add_argument("-n", "--num_procesos", help="Numero de procesos a crear" +
                    ", de no ser especificado, n = 100", metavar="", type=int, default=100)
parser.add_argument("-m", "--media", help="Media de los CPU bursts"  + 
                    ", de no ser especificado, media = 15.",
                    metavar = "", type=float, default=15)
parser.add_argument("-s", "--desv_est", help="Desviacion estandar de los CPU bursts" + 
                    ", de no ser especificado, s = 5",
                    metavar="", type=float, default=5)

args = parser.parse_args()



archivo = args.archivo
n = args.num_procesos
media = args.media
sd = args.desv_est

# Creo que hay que ordernar los tiempos para que tenga mas sentido
tiempos_llegada = np.sort(randint(0, 2 * n, (n,)))
cpu_bursts = normal(media, sd, n).reshape(n,)
ids = np.arange(n)


procesos = np.array([ids, tiempos_llegada, cpu_bursts]).T

procesos = asarray(procesos)
savetxt(archivo, procesos, delimiter=', ', fmt='%d')