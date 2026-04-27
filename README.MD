# 🐧 Bitácora de Proyecto: Expedición Antártida Bio-Polar
> **Estado:** En Progreso 🟢 | **Versión:** 1.0 | **Investigadores:** Alejandro08, Francisco, Graceila, Diana, Julia, Juan.G

---
## [Abrir Dashboard](https://biopolares.streamlit.app/){:target="_blank" rel="noopener"}

## 📋 Resumen del Proyecto
Este proyecto tiene como objetivo el estudio demográfico y morfométrico de tres especies de pingüinos en el Archipiélago Palmer. Se busca identificar patrones de crecimiento y diferencias clave entre especies según su hábitat.

### 📍 Ubicación de Estudio
* **Islas:** Torgersen, Biscoe y Dream.
* **Especies:** Adélie, Chinstrap y Gentoo.

---

## 📅 Diario de Campo

### [Día 1] - Inicio de la Observación
**Fecha:** 14 de Abril, 2026
**Clima:** -12°C, Viento fuerte.

* **Actividad:** Calibración de equipos de medición.
* **Observaciones:** Se detectó una colonia masiva de pingüinos *Adélie* en la Isla Torgersen.
* **Notas:** Los sensores de peso deben limpiarse cada 2 horas debido al hielo.

---

## 📊 Datos y Metodología

Para el análisis, nos centramos en cuatro variables críticas:

1.  **Longitud del culmen (mm):** Largo del pico.
2.  **Profundidad del culmen (mm):** Grosor del pico.
3.  **Longitud de la aleta (mm).**
4.  **Masa corporal (g).**

### 🔬 Clasificación de Especies

| Especie | Isla nacimiento | Pico (promedio) | Notas |
| :--- | :--- | :--- | :--- |
| **Adélie** | Dream | Corto / Grueso | Muy territoriales |
| **Chinstrap** | Dream | Largo / Grueso | "Barbijo" distintivo |
| **Gentoo** | Biscoe | Largo / Estrecho | Los de mayor tamaño |

---

## 📉 Hallazgos Preliminares

> [!TIP]
> **Dato Curioso:** Existe una correlación positiva alta entre la masa corporal y la longitud de la aleta en los pingüinos Gentoo.

### Visualización de Referencia
A continuación se muestra un esquema de cómo se mide el pico (culmen):



```python
# Ejemplo de código para cargar datos en Python
import seaborn as sns
penguins = sns.load_dataset("penguins")
print(penguins.groupby('species').mean())
```
### [Día 7] - Inicio de la Observación
**Fecha:** 21 de Abril, 2026
**Clima:** -7°C, Viento ligero.

* **Actividad:** Preparación del proyecto para su lanzamiento.
* **Observaciones:** Se detectaron varios fallos, detallados mas adelante
* **Notas:** Los sensores de peso deben limpiarse cada 5 horas debido al hielo.

```python
# Ejemplo de código para cargar datos en Streamlit
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Penguins", layout="wide")

st.title("🐧 Los Pingüinos Bio-polares")
st.markdown("## Investigación y exploración interactiva de los datos del equipo II")

url = "https://raw.githubusercontent.com/xuangfm/ejercicio_pinguinos/analisis_univariado/df_clean_penguins.csv"

```
* **Limitaciones del proyecto:** Detallamos las limitaciones encontradas durante el estudio.
```
1- Desconocer el objetivo del estudio.

2.- Las ID no son individuales de cada pinguino, la identificación es general y anual.

3.- ¿la ausencia de registros de algunas especies en determindas islas, se debe a una ausencia real o inaccesibilidad a los nidos?

4.- Datos inexistentes o nulos. La muestra aportada no desvela si es el 100% de la nueva población.
```

* **Conclusiones :** En cuanto a datos.

```
1.- El dataset no es equilibrado en cuanto a sus especies. No todas las especies de pinguinos nacen en todas las islas.

2.- El dataset tiene falta de datos. Principalmente en el sexo de los pinguinos

3.- Detectamos tres variables: especies, islas y sexo

4.-La mitad de los pingüinos nacen en la isla Biscoe, una minoria (Adelie) en la isla Torgersen, y los demás en la isla Dream.

5.- Solo se registra el primer año de vida del pinguino en cada estudio.
```

* **Recomendaciones:** Detallamos las limitaciones encontradas durante el estudio.

```
1-. Añadir casillas múltiples para concretar el motivo por el que no se han recogido las muestras, ejem. Innaccesibilidad al nido, falta de material adecuado para realizarlas.

2.- Organizar muestreo individualizado para cada individuo.

3.- No se puede concluir con estos datos la vida del pinguino, porque solo tenemos datos de un año. Quizás sería interesante ampliar el periodo del estudio.
```

### [Día 14] - Fin de la Observación
**Fecha:** 28 de Abril, 2026
**Clima:** -17°C, nevada fuerte.

* **Actividad:** Presentación del proyecto.
* **Observaciones:** Se detectaron nervios.
* **Notas:** Los sensores de peso deben limpiarse cada 1 hora debido al hielo.

