"""
Este código se encarga de encontrar la ruta de cada una de las tortugas
"""
import pulp
from itertools import combinations
from globales import RUTA_GUARDAR, RUTA_GUARDAR_2
import json
from grafo import Grafo


def crear_diccionario_distancias(grafo):
    """
    Esta función se encarga de crear un diccionario con las distancias entre los nodos.
    """

    # Diccionario con las distancias entre los nodos
    distancias = dict()
    # Conjunto de nodos que tiene una tortuga o una tarea
    colores = set(int(i) for i in grafo.colors.keys() if grafo.colors[i] == 'red')
    tortugas = set(int(i) for i in grafo.turtle.keys())
    nodos = colores.union(tortugas)

    aristas = grafo.E
    for arista in aristas.keys():
        # la arista es una tupla de tipo string, se convierte a tupla
        arista2 = eval(arista)
        if arista2[0] in nodos and arista2[1] in nodos:
            distancias[arista2] = aristas[arista]

    return distancias, tortugas, colores

def d(i, j, aristas):
    """
    A partir del diccionario de distancias, se obtiene la distancia entre dos nodos.
    """
    if i == j:
        return 0.0
    else:
        return aristas.get((i,j)) or aristas.get((j,i))


def obtenerConjuntos(grafo_espacio):
    """
    Esta función se encarga de obtener los conjuntos C, D y las distancias entre los nodos.
    """
    d_ij, D, C =crear_diccionario_distancias(grafo_espacio)
    return d_ij, D, C

def solve():
    """
    Esta función se encarga de resolver el problema de optimización.
    """

    # Carga el grafo
    with open(RUTA_GUARDAR_2, 'r') as file:
        datos = json.load(file)

    V = datos['V']
    E = datos['E']
    turtle = datos['turtle']
    coloress = datos['colors']

    grafo_espacio = Grafo(V, E, turtle, coloress)
    d_ij, D, C = obtenerConjuntos(grafo_espacio)
    CUD = C.union(D)


    # Definir el problema de optimización
    prob = pulp.LpProblem("Rutas_de_Tortugas", pulp.LpMinimize)

    # Variables de decisión
    x = pulp.LpVariable.dicts("x", ((i, j, k) for i in CUD for j in CUD for k in D), cat="Binary")

    # Función objetivo
    prob += pulp.lpSum(d(i, j, d_ij) * x[i, j, k] for i in CUD for j in CUD for k in D)

    # Restricciones
    # Todas las tareas deben ser visitadas exactamente una vez
    for j in C:
        prob += pulp.lpSum(x[i, j, k] for k in D for i in CUD if i != j) == 1

    # Cada tortuga que llega a una tarea debe salir de ella
    for k in D:
        for i in CUD:
            prob += pulp.lpSum(x[i, j, k] for j in CUD if j != i) == pulp.lpSum(x[j, i, k] for j in CUD if j != i)

    # Asegurar que cada tortuga empieza y termina en su posición inicial
    for k in D:
        prob += pulp.lpSum(x[k, j, k] for j in CUD if j != k) == 1
        prob += pulp.lpSum(x[i, k, k] for i in CUD if i != k) == 1

    # Restricciones de eliminación de sub ciclos (General)
    for k in D:
        for s in range(2, len(C)):
            for S in combinations(C, s):
                prob += pulp.lpSum(x[i, j, k] for i in S for j in S if i != j) <= len(S) - 1

    # Resolver el problema
    prob.solve()

    # Guardar el recorrido de las tortugas
    recorrido = dict()
    for k in D:

        recorrido[k] = {}
        for i in CUD:
            for j in CUD:
                if pulp.value(x[i, j, k]) == 1:

                    recorrido[k][i] = (i, j)

    with open('recorrido_tortugas.json', 'w') as file:
        json.dump(recorrido, file, indent=4)

