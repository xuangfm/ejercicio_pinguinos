import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Penguins", layout="wide", page_icon="🐧")

# 2. ESTILOS CSS (Con Sombras para todo)
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3)), 
                    url("https://images.pexels.com/photos/533856/pexels-photo-533856.jpeg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    section[data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(15px);
    }

    /* Estilo para tarjetas de métricas, tabla y Gráficos Univariados (Transparentes) */
    .stMatplotlibChart, div[data-testid="stDataFrame"], div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.15) !important; 
        padding: 15px;
        border-radius: 15px;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    }

    /* Estilo para Gráficos Bivariados (Blanco + Sombra Pronunciada) */
    div[data-testid="stPlotlyChart"] {
        background-color: white !important;
        padding: 15px;
        border-radius: 15px;
        /* Sombra más oscura y definida para resaltar el blanco */
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.45), 0 8px 10px rgba(0, 0, 0, 0.22) !important;
    }

    h1, h2, h3, p, label, .stMarkdown {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
    }
</style>
""", unsafe_allow_html=True)

# 3. CARGA DE DATOS
url = "https://raw.githubusercontent.com/xuangfm/ejercicio_pinguinos/analisis_univariado/df_clean_penguins.csv"

@st.cache_data
def load_data(url):
    data = pd.read_csv(url)
    data["sex"] = data["sex"].fillna("Desconocido")
    data["clutch_completion"] = data["clutch_completion"].fillna("Desconocido")
    return data

df = load_data(url)

# 🎛️ FILTROS SIDEBAR
st.sidebar.header("Filtros")
species_f = st.sidebar.multiselect("Especie:", options=sorted(df["species"].unique()), default=sorted(df["species"].unique()))
island_f = st.sidebar.multiselect("Isla:", options=sorted(df["island"].unique()), default=sorted(df["island"].unique()))

filtered_df = df[(df["species"].isin(species_f)) & (df["island"].isin(island_f))]

# 📊 PESTAÑAS
tab1, tab2, tab3 = st.tabs(["📋 Datos", "📉 Univariado", "📊 Bivariado"])

# --- TAB 1: DATOS ---
with tab1:
    st.subheader("Resumen de Datos")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Pingüinos", value=len(filtered_df))
    with col2:
        st.metric(label="Especies", value=filtered_df["species"].nunique())
    with col3:
        st.metric(label="Islas", value=filtered_df["island"].nunique())
    
    st.divider()
    st.dataframe(filtered_df, use_container_width=True)

# --- TAB 2: UNIVARIADO (Transparente con Sombra) ---
with tab2:
    st.subheader("📉 Análisis Univariado")
    variable = st.selectbox("Variable numérica:", ['culmen_length_(mm)', 'flipper_length_(mm)', 'body_mass_(g)'])
    
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.histplot(filtered_df[variable], kde=True, ax=ax, color="#00b4d8")
    
    fig.patch.set_alpha(0) 
    ax.set_facecolor((0,0,0,0))
    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    for spine in ax.spines.values():
        spine.set_color('white')
        
    st.pyplot(fig)

# --- TAB 3: BIVARIADO (Blanco con Sombra) ---
with tab3:
    st.subheader("📊 Análisis Bivariado")
    
    # Gráfico 1
    fig_scatter = px.scatter(
        filtered_df, x="culmen_length_(mm)", y="culmen_depth_(mm)", color="species",
        title="Relación Largo vs Profundidad del Pico", template="plotly_white"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.write(" ") # Espaciado

    # Gráfico 2
    fig_box = px.box(
        filtered_df, x="species", y="body_mass_(g)", color="species",
        title="Distribución de Masa por Especie", template="plotly_white"
    )
    st.plotly_chart(fig_box, use_container_width=True)