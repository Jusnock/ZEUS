import asyncio
import socket
import argparse
from rich.console import Console
from rich.table import Table
from rich.progress import Progress

# Incializamos la consola de Rich
console = Console()


class Target:
    """
    Esta clase representa la victima, se guarda la informacion y sus resultados.
    """

    def __init__(self, dominio):
        self.dominio = dominio
        self.ip = None
        self.puertos_abiertos = []

    def __str__(self):
        return f"{self.dominio} ({self.ip})"


class Scanner:
    """
    Esta clase contiene la logica asincrona.
    Donde se ejecutan todas las tereas.
    """

    def __init__(self, timeout):
        self.timeout = timeout

    async def resolver_ip(self, target):
        """Convierte el dominio a IP de forma asincrona"""
        try:
            loop = asyncio.get_running_loop()
            # getaddrinfo es bloqueante, asi que lo corremos en un "executor" aparte
            # para no frenar el loop asincrono.
            console.print(
                f"[yellow][*] Resolviendo IP para {target.dominio}...[/yellow]"
            )

            data = await loop.getaddrinfo(target.dominio, None, family=socket.AF_INET)
            target.ip = data[0][4][0]

            console.print(f"[green][+] IP Encontrada: {target.ip}[/green]")
            return True

        except Exception as e:
            console.print(f"[red][!] Error resolviendo DNS: {e}[/red]")
            return False

    async def grab_banner(self, reader):
        """
        Intenta ler los primeros bytes qeu envia el servidor.
        """
        try:
            # Esperamos maximo 1.5 seg para que el servidor diga algo.
            # # Si no habla, asumimos que es timido (o web) y cortamos.
            data = await asyncio.wait_for(reader.read(1024), timeout=1.5)
            return data.decode().strip()
        except:
            return "Desconocido / Silencioso"

    async def check_port(self, ip, port, progress, task_id):
        """
        Conecta -> Escucha Banner -> Desconecta
        """
        banner = None
        try:
            # 1. CONEXIÓN
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(ip, port), timeout=self.timeout
            )

            # 2. ESCUCHA (Banner Grabbing)
            # No cerramos todavía. Intentamos escuchar.
            # Algunos puertos web (80/443) no envían nada hasta recibir un GET,
            # así que esperamos un timeout corto.
            if port not in [80, 443]:
                banner = await self.grab_banner(reader)
            else:
                banner = "Servicio Web (HTTP/HTTPS)"

            # 3. CIERRE
            writer.close()
            try:
                await writer.wait_closed()
            except:
                pass

            progress.update(task_id, advance=1)
            # Devolvemos la TUPLA (Puerto, Banner)
            return (port, banner)

        except:
            # Falla (Cerrado/Timeout)
            progress.update(task_id, advance=1)
            return None

    async def escanear_puertos(self, target, puertos):
        if not target.ip:
            return
        console.print(f"\n[bold cyan]Iniciando Escaneo en {target.ip}[/bold cyan]")
        console.print(f"[dim]Timeouts: Conexion {self.timeout}s | Banner 1.5s [/dim]")

        tareas = []

        with Progress() as progress:
            task_id = progress.add_task(
                "[cyan]Escanenado y Analizando...", total=len(puertos)
            )

            for port in puertos:
                tareas.append(self.check_port(target.ip, port, progress, task_id))

            resultados = await asyncio.gather(*tareas)

        # Filtramos los None y guardamos las tuplas (puerto, banner)
        target.abiertos = [r for r in resultados if r is not None]


BANNER = r"""
[bold green]
███████╗███████╗██╗   ██╗███████╗
╚══███╔╝██╔════╝██║   ██║██╔════╝
  ███╔╝ █████╗  ██║   ██║███████╗
 ███╔╝  ██╔══╝  ██║   ██║╚════██║
███████╗███████╗╚██████╔╝███████║
╚══════╝╚══════╝ ╚═════╝ ╚══════╝
[/bold green]
"""


async def main():
    # 1. CONFIGURACION DE ARGUMENTOS (CLI)

    console.print(BANNER)
    parser = argparse.ArgumentParser(
        description="ZEUS: Motor de Reconocimiento Asíncrono",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-t", "--target", required=True, help="Dominio objetivo")
    parser.add_argument(
        "-p", "--ports", default="1-1000", help="Rango de puertos (ej: 22,80 o 1-100)"
    )
    parser.add_argument("--timeout", type=float, default=1.0, help="Timeut de conexion")

    args = parser.parse_args()

    # 2. PARSEO DE PUERTOS
    # Permite "1-1000" o "22,80,443"

    lista_puertos = []

    if "-" in args.ports:
        inicio, fin = map(int, args.ports.split("-"))
        lista_puertos = range(inicio, fin + 1)
    else:
        lista_puertos = [int(p) for p in args.ports.split(",")]

    # 3. INICIO DEL MOTOR
    objetivo = Target(args.target)
    motor = Scanner(timeout=args.timeout)

    if await motor.resolver_ip(objetivo):
        await motor.escanear_puertos(objetivo, lista_puertos)

        # 4. REPORTE FINAL MEJORADO
        table = Table(title=f"Resultados para {objetivo.dominio}")
        table.add_column("Puerto", justify="right", style="cyan", no_wrap=True)
        table.add_column("Estado", style="green")
        table.add_column("Servicio / Banner", style="magenta")  # ¡Nueva Columna!

        if objetivo.abiertos:
            # Ordenamos por número de puerto para que se vea lindo
            for puerto, banner in sorted(objetivo.abiertos, key=lambda x: x[0]):
                table.add_row(str(puerto), "ABIERTO 🔓", banner)
        else:
            table.add_row("-", "Ningún puerto abierto", "-")

        console.print(table)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[red][!] Interrumpido por el usuario[/red]")
