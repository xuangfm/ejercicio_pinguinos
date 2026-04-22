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

species_sel = st.sidebar.multiselect(
    "Selecciona especie:",
    options=sorted(df["species"].unique()),
    default=sorted(df["species"].unique())
)

island_sel = st.sidebar.multiselect(
    "Selecciona isla:",
    options=sorted(df["island"].unique()),
    default=sorted(df["island"].unique())
)

sex_sel = st.sidebar.multiselect(
    "Selecciona sexo:",
    options=sorted(df_ui["sex_ui"].unique()),
    default=sorted(df_ui["sex_ui"].unique())
)

# Aplicar filtros
mask = (
    df_ui["species"].isin(species_sel) &
    df_ui["island"].isin(island_sel) &
    df_ui["sex_ui"].isin(sex_sel)
)
filtered_df = df[mask]

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
        # Scatter plot
        fig_scatter = px.scatter(
            filtered_df, 
            x="culmen_length_(mm)", 
            y="culmen_depth_(mm)", 
            color="species",
            title="Longitud vs Profundidad del Pico"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Barra de peso
    mass_by_species = filtered_df.groupby("species")["body_mass_(g)"].mean().reset_index()
    fig_bar = px.bar(mass_by_species, x="species", y="body_mass_(g)", color="species", 
                     title="Masa corporal promedio (g)")
    st.plotly_chart(fig_bar, use_container_width=True)