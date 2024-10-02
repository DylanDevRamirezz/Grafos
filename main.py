# LIBRERIAS
import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt

# MODULOS
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

# ARCHIVOS
from grafo import grafo
from busqueda_amplitud import amplitud
from busqueda_profundida import profundida
from busqueda_coste import coste
from busqueda_iterativa import iterativa

class GraphTraversalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Búsquedas en Grafos Comuna 13")
        self.root.state('zoomed')  # Maximizar la ventana

        self.graph = self.create_graph()
        self.pos = nx.spring_layout(self.graph, k=1)  # Posiciones de los nodos para el dibujo
        self.canvas = None

        self.labelDistancia = None

        self.create_widgets()
        self.draw_graph()

    def create_graph(self):
        g = nx.Graph()
        graph_data = grafo()  # Obtener el diccionario de adyacencia

        # Agregar las aristas sin duplicarlas
        for node, neighbors in graph_data.items():
            for neighbor, weight in neighbors.items():  # Aquí usamos items() para obtener el vecino y el peso
                g.add_edge(node, neighbor, weight=weight)  # Añadir la arista con peso

        return g


    def create_widgets(self):
        # Opciones para los nodos
        nodos = list(grafo().keys())
        
        # OPCIONES PARA BUSQUEDA
        busquedas = {   'BFS'   : 'Búsqueda en Amplitud',
                        'DFS'   : 'Búsqueda en Profundidad',
                        'UCS'   : 'Búsqueda de Coste Uniforme',
                        'IDDFS' : 'Búsqueda en Profundidad Iterativa' }

        # Crear un marco para contener los controles
        frame = ttk.Frame(self.root)
        frame.pack(pady=10)

        # Crear etiquetas y combobox para el nodo de inicio
        ttk.Label(frame, text="Nodo de Inicio:").grid(row=0, column=0, padx=5, pady=5)
        self.start_combobox = ttk.Combobox(frame, values=nodos)
        self.start_combobox.grid(row=1, column=0, padx=5, pady=5)
        self.start_combobox.set('')

        # Crear etiquetas y combobox para el nodo de fin
        ttk.Label(frame, text="Nodo de Fin:").grid(row=0, column=1, padx=5, pady=5)
        self.end_combobox = ttk.Combobox(frame, values=nodos)
        self.end_combobox.grid(row=1, column=1, padx=5, pady=5)
        self.end_combobox.set('')

        # Crear botones para cada tipo de búsqueda en formato 2x2
        # ttk.Button(frame, text="Búsqueda en Amplitud (BFS)", command=lambda: self.show_result("BFS")).grid(row=2, column=0, padx=5, pady=5)
        # ttk.Button(frame, text="Búsqueda en Profundidad (DFS)", command=lambda: self.show_result("DFS")).grid(row=2, column=1, padx=5, pady=5)
        # ttk.Button(frame, text="Búsqueda de Coste Uniforme (UCS)", command=lambda: self.show_result("UCS")).grid(row=3, column=0, padx=5, pady=5)
        # ttk.Button(frame, text="Búsqueda en Profundidad Iterativa (IDDFS)", command=lambda: self.show_result("IDDFS")).grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Busquedas Informadas:").grid(row=0, column=3, padx=5, pady=5)
        # Crear el Combobox con solo los valores del diccionario
        values = list(busquedas.values())
        self.busqueda_combobox = ttk.Combobox(frame, values=values)
        self.busqueda_combobox.grid(row=1, column=3, padx=5, pady=5)
        self.busqueda_combobox.set('')  # Dejar en blanco por defecto

        # Diccionario inverso para obtener la llave a partir del valor seleccionado
        value_to_key = {v: k for k, v in busquedas.items()}

        # Función para manejar la selección
        def on_selection(event):
            # Obtener el valor seleccionado
            selected_value = self.busqueda_combobox.get()
            # Obtener la clave asociada con el valor seleccionado
            self.busqueda_selected_key = value_to_key.get(selected_value, None)

        # Vincular la función a la selección del Combobox
        self.busqueda_combobox.bind("<<ComboboxSelected>>", on_selection)
        max_length = max(len(f"{k}: {v}") for k, v in busquedas.items())

        # Configurar el ancho del combobox basado en la longitud calculada
        self.busqueda_combobox.config(width=max_length)

        # Crear un marco para los botones de limpiar y cerrar
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        # Botones para limpiar y cerrar, alineados en fila
        ttk.Button(button_frame, text="Limpiar", command=self.clear_entries).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cerrar", command=self.root.quit).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Buscar", command=self.show_result).pack(side=tk.LEFT, padx=5)


    def draw_graph(self, path_edges=None, path_nodes=None):
        if self.canvas:
            self.canvas.get_tk_widget().pack_forget()

        fig, ax = plt.subplots(figsize=(8, 6))

        nx.draw(self.graph, self.pos, with_labels=True, node_color='orange', node_size=1000, font_size=8,
                font_weight='bold', ax=ax)
        if path_nodes:
            nx.draw_networkx_nodes(self.graph, self.pos, nodelist=path_nodes, node_color="green", node_size=1000)

        if path_edges:
            nx.draw_networkx_edges(self.graph, self.pos, edgelist=path_edges, width=5, edge_color='r', ax=ax)

        nx.draw_networkx_edge_labels(self.graph, self.pos, edge_labels=nx.get_edge_attributes(self.graph, 'weight'), ax=ax)


        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def show_result(self):
        start = self.start_combobox.get().strip()  # Obtener el nodo de inicio
        goal = self.end_combobox.get().strip()      # Obtener el nodo de fin
        search_type =  self.busqueda_selected_key

        if search_type == "BFS":
            result = amplitud(self.graph, start, goal)
        elif search_type == "DFS":
            result = profundida(self.graph, start, goal)
        elif search_type == "UCS":
            result = coste(self.graph, start, goal)
        elif search_type == "IDDFS":
            result = iterativa(self.graph, start, goal, max_depth=3)

        # Resaltar el camino encontrado
        if result:
            path_edges = [(result[i], result[i + 1]) for i in range(len(result) - 1)]
            path_nodes = result  # Los nodos del camino son los que están en `result`
            self.draw_graph(path_edges, path_nodes)

            if search_type == "UCS":
                self.show_distance(sum(self.graph[u][v]['weight'] for u, v in path_edges))
        else:
            self.draw_graph()  # Redibujar el grafo sin resaltado aristas si no se encontró un camino

    def clear_entries(self):
        # Limpiar los campos de entrada
        self.start_combobox.set('')  # Limpiar selección del Combobox de inicio
        self.end_combobox.set('')    # Limpiar selección del Combobox de fin
        self.draw_graph()  # Redibujar el grafo sin resaltado
        
        
    def show_distance(self, total_weight):
        messagebox.showinfo("Distancia Total (UCS)", f"Distancia total recorrida {self.start_combobox.get().strip()} - {self.end_combobox.get().strip()}: {total_weight} metros")


def main():
    root = tk.Tk()
    app = GraphTraversalApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
