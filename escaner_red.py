import nmap
from datetime import datetime as timestamp

class Scanner:
    def __init__(self,red : str):
        self.red = red
        self.equipos_vivos = {}

    def scaneo_equipos_vivos(self) :
        scan = nmap.PortScanner()
        ahora = timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
        scan.scan(hosts=self.red,arguments='-sn -n -T4')
        
        self.equipos_vivos.clear()
        contador = 1
        for host in scan.all_hosts():
            if scan[host].state() == 'up':
                name = scan[host].hostname()
                self.equipos_vivos[contador]={"ip": host,"mac":scan[host]['addresses'].get('mac', 'Este equipo')}
                contador += 1

        return self.equipos_vivos,ahora

    def texto_lista_equipos_vivos(self) -> str:
        texto = ""
        equipos = self.scaneo_equipos_vivos()
        for num,datos in equipos.items():
            texto += f"{num}. IP : {datos['ip']} | MAC : {datos['mac']}\n"
        return texto
        

def main() -> None:
    pass

if __name__ == '__main__':
    main()

