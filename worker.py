"""
Este código se encarga de crear el espacio de trabajo.
"""

import time
from globales import *
import grafo
from random import randint
from labyrinth import Labyrinth
import threading


def espacio(grafo1, grafo2):
    """
    Esta funcion se encarga de crear agregar los nodos del


    """
    for current_vertex in range(FILAS * COLUMNAS):
        neighbors = vecinos(current_vertex)
        for neighbor in neighbors:
            grafo1.add_edge(current_vertex, neighbor, 1)
            grafo2.add_edge(current_vertex, neighbor, 1)

def vecinos(current):

    vecinos = []

    if current % COLUMNAS != 0:  # Izquierda
        vecinos.append(current - 1)
    if current % COLUMNAS != COLUMNAS - 1:  # Derecha
        vecinos.append(current + 1)
    if current // COLUMNAS != 0:  # Arriba
        vecinos.append(current - COLUMNAS)
    if current // COLUMNAS != FILAS - 1:  # Abajo
        vecinos.append(current + COLUMNAS)
    return vecinos


def agregar_obstaculos(grafo1, grafo2):
    """
    Esta función se encarga de agregar obstáculos al espacio
    """
    obstaculos = 0
    while obstaculos < MAX_OBSTACULOS:
        pos = randint(0, FILAS*COLUMNAS-1)
        grafo1.add_color(str(pos), 'black')
        grafo2.add_color(str(pos), 'black')

        neightbors = vecinos(pos)

        for neighbor in neightbors:
            grafo2.delete_edge(pos, neighbor)

        obstaculos += 1


def agregar_tortugas(grafo1, grafo2):
    """
    Esta función se encarga de agregar tortugas al espacio
    """

    obstaculos = set()
    colores = grafo1.colors.keys()


    for color in colores:
        if grafo1.colors[color] == 'black':
            obstaculos.add(int(color))

    tortugas = 0
    while tortugas < MAX_TORTUGAS:
        pos = randint(0, FILAS*COLUMNAS-1)
        if pos not in obstaculos:
            grafo1.add_direction_turtle(pos)
            grafo2.add_direction_turtle(pos)
            tortugas += 1


def agregar_tareas(grafo1, grafo2):
    """
    Esta función se encarga de agregar tareas al espacio
    """
    obstaculos = set()
    colores = grafo1.colors.keys()


    tortugas = grafo1.turtle.keys()

    for color in colores:
        if grafo1.colors[color] == 'black':
            obstaculos.add(int(color))

    for tortuga in tortugas:
        obstaculos.add(tortuga)

    tareas = 0
    while tareas < MAX_TAREAS:
        pos = randint(0, FILAS*COLUMNAS-1)
        if pos not in obstaculos:
            grafo1.add_color(str(pos), 'red')
            grafo2.add_color(str(pos), 'red')
            tareas += 1


def create_labyrinth():
    maze = Labyrinth(FILAS, COLUMNAS)
    maze.start()


def crear_grafos():
    grafo_e = grafo.Grafo()
    grafo_t = grafo.Grafo()

    espacio(grafo_e, grafo_t)
    agregar_obstaculos(grafo_e, grafo_t)
    agregar_tortugas(grafo_e, grafo_t)
    agregar_tareas(grafo_e, grafo_t)

    grafo_e.save_graph(RUTA_DIBUJAR)
    grafo_e.send_graph()

    grafo_t.save_graph(RUTA_GUARDAR)


def crear_espacio_trabajo():
    crear_grafos()
