class Busqueda:
    def __init__(self, tipo,  nombre):
        self.tipo = tipo
        self.nombre = nombre

class ProcesosDiccionario:
    busquedas = {}

    @classmethod
    def load_dictionary(cls):
        # INFORMADAS
        cls.add("BFS", "NOINFORMADA", "Búsqueda en amplitud")
        cls.add("DFS", "NOINFORMADA", "Búsqueda en profundidad")
        cls.add("UCS", "NOINFORMADA", "Búsqueda de coste uniforme")
        cls.add("IDDFS", "NOINFORMADA", "Búsqueda de profundidad iterativa")
        # NO INFORMADAS
        
        cls.add("GRD", "INFORMADA", "Búsqueda voráz")
        cls.add("DFS", "INFORMADA", "Búsqueda de dependencia iterativa")
        cls.add("UCS", "INFORMADA", "Búsqueda simplificada")
        cls.add("IDDFS", "INFORMADA", "Búsqueda de profundidad iterativa")

    @classmethod
    def add(cls, key, tipo, nombre):
        cls.busquedas[key] = Busqueda(tipo, nombre)

    @classmethod
    def get_by_tipo(cls, tipo):
        """
        Retorna un diccionario filtrado por el tipo especificado.
        
        :param tipo: Tipo del proceso a filtrar (e.g., "MENU", "PROCESO", "CATALOGO", "ENTIDAD").
        :return: Diccionario de procesos filtrados por el tipo especificado.
        """
        return {k: v for k, v in cls.busquedas.items() if v.tipo == tipo}


