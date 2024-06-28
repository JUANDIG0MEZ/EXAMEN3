from worker import crear_espacio_trabajo
from prelineal import grafo_tt
from lineal import solve
from movimiento import recorrido
from labyrinth import Labyrinth
from globales import FILAS, COLUMNAS
from threading import Thread
import time
def create_labyrinth():
    maze = Labyrinth(FILAS, COLUMNAS)
    maze.start()


if __name__ == '__main__':

    hilo1 = Thread(target=create_labyrinth)
    hilo1.start()
    for i in range(50):
        crear_espacio_trabajo()
        grafo_tt()
        solve()
        recorrido()
    hilo1.join()
