# 🚀 Optimizador de Espacio con Algoritmos Genéticos

Este proyecto es un sistema inteligente diseñado para resolver el problema de optimización de espacio, maximizando la rentabilidad de un conjunto de artículos dentro de un área limitada. Utiliza un **Algoritmo Genético** para encontrar la combinación óptima de productos y una interfaz web interactiva construida con **Streamlit** para configurar los parámetros, ejecutar simulaciones y visualizar los resultados en tiempo real.

Este proyecto fue desarrollado como parte del Taller No. 3 para la asignatura de Machine Learning de la carrera de Ingeniería de Sistemas y Computación en la Universidad de Cundinamarca.

-----

## 📝 Descripción del Problema y Modelo Matemático

El objetivo es determinar la cantidad de cada artículo a seleccionar de un catálogo para maximizar la ganancia total, sin exceder un área de almacenamiento máxima disponible.

### **1. Función Objetivo**

Maximizar la ganancia total (Z), que es la suma de las ganancias de todos los artículos seleccionados.

$$
\text{Maximizar } Z = \sum_{i=1}^{n} g_i \cdot x_i
$$

Donde:

- $g_i$ es la ganancia del artículo $i$.
- $x_i$ es la cantidad de unidades seleccionadas del artículo $i$.

### **2. Variables de Decisión**

- $x_i$: Número entero de unidades a seleccionar del artículo $i$.

### **3. Restricciones**

1.  **Restricción de Área:** El área total ocupada por los artículos seleccionados no debe superar el área máxima ($A_{\text{max}}$).


$$
\\sum\_{i=1}^{n} a\_i \\cdot x\_i \\leq A\_{\\text{max}}
$$

Donde $a_i$ es el área del artículo $i$.

2.  **Restricción de Stock:** La cantidad seleccionada de cada artículo no puede superar su stock disponible ($s_i$).

$$
0 \\leq x\_i \\leq s\_i \\quad \\forall i \\in {1, ..., n}
$$

-----

## 🛠️ Tecnologías Utilizadas

  - **Backend:** Python
  - **Frontend Interactivo:** Streamlit
  - **Manipulación de Datos:** Pandas
  - **Visualización de Gráficos:** Matplotlib & Squarify

-----

## ⚙️ Instalación y Configuración

Sigue estos pasos para configurar y ejecutar el proyecto en tu máquina local.

### **1. Prerrequisitos**

  - Tener instalado Python 3.8 o superior.
  - Tener instalado `pip` (el gestor de paquetes de Python).

### **2. Clonar el Repositorio**

Abre tu terminal y clona este repositorio:

```bash
git clone https://github.com/TatoNaranjo/Optimizador-de-Areas-AG
cd Optimizador-de-Areas-AG
```

### **3. Crear un Entorno Virtual (Recomendado)**

Es una buena práctica aislar las dependencias del proyecto.

```bash
# Crear el entorno
python -m venv venv

# Activar el entorno
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

### **4. Instalar Dependencias**

El archivo `requirements.txt` contiene todas las librerías necesarias. Instálalas con un solo comando:

```bash
pip install -r requirements.txt
```

-----

## ▶️ Ejecución

Una vez instaladas las dependencias, ejecuta la aplicación de Streamlit con el siguiente comando:

```bash
streamlit run app.py
```

Se abrirá automáticamente una pestaña en tu navegador web en `http://localhost:8501` con la aplicación en funcionamiento.

-----

## 📂 Estructura de Archivos

El proyecto está organizado en dos archivos principales para separar la lógica del algoritmo de la interfaz de usuario:

  - `ga_backend.py`: Contiene la clase `GeneticAlgorithm` que encapsula toda la lógica del algoritmo: creación de la población, evaluación del fitness, selección (torneo y ruleta), cruce, mutación y elitismo.
  - `app.py`: Es el punto de entrada de la aplicación. Contiene todo el código del frontend construido con Streamlit. Se encarga de crear los sliders, tablas interactivas y gráficos para visualizar los resultados.

-----

## 👨‍💻 Autores

  - **Santiago Naranjo Herrera**
  - **Daniel Steven Hincapié Cetina**

-----
