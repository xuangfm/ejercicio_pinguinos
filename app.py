import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl


# -------------------------
# CONFIGURACIÓN DE PÁGINA
# -------------------------
st.set_page_config(
    page_title="Pingüinos Bio-polares",
    layout="wide",
    page_icon="🐧"
)

is_dark = st.get_option("theme.base") == "dark"

# -------------------------
# 🎨 SISTEMA DE ESTILOS PRO (MEJORADO)
# -------------------------
def load_css():
    overlay = "rgba(20,0,0,1)" if is_dark else "rgba(255,255,255,0.3)"
    card_bg = "rgba(255,255,255,0.1)" if is_dark else "rgba(100,150,100,0.1)"
    text_color = "#F7F7F7" if is_dark else "#2A2424"
    
    st.markdown(f"""
    <style>
    /* Fondo General */
    .stApp {{
        background-image: linear-gradient({overlay}, {overlay}),
                          url("https://images.pexels.com/photos/533856/pexels-photo-533856.jpeg") !important;
        background-size: cover !important;
        background-attachment: fixed !important;
    }}
    /* Cabecera */
    header[data-testid="stHeader"] {{
        background: rgba(0,0,0,0) !important;
        backdrop-filter: blur(1px);
        -webkit-backdrop-filter: blur(8px);
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }}
    /* Títulos con Estilo */
    .main-title {{
        font-size: 2rem !important;
        font-weight: 500 !important;
        color: {text_color} !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 0px;
    }}
    
    .sub-title {{
        color: #00b4d8 !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        margin-bottom: 2rem;
    }}

    /* Tarjetas personalizadas para métricas */
    [data-testid="stMetricValue"] {{
        font-size: 2rem !important;
        color: #00b4d8 !important;
    }}
    
    div[data-testid="stMetric"] {{
        background: {card_bg};
        border-radius: 15px;
        padding: 10px !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }}

    /* Contenedores de Gráficos */
    div[data-testid="stPlotlyChart"], .stMatplotlibChart {{
        background: {card_bg} !important;
        border-radius: 20px !important;
        padding: 1px !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2) !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
    }}
    
    /* Contenedores de Gráficos */
    div[data-testid="stPlotlyChart"], .stMatplotlibChart {{
        background: {card_bg} !important;
        border-radius: 20px !important;
        padding: 1px !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2) !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
    }}
  

    /* Sidebar Refinado */
    section[data-testid="stSidebar"] {{
        background: rgba(1,1,1,0.1) !important;
        backdrop-filter: blur(5px);    
    }}
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {{
    background: rgba(255, 255, 255, 0.08) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    }}
    /* 🎯 Tags seleccionados en multiselect */
    section[data-testid="stSidebar"] [data-baseweb="tag"] {{
    background-color: rgba(0, 180, 216, 0.35) !important;
    color: white !important;
    border-radius: 8px !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }}
    
    
    .stMarkdown p {{ color: {text_color}; }}
    </style>
    """, unsafe_allow_html=True)

load_css()

# -------------------------
# 2. CARGA Y PROCESAMIENTO
# -------------------------
url = "https://raw.githubusercontent.com/xuangfm/ejercicio_pinguinos/dev/df_clean_penguins.csv"

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

df = load_data(url)
color_palette = {"adelie": "#98bd49",
                 "chinstrap": "#e622b8",
                 "gentoo": "#237ca5"}

# ----
# Manejo de nulos para la UI
df_ui = df.copy()
df_ui["sex_ui"] = df["sex"].fillna("Desconocido")
df_ui["clutch_ui"] = df["clutch_completion"].fillna("Desconocido")

# -------------------------
# 🏗️ HEADER CON HTML/MARKDOWN
# -------------------------
st.markdown('<h1 class="main-title">🐧 Los Pingüinos Bio-polares</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Investigación y exploración interactiva de datos • Equipo II</p>', unsafe_allow_html=True)

# -------------------------
# 🎛️ FILTROS (SIDEBAR)
# -------------------------
with st.sidebar:
    st.image("https://cdn.creazilla.com/silhouettes/7950517/penguin-silhouette-4bb7ee-lg.png", width=160)
    st.header("Filtros")
    
    species = st.multiselect("Especies:", options=sorted(df["species"].unique()), default=df["species"].unique())
    island = st.multiselect("Islas:", options=sorted(df["island"].unique()), default=df["island"].unique())
    sex = st.multiselect("Sexo:", options=sorted(df_ui["sex_ui"].unique()), default=df_ui["sex_ui"].unique())

# Filtrado de datos
mask = (df_ui["species"].isin(species) & df_ui["island"].isin(island) & df_ui["sex_ui"].isin(sex))
filtered_df = df_ui[mask].copy()

# -------------------------
# 📊 PESTAÑAS
# -------------------------
tab1, tab2, tab3 = st.tabs(["📋 Vista General", "📉 Univariado", "📊 Bivariado"])

# sugerencia skynet
all_species = ["adelie", "chinstrap", "gentoo"]
#-------
with tab1:
    # Visualización de datos
    with st.expander("🔍 Ver tabla de datos."):
        st.dataframe(filtered_df, use_container_width=True)
    # Métricas clave en la parte superior
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Observaciones", len(filtered_df))
    m2.metric("Especies Seleccionadas", len(species))
    m3.metric("Islas Cubiertas", len(island))

    st.spacer = st.markdown("<br>", unsafe_allow_html=True)
    
    #-----------
    col_left, col_right = st.columns(2)
   
    with col_left:
        fig_pie = px.pie(
            filtered_df,
            names="species",
            color="species",
            category_orders={"species": ["adelie", "chinstrap", "gentoo"]},# 👈 important
            color_discrete_map=color_palette,         
            hole=0.4,
            title="Distribución de Especies"
        )       
        fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white" if is_dark else "black")
        st.plotly_chart(fig_pie, use_container_width=True,)
        
        st.divider()
        fig_sex = px.histogram(
            filtered_df,
            x="sex",
            color="species",
            category_orders={"species": ["adelie", "chinstrap", "gentoo"]},
            barmode="group",
            title="Existe paridad de género",
            color_discrete_map=color_palette
        )
        fig_sex.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_sex, use_container_width=True)
    
    with col_right:
        fig_hist = px.histogram(
            filtered_df,
            x="island",
            color="species",
            barmode="group",
            category_orders={"species": ["adelie", "chinstrap", "gentoo"]},
            title="Población por Isla",
            color_discrete_map=color_palette
        )
        fig_hist.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white" if is_dark else "black")
        st.plotly_chart(fig_hist, use_container_width=True)

        st.divider()

        clutch_counts = filtered_df.groupby(["species", "clutch_completion"]).size().reset_index(name="count")
        clutch_counts["proportion"] = clutch_counts["count"] / clutch_counts.groupby("species")["count"].transform("sum")
        fig_clutch = px.bar(
            clutch_counts,
            x="clutch_completion",
            y="proportion",
            color="species",
            category_orders={"species": ["adelie", "chinstrap", "gentoo"]},
            barmode="group",
            title="Observación de anidado por especie",
            color_discrete_map=color_palette
        )
        fig_clutch.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_clutch, use_container_width=True)

       
    with st.expander("🔍 Resumen estadístico."):
        st.write(filtered_df[["species", "island", "sex", "culmen_length_(mm)", "culmen_depth_(mm)", "flipper_length_(mm)", "body_mass_(g)"]].describe())
    
    

with tab2:
    st.markdown("### 🧬 Análisis de Atributos")
    variable = st.selectbox("Selecciona una variable numérica:", ['culmen_length_(mm)', 'culmen_depth_(mm)', 'flipper_length_(mm)', 'body_mass_(g)'])
    chart_type = st.radio("Selecciona tipo de visualización:", ["Histograma", "Boxplot", "Densidad (KDE)"], horizontal=True)

    fig, ax = plt.subplots(figsize=(10, 4))
    fig.patch.set_alpha(0)
    ax.set_facecolor((0,0,0,0))
    
    if chart_type == "Histograma":
        sns.histplot(filtered_df[variable], bins=30, kde=True, ax=ax, color="#00b4d8")
    elif chart_type == "Boxplot":
        sns.boxplot(x=filtered_df[variable], ax=ax, color="#00b4d8")
    elif chart_type == "Densidad (KDE)":
        sns.kdeplot(filtered_df[variable], fill=True, ax=ax, color="#00b4d8")
    
    st.pyplot(fig)
    
    st.markdown("### 📊 Resumen estadístico")
    c1, c2, c3 = st.columns(3)
    c1.metric("Media", round(filtered_df[variable].mean(), 2))
    c2.metric("Mediana", round(filtered_df[variable].median(), 2))
    c3.metric("Desv. estándar", round(filtered_df[variable].std(), 2))
    
    st.divider()
    st.markdown("### Distribución por especie")
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    fig2.patch.set_alpha(0)
    ax2.set_facecolor((0,0,0,0))
    sns.kdeplot(data=filtered_df, x=variable, hue="species", fill=True, alpha=0.4, ax=ax2)
    st.pyplot(fig2)

with tab3:
    st.markdown("### 🔗 Relaciones Morfológicas")
    
    st.markdown("## Análisis de masa corporal")
    fig_box = px.box(filtered_df, x="species", y="body_mass_(g)", color="species", title="Distribución de masa corporal por especie")
    fig_box.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_box, use_container_width=True)

    st.divider()
    #grafica sobre  formas de pico
    st.markdown("### Morfología del pico")
    
    fig_scatter = px.scatter(
        filtered_df,
        x="culmen_length_(mm)",
        y="culmen_depth_(mm)", 
        color="species",
        size="body_mass_(g)",
        hover_name="island",
        title="Longitud vs Profundidad del Culmen (Pico)",
        template="plotly_dark" if is_dark else "plotly_white"
    )
    fig_scatter.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_scatter, use_container_width=True)
    #----------

    st.divider()
    st.markdown("### Relación entre aleta y género, distribuida por especie")
    
 ##--------

    fig_flipper_sex = px.strip(
        filtered_df,
            x="sex",
            y="flipper_length_(mm)",
            color="species",
            hover_name="species",
            title="Flipper length por sexo y especie"
    )

    fig_flipper_sex.update_traces(jitter=1, pointpos=2, marker_size=15, opacity=0.9, marker_line_width=1)

    fig_flipper_sex.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white" if is_dark else "black",
        legend_title_text="Especie"
    )

    st.plotly_chart(fig_flipper_sex, use_container_width=True)
