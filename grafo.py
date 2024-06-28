import json
from globales import cola, candado, RUTA_GUARDAR
from copy import deepcopy


class Grafo:

    def __init__(self, V: dict = None, E: dict = None, turtle: dict = None, colors: dict = None):

        if V is None:
            V = dict()
        self.V = V
        if E is None:
            E = dict()
        self.E = E
        if turtle is None:
            turtle = dict()
        self.turtle = turtle
        if colors is None:
            colors = dict()
        self.colors = colors
        self._show_graph = False

    def __repr__(self):

        return f'Vertices: {self.V}\nEdges: {self.E}\nTurtle: {self.turtle}\nColors: {self.colors}'

    def get_graph(self):

        grafo_g = {'V': self.V, 'E': self.E, 'turtle': self.turtle, 'colors': self.colors}
        return grafo_g

    def send_graph(self):

        grafo_g = self.get_graph()
        with candado:
            # Put the graph into the global queue 'cola'
            # The deepcopy function is used to avoid
            # the Queue storing a reference to the graph to the original graph
            cola.put(deepcopy(grafo_g))

    def save_graph(self, path: str):

        grafo_g = self.get_graph()
        with open(path, 'w') as file_graph:
            json.dump(grafo_g, file_graph, indent=4)
        # Close the file_graph
        file_graph.close()


    def add_edge(self, vertex_o: int, vertex_i: int, weight: int):

        # Verify if the edge already exists
        if f"({vertex_o}, {vertex_i})" in self.E or f"({vertex_i}, {vertex_o})" in self.E:
            if __name__ == '__main__':
                print(f"The edge ({vertex_o}, {vertex_i}) already exists.")
        else:
            # Verify if vertices exist or add them if they are not in the graph
            if vertex_o not in self.V:
                self.V[vertex_o] = [vertex_i]
            else:
                self.V[vertex_o].append(vertex_i)
            if vertex_i not in self.V:
                self.V[vertex_i] = [vertex_o]
            else:
                self.V[vertex_i].append(vertex_o)
            # Add the edge to the graph
            self.E[f"({vertex_o}, {vertex_i})"] = weight

    def delete_edge(self, vertex_o: int, vertex_i: int):
        """
        This method deletes an edge between two vertices in the graph. If the edge does not exist, it prints a message and
        does not delete the edge. If the vertices do not exist in the graph, it prints a message and does not delete the edge.

        :param vertex_o: (int) The origin vertex of the edge.
        :param vertex_i: (int) The destination vertex of the edge.
        :return: None
        """
        # Verify if the edge exists
        logical_a = f"({vertex_o}, {vertex_i})" in self.E
        logical_b = f"({vertex_i}, {vertex_o})" in self.E
        if logical_a or logical_b:
            # Delete the edge from the graph
            if logical_a:
                del self.E[f"({vertex_o}, {vertex_i})"]
            else:
                del self.E[f"({vertex_i}, {vertex_o})"]

            # Delete the edge from the vertices
            self.V[vertex_o].remove(vertex_i)
            self.V[vertex_i].remove(vertex_o)
        else:
            if __name__ == '__main__':
                print(f"The edge ({vertex_o}, {vertex_i}) does not exist.")


    def add_direction_turtle(self, pos):
        self.turtle[pos] = 'f'

    def add_direction_turtle2(self, diccionario):
        self.turtle = diccionario

    def add_color(self, vertex: int, color: str):
        self.colors[vertex] = color
    def reset_colors(self):
        self.colors = dict()


    def show(self, show: bool = True):
        """
        This method is used to control the visibility of the graph in the GUI. It sets the _show_graph attribute to the
        value passed in the 'show' parameter. If 'show' is True, the graph will be displayed in the GUI; if 'show' is False,
        the graph will not be displayed.

        :param show: (bool) A flag to control the visibility of the graph in the GUI. Default is True.
        :return: None
        """
        self._show_graph = show




