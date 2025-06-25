import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMapRetailer = {}
        self._pesoBest = 0
        self._sol_Best = []

    def getAllNazioni(self):
        return DAO.getAllNazioni()

    def buildGraph(self, nazione, anno):
        self._graph.clear()
        nodes = DAO.getAllNodes(nazione)

        for n in nodes:
            self._idMapRetailer[n.Retailer_code] = n

        for n in nodes:
            self._graph.add_node(n)

        self.addAllArchi(anno, nazione)

    def addAllArchi(self, anno, nazione):
        archi = DAO.getAllArchi(anno, nazione, self._idMapRetailer)
        for arco in archi:
            a1 = arco[0]
            a2 = arco[1]
            self._graph.add_edge(a1, a2, weight=arco[2])

    def getNumNodi(self):
        return self._graph.number_of_nodes()

    def getNumArchi(self):
        return self._graph.number_of_edges()

    def getVolumi(self):
        lista_volumi = []
        for nodo in self._graph.nodes:
            vicini = self._graph.neighbors(nodo)
            peso = 0
            for v in vicini:
                peso += self._graph[nodo][v]["weight"]
            lista_volumi.append((nodo, peso))
        #il peso è il secondo valore della tupla,
        #io devo ordinarli in modo decrescente per peso
        lista_volumi.sort(key=lambda x: x[1], reverse=True)
        return lista_volumi


    def _ricorsione(self,parziale, N):
        #condizione terminale
        if len(parziale)==N:
            if self._graph.has_edge(parziale[-1],parziale[0]): #se dall'ultimo nodo posso ritornare al primo
                ciclo = parziale + [parziale[0]]
                peso = self.getPeso(ciclo)
                if peso > self._pesoBest:
                    self._pesoBest = peso
                    self._sol_Best = copy.deepcopy(ciclo)
                return

        vicini = self._graph.neighbors(parziale[-1])
        for v in vicini:
            if v not in parziale and self._graph.has_edge(parziale[-1], v):
                parziale.append(v)
                self._ricorsione(parziale, N)
                parziale.pop()


    def getPercorso(self, N):
       #Inizializza il miglior peso e la migliore soluzione
        self._pesoBest = 0
        self._sol_Best = []
        parziale = []
       #Per ogni nodo del grafo, prova ad avviare una ricerca ricorsiva a partire da quel nodo
        for n in self._graph.nodes:
            parziale.append(n)
            self._ricorsione(parziale, N)
            parziale.pop()
        #Alla fine, restituisce il miglior ciclo trovato e il suo peso
        return self._sol_Best, self._pesoBest

    def getPesoArco(self, a, b):
        return self._graph[a][b]["weight"]

    def getPeso(self, parziale):
        peso = 0
        for i in range(0, len(parziale)-1):
            peso += self._graph[parziale[i]][parziale[i+1]]["weight"]
        return peso