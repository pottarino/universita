# -*- coding: utf-8 -*-
"""
Libreria per algoritmi 2

@author: potta
"""

import matplotlib.pyplot as plt
import networkx as nx
import random as r


class grafo:
    #Classe grafo. questa NON dovrebbe essere utilizzata per istanziare grafi
    def __init__(self, nodi, archi, oriented=False, cappi=False):

        archi_set = set()

        for a, b in archi:

            if not cappi and a == b:
                continue

            arco = (a, b) if oriented else tuple(sorted((a, b)))
            archi_set.add(arco)

        self.archi = list(archi_set)
        self.nodi = list(nodi)
        self.oriented = oriented

        self.numeroNodi = len(self.nodi)
        self.numeroArchi = len(self.archi)

        limite = (self.numeroNodi * self.numeroNodi) / (1 + (not oriented))
        assert self.numeroArchi <= limite


    def plot(self):
        #plotta un grafo
        G = nx.DiGraph() if self.oriented else nx.Graph()
        G.add_nodes_from(self.nodi)
        G.add_edges_from(self.archi)

        pos = nx.spring_layout(G)

        plt.figure(figsize=(8,6))

        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color="lightblue",
            node_size=2000,
            arrowstyle='-|>' if self.oriented else None,
            arrowsize=20 if self.oriented else 0
        )

        plt.show()
        


class grafoMatriciale(grafo):
    #grafo con struttura di salvataggio di una matrice
    def __init__(self, matrice, oriented=False):

        n = len(matrice)

        archi = [
            (i, j)
            for i in range(n)
            for j in range(n)
            if matrice[i][j] == 1
        ]

        super().__init__(range(n), archi, oriented)

        self.matrice = matrice

    def __iter__(self):
        return self.matrice.__iter__()
    

    @staticmethod
    def casuale(n, p=0.5, oriented=False):
        #restituisce un grafo con matrice casuale
        #è possibile regolare la probabilità che ci siano archi tra due nodi
        #è possibile decidere se riceverlo orientato o meno
        matrice = [[0]*n for _ in range(n)]

        if oriented:

            for i in range(n):
                for j in range(n):
                    if i != j and r.random() < p:
                        matrice[i][j] = 1

        else:

            for i in range(n):
                for j in range(i+1, n):

                    if r.random() < p:
                        matrice[i][j] = matrice[j][i] = 1

        return grafoMatriciale(matrice, oriented)


    @staticmethod
    def tuttiGrafi(n):
        #MOLTO MOLTO MOOOOOOOOLTO LENTO O(2^(n^2))
        #usare con cautela
        edges = [(i,j) for i in range(n) for j in range(i+1,n)]
        m = len(edges)

        for mask in range(1 << m):

            A = [[0]*n for _ in range(n)]

            for k in range(m):

                if mask & (1<<k):

                    i,j = edges[k]
                    A[i][j] = A[j][i] = 1

            yield grafoMatriciale(A)


class grafoLista(grafo):
    #Grafo implementato con liste di adiacenza
    def __init__(self, lista, oriented=False, cappi=False):

        nodi = range(len(lista))

        archi = []

        nuova_lista = []

        for i, vicini in enumerate(lista):

            puliti = [v for v in vicini if cappi or v != i]

            nuova_lista.append(puliti)

            for v in puliti:
                archi.append((i,v))

        super().__init__(nodi, archi, oriented)

        self.lista = nuova_lista
        
        
    def __iter__(self):
        return self.lista.__iter__()
    

    @staticmethod
    def casuale(n, p=0.5, oriented=False):
        #restituisce un grafo implementato con liste di adiacenza casuale
        #è possibile regolare la probabilità che tra due nodi ci siano archi
        #è possibile scegliere se farlo orientato o meno
        lista = [[] for _ in range(n)]

        if oriented:

            for i in range(n):
                for j in range(n):
                    if r.random() < p:
                        lista[i].append(j)

        else:

            for i in range(n):
                for j in range(i+1,n):

                    if r.random() < p:

                        lista[i].append(j)
                        lista[j].append(i)

        return grafoLista(lista, oriented)


class grafoDizionario(grafo):
    #grafo con dizionario
    def __init__(self, dizionario, oriented=False):

        nodi = list(dizionario.keys())

        archi = [
            (nodo, vicino)
            for nodo, vicini in dizionario.items()
            for vicino in vicini
        ]

        super().__init__(nodi, archi, oriented)

        self.dizionario = dizionario
        
    def __iter__(self):
        return self.dizionario.__iter__()


if __name__ == "__main__":
    pass