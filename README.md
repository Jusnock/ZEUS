<div align="center">
```text
███████╗███████╗██╗   ██╗███████╗
╚══███╔╝██╔════╝██║   ██║██╔════╝
  ███╔╝ █████╗  ██║   ██║███████╗
 ███╔╝  ██╔══╝  ██║   ██║╚════██║
███████╗███████╗╚██████╔╝███████║
╚══════╝╚══════╝ ╚═════╝ ╚══════╝
```
</div>

<h1 align="center">⚡ ZEUS: Asynchronous Reconnaissance Engine</h1>
<p align="center"><i>"Velocidad de rayo, precisión de dios."</i></p>

---

## Contenido

- [Arquitectura & Filosofía](#arquitectura--filosofía)
- [Características](#características-v02---beta)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Instalación y Configuración](#instalación-y-configuración)
- [Modo de Uso](#modo-de-uso)
- [Guía de Estudio (Arquitectura Interna)](#guía-de-estudio-arquitectura-interna)
- [Uso de CLI y ejemplo de encabezado ASCII](#uso-de-cli-y-ejemplo-de-encabezado-ascii)
- [Advertencia Legal](#advertencia-legal-disclaimer)

---

ZEUS es un motor de reconocimiento de puertos y redes de próxima generación escrito en Python moderno.

A diferencia de los escáneres tradicionales que operan secuencialmente o mediante hilos pesados, ZEUS aprovecha el poder del Bucle de Eventos (`asyncio`) para realizar miles de operaciones de red concurrentes en un solo hilo de ejecución.

---

## Arquitectura & Filosofía

ZEUS representa un cambio de paradigma respecto a las herramientas de scripting convencionales. Su diseño se basa en tres pilares fundamentales:

### 1. Motor Asíncrono (Non-Blocking I/O)

- **Tecnología:** `asyncio` nativo de Python 3.
- **Rendimiento:** Miles de conexiones simultáneas con mínimo uso de CPU.
- **Analogía:** No es un cajero atendiendo una fila uno por uno; es un pulpo gestionando mil teléfonos a la vez.

### 2. Diseño Orientado a Objetos (POO)

- **Target:** Encapsula el estado, datos y resultados de la víctima (IP, dominio, puertos, banners).
- **Scanner:** Encapsula la lógica de negocio, resolución DNS y rutinas de conexión.

### 3. Experiencia de Usuario (UX)

- Impulsado por la librería `rich` para una interfaz de terminal moderna con barras de progreso, tablas dinámicas y colores semánticos.

---

## Características (v0.2 - Beta)

Esta versión introduce inteligencia de servicios y control total:

- **Banner Grabbing Asíncrono:** (NUEVO) ZEUS no solo toca la puerta, ahora "escucha" la respuesta del servicio (SSH, FTP, SMTP, etc.) sin bloquear el escaneo.
- **Interfaz de Comandos (CLI):** (NUEVO) Control total mediante argumentos (`-t`, `-p`, `--timeout`).
- **Parsing de Puertos Inteligente:** (NUEVO) Soporta rangos (`1-1000`) y listas específicas (`22,80,443`).
- **Resolución DNS Asíncrona:** Convierte dominios a IPs utilizando el `Event Loop`.
- **Escaneo Masivo:** Capaz de escanear los 65535 puertos en tiempos récord.

---

## Tecnologías Utilizadas

- **Python 3.8+**: Sintaxis moderna (`async/await`).
- **asyncio**: Concurrencia nativa y manejo de `StreamReaders`.
- **rich**: Texto enriquecido y formateo en terminal.
- **argparse**: Gestión profesional de argumentos de línea de comandos.

## Requisitos

- Python 3.8+ recomedado
- `rich` para UI de terminal: incluido en `requirements.txt`

---

## Instalación y Configuración

Se recomienda el uso de un entorno virtual (`venv`) para mantener limpio tu sistema.

```bash
# Clona el repositorio
git clone https://github.com/Jusnock/ZEUS.git
cd ZEUS

# Crea y activa el entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux / Mac

# En Windows
# python -m venv venv
# venv\Scripts\activate

# Instala las dependencias (recomendado: usar requirements.txt)
pip install -r requirements.txt

```

## Modo de Uso

ZEUS v0.2 es totalmente configurable desde la terminal.

### Sintaxis Básica

```bash
python3 zeus.py -t <OBJETIVO> [OPCIONES]
```

## Salida esperada

```text
[*] Resolviendo IP para scanme.nmap.org...
[+] IP Encontrada: 45.33.32.156

Iniciando Escaneo Masivo en 45.33.32.156
Escaneando y Analizando... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:02

Resultados para scanme.nmap.org
┏━━━━━━━━╤━━━━━━━━━━━━━━╤━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Puerto │ Estado       ┃ Servicio / Banner            ┃
┡━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│     22 │ ABIERTO 🔓   │ SSH-2.0-OpenSSH_7.4          │
│     80 │ ABIERTO 🔓   │ Servicio Web (HTTP/HTTPS)    │
│   9929 │ ABIERTO 🔓   │ nping-echo                   │
└────────┴──────────────┴──────────────────────────────┘
```

## Guía de Estudio (Arquitectura Interna)

### 1. El Event Loop (Bucle de Eventos)

ZEUS inicia un "Director de Orquesta" (Event Loop). Cuando una función necesita esperar, cede el control al bucle, eliminando tiempos muertos y permitiendo que otras tareas (I/O) sigan ejecutándose en el mismo hilo.

### 2. Oídos Asíncronos (StreamReader)

En la v0.2, utilizamos `reader.read(1024)`. A diferencia de `socket.recv()`, que bloquea todo el programa hasta que lleguen datos, `reader` permite a ZEUS "dejar la oreja puesta" en un puerto esperando datos mientras simultáneamente toca el timbre en otros 100 puertos. Esto mejora la latencia y el rendimiento en escaneos masivos.

### 3. Paralelismo con `asyncio.gather`

`asyncio.gather` es clave para la velocidad y escala del motor: toma una lista de corrutinas y las lanza simultáneamente en el bucle.

```python
# Python
await asyncio.gather(*tareas)
```

Toma miles de micro-tareas y las ejecuta concurrentemente, reduciendo drásticamente el tiempo total del escaneo respecto a un enfoque secuencial.

### 4. Integración CLI + POO

Los argumentos del CLI (por ejemplo `args.timeout`) se inyectan en los objetos del motor para que la configuración del usuario modifique el comportamiento en tiempo de ejecución. Esto hace que la lógica del escáner sea configurable y reutilizable:

```python
# Ejemplo
parser.add_argument("--timeout", type=int, default=3)

# Más tarde, en el código:
scanner = Scanner(timeout=args.timeout)
```

Esto permite que parámetros del CLI afecten directamente a la instancia del `Scanner`, manteniendo separación de responsabilidades y fácil testeo.

## ⚠️ Advertencia Legal (Disclaimer)

ZEUS es una herramienta ofensiva de alta velocidad.

> **Este software ha sido creado únicamente con fines educativos y de investigación académica. El uso de este escáner contra redes, servidores o infraestructuras sin el consentimiento explícito y por escrito de sus propietarios es ilegal y puede ser penalizado severamente por las leyes locales e internacionales.**
>
> El autor y los contribuyentes no se hacen responsables de daños, interrupciones de servicio o consecuencias legales derivadas del uso irresponsable de esta herramienta.

**Úsalo con sabiduría. Úsalo éticamente.**

---

## Contribuciones

Contribuciones son bienvenidas. Abre un issue si encuentras un bug o quieres añadir una mejora. Si quieres contribuir con código, crea un fork y abre un Pull Request explicando los cambios.
