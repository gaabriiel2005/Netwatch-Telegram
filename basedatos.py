import sqlite3
from datetime import datetime as timestamp

class database:
    def __init__(self,database_name : str):
        self.database_name = database_name

    def conetar(self):
        with sqlite3.connect(self.database_name) as con:
            con.execute("PRAGMA foreign_keys = ON;") # Las clas foreing key y los delete on cascade vienen descativadas cuando abres una conexión nueva asi que ejecutamos esto cada vez que nos conectamos
            cur = con.cursor()
        return con,cur

    def insert(self,ip : str,mac : str,name_host : str,fabricante : str,pvisto : timestamp,uvisto : timestamp) -> None:
        if not self.equipo_existe(mac):
            data = (ip,mac,name_host,fabricante,pvisto,uvisto)
            con,cur = self.conetar()
            cur.execute("INSERT INTO equipos (direccion_ip,mac,nombre_host,fabricante,primer_visto,ultimo_visto) VALUES (?,?,?,?,?,?)",data)
            con.commit()
        return None

    def select(self,opcion : str,filtro = "") -> list:
        _,cur = self.conetar()
        res = cur.execute(f"SELECT {opcion} From equipos {filtro}")
        return res.fetchall()

    def equipo_existe(self,mac) -> bool:
        if self.select("mac",f"WHERE mac = '{mac}'"):
            return True
        return False

    def actualizar_uvisto(self,uvisto : timestamp,mac : str):
        if self.equipo_existe(mac):
            con,cur = self.conetar()
            cur.execute(f"UPDATE equipos SET ultimo_visto = '{uvisto}' WHERE mac = '{mac}'")
            con.commit()

def main():
    # conexion = database("database.db")
    # ahora = timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    # conexion.insert("192.168.1.40/24","02:00:00:1A:2B:3F","PC 1","Microsoft",ahora,ahora)
    # print(conexion.select("*"))
    # print(conexion.equipo_existe("02:00:00:1A:2B:3C"))
    # print(conexion.equipo_existe("02:00:00:1A:2B:4C"))
    # conexion.actualizar_uvisto(ahora,"02:00:00:1A:2B:3C")
    pass

if __name__ == '__main__':
    main()