import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Penguins", layout="wide")

st.title("🐧 Pingüinos")
st.markdown("## Exploración interactiva")

url = "https://raw.githubusercontent.com/xuangfm/ejercicio_pinguinos/analisis_univariado/df_clean_penguins.csv"

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

df = load_data(url)
counts = df["species"].value_counts().reset_index()
counts.columns = ["species", "count"]

# -------------------------
# 🎛️ FILTROS (SIDEBAR)
# -------------------------
st.sidebar.header("Filtros")

species = st.sidebar.multiselect(
    "Selecciona especie:",
    options=df["species"].unique(),
    default=df["species"].unique()
)

island = st.sidebar.multiselect(
    "Selecciona isla:",
    options=df["island"].unique(),
    default=df["island"].unique()
)
sex = st.sidebar.multiselect(
    "Selecciona sexo:",
    options=df["sex"].unique(),
    default=df["sex"].unique()
)
Nido = st.sidebar.multiselect(
    "Selecciona eclosión de nidos:",
    options=df["clutch_completion"].unique(),
    default=df["clutch_completion"].unique()
)

# -------------------------
# 🔍 FILTRADO
# -------------------------
filtered_df = df[
    (df["species"].isin(species)) &
    (df["island"].isin(island))
]

# -------------------------
# 📊 VISUALIZACIÓN
# -------------------------
st.write("### Datos filtrados")
st.dataframe(filtered_df)

# -------------------------
# 📈 GRÁFICOS
# -------------------------
# pie chart
fig = px.pie(
    counts,
    names="species",
    values="count",
    title="Especies obse"
)
st.plotly_chart(fig)


st.write("### Distribución de masa corporal")
st.bar_chart(filtered_df["body_mass_(g)"])

st.write("### Longitud del pico vs profundidad")
st.scatter_chart(
    filtered_df,
    x="culmen_length_(mm)",
    y="culmen_depth_(mm)"
)

st.write("### Distribución por eclosión de nidos")
st.bar_chart(
    filtered_df["clutch_completion"].value_counts(),
    use_container_width=True
)
    
# -------------------------
# 📌 INFO EXTRA
# -------------------------
st.write("Número de registros:", filtered_df.shape[0])


