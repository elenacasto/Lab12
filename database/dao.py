from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.rifugio import Rifugio


class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    def __init__(self):
        pass

    @staticmethod
    def get_rifugi():

        conn = DBConnect.get_connection()
        cursor = conn.cursor()

        query = """
        SELECT *
        FROM rifugio
        """

        rifugi = []
        cursor.execute(query)
        for row in cursor:
            r = Rifugio(
                id=row[0],
                nome=row[1],
                localita=row[2],
                altitudine=row[3],
                capienza=row[4],
                aperto=row[5],
            )
            rifugi.append(r)

        cursor.close()
        conn.close()

        return rifugi

    @staticmethod
    def get_connessioni():

        conn = DBConnect.get_connection()
        cursor = conn.cursor()

        query = """
        SELECT *
        FROM connessione
        """

        connessioni = []
        cursor.execute(query)
        for row in cursor:
            anno_str = row[6]
            anno = int(str(anno_str).replace(",", ""))

            c = Connessione(
                id= row[0],
                id_rifugio1=row[1],
                id_rifugio2=row[2],
                distanza=row[3],
                difficolta=row[4],
                durata=row[5],
                anno=anno,
            )
            connessioni.append(c)

        cursor.close()
        conn.close()

        return connessioni
