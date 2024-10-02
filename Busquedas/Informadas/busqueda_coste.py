import heapq

def coste(grafo, inicio, objetivo):
    cola_prioridad = [(0, inicio, [])]
    visitados = set()

    while cola_prioridad:
        (coste_actual, nodo_actual, camino) = heapq.heappop(cola_prioridad)

        if nodo_actual in visitados:
            continue

        visitados.add(nodo_actual)
        camino = camino + [nodo_actual]

        if nodo_actual == objetivo:
            return camino

        for vecino, distancia in grafo[nodo_actual].items():
            if vecino not in visitados:
                heapq.heappush(cola_prioridad, (coste_actual + distancia['weight'], vecino, camino))

    return None
