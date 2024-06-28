
import threading
import queue


# Dimensiones del espacio de trabajo
COLUMNAS = 20
FILAS = 10

# Parámetros importantes para crear el espacio de trabajo
MAX_TORTUGAS = 1
MAX_TAREAS = 15
MAX_OBSTACULOS = 10



# Lugar donde se guardará el grafo a dibujar
RUTA_DIBUJAR = r"C:\Users\juand\OneDrive\Desktop\Archivos\Universidad\Maestria\Semestre 1\Computacional\Examenes\labyrinth\grafo_dibujar.json"

# Lugar donde se guardará el grafo con las tareas, obstaculos y tortugas
RUTA_GUARDAR = r"C:\Users\juand\OneDrive\Desktop\Archivos\Universidad\Maestria\Semestre 1\Computacional\Examenes\labyrinth\grafo_obs.json"

# lugar donde se guardará el grafo con las distancias entre los nodos donde se encuentran las tortugas y tareas
RUTA_GUARDAR_2 = r"C:\Users\juand\OneDrive\Desktop\Archivos\Universidad\Maestria\Semestre 1\Computacional\Examenes\labyrinth\grafo_pos.json"

# lugar donde se guardará el recorrido de las tortugas
RUTA_GUARDAR_3 = r"C:\Users\juand\OneDrive\Desktop\Archivos\Universidad\Maestria\Semestre 1\Computacional\Examenes\labyrinth\recorrido_tortugas.json"

candado = threading.Lock()
# A queue object to handle inter-thread communication
cola = queue.Queue()
