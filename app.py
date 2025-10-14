import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import squarify
import numpy as np

from ga_backend import GeneticAlgorithm 

# --- Configuración de la Página e Inicial ---
st.set_page_config(layout="wide")
st.title("️🚀 Optimizador de Espacio con Algoritmo Genético")

initial_catalogo = [
    {"id": 1, "nombre": "Mini nevera", "area": 0.25, "ganancia": 40, "stock": 20},
    {"id": 2, "nombre": "Televisor 32\"", "area": 0.1125, "ganancia": 60, "stock": 6},
    {"id": 3, "nombre": "Lavadora", "area": 0.36, "ganancia": 90, "stock": 3},
    {"id": 4, "nombre": "Microondas", "area": 0.20, "ganancia": 25, "stock": 8},
    {"id": 5, "nombre": "Aire acondicionado", "area": 0.27, "ganancia": 110, "stock": 2},
    {"id": 6, "nombre": "Licuadora", "area": 0.04, "ganancia": 8, "stock": 10},
    {"id": 7, "nombre": "Nevera grande", "area": 0.6, "ganancia": 220, "stock": 2},
    {"id": 8, "nombre": "Horno eléctrico", "area": 0.36, "ganancia": 65, "stock": 3},
    {"id": 9, "nombre": "Aspiradora", "area": 0.0875, "ganancia": 28, "stock": 6},
    {"id": 10, "nombre": "Plancha", "area": 0.06, "ganancia": 10, "stock": 12},
    {"id": 11, "nombre": "Cocina a gas", "area": 0.48, "ganancia": 130, "stock": 2},
    {"id": 12, "nombre": "Extractor cocina", "area": 0.18, "ganancia": 45, "stock": 4},
]

# --- Definición de la Interfaz en Columnas ---
col1, col2 = st.columns([1, 1.5]) 

with col1:
    st.header("🔧 Configuración")
    
    # Panel de Parámetros del Algoritmo Genético
    st.subheader("Parámetros del Algoritmo")
    area_maxima = st.number_input("Área Máxima del Espacio (m²)", 1.0, 500.0, 50.0)
    
    # ✨ NUEVO: Selector de método de selección
    selection_method = st.selectbox("Método de Selección", ('torneo', 'ruleta'))
    
    # ✨ NUEVO: Toggle para elitismo
    elitism_on = st.toggle("Activar Elitismo", value=True)
    elitismo_val = 0
    if elitism_on:
        elitismo_val = st.slider("Individuos de Élite", 1, 10, 2, 1)

    tam_poblacion = st.slider("Tamaño de Población", 50, 500, 100, 10)
    num_generaciones = st.slider("Número de Generaciones", 10, 1000, 50, 10)
    prob_cruce = st.slider("Probabilidad de Cruce", 0.0, 1.0, 0.6, 0.05)
    prob_mutacion = st.slider("Probabilidad de Mutación", 0.0, 1.0, 0.15, 0.01)

    # ✨ NUEVO: Panel de edición del Catálogo con Checkbox de selección
    st.subheader("Catálogo de Artículos")
    df_catalogo = pd.DataFrame(initial_catalogo)
    df_catalogo.insert(0, "Seleccionar", True) # Añade la columna de checkboxes
    
    edited_df = st.data_editor(
        df_catalogo,
        hide_index=True,
        column_config={"Seleccionar": st.column_config.CheckboxColumn(required=True)},
        key="data_editor"
    )
    
    # Filtra los artículos que el usuario seleccionó
    articulos_seleccionados = edited_df[edited_df["Seleccionar"]].to_dict('records')
    
    run_button = st.button("📊 Ejecutar Optimización", type="primary", use_container_width=True)

with col2:
    st.header("📈 Resultados")
    if run_button:
        if not articulos_seleccionados:
            st.warning("⚠️ No hay artículos seleccionados. Por favor, marca al menos uno.")
        else:
            with st.spinner('Evolucionando soluciones... por favor espere.'):
                ga = GeneticAlgorithm(
                    catalogo=articulos_seleccionados, # <-- Pasa solo los seleccionados
                    area_maxima=area_maxima,
                    tam_poblacion=tam_poblacion,
                    num_generaciones=num_generaciones,
                    prob_cruce=prob_cruce,
                    prob_mutacion=prob_mutacion,
                    elitismo=elitismo_val, # <-- Pasa el valor correcto
                    selection_method=selection_method # <-- Pasa el método
                )
                mejor_solucion, historial = ga.ejecutar()

            st.success("¡Optimización completada!")

            if mejor_solucion:
                mejor_area = sum(q * item["area"] for q, item in zip(mejor_solucion, articulos_seleccionados))
                mejor_ganancia = sum(q * item["ganancia"] for q, item in zip(mejor_solucion, articulos_seleccionados))
                area_libre = area_maxima - mejor_area

                st.subheader("Mejor Combinación Encontrada")
                m1, m2 = st.columns(2)
                m1.metric("💰 Ganancia Total Óptima", f"${mejor_ganancia:,.2f}")
                m2.metric("📦 Área Total Usada", f"{mejor_area:.2f} / {area_maxima} m² ({area_libre:.2f} m² libres)")
                
                st.subheader("Visualizaciones")
                
                # Gráfico de Convergencia
                fig1, ax1 = plt.subplots()
                ax1.plot(range(len(historial)), historial)
                ax1.set_title("Evolución del Fitness (Convergencia)")
                ax1.set_xlabel("Generación")
                ax1.set_ylabel("Fitness (Ganancia)")
                ax1.grid(True)
                st.pyplot(fig1)

                # ✨ NUEVO: Gráfico de Distribución con Espacio Vacío
                items_en_solucion = [item for q, item in zip(mejor_solucion, articulos_seleccionados) if q > 0]
                areas_solucion = [q * item['area'] for q, item in zip(mejor_solucion, articulos_seleccionados) if q > 0]
                nombres_solucion = [f"{item['nombre']}\n({q} uds)" for q, item in zip(mejor_solucion, articulos_seleccionados) if q > 0]
                
                # Añadir el espacio vacío como un elemento más del gráfico
                if area_libre > 0.01: # Solo mostrar si es significativo
                    areas_solucion.append(area_libre)
                    nombres_solucion.append(f"Espacio Vacío\n({area_libre:.2f} m²)")
                
                if areas_solucion:
                    fig2, ax2 = plt.subplots()
                    # Generar colores y hacer que el último (espacio vacío) sea gris
                    colors = [plt.cm.viridis(i/float(len(areas_solucion)-1)) for i in range(len(areas_solucion))]
                    if area_libre > 0.01:
                        colors[-1] = (0.8, 0.8, 0.8, 1.0) # Gris claro

                    squarify.plot(sizes=areas_solucion, label=nombres_solucion, alpha=0.8, ax=ax2, color=colors)
                    plt.axis('off')
                    ax2.set_title(f"Distribución Visual del Área Total: {area_maxima} m²")
                    st.pyplot(fig2)
            else:
                st.error("No se pudo encontrar una solución.")