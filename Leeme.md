# Robot Llenador de Formularios

Este proyecto consta de dos componentes principales:
1.  Un script de shell para Linux (`get_coords.sh`) o una app en python (`get_coords.py`) para capturar las coordenadas de la pantalla para campos de formulario y botones.
2.  Una aplicación Python (`form_filler.py`) que lee datos de un archivo CSV y utiliza las coordenadas capturadas para llenar y enviar automáticamente formularios web u otras aplicaciones GUI.

## Características

-   **Captura de Coordenadas:** Captura interactivamente coordenadas X,Y usando Python (`get_coords.py`) o un script de shell en Linux (`get_coords.sh`).
-   **Entrada de Datos CSV:** Lee datos de un archivo CSV (delimitado por punto y coma), esperando que la primera fila contenga las cabeceras.
-   **Llenado Automático de Formularios:** Utiliza `pyautogui` para simular movimientos del ratón, clics y escritura.
-   **Retrasos Configurables:** Permite ajustar los retrasos entre acciones para adaptarse a diferentes velocidades del sistema y capacidad de respuesta de la aplicación.
-   **Interfaz de Línea de Comandos:** Todos los scripts se ejecutan desde la línea de comandos.
-   **Multiplataforma (componentes Python):** `get_coords.py` y `form_filler.py` están escritos en Python y deberían funcionar en Windows, macOS y Linux, siempre que Python y `pyautogui` estén configurados correctamente.

## Prerrequisitos

**Requisitos Principales (para `get_coords.py` y `form_filler.py`):**
-   **Python 3:**
    -   **Windows:** Descargar desde `https://www.python.org/downloads/`. Asegúrate de marcar "Add Python to PATH" durante la instalación.
    -   **Linux/macOS:** Python 3 suele estar preinstalado. Si no, usa el gestor de paquetes de tu sistema (p.ej., `sudo apt install python3` en Debian/Ubuntu, o `brew install python` en macOS).
-   **pip (instalador de paquetes de Python):** Normalmente viene con Python 3. Si no, busca "instalar pip" para tu SO.
-   **Biblioteca Python `pyautogui`:** Para automatización GUI. Instalar vía pip:
    ```bash
    pip install pyautogui
    ```
    *   **Nota Importante para `pyautogui`:** Esta biblioteca puede tener dependencias adicionales del sistema para interactuar con el servidor de visualización, especialmente en Linux (p.ej., `scrot`, `python3-tk`, `python3-dev`, `xclip`/`xsel`). Si la importación de `pyautogui` falla o no funciona correctamente (p.ej., problemas de control del ratón), por favor consulta su guía oficial de instalación para tu SO: `https://pyautogui.readthedocs.io/en/latest/install.html`

**Para el Script de Shell Específico de Linux (`get_coords.sh` únicamente):**
-   **Entorno Linux.**
-   **xdotool:** Requerido por `get_coords.sh` para capturar las coordenadas del ratón.
    -   Instalación (Debian/Ubuntu): `sudo apt update && sudo apt install xdotool`

## Configuración y Flujo de Uso General

El flujo de trabajo general implica dos pasos principales:
1.  **Capturar Coordenadas:** Usa uno de los scripts proporcionados para obtener las posiciones X,Y de los elementos de la interfaz de usuario.
2.  **Automatizar Llenado:** Usa `form_filler.py` con tus coordenadas capturadas y datos CSV.

### 1. Capturar Coordenadas

Tienes dos opciones para capturar coordenadas. Se recomienda el script basado en Python para compatibilidad multiplataforma.

**a. Usando `get_coords.py` (Recomendado para Windows, macOS, Linux)**

Este script de Python captura interactivamente las coordenadas del ratón y las guarda en `coords.txt`.

-   **Ejecutar el script:**
    ```bash
    # Asegúrate de que Python esté instalado y en tu PATH
    python get_coords.py
    ```
    (En algunos sistemas, puede que necesites usar `python3` explícitamente: `python3 get_coords.py`)

-   **Sigue las instrucciones en pantalla:**
    -   Te preguntará si quieres sobrescribir o añadir a un `coords.txt` existente.
    -   Introduce un nombre para cada coordenada (p.ej., `campo_usuario`, `boton_enviar`). Este nombre se usará en `coords.txt`.
    -   Después de introducir un nombre, tendrás una cuenta atrás de 5 segundos para posicionar tu ratón sobre el elemento de la interfaz de usuario deseado.
    -   El script usa `pyautogui.position()` para obtener las coordenadas.
    -   Escribe `done` cuando hayas terminado.

**b. Específico de Linux: Usando `get_coords.sh`**

Este script de shell es una alternativa para usuarios de Linux que tengan `xdotool` instalado.

-   **Haz el script ejecutable (si no lo has hecho ya):**
    ```bash
    chmod +x get_coords.sh
    ```
-   **Ejecuta el script:**
    ```bash
    ./get_coords.sh
    ```
-   **Sigue las instrucciones en pantalla:**
    -   Introduce un nombre para cada coordenada.
    -   Después de introducir un nombre, tendrás 5 segundos para mover el cursor de tu ratón a la ubicación deseada.
    -   El script usa `xdotool` para capturar coordenadas.
    -   Introduce `done` cuando hayas terminado.

**Detalles del Archivo `coords.txt`:**

Ambos scripts generan un archivo `coords.txt` (o añaden a él). Este archivo actúa como un **script ordenado de acciones** a realizar por `form_filler.py` para cada fila de tu archivo CSV.

-   **Para Entrada de Datos:** Si un nombre que defines en `coords.txt` **coincide con una cabecera en tu archivo CSV**, el script escribirá los datos correspondientes del CSV en el campo en esas coordenadas.
-   **Para Acciones de Solo Clic:** Si un nombre en `coords.txt` **no coincide con ninguna cabecera en tu archivo CSV**, el script simplemente realizará un clic en esas coordenadas.
-   **El Orden es Primordial:** El archivo `coords.txt` ahora define un **script exacto de operaciones** a realizar para cada fila de tu archivo CSV. Las acciones (escribir o hacer clic) se ejecutan en el orden preciso en que aparecen en `coords.txt`.

    **Ejemplo de `coords.txt`:**
    ```
    campo_email:100,200     # Si 'campo_email' está en el CSV para la fila actual, escribe datos. Si no, hace clic.
    nombre_empresa:100,250  # Si 'nombre_empresa' está en el CSV para la fila actual, escribe datos. Si no, hace clic.
    boton_siguiente_paso:50,300 # Probablemente no sea una cabecera CSV, así que esto usualmente será un clic.
    campo_edad:100,350       # Si 'campo_edad' está en el CSV para la fila actual, escribe datos. Si no, hace clic.
    envio_final:100,400    # Probablemente no sea una cabecera CSV, así que esto usualmente será un clic.
    ```
    **Puntos Clave para `coords.txt`:**
    - Para cada entrada en `coords.txt`, su `nombre_accion` se compara con las claves/cabeceras de la fila CSV actual.
    - Si `nombre_accion` coincide con una cabecera CSV, el script escribe los datos de ese campo CSV en la posición (X,Y).
    - Si `nombre_accion` no coincide con ninguna cabecera CSV para la fila actual, el script realiza un clic en (X,Y).
    - Este proceso se repite secuencialmente para cada entrada en `coords.txt`, para cada fila en el CSV. El orden en `coords.txt` se sigue estrictamente.

### 2. Prepara Tu Archivo de Datos CSV

Crea un archivo CSV (p.ej., `datos.csv`) donde:
-   La primera fila contiene cabeceras, y los campos **deben estar separados por punto y coma (;)**. Estas cabeceras **deben coincidir con los nombres** que asignaste a las coordenadas en `coords.txt` (p.ej., si usaste `nombre` en `coords.txt`, tu CSV debería tener una columna `nombre`).
-   Las filas subsecuentes contienen los datos a llenar en el formulario, también usando punto y coma como delimitadores.
-   *Nota: El delimitador de punto y coma se usa para evitar conflictos con datos que puedan contener comas (p.ej., números decimales en algunos formatos europeos o campos de texto libre).*

**Ejemplo de `datos.csv`:**
```csv
nombre;apellido;email
Juan;Perez;juan.perez@example.com
Maria;Garcia;maria.garcia@example.com
```

### 3. Ejecuta el Llenador de Formularios (`form_filler.py`)

Este script de Python lee tu `coords.txt` y tu archivo CSV, luego automatiza el proceso de llenado de formularios.

a.  **Abre la aplicación/página web destino** que quieres llenar.

b.  **Ejecuta el script desde tu terminal:**
    ```bash
    # Para Windows (asumiendo que Python está en el PATH)
    python form_filler.py tus_datos.csv

    # Para Linux/macOS (usa python3 si python es Python 2)
    python3 form_filler.py tus_datos.csv
    # O si python ya es Python 3:
    # python form_filler.py tus_datos.csv
    ```
    -   Reemplaza `tus_datos.csv` con la ruta a tu archivo CSV.
    -   También puedes usar argumentos opcionales como `--coords-file` y `--delay`.

c.  **¡Cambia rápidamente a la ventana de la aplicación destino!** El script tiene un breve retraso (3 segundos por defecto después de iniciar) antes de comenzar a controlar tu ratón y teclado.

**Argumentos de Línea de Comandos para `form_filler.py`:**
-   `csv_file`: (Requerido) Ruta a tu archivo de datos CSV.
-   `--coords-file COORDS_FILE` (o `--coords_file`): (Opcional) Ruta a tu archivo de coordenadas. Por defecto es `coords.txt`.
-   `--delay DELAY`: (Opcional) Retraso general en segundos entre la mayoría de las acciones GUI. Por defecto es `0.5`.

**Ejemplo de Uso (multiplataforma):**
```bash
python form_filler.py datos.csv --coords-file mis_coords_personalizadas.txt --delay 0.7
```
*(Nota: `argparse` típicamente permite tanto `-` como `_` en los nombres de los argumentos, p.ej. `--coords-file` y `--coords_file`.)*

## Cómo Funciona

1.  **Creación del Script de Coordenadas (usando `get_coords.py` o `get_coords.sh`):**
    -   Creas `coords.txt`. Este archivo actúa como un **script ordenado de acciones**. Cada línea define una coordenada nombrada (`nombre_accion:X,Y`). La secuencia de estas líneas es crítica.

2.  **Automatización con Python (`form_filler.py`):**
    -   El script carga `coords.txt` (preservando el orden de las entradas `nombre_accion`) y el archivo CSV de entrada (delimitado por punto y coma).
    -   Luego itera a través de cada **fila** de tus datos CSV. Para cada fila CSV, realiza la siguiente secuencia de operaciones:
        -   Itera a través de cada `nombre_accion` de tu `coords.txt` cargado, **en el orden exacto en que fueron definidos**.
        -   Para el `nombre_accion` actual y sus correspondientes coordenadas (X,Y):
            -   **Compara con los datos de la fila CSV actual:** El script comprueba si `nombre_accion` existe como una clave (cabecera) en el diccionario que representa la fila CSV actual.
            -   **Si `nombre_accion` ES una clave en la fila CSV actual (Acción de Entrada de Datos):**
                1.  El ratón se mueve a la coordenada (X,Y).
                2.  Se realiza un clic.
                3.  Ocurre una breve pausa (`args.delay / 2`).
                4.  El script escribe el valor asociado con `nombre_accion` de la fila CSV actual (p.ej., `fila[nombre_accion]`).
                5.  Ocurre un retraso configurable (`args.delay`) después de completar la escritura para este campo.
            -   **Si `nombre_accion` NO ES una clave en la fila CSV actual (Acción de Solo Clic):**
                1.  El ratón se mueve a la coordenada (X,Y).
                2.  Se realiza un clic.
                3.  Ocurre un **retraso fijo de 1 segundo** inmediatamente después de este clic. Este retraso no se ve afectado por el argumento `--delay`.
        -   Esta secuencia completa (iterar a través de todas las entradas `nombre_accion` de `coords.txt` y realizar la acción correspondiente) se completa para la fila CSV actual antes de que el script proceda a la siguiente fila en el archivo CSV.

3.  **Resumen de Retrasos (controlado por `form_filler.py`):**
    -   **Antes de Escribir (Entrada de Datos):** `args.delay / 2`.
    -   **Después de Escribir (Entrada de Datos):** `args.delay`.
    -   **Después de Acción de Solo Clic:** Retraso fijo de 1 segundo.
    -   **Fin del Procesamiento de cada Fila CSV:** Después de que todas las acciones definidas en `coords.txt` se realizan para una sola fila CSV, ocurre un retraso más largo de `args.delay * 2`. Esto tiene la intención de dar tiempo a la interfaz de usuario para reaccionar (p.ej., procesar envíos, cargar nuevas páginas) antes de que comience la automatización de la siguiente fila.

## Solución de Problemas

-   **Coordenadas Incorrectas:** Si el ratón no está haciendo clic en los lugares correctos, vuelve a ejecutar `get_coords.py` (o `get_coords.sh`) con cuidado. Asegúrate de que la ventana de tu aplicación no se mueva ni cambie de tamaño entre la captura de coordenadas y la ejecución del llenador.
-   **Problemas con `pyautogui`:**
    -   **FailSafeException:** Si `pyautogui` lanza una `FailSafeException`, significa que moviste el ratón a una esquina de la pantalla (normalmente arriba a la izquierda) como medida de seguridad para detener el script. El script está diseñado para capturar esto y salir de forma controlada.
    -   **Permisos/Servidor de Visualización:** En algunos sistemas Linux, `pyautogui` podría necesitar permisos adicionales o configuraciones específicas para controlar el ratón y el teclado. Esto es especialmente cierto bajo Wayland (intenta ejecutar en una sesión X11 si los problemas persisten). Consulta la documentación de `pyautogui` y las notas de instalación en `form_filler.py`.
    -   **Módulo No Encontrado:** Asegúrate de que `pyautogui` esté instalado en el entorno Python que estás utilizando (`pip install pyautogui`).
-   **Problemas de Sincronización:** Si el script es demasiado rápido o demasiado lento para tu aplicación destino, ajusta la opción `--delay` en `form_filler.py`. Algunas aplicaciones necesitan más tiempo para procesar entradas o cargar nuevas secciones.
-   **Foco de la Ventana:** Asegúrate de que la ventana de la aplicación destino esté activa y enfocada antes de que `form_filler.py` comience su secuencia de automatización. El script incluye una breve pausa al principio para esto. Si la ventana incorrecta está activa, el script interactuará con esa ventana en su lugar.
-   **`xdotool` no encontrado/no funciona:** Asegúrate de que `xdotool` esté instalado correctamente y funcionando desde tu terminal. Si `get_coords.sh` reporta errores al capturar coordenadas, esta es la causa probable.

## Licencia
Este proyecto está licenciado bajo la Licencia MIT. Puedes crear un archivo `LICENSE` y pegar el texto de la Licencia MIT en él si lo deseas.
(Una plantilla básica de la Licencia MIT se puede encontrar en https://opensource.org/licenses/MIT)
