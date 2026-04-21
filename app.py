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
    options=sorted(df["species"].dropna().unique()),
    default=sorted(df["species"].dropna().unique())
)

island = st.sidebar.multiselect(
    "Selecciona isla:",
    options=sorted(df["island"].dropna().unique()),
    default=sorted(df["island"].dropna().unique())
)

sex = st.sidebar.multiselect(
    "Selecciona sexo:",
    options=sorted(df["sex"].dropna().unique()),
    default=sorted(df["sex"].dropna().unique())
)

Nido = st.sidebar.multiselect(
    "Selecciona eclosión de nidos:",
    options=sorted(df["clutch_completion"].dropna().unique()),
    default=sorted(df["clutch_completion"].dropna().unique())
)

# -------------------------
# 🔍 FILTRADO
# -------------------------
filtered_df = df[
    (df["species"].isin(species)) &
    (df["island"].isin(island)) &
    (df["sex"].isin(sex)) &
    (df["clutch_completion"].isin(Nido))
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
    title="Especies observadas"
)
st.plotly_chart(fig, use_container_width=True)


mass_by_species = (
    filtered_df
    .groupby("species")["body_mass_(g)"]
    .mean()
    .reset_index()
)

fig = px.bar(
    mass_by_species,
    x="species",
    y="body_mass_(g)",
    color="species",
    title="Masa corporal promedio por especie",
    labels={"body_mass_(g)": "Masa corporal (g)"}
)

st.plotly_chart(fig, use_container_width=True)

fig = px.scatter(
    filtered_df,
    x="culmen_length_(mm)",
    y="culmen_depth_(mm)",
    color="species",
    title="Relación longitud vs profundidad del pico",
    labels={
        "culmen_length_(mm)": "Longitud (mm)",
        "culmen_depth_(mm)": "Profundidad (mm)"
    }
)

st.plotly_chart(fig, use_container_width=True)

clutch_counts = filtered_df["clutch_completion"].value_counts().reset_index()
clutch_counts.columns = ["clutch_completion", "count"]

fig = px.bar(
    clutch_counts,
    x="clutch_completion",
    y="count",
    color="clutch_completion",
    title="Distribución de eclosión de nidos"
)

st.plotly_chart(fig, use_container_width=True)

    
# -------------------------
# 📌 INFO EXTRA
# -------------------------
st.write("Número de registros:", filtered_df.shape[0])


