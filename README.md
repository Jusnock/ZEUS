<div align="center">
<pre>
███████╗███████╗██╗   ██╗███████╗
╚══███╔╝██╔════╝██║   ██║██╔════╝
  ███╔╝ █████╗  ██║   ██║███████╗
 ███╔╝  ██╔══╝  ██║   ██║╚════██║
███████╗███████╗╚██████╔╝███████║
╚══════╝╚══════╝ ╚═════╝ ╚══════╝
                                
</pre>
</div>

<h1 align="center">⚡ ZEUS: Asynchronous Reconnaissance Engine</h1>
<p align="center"><i>"Velocidad de rayo, precisión de dios."</i></p>

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

- **Target:** Encapsula el estado, datos y resultados de la víctima (IP, dominio, puertos abiertos).
- **Scanner:** Encapsula la lógica de negocio, resolución DNS y rutinas de conexión.

### 3. Experiencia de Usuario (UX) Profesional 🎨

- Impulsado por la librería `rich` para una interfaz de terminal moderna con barras de progreso y tablas dinámicas.

---

## Características (v0.1)

- **Resolución DNS Asíncrona:** Convierte dominios a IPs sin bloquear el proceso principal.
- **Escaneo de Puertos Masivo:** Escanea rangos completos (1-1000+) en segundos gracias a `asyncio.gather`.
- **Barra de Progreso Atómica:** Visualización precisa del avance usando Context Managers.
- **Reporte Tabular:** Salida limpia y estructurada lista para análisis.
- **Timeouts Agresivos:** Optimizado para redes rápidas y descarte inmediato de hosts muertos.

---

## Tecnologías Utilizadas

- **Python 3.8+**: Sintaxis moderna (`async/await`).
- **asyncio**: Concurrencia nativa.
- **rich**: Texto enriquecido y formateo en terminal.
- **socket**: Modo no bloqueante para conexiones de bajo nivel.

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

# Instala las dependencias
pip install rich
```

---

## ⚡ Modo de Uso

Actualmente (v0.1 Alpha), el objetivo se configura directamente en el main para propósitos de depuración y aprendizaje.

```bash
python3 zeus.py
```

### Salida Esperada

```plaintext
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
```

---

## 🧠 Guía de Estudio (Arquitectura Interna)

### 1. El Event Loop (Bucle de Eventos)

A diferencia de los scripts lineales, ZEUS inicia un "Director de Orquesta" (Event Loop). Cuando una función necesita esperar (ej. una conexión de red), cede el control al bucle, el cual ejecuta la siguiente tarea pendiente.

### 2. `async def` y `await`

- `async def`: Define una corrutina, que puede ser pausada.
- `await`: Punto de suspensión; pausa la función y permite que el bucle ejecute otras tareas.

### 3. Paralelismo con `asyncio.gather`

Esta es la clave de la velocidad:

```python
await asyncio.gather(*tareas)
```

Permite escanear 1000 puertos en el tiempo que toma escanear uno solo.

### 4. Patrón de Diseño con `rich`

Utilizamos Context Managers (`with Progress() as...`) para manejar la interfaz gráfica, asegurando limpieza y profesionalidad incluso tras un `CTRL+C`.

---

## ⚠️ Advertencia Legal (Disclaimer)

ZEUS es una herramienta ofensiva de alta velocidad.

> **Este software ha sido creado únicamente con fines educativos y de investigación académica. El uso de este escáner contra redes, servidores o infraestructuras sin el consentimiento explícito y por escrito de sus propietarios es ilegal y puede ser penalizado severamente por las leyes locales e internacionales.**
>
> El autor y los contribuyentes no se hacen responsables de daños, interrupciones de servicio o consecuencias legales derivadas del uso irresponsable de esta herramienta.

**Úsalo con sabiduría. Úsalo éticamente.**

---