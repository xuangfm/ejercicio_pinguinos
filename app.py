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
tab1, tab2, tab3 = st.tabs(["📋 Vista de Datos", "📉 Análisis Univariado", "📊 Gráficos Interactivos"])

# --- TAB 1: VISTA DE DATOS ---
with tab1:
    st.subheader("Exploración de la tabla")
    st.write(f"Mostrando {filtered_df.shape[0]} registros")
    st.dataframe(filtered_df, use_container_width=True)

# --- TAB 2: ANÁLISIS UNIVARIADO (Seaborn/Matplotlib) ---
with tab2:
    st.subheader("Distribución estadística")
    
    # Asegúrate de usar los nombres exactos de las columnas del CSV
    variable = st.selectbox("Selecciona una variable numérica:", [
        'culmen_length_(mm)', 'culmen_depth_(mm)',
        'flipper_length_(mm)', 'body_mass_(g)'
    ])
    
    if not filtered_df.empty:
        fig, ax = plt.subplots(1, 3, figsize=(15, 5))
        
        # Boxplot
        sns.boxplot(x=filtered_df[variable], ax=ax[0], color="skyblue")
        ax[0].set_title('Boxplot')
        
        # Histograma
        sns.histplot(filtered_df[variable], ax=ax[1], kde=False, color="salmon")
        ax[1].set_title('Histograma')
        
        # KDE
        sns.kdeplot(filtered_df[variable], ax=ax[2], fill=True, color="green")
        ax[2].set_title('Densidad (KDE)')
        
        st.pyplot(fig)
    else:
        st.warning("No hay datos disponibles con los filtros seleccionados.")

# --- TAB 3: GRÁFICOS INTERACTIVOS (Plotly) ---
with tab3:
    st.subheader("Relaciones y proporciones")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart de especies
        counts = filtered_df["species"].value_counts().reset_index()
        fig_pie = px.pie(counts, names="species", values="count", title="Distribución por Especie")
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        # histograma de especies por islas
        fig_hist = px.histogram(filtered_df, x="island", color="species", title="Distribución por Isla")
        st.plotly_chart(fig_hist, use_container_width=True)
    
    # Barra de peso
    mass_by_species = (
        filtered_df
        .groupby("species")["body_mass_(g)"]
        .agg(["mean", "std"])
        .reset_index()
    )
    mass_by_species = mass_by_species.sort_values(by="mean", ascending=False)
    
# Crear gráfico con barras de error
fig = px.bar(
    mass_by_species,
    x="species",
    y="mean",
    color="species",
    error_y="std",  # 🔥 aquí está la clave
    title="Masa corporal promedio por especie (± desviación estándar)",
    labels={
        "mean": "Masa corporal (g)",
        "species": "Especie"
    }
)

st.plotly_chart(fig, use_container_width=True)
# Scatter plot
fig_scatter = px.scatter(
            filtered_df, 
            x="culmen_length_(mm)", 
            y="culmen_depth_(mm)", 
            color="species",
            title="Longitud vs Profundidad del Pico",
            labels={
                "culmen_length_(mm)": "Longitud (mm)",
                "culmen_depth_(mm)": "Profundidad (mm)"
            }
        )
st.plotly_chart(fig_scatter, use_container_width=True)
    



