# 🧠 Red Neuronal ART1 - Reconocimiento y Restauración de Patrones

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![GUI](https://img.shields.io/badge/Interfaz-CustomTkinter-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Estado-Terminado-success?style=for-the-badge)

Una implementación de la **Teoría de Resonancia Adaptativa (ART1)** con una interfaz gráfica moderna. Este proyecto no solo clasifica patrones binarios, sino que actúa como un sistema de **memoria y restauración visual**: es capaz de "recordar" la versión más perfecta de una imagen y usarla para corregir entradas ruidosas o incompletas en tiempo real.


## 📋 Características Principales

* **Interfaz Moderna (Dark Mode):** Desarrollada con `customtkinter`, ofreciendo una experiencia visual limpia y profesional.
* **Autocorrección Visual:** Si el usuario dibuja un patrón incompleto, el sistema lo reemplaza visualmente por la versión "ideal" almacenada en su memoria.
* **Aprendizaje No-Destructivo (Lógica Personalizada):** A diferencia del ART1 estándar que erosiona la memoria, este algoritmo conserva siempre la versión con mayor detalle (ver *Enfoque Técnico*).
* **Control de Vigilancia ($\rho$):** Slider en tiempo real para ajustar la rigurosidad de la clasificación (0.0 a 1.0).
* **Galería de Memoria:** Visualización dinámica de todos los prototipos aprendidos por la red.

## 🛠️ Instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/danmtzzz/Proyecto-RNA.git](https://github.com/danmtzzz/Proyecto-RNA.git)
    ```

2.  **Instalar dependencias:**
    Asegúrate de tener Python instalado. Luego ejecuta:
    ```bash
    pip install numpy customtkinter pillow
    ```

## ▶️ Uso

1.  Ejecuta la aplicación principal:
    ```bash
    python app.py
    ```
    *(Nota: Si tu archivo principal tiene otro nombre, ajústalo aquí).*

2.  **Flujo de Trabajo:**
    * **Cargar Imagen:** Sube una imagen (PNG/JPG). El sistema la convertirá automáticamente a binario (blanco/negro).
    * **Ajustar Vigilancia ($\rho$):** Define qué tan estricta debe ser la red.
        * $\rho$ alto (ej. 0.9): Diferencia entre detalles pequeños.
        * $\rho$ bajo (ej. 0.5): Agrupa imágenes vagamente similares.
    * **Botón "APRENDER":**
        * Si la imagen es nueva y detallada → La red la aprende.
        * Si la imagen es una versión ruidosa de una conocida → La red la reconoce y **te muestra la versión limpia**.

## 🧠 Enfoque Técnico y Algoritmo

Este proyecto implementa una modificación específica sobre la arquitectura ART1 estándar para priorizar la calidad de la imagen.

### Diferencia Clave: Regla de Aprendizaje

En el ART1 clásico (Carpenter & Grossberg), el aprendizaje ocurre mediante intersección lógica ($AND$), lo que causa que los píxeles "extra" se borren con el tiempo (erosión).

**Nuestra Implementación ("Mayor Detalle Gana"):**
Utilizamos una lógica condicional para preservar la integridad visual:

1.  **Vigilancia:** Se calcula la similitud estándar:
    $$ \frac{|P \cap T|}{|P|} \ge \rho $$
2.  **Actualización de Pesos:**
    * Si la **Entrada ($I$)** tiene *más* píxeles activos que la **Memoria ($T$)**:
        $$ T_{new} = I $$
        *(Asumimos que la entrada es una versión mejorada/más completa y actualizamos la memoria).*
    * Si la **Entrada ($I$)** tiene *menos* píxeles (es ruidosa o incompleta):
        $$ T_{new} = T_{old} $$
        *(Conservamos la memoria original y la usamos para corregir la visualización del usuario).*

## 📂 Estructura del Proyecto

* `app.py`: Código de la interfaz gráfica (`ArtAppModerno`) y manejo de eventos.
* `art.py`: Clase `RedNeuronalART1` con la lógica matemática y matricial.
* `utils/`: Módulos de soporte para procesamiento y binarización de imágenes.

