import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Penguins", layout="wide")

st.title("🐧 Los Pingüinos Bio-polares")
st.markdown("## Investigación y exploración interactiva de los datos del equipo II")

url = "https://raw.githubusercontent.com/xuangfm/ejercicio_pinguinos/analisis_univariado/df_clean_penguins.csv"

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

df = load_data(url)
counts = df["species"].value_counts().reset_index()
counts.columns = ["species", "count"]
# -------------------------
# Preparación de datos UI
# -------------------------
df_ui = df.copy()
df_ui["sex_ui"] = df["sex"].fillna("Desconocido")
df_ui["clutch_ui"] = df["clutch_completion"].fillna("Desconocido")

# -------------------------
# 🎛️ FILTROS (SIDEBAR)
# -------------------------
st.sidebar.header("Filtros Globales")

species = st.sidebar.multiselect(
    "Selecciona especie:",
    options=sorted(df["species"].unique()),
    default=sorted(df["species"].unique())
)

island = st.sidebar.multiselect(
    "Selecciona isla:",
    options=sorted(df["island"].unique()),
    default=sorted(df["island"].unique())
)

sex = st.sidebar.multiselect(
    "Selecciona sexo:",
    options=sorted(df_ui["sex_ui"].unique()),
    default=sorted(df_ui["sex_ui"].unique())
)
nido = st.sidebar.multiselect(
    "Selecciona eclosión de nidos:",
    options=sorted(df_ui["clutch_ui"].unique()),
    default=sorted(df_ui["clutch_ui"].unique())
)

# -------------------------
# 🔍 FILTRADO
# -------------------------
filtered_df = df[
    (df["species"].isin(species)) &
    (df["island"].isin(island)) &
    (df["sex"].isin(sex)) &
    (df["clutch_completion"].isin(nido))
]
mask = (
    df_ui["species"].isin(species) &
    df_ui["island"].isin(island) &
    df_ui["sex_ui"].isin(sex) &
    df_ui["clutch_ui"].isin(nido)
)

filtered_df = df[mask]  # 👈 importante: vuelves al DF original

# -------------------------
# 📊 ESTRUCTURA DE PESTAÑAS
# -------------------------
tab1, tab2, tab3 = st.tabs(["📋 Vista de Datos", "📉 Análisis Univariado", "📊 Análisis Bivariado"])

# --- TAB 1: VISTA DE DATOS ---
with tab1:
    st.subheader("Exploración de la tabla")
    st.write(f"Mostrando {filtered_df.shape[0]} registros")
    st.dataframe(filtered_df, use_container_width=True)
    st.divider()
    st.markdown("### Conteo preliminar básico")
    st.markdown("""
    <style>
    .divider {
        border-left: 2px solid #fff;
        height: 100%;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, divider, col2 = st.columns([1, 0.1, 1])
    
    with col1:
        # Pie chart de especies
        counts = filtered_df["species"].value_counts().reset_index()
        fig_pie = px.pie(counts, names="species", values="count", title="Especies observadas")
        st.plotly_chart(fig_pie, use_container_width=True)
   
    with col2:
        # histograma de especies por islas
        fig_hist = px.histogram(filtered_df, x="island", color="species", title="Distribución por Isla")
        st.plotly_chart(fig_hist, use_container_width=True)
    #---
    st.divider()

    st.markdown("### Observación de anidado por especie")
    clutch_counts = (
    filtered_df
    .groupby(["species", "clutch_completion"])
    .size()
    .reset_index(name="count")
    )

# Calcular proporciones correctamente
    
    clutch_counts["proportion"] = (
    clutch_counts["count"] /
    clutch_counts.groupby("species")["count"].transform("sum")

    )

    fig = px.bar(
    clutch_counts,
    x="clutch_completion",
    y="proportion",
    color="species",
    barmode="group",
    title="Proporción de exito"
    )
    st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: ANÁLISIS UNIVARIADO (Seaborn/Matplotlib) ---
with tab2:
    st.subheader("📉 Análisis Univariado")

    variable = st.selectbox(
        "Selecciona una variable numérica:",
        [
            'culmen_length_(mm)', 
            'culmen_depth_(mm)',
            'flipper_length_(mm)', 
            'body_mass_(g)'
        ]
    )

    if filtered_df.empty:
        st.warning("No hay datos disponibles con los filtros seleccionados.")
        st.stop()

    # Selector de tipo de gráfico
    chart_type = st.radio(
        "Selecciona tipo de visualización:",
        ["Histograma", "Boxplot", "Densidad (KDE)"],
        horizontal=True
    )

    # 📊 GRÁFICO PRINCIPAL (GRANDE)
  
    fig, ax = plt.subplots(figsize=(10, 6))

    if chart_type == "Histograma":
        sns.histplot(
            filtered_df[variable],
            bins=30,
            kde=True,
            ax=ax
        )
        ax.set_title(f"Distribución de {variable}")

    elif chart_type == "Boxplot":
        sns.boxplot(
            x=filtered_df[variable],
            ax=ax
        )
        ax.set_title(f"Boxplot de {variable}")

    elif chart_type == "Densidad (KDE)":
        sns.kdeplot(
            filtered_df[variable],
            fill=True,
            ax=ax
        )
        ax.set_title(f"Densidad de {variable}")

    st.pyplot(fig)

    
    # 📌 ESTADÍSTICAS CLAVE
    
    st.markdown("### 📊 Resumen estadístico")

    col1, col2, col3 = st.columns(3)

    col1.metric("Media", round(filtered_df[variable].mean(), 2))
    col2.metric("Mediana", round(filtered_df[variable].median(), 2))
    col3.metric("Desv. estándar", round(filtered_df[variable].std(), 2))
    
    
    st.divider()
    #---
    # Distribución analisis univariado por cada especie
    #---
    st.markdown("### Distribución por especie")

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.kdeplot(
            data=filtered_df,
            x=variable,
            hue="species",
            fill=True,
            alpha=0.4,
            ax=ax
    )
    
    ax.set_title(f"Densidad de {variable} por especie")
    st.pyplot(fig)

    #---

    max_value = filtered_df[variable].max()
    min_value = filtered_df[variable].min()
    st.info(f"El valor máximo observado en {variable} es de {round(max_value, 2)}, y el mínimo es {round(min_value, 2)}")


# --- TAB 3: GRÁFICOS INTERACTIVOS (Plotly) ---
with tab3:
    st.subheader("Relaciones y proporciones")
   
    
    # Grafico de masa por especie
    st.divider()
    st.markdown("## Análisis de masa corporal")
    fig = px.box(
        filtered_df,
        x="species",
        y="body_mass_(g)",
        color="species",
        title="Distribución de masa corporal por especie"
    )

    st.plotly_chart(fig, use_container_width=True)
    st.divider()
    st.markdown("### Morfología del pico")
    # Scatter plot
    fig_scatter = px.scatter(
        filtered_df, 
        x="culmen_length_(mm)", 
        y="culmen_depth_(mm)", 
        color="species",
        title="Análisis comparativo de la longitud y profundidad del pico",    
        labels={
            "culmen_length_(mm)": "Longitud (mm)",
            "culmen_depth_(mm)": "Profundidad (mm)"
            }
        )
    st.plotly_chart(fig_scatter, use_container_width=True)
    



