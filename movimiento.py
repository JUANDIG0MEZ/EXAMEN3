import time

from globales import RUTA_GUARDAR_3, RUTA_GUARDAR
import json
from grafo import Grafo

max_long = -1
def busqueda_dijkstra(grafo, start):
    """
    Esta función realiza la búsqueda de Dijkstra para encontrar el camino más corto entre dos nodos.
    """

    V = grafo.V
    E = grafo.E

    # Variable para almacenar la distancia entre el nodo inicial y los nodos restantes.
    dist = {nodo: float('inf') for nodo in V}
    dist[start] = 0

    # Variable para almacenar el predecesor de cada nodo.
    padre = {nodo: None for nodo in V}
    padre[start] = str(start)

    # conjunto de nodos visitados
    S = set()
    # conjunto de nodos sin visitar
    Q = set(V.keys())

    while Q:
        # Encuentra el nodo con menor distancia.
        u = min(Q, key=lambda nodo: dist[nodo])

        # Elimina el nodo de los nodos sin visitar
        Q.remove(u)
        # Añade el nodo a los nodos visitados
        S.add(u)

        # Añade la tortuga para la visualización
        # Recorre los vecinos del nodo u(nodo con menor distancia).
        for v in V[u]:
            # Esta línea de código es para obtener el peso de la arista.
            # Puede ser eliminada si las distancias entre nodos es de solo 1.
            # weight = E.get(f"({u}, {v})") or E.get(f"({v}, {u})")
            weight = 1

            # Se comprueba si los nodos vecinos están en los nodos sin visitar.
            if str(v) in Q:

                # Se calcula la distancia entre el nodo inicial y el nodo "v", pasando por el nodo "u".
                alt = dist[u] + weight

                # Si la distancia es menor a la distancia actual, se actualiza la distancia.
                if alt < dist[str(v)]:

                    # Actualiza la distancia.
                    dist[str(v)] = alt
                    # Guarda el predecesor del nodo "v" para reconstruir el camino.
                    padre[str(v)] = u

    # Retorna la distancia y el predecesor de cada nodo.
    return dist, padre


def camino_dos_nodos(grafo, start, end):
    """
    Esta función reconstruye el camino más corto entre dos nodos a partir de las variables
    entregadas por la función busqueda_dijkstra.
    """

    # Se realiza la búsqueda de Dijkstra.
    _, padre = busqueda_dijkstra(grafo, str(start))
    # Variable para almacenar el camino.
    camino = []

    # Nodo final.
    u = str(end)

    # Se recorre los predecesores de cada nodo.
    while padre[u] is not None and u != str(start):

        # Se añade el nodo al camino.
        camino.append(u)
        # Se actualiza el nodo final.
        u = padre[u]
    camino.reverse()

    return camino


def orden_nodos_tortugas(datos):
    """
    Devuelve el orden en el que visita los nodos cada tortuga.
    """

    orden_nodos = {}

    tortugas = datos.keys()

    for tortuga in tortugas:
        lista_recorrido = []
        actual = tortuga
        visitados_internos = {actual}

        nodos_internos = set(datos[tortuga].keys())

        lista_recorrido.append(int(actual))

        while nodos_internos != visitados_internos and str(datos[tortuga][actual][1]) != tortuga:
            lista_recorrido.append(datos[tortuga][actual][1])
            visitados_internos.add(str(datos[tortuga][actual][1]))
            actual = str(datos[tortuga][actual][1])
        orden_nodos[tortuga] = lista_recorrido

    return orden_nodos


def recorrido_tortuga_completo(grafo, listanodos):
    """
    Esta función devuelve el recorrido completo de una tortuga en el grafo.
    """
    camino = []

    for i in range(len(listanodos) - 1):
        if listanodos[i] != listanodos[i+1]:
            camino_sub = camino_dos_nodos(grafo, listanodos[i], listanodos[i + 1])
            camino = camino + camino_sub
    return camino


def recorrido_tortugas(grafo, orden):
    """
    Esta función utiliza las funciones anteriores para obtener el recorrido de todas las tortugas.
    """
    global max_long

    # Se crea un diccionario para almacenar el recorrido de las tortugas.
    recorridos = dict()

    # Se recorre el diccionario de orden de recorrido de las tortugas.
    for tortuga, nodos in orden.items():

        # Se crea una lista para almacenar el camino de la tortuga.
        camino = recorrido_tortuga_completo(grafo, nodos)
        recorridos[tortuga] = camino
        if len(camino) > max_long:
            max_long = len(camino)

    return recorridos


def dibujar_tortuga(grafo, recorridos):
    """
    Esta función se encarga de dibujar el recorrido de las tortugas.
    """
    global max_long

    tortuga_dict = {}
    tortugas = recorridos.keys()

    colores = set(grafo.colors.keys())


    # Posicion inicial de las tortugas
    for tortuga in tortugas:
        tortuga_dict[str(tortuga)] = 'f'
    grafo.add_direction_turtle2(tortuga_dict)
    grafo.send_graph()

    for i in range(max_long+1):
        tortuga_dict = {}
        for tortuga in tortugas:
            if len(recorridos[tortuga]) > i:
                tortuga_dict[recorridos[tortuga][i]] = 'f'
                if recorridos[tortuga][i] in colores:
                    grafo.colors[recorridos[tortuga][i]] = "green"

            else:
                tortuga_dict[recorridos[tortuga][-1]] = 'f'

        grafo.add_direction_turtle2(tortuga_dict)
        grafo.send_graph()

    return grafo


def recorrido():
    """
    Esta funcion se encarga de correr las funciones necesarias para obtener el recorrido de las tortugas y dibujarlo.
    """
    # Se lee el grafo que tiene el espacio de trabajo
    with open(RUTA_GUARDAR, 'r') as file:
        datos = json.load(file)

    V = datos['V']
    E = datos['E']
    colores = datos['colors']
    turtle = datos['turtle']

    # grafo del espacio de trabajo
    grafo_espacio = Grafo(V, E, turtle, colores)

    # Se lee el grafo con los recorridos que debe hacer cada tortuga
    with open(RUTA_GUARDAR_3, 'r') as file:
        datos = json.load(file)

    # orden de los nodos que debe visitar cada tortuga
    orden = orden_nodos_tortugas(datos)

    # recorrido de las tortugas
    dict_recorrido = recorrido_tortugas(grafo_espacio, orden)

    dibujar_tortuga(grafo_espacio, dict_recorrido)


