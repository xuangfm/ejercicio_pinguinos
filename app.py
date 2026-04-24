import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
# -------------------------
# CONFIGURACIÓN
# -------------------------
st.set_page_config(
    page_title="Pingüinos Bio-polares",
    layout="wide",
    page_icon="🐧"
)

# Detectar modo oscuro/claro
is_dark = st.get_option("theme.base") == "dark"
#----------------------
# 🎨 SISTEMA DE ESTILOS PRO
# -------------------------

def load_css():
     overlay = "rgba(0,0,0,0.6)" if is_dark else "rgba(255,255,255,0.4)"
     text_color = "white" if is_dark else "#111"
     sidebar_bg = "rgba(0,0,0,0.4)" if is_dark else "rgba(255,255,255,0.6)"
     st.markdown(f"""
<style>

/* ===== BACKGROUND ===== */
    .stApp {{
    background: linear-gradient(rgba({overlay}, {overlay}),
    url("https://images.pexels.com/photos/533856/pexels-photo-533856.jpeg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    }}
    

/* ===== CONTENEDOR PRINCIPAL (CLAVE REAL) ===== */
    .main * {{
    color: {text_color} !important;
    }}

/* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] * {{
    background: {sidebar_bg} !important;
    backdrop-filter: blur(12px);
    }}

    section[data-testid="stSidebar"] * {{
        color: {text_color} !important;
    }}

    </style>
    """, unsafe_allow_html=True)

# 👇 LLAMADA CORRECTA
load_css()

# -------------------------
# 🧱 COMPONENTE REUTILIZABLE
# -------------------------
def card(content_func):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    content_func()
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# 📊 CONFIGURACIÓN GLOBAL MATPLOTLIB
# -------------------------
mpl.rcParams.update({
    "text.color": "white" if is_dark else "black",
    "axes.labelcolor": "white" if is_dark else "black",
    "xtick.color": "white" if is_dark else "black",
    "ytick.color": "white" if is_dark else "black",
    "axes.edgecolor": "white" if is_dark else "black"
})

# -------------------------
# 2. CARGA DE DATOS (Original)
# -------------------------
st.title("🐧 Los Pingüinos Bio-polares")
st.markdown("## Investigación y exploración interactiva de los datos del equipo II")

url = "https://raw.githubusercontent.com/xuangfm/ejercicio_pinguinos/analisis_univariado/df_clean_penguins.csv"

@st.cache_data
def load_data(url):
    return pd.read_csv(url)
text_color = "white" if is_dark else "#111"
df = load_data(url)
counts = df["species"].value_counts().reset_index()
counts.columns = ["species", "count"]

# Preparación de datos UI
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
mask = (
    df_ui["species"].isin(species) &
    df_ui["island"].isin(island) &
    df_ui["sex_ui"].isin(sex) &
    df_ui["clutch_ui"].isin(nido)
)

filtered_df = df[mask]

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
    
    col1, divider, col2 = st.columns([1, 0.1, 1])
    
    with col1:
        counts_pie = filtered_df["species"].value_counts().reset_index()
        # Se añade template="plotly_white" para que combine con el estilo de app_estilo.py
        fig_pie = px.pie(counts_pie, names="species", values="count", title="Especies observadas", template="plotly_white")
        st.plotly_chart(fig_pie, use_container_width=True)
   
    with col2:
        fig_hist = px.histogram(filtered_df, x="island", color="species", title="Distribución por Isla", template="plotly_white")
        st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("##### 342 observaciones")
    st.dataframe(counts, use_container_width = True, hide_index=True)
    
    st.divider()
    st.markdown("### Observación de anidado por especie")
    clutch_counts = (
        filtered_df
        .groupby(["species", "clutch_completion"])
        .size()
        .reset_index(name="count")
    )
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
        title="Proporción de exito",
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.markdown("### Distribucion de genero por especie")
    fig = px.histogram(
        filtered_df, 
        x="sex", 
        color="species",
        barmode="group",
        title="Existe paridad de genero",
        template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🧠 Resumen de hallazgos")
    sex_counts = filtered_df.groupby(["species", "sex"]).size().reset_index(name="count")

    for especie in sex_counts["species"].unique():
        subset = sex_counts[sex_counts["species"] == especie]
        total = subset["count"].sum()
        if total == 0: continue
        
        subset = subset.copy()
        subset["prop"] = subset["count"] / total
        max_count = subset["count"].max()
        top = subset[subset["count"] == max_count]

        if len(top) > 1:
            st.write(f"En la especie **{especie}** no hay un género predominante.")
        else:
            row = top.iloc[0]
            porcentaje = round(row["prop"] * 100, 1)
            st.write(f"En la especie **{especie}**, predomina el género **{row['sex']}** con un {porcentaje}% de los individuos.")
            if porcentaje < 60:
                st.write(f"En la especie **{especie}**, la distribución de género es bastante equilibrada.")

# --- TAB 2: ANÁLISIS UNIVARIADO ---
with tab2:
    st.subheader("📉 Análisis Univariado")
    variable = st.selectbox(
        "Selecciona una variable numérica:",
        ['culmen_length_(mm)', 'culmen_depth_(mm)', 'flipper_length_(mm)', 'body_mass_(g)']
    )

    if filtered_df.empty:
        st.warning("No hay datos disponibles con los filtros seleccionados.")
        st.stop()

    chart_type = st.radio("Selecciona tipo de visualización:", ["Histograma", "Boxplot", "Densidad (KDE)"], horizontal=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Aplicar transparencia a Matplotlib como en app_estilo.py
    fig.patch.set_alpha(0) 
    ax.set_facecolor((0,0,0,0))
    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    for spine in ax.spines.values():
        spine.set_color('white')

    if chart_type == "Histograma":
        sns.histplot(filtered_df[variable], bins=30, kde=True, ax=ax, color="#00b4d8")
        ax.set_title(f"Distribución de {variable}", color="white")
    elif chart_type == "Boxplot":
        sns.boxplot(x=filtered_df[variable], ax=ax, color="#00b4d8")
        ax.set_title(f"Boxplot de {variable}", color="white")
    elif chart_type == "Densidad (KDE)":
        sns.kdeplot(filtered_df[variable], fill=True, ax=ax, color="#00b4d8")
        ax.set_title(f"Densidad de {variable}", color="white")

    st.pyplot(fig)
    
    st.markdown("### 📊 Resumen estadístico")
    col1, col2, col3 = st.columns(3)
    col1.metric("Media", round(filtered_df[variable].mean(), 2))
    col2.metric("Mediana", round(filtered_df[variable].median(), 2))
    col3.metric("Desv. estándar", round(filtered_df[variable].std(), 2))
    
    st.divider()
    st.markdown("### Distribución por especie")
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    fig2.patch.set_alpha(0)
    ax2.set_facecolor((0,0,0,0))
    ax2.tick_params(colors='white')
    
    sns.kdeplot(data=filtered_df, x=variable, hue="species", fill=True, alpha=0.4, ax=ax2)
    ax2.set_title(f"Densidad de {variable} por especie", color="white")
    st.pyplot(fig2)

    max_value = filtered_df[variable].max()
    min_value = filtered_df[variable].min()
    st.info(f"El valor máximo observado en {variable} es de {round(max_value, 2)}, y el mínimo es {round(min_value, 2)}")

# --- TAB 3: GRÁFICOS INTERACTIVOS (Bivariado) ---
with tab3:
    st.subheader("Relaciones y proporciones")
    st.divider()
    st.markdown("## Análisis de masa corporal")
    fig = px.box(
        filtered_df,
        x="species",
        y="body_mass_(g)",
        color="species",
        title="Distribución de masa corporal por especie",
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    st.markdown("### Morfología del pico")
    fig_scatter = px.scatter(
        filtered_df, 
        x="culmen_length_(mm)", 
        y="culmen_depth_(mm)", 
        color="species",
        title="Análisis comparativo de la longitud y profundidad del pico",
        template="plotly_white",
        labels={"culmen_length_(mm)": "Longitud (mm)", "culmen_depth_(mm)": "Profundidad (mm)"}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)