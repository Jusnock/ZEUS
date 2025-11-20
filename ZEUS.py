import asyncio
import socket
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
    def __init__(self):
        self.timeout = 1.0

    async def resolver_ip(self, target):
        """Convierte el dominio a IP de forma asincrona"""
        try:
            loop=asyncio.get_running_loop()
            # getaddrinfo es bloqueante, asi que lo corremos en un "executor" aparte
            # para no frenar el loop asincrono.
            console.print(f"[yellow][*] Resolviendo IP para {target.dominio}...[/yellow]")
            data = await loop.getaddrinfo(target.dominio, None, family=socket.AF_INET)
            target.ip = data[0][4][0]
            console.print(f"[green][+] IP Encontrada: {target.ip}[/green]")
            return True
        except Exception as e:
            console.print(f"[red][!] Error resolviendo DNS: {e}[/red]")
            return False
        
    async def check_port(self, ip, port, progress, task_id):
        """Revisa un solo puerto (micro-tarea)"""
        conn= asyncio.open_connection(ip, port)

        try:
            # Intentamos conectar con timeout
            reader , writer = await asyncio.wait_for(conn, timeout=self.timeout)

            # Si llegamos aqui, esta abierto
            writer.close()
            await writer.wait_closed()

            # Actualizamos la barra de progreso
            progress.update(task_id, advance=1)
            return port
        
        except:
            # Si falla (este cerrado o timeout), simplemente avanzamos la barra
            progress.update(task_id, advance=1)
            return None
        
    async def escanear_puertos(self, target, puertos):
        """Escaneo masivo de puertos"""

        if not target.ip:
            console.print("[red] No hay IP. Saltando escaneo.[/red]")
            return
        
        console.print(f"\n[bold cyan]Iniciando escaneo masivo en {target.ip}[/bold cyan]")

        tareas = []

        # Usamos 'rich.progress' para crear una barra de carga
        with Progress() as progress:
            # Creamos la tarea visual
            task_id = progress.add_task("[cyan] Escanenado puertos...", total=len(puertos))

            # Preparamos las 100, 500 o 1000 corrutinas
            for port in puertos:
                # Le pasamos 'progress' y 'task_id' para cada micro-tarea actualice la barra
                tareas.append(self.check_port(target.ip, port, progress, task_id))

            # Lanzamos todo a la vez
            resultados = await asyncio.gather(*tareas)

        # Filtramos ñps reultados (quitamos los None)
        target.puertos_abiertos = [p for p in resultados if p is not None]

async def main():
    # 1. Configuracion
    dominio = "nmap.org"
    # Vamos a escaenar los primeros 1000 puertos para probar la velocidad
    lista_puertos = range(1, 1000)

    # 2. Instanciamos los objetos
    objetivo = Target(dominio)
    motor = Scanner()

    # 3. Ejecucion (paso a paso asincrono)
    console.rule(f"[bold blue]PROYECTO ZEUS V0.1[/bold blue]")

    # Paso A: DNS
    if await motor.resolver_ip(objetivo):

        # Paso B: Escaneo de Puertos
        await motor.escanear_puertos(objetivo, lista_puertos)

        # Paso C: Reporte final
        table = Table(title="Resultados para {objetivo.dominio}")
        table.add_column("Puerto", justify="right", style="cyan", no_wrap=True)
        table.add_column("Estado", style= "green")

        if objetivo.puertos_abiertos:
            for puerto in objetivo.puertos_abiertos:
                table.add_row(str(puerto), "ABIERTO 🔓")
        else:
            table.add_row("-", "Ningun puerto abierto encontrado")

        console.print(table)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[red][!] Interrumpido por el usuario[/red]")
