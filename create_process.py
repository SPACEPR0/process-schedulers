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
parser.add_argument("-i", "--iniciales", help="Indicar el numero de procesos que se aseguran en el t = 0" + 
                    ", de no ser especificado, i = 2", metavar="", type=int, default=2)

args = parser.parse_args()

archivo = args.archivo
n = args.num_procesos
media = args.media
sd = args.desv_est
init = args.iniciales

# Aseguramos los procesos iniciales
iniciales = np.zeros((init, ))
# Creo que hay que ordernar los tiempos para que tenga mas sentido
tiempos_llegada = np.sort(randint(0, media * n, (n - init,)))

# Juntamos todos los tiempos
tiempos_llegada = np.append(iniciales, tiempos_llegada)

# Tomamos tiempos de una normal
cpu_bursts = normal(media, sd, n).reshape(n,)

# Como se redondea a entero al convertir a archivo, cambiamos 
#   todos los valores menores que 1 por la media mañosamente
#   Esto deberia asegurar que no haya cpu bursts iguales a 0
cpu_bursts = np.where(cpu_bursts < 1, media, cpu_bursts)

ids = np.arange(n)


procesos = np.array([ids, tiempos_llegada, cpu_bursts]).T

# Guardamos sin que tenga corchetes 
procesos = asarray(procesos)
savetxt(archivo, procesos, delimiter=', ', fmt='%d')