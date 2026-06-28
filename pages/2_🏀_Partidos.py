import streamlit as st
import pandas as pd
from utils.loaders import load_matches
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

# ------------------------
# Seguridad
# ------------------------

if not st.session_state.get("logged_in", False):
    st.warning("Debes iniciar sesión.")
    st.stop()

st.title("🏀 Partidos Liga Endesa")

df, source = load_matches()

st.caption(f"Fuente de datos: {'API ACB' if source == 'api' else 'CSV de respaldo'}")

if source == "csv":
    st.warning(
        "No se ha podido conectar con la API. Mostrando la última copia disponible."
    )

st.write(
    "Consulta los resultados y el estado de los partidos de la última jornada disputada."
)

df = (
    df.rename(
        columns={
            "startDateTime": "Fecha",
            "homeTeam": "Local",
            "awayTeam": "Visitante",
            "homeScore": "Pts Local",
            "awayScore": "Pts Visitante",
            "matchStatus": "Estado"
        }
    )
)

df["Fecha"] = (
    pd.to_datetime(df["Fecha"])
    .dt.strftime("%d/%m/%Y %H:%M")
)

df["Resultado"] = (
    df["Pts Local"].astype(str)
    + " - "
    + df["Pts Visitante"].astype(str)
)

df_table = df[
    [
        "Fecha",
        "Local",
        "Resultado",
        "Visitante",
        "Estado"
    ]
]

st.divider()

st.subheader("Resultados")

st.dataframe(
    df_table,
    hide_index=True,
    use_container_width=True
)

st.divider()

###### VISUALIZACIÓN #####

df_plot = df.copy()

st.subheader("Visualización")

fig, ax = plt.subplots(figsize=(5, 2.8))

x = range(len(df_plot))
width = 0.35

bars_home = ax.bar(
    [i - width / 2 for i in x],
    df_plot["Pts Local"],
    width=width,
    label="Local"
)

bars_away = ax.bar(
    [i + width / 2 for i in x],
    df_plot["Pts Visitante"],
    width=width,
    label="Visitante"
)

ax.set_xticks(x)

ax.set_xticklabels(
    [
        f"{l}\nvs\n{v}"
        for l, v in zip(
            df_plot["Local"],
            df_plot["Visitante"]
        )
    ],
    fontsize=8
)

ax.set_title(
    "Puntos anotados por partido",
    fontsize=10
)

ax.set_ylabel(
    "Puntos",
    fontsize=9
)

ax.tick_params(axis="y", labelsize=8)

ax.legend(fontsize=8)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.grid(axis="y", alpha=0.3)

ax.bar_label(
    bars_home,
    fontsize=7,
    padding=2
)

ax.bar_label(
    bars_away,
    fontsize=7,
    padding=2
)

fig.tight_layout()

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.pyplot(fig, use_container_width=False)
# st.divider()

st.subheader("¿Cómo imprimir la página actual?")

st.info(
    "Utiliza la opción de impresión del navegador (Ctrl+P en Windows o Cmd+P en macOS)."
)