# LIBRERIAS
import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg  # Importar la librería para manejar imágenes

# MODULOS
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

# ARCHIVOS
from Basics.grafo import grafo
from Basics.PositionDictionary import posiciones
from Basics.BusquedasDictionary import ProcesosDiccionario as dictionary
from Busquedas.NInformadas.busqueda_amplitud import amplitud
from Busquedas.NInformadas.busqueda_profundida import profundida
from Busquedas.NInformadas.busqueda_coste import coste
from Busquedas.NInformadas.busqueda_iterativa import iterativa

class GraphTraversalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Búsquedas en Grafos Comuna 13")
        self.root.state('zoomed')  # Maximizar la ventana

        self.graph = self.create_graph()
        self.pos = posiciones()

        self.canvas = None
        self.show_image = tk.BooleanVar()
        self.busqueda_selected_key = ''
        self.labelDistancia = None

        # Crear un marco para contener los controles
        self.frame = ttk.Frame(self.root)
        self.frame.pack(pady=10)


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
        dictionary.load_dictionary()
        busquedasInformadas = dictionary.get_by_tipo("INFORMADA")

        self.load_busquedas(busquedasInformadas)


        # Crear etiquetas y combobox para el nodo de inicio
        ttk.Label(self.frame, text="Nodo de Inicio:").grid(row=0, column=0, padx=5, pady=5)
        self.start_combobox = ttk.Combobox(self.frame, values=nodos)
        self.start_combobox.grid(row=1, column=0, padx=5, pady=5)
        self.start_combobox.set('')

        # Crear etiquetas y combobox para el nodo de fin
        ttk.Label(self.frame, text="Nodo de Fin:").grid(row=0, column=1, padx=5, pady=5)
        self.end_combobox = ttk.Combobox(self.frame, values=nodos)
        self.end_combobox.grid(row=1, column=1, padx=5, pady=5)
        self.end_combobox.set('')

        # Crear un marco para los botones de limpiar y cerrar
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        # Botones para limpiar y cerrar, alineados en fila
        ttk.Button(button_frame, text="Limpiar", command=self.clear_entries).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cerrar", command=self.root.quit).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Buscar", command=self.show_result).pack(side=tk.LEFT, padx=5)
        
                # Checkbutton para activar/desactivar la imagen de fondo
        self.image_switch = ttk.Checkbutton(button_frame, text="Mostrar Imagen de Fondo",
                                    variable=self.show_image,
                                    command=self.toggle_image).pack(side=tk.LEFT, padx=5)


    def draw_graph(self, path_edges=None, path_nodes=None, check=False):
        if self.canvas:
            self.canvas.get_tk_widget().pack_forget()

        fig, ax = plt.subplots(figsize=(8, 6))

        start = self.start_combobox.get().strip()  # Obtener el nodo de inicio
        goal = self.end_combobox.get().strip()      # Obtener el nodo de fin
        search_type =  self.busqueda_selected_key
        
        if start and goal and search_type and check:
            self.show_result()
            return


        if self.show_image.get():
            img = mpimg.imread("resources/map.jpg")  # Ruta de la imagen
            img_extent = [-1, 1, -1, 1]  # Ajustar esto a las coordenadas que deseas usar para la imagen
            ax.imshow(img, extent=img_extent, aspect='auto', zorder=-1)  # Dibujar la imagen en el fondo


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
        self.canvas.mpl_connect("button_press_event", self.on_click)


    def show_result(self):
        start = self.start_combobox.get().strip()  # Obtener el nodo de inicio
        goal = self.end_combobox.get().strip()      # Obtener el nodo de fin
        search_type =  self.busqueda_selected_key
        result = None

        if not start:
            self.show_validation('Debe elegir un punto de inicio')
            return
        if not goal:
            self.show_validation('Debe elegir un punto final')
            return



        if search_type == "BFS":
            result = amplitud(self.graph, start, goal)
        elif search_type == "DFS":
            result = profundida(self.graph, start, goal)
        elif search_type == "UCS":
            result = coste(self.graph, start, goal)
        elif search_type == "IDDFS":
            result = iterativa(self.graph, start, goal, max_depth=3)
        else:
            self.show_validation(f'Es necesario seleccionar una busqueda')
            return 


        # Resaltar el camino encontrado
        if result:
            path_edges = [(result[i], result[i + 1]) for i in range(len(result) - 1)]
            path_nodes = result  # Los nodos del camino son los que están en `result`
            self.draw_graph(path_edges, path_nodes)

            if search_type == "UCS":
                self.show_distance(sum(self.graph[u][v]['weight'] for u, v in path_edges))
        else:
            self.show_validation('No se encontró un camino')
            return
        
    def clear_entries(self):
        # Limpiar los campos de entrada
        self.start_combobox.set('')  # Limpiar selección del Combobox de inicio
        self.end_combobox.set('')    # Limpiar selección del Combobox de fin
        self.busqueda_combobox.set('')
        self.draw_graph()  # Redibujar el grafo sin resaltado
        
        
    def show_distance(self, total_weight):
        messagebox.showinfo("Distancia Total (UCS)", f"Distancia total recorrida {self.start_combobox.get().strip()} - {self.end_combobox.get().strip()}: {total_weight} metros")
        
    def show_validation(self, mensaje):
        messagebox.showinfo("Validación", mensaje)
    # Método para manejar el evento de clic en el canvas
    def on_click(self, event):
        if event.inaxes:  # Verificar que se hizo clic dentro de los ejes del gráfico
            x, y = event.xdata, event.ydata
            print(f"Coordenadas del clic: ({x:.3f}, {y:.3f})")
            
    def load_busquedas(self, busquedas):
        ttk.Label(self.frame, text="Busquedas Informadas:").grid(row=0, column=3, padx=5, pady=5)
        # Crear el Combobox con solo los valores del diccionario
        values = list(busquedas.values())
        nombres = [obj.nombre for obj in values]
        self.busqueda_combobox = ttk.Combobox(self.frame, values=nombres)
        self.busqueda_combobox.grid(row=1, column=3, padx=5, pady=5)
        self.busqueda_combobox.set('')  # Dejar en blanco por defecto

        # Diccionario inverso para obtener la llave a partir del valor seleccionado
        value_to_key = {v.nombre: k for k, v in busquedas.items()}

        # Función para manejar la selección
        def on_selection(event):
            # Obtener el valor seleccionado
            selected_value = self.busqueda_combobox.get()
            # Obtener la clave asociada con el valor seleccionado
            self.busqueda_selected_key = value_to_key.get(selected_value, None)

        # Vincular la función a la selección del Combobox
        self.busqueda_combobox.bind("<<ComboboxSelected>>", on_selection)
        max_length = max(len(f"{k}") for k in nombres)

        # Configurar el ancho del combobox basado en la longitud calculada
        self.busqueda_combobox.config(width=max_length)

    def toggle_image(self):
        self.draw_graph(check=True)  # Redibujar el grafo cada vez que se cambie el estado del switch

def main():
    root = tk.Tk()
    app = GraphTraversalApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
