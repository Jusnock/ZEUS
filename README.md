⚡ ZEUS: Asynchronous Reconnaissance Engine

```text
███████╗███████╗██╗   ██╗███████╗
╚══███╔╝██╔════╝██║   ██║██╔════╝
  ███╔╝ █████╗  ██║   ██║███████╗
 ███╔╝  ██╔══╝  ██║   ██║╚════██║
███████╗███████╗╚██████╔╝███████║
╚══════╝╚══════╝ ╚═════╝ ╚══════╝
"Velocidad de rayo, precisión de dios."

ZEUS es un motor de reconocimiento de puertos y redes de próxima generación escrito en Python moderno.

A diferencia de los escáneres tradicionales que operan secuencialmente o mediante hilos pesados ("threading"), ZEUS aprovecha el poder del Bucle de Eventos (Event Loop) y la Programación Asíncrona (asyncio) para realizar miles de operaciones de red concurrentes en un solo hilo de ejecución.

🏛️ Arquitectura & Filosofía
ZEUS representa un cambio de paradigma respecto a las herramientas de scripting convencionales. Su diseño se basa en tres pilares fundamentales:

1. El Motor Asíncrono (Non-Blocking I/O) ⚡
Mientras que un escáner tradicional (socket bloqueante) espera ociosamente a que un servidor responda, ZEUS dispara miles de sondas y continúa trabajando.

Tecnología: asyncio nativo de Python 3.

Rendimiento: Capaz de manejar miles de conexiones simultáneas con un overhead de CPU mínimo.

Analogía: No es un cajero atendiendo una fila uno por uno; es un pulpo gestionando mil teléfonos a la vez.

2. Diseño Orientado a Objetos (OOP) 🧩
El código está desacoplado en entidades lógicas para máxima escalabilidad:

Target: Encapsula el estado, datos y resultados de la víctima (IP, dominio, puertos abiertos).

Scanner: Encapsula la lógica de negocio, resolución DNS y rutinas de conexión.

3. Experiencia de Usuario (UX) Profesional 🎨
Impulsado por la librería rich, ZEUS ofrece una interfaz de terminal moderna con barras de progreso thread-safe y tablas formateadas dinámicamente.

🚀 Características (v0.1)
Resolución DNS Asíncrona: Convierte dominios a IPs utilizando el Event Loop sin bloquear el proceso principal.

Escaneo de Puertos Masivo: Escanea rangos completos (1-1000+) en segundos gracias a asyncio.gather.

Barra de Progreso Atómica: Visualización precisa del avance usando Context Managers.

Reporte Tabular: Salida limpia y estructurada lista para análisis.

Timeouts Agresivos: Optimizado para redes rápidas y descarte inmediato de hosts muertos.

🛠️ Tecnologías Utilizadas
Este proyecto es una demostración avanzada de Python moderno:

Python 3.8+: Sintaxis moderna (async/await).

asyncio: Librería estándar para concurrencia.

rich: Para texto enriquecido y formateo en terminal.

socket: Modo no bloqueante para conexiones de bajo nivel.

⚙️ Instalación y Configuración
Se recomienda el uso de un entorno virtual (venv) para mantener limpio tu sistema.

Clona el repositorio:

Bash

git clone [https://github.com/TU_USUARIO/ZEUS.git](https://github.com/TU_USUARIO/ZEUS.git)
cd ZEUS
Crea y activa el entorno virtual:

Bash

# Linux / Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
Instala las dependencias:

Bash

pip install rich
⚡ Modo de Uso
Actualmente (v0.1 Alpha), el objetivo se configura directamente en el main para propósitos de depuración y aprendizaje.

Ejecución Básica:

Bash

python3 zeus.py
Salida Esperada
Verás la resolución de IP asíncrona, la barra de progreso y la tabla final:

Plaintext

─────────────────────────── PROYECTO ZEUS v0.1 ───────────────────────────
[*] Resolviendo IP para scanme.nmap.org...
[+] IP Encontrada: 45.33.32.156

Iniciando Escaneo Masivo en 45.33.32.156
Escaneando puertos... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:01

Resultados para scanme.nmap.org
┏━━━━━━━━╤━━━━━━━━━━━━━━┓
┃ Puerto │ Estado       ┃
┡━━━━━━━━╇━━━━━━━━━━━━━━┩
│     22 │ ABIERTO 🔓   │
│     80 │ ABIERTO 🔓   │
│   9929 │ ABIERTO 🔓   │
└────────┴──────────────┘
🧠 Guía de Estudio (Arquitectura Interna)
Esta sección es para estudiantes y desarrolladores que deseen comprender la teoría detrás del código.

1. El Event Loop (Bucle de Eventos)
A diferencia de los scripts lineales, ZEUS inicia un "Director de Orquesta" (Event Loop). Cuando una función necesita esperar (ej. esperar una conexión de red), cede el control al Bucle, el cual inmediatamente ejecuta la siguiente tarea pendiente. Esto elimina los tiempos muertos.

2. async def y await
async def: Define una corrutina. Indica que la función puede ser pausada.

await: Es el punto de suspensión. Le dice al script: "Pausa esta función aquí, guarda el estado, y ve a hacer otra cosa útil mientras esperamos la respuesta de la red".

3. Paralelismo con asyncio.gather
Esta es la clave de la velocidad.

Python

await asyncio.gather(*tareas)
Esta instrucción toma una lista de miles de corrutinas y las programa para ejecutarse concurrentemente. Es lo que permite escanear 1000 puertos en el tiempo que toma escanear uno solo.

4. Patrón de Diseño con rich
Utilizamos Context Managers (with Progress() as...) para manejar la interfaz gráfica. Esto asegura que la terminal siempre se restaure correctamente (incluso tras un CTRL+C), manteniendo la limpieza y profesionalidad.

⚠️ Advertencia Legal (Disclaimer)
ZEUS es una herramienta ofensiva de alta velocidad.

Este software ha sido creado únicamente con fines educativos y de investigación académica. El uso de este escáner contra redes, servidores o infraestructuras sin el consentimiento explícito y por escrito de sus propietarios es ilegal y puede ser penalizado severamente por las leyes locales e internacionales.

El autor y los contribuyentes no se hacen responsables de daños, interrupciones de servicio o consecuencias legales derivadas del uso irresponsable de esta herramienta.

Úsalo con sabiduría. Úsalo éticamente.