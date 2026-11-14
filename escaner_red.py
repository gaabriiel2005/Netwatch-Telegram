import nmap
from datetime import datetime as timestamp
from basedatos import database
import asyncio
from mac_vendor_lookup import AsyncMacLookup

class Scanner:
    def __init__(self,red : str):
        self.red = red
        self.equipos_vivos = {}

    async def ver_fabricante(self,mac : str) -> str:
        if mac == 'Este equipo':
            return await self.ver_fabricante('8C:C8:4B:87:3C:59') # Aqui he puesto mi direccion mac
        try:
            fabricante = AsyncMacLookup()
            fabricante_final = await fabricante.lookup(mac)
        except Exception as e:
            return 'Fabricante desconocido'
        return fabricante_final

    async def scaneo_equipos_vivos(self) :
        scan = nmap.PortScanner()
        ahora = timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
        scan.scan(hosts=self.red,arguments='-sn -n -T4')
        
        self.equipos_vivos.clear()
        contador = 1
        for host in scan.all_hosts():
            if scan[host].state() == 'up':
                name = scan[host].hostname() or 'Unknow'
                self.equipos_vivos[contador]={"ip": host,"mac":scan[host]['addresses'].get('mac', 'Este equipo'),"name":name}
                contador += 1

        conexion = database("database.db")
        for i in self.equipos_vivos:
            fabricante = await self.ver_fabricante(str(self.equipos_vivos[i]['mac']))
            if conexion.equipo_existe(str(self.equipos_vivos[i]['mac'])):
                conexion.actualizar_uvisto(ahora,self.equipos_vivos[i]['mac'])
            else:
                conexion.insert(self.equipos_vivos[i]['ip'],self.equipos_vivos[i]['mac'],self.equipos_vivos[i]['name'],fabricante,ahora,ahora)
            
        return self.equipos_vivos,ahora

    async def texto_lista_equipos_vivos(self) -> str:
        texto = ""
        equipos,_ = await self.scaneo_equipos_vivos()
        for num,datos in equipos.items():
            texto += f"{num}. IP : {datos['ip']} | MAC : {datos['mac']}\n"
        return texto
        

def main() -> None:
    pass

if __name__ == '__main__':
    main()

