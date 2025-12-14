import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        self.G = nx.Graph()

    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        self.G.clear()

        fattore_difficolta = {
            "facile" : 1,
            "media" : 1.5,
            "difficile" : 2
        }

        self.rifugi = {}

        rifugi = DAO.get_rifugi()
        for r in rifugi:
            self.rifugi[r.id] = r

        connessioni = DAO.get_connessioni()
        for c in connessioni:
            if c.anno <= year:
                rif1 = self.rifugi.get(c.id_rifugio1)
                rif2 = self.rifugi.get(c.id_rifugio2)

                fattore = fattore_difficolta.get(c.difficolta)
                weight = float(c.distanza) * fattore

                if rif1 and rif2:
                    if rif1 not in self.G:
                        self.G.add_node(rif1)
                    if rif2 not in self.G:
                        self.G.add_node(rif2)

                    self.G.add_edge(rif1,rif2, weight=weight)

    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """

        if self.G.number_of_edges() == 0:
            return None, None

        pesi = [data['weight'] for _,_,data in self.G.edges(data=True)]

        peso_min = min(pesi)
        peso_max = max(pesi)

        return peso_min, peso_max

    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """

        count_min = 0
        count_max = 0

        for _,_,data in self.G.edges(data=True):
            if data['weight'] < soglia:
                count_min += 1
            if data['weight'] > soglia:
                count_max += 1

        return count_min, count_max

    """Implementare la parte di ricerca del cammino minimo"""
    # TODO
