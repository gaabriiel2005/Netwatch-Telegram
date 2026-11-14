# Monitor de red doméstica con bot de Telegram

Bot de Telegram personal que escanea la red local con **nmap**, guarda los equipos detectados en una base de datos **SQLite** y permite consultarlos desde el móvil.

> Proyecto en desarrollo. Pensado para uso personal sobre una red local doméstica.

## Funcionalidades

- Escaneo de la red local para listar los equipos conectados (IP y MAC).
- Base de datos SQLite con los equipos conocidos (IP, MAC, hostname, fabricante, primera y última vez visto).
- Bot de Telegram con comandos.
- Acceso restringido a un único usuario (el administrador).

## Comandos del bot

| Comando    | Descripción                                       |
|------------|---------------------------------------------------|
| `/start`   | Inicia el bot y muestra el menú                   |
| `/ayuda`   | Muestra los comandos disponibles                  |
| `/scann`   | Escanea la red y lista los equipos activos        |
| `/dbhosts` | Muestra los equipos guardados en la base de datos |

## Requisitos

- Python 3.10 o superior
- [nmap](https://nmap.org/download.html) instalado en el sistema y accesible desde el PATH
- Un bot de Telegram creado con [@BotFather](https://t.me/BotFather)
- Permisos de administrador/root al ejecutar el escaneo para obtener las direcciones MAC

## Instalación

```bash
git clone https://github.com/gaabriiel2005/Netwatch-Telegram.git
cd Netwatch-Telegram

python -m venv venv
# Linux / macOS
source venv/bin/activate
# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

## Configuración

Crea un archivo `.env` en la raíz del proyecto:

```env
TOKEN_TELEGRAM=el_token_que_te_da_botfather
ADMIN_ID=tu_id_numerico_de_telegram
```

Puedes obtener tu ID de Telegram escribiendo a un bot como [@userinfobot](https://t.me/userinfobot).

El rango de red escaneado (`192.168.1.0/24`) está actualmente fijado en el código; ajústalo a tu red.

## Uso

```bash
python main.py
```

Después abre el chat con tu bot en Telegram y envía `/start`.

## Estructura del proyecto

```
.
├── main.py   # Bot de Telegram y comandos
├── escaner_red.py      # Escaneo de red con nmap
├── basedatos.py        # Acceso a la base de datos SQLite
├── requirements.txt    # Dependencias
└── README.md
```

## Aviso

Esta herramienta está pensada únicamente para analizar redes propias o con permiso expreso de su propietario. Escanear redes ajenas sin autorización puede ser ilegal.
