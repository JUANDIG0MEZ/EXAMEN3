from globales import COLUMNAS, FILAS, RUTA_GUARDAR_2, RUTA_GUARDAR
from grafo import Grafo
import json
def distancias(indice1, indice2):
    """
    Esta función calcula la distancia Manhattan entre dos vértices del laberinto.
    """

    fila1 = indice1 // COLUMNAS
    columna1 = indice1 % COLUMNAS

    fila2 = indice2 // COLUMNAS
    columna2 = indice2 % COLUMNAS

    return abs(fila1 - fila2) + abs(columna1 - columna2)


def grafo_tareas(grafo_completo):
    """
    Esta función crea un grafo completamente conectado, donde cada vertice es una tarea o una tortuga.
    El peso de las aristas es la distancia Manhattan entre los nodos.
    """
    tortugas = grafo_completo.turtle
    colores = grafo_completo.colors
    grafo_t = Grafo(turtle=tortugas, colors=colores)

    pos_D = tortugas.keys()

    pos_C = set()
    for pos_T in colores:
        if colores[pos_T] == 'red':
            pos_C.add(pos_T)

    pos_CUD = pos_C.union(pos_D)

    # Crea un grafo completamente conectado
    for i in pos_CUD:
        for j in pos_CUD:
            if i != j:
                grafo_t.add_edge(int(i), int(j), distancias(int(i), int(j)))
    grafo_t.save_graph(RUTA_GUARDAR_2)


def grafo_tt():
    """
    Esta función corre las funciones necesarias para crear el grafo de tareas.
    """
    # Carga el grafo
    with open(RUTA_GUARDAR, 'r') as file:
        datos = json.load(file)

    V = datos['V']
    E = datos['E']
    turtle = datos['turtle']
    coloress = datos['colors']

    grafo_espacio = Grafo(V, E, turtle, coloress)

    grafo_tareas(grafo_espacio)

