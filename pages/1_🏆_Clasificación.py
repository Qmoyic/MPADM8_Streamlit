import streamlit as st
import matplotlib.pyplot as plt
from utils.loaders import load_standings
from utils.pdf import generate_classification_pdf
import streamlit.components.v1 as components

# ------------------------
# Seguridad
# ------------------------

if not st.session_state.get("logged_in", False):
    st.warning("Debes iniciar sesión.")
    st.stop()

st.title("🏆 Clasificación Liga Endesa")

df, source = load_standings()  

st.caption(f"Fuente de datos: {'API ACB' if source == 'api' else 'CSV de respaldo'}")

if source == "csv":
    st.warning(
        "No se ha podido conectar con la API. Mostrando la última copia disponible."
    )

st.write(
    "Consulta la clasificación actual de la Liga Endesa con los principales indicadores de rendimiento."
)
# ------------------------
# Datos
# ------------------------

df = (
    df.rename(
        columns={
            "position": "Pos",
            "fullName": "Equipo",
            "wins": "V",
            "loses": "D",
            "winPercentage": "% Victorias",
            "pointsFor": "Puntos a Favor",
            "pointsAgainst": "Puntos en Contra",
            "plusMinus": "+/-"
        }
    )
    .assign(
        **{
            "% Victorias": lambda x: x["% Victorias"].round(2),
        }
    )
    .sort_values("Pos")
    [
        [
            "Pos",
            "Equipo",
            "V",
            "D",
            "% Victorias",
            "Puntos a Favor",
            "Puntos en Contra",
            "+/-"
        ]
    ]
)

df_display = df.copy()

df_display["Puntos a Favor"] = (
    df_display["Puntos a Favor"]
    .map("{:,}".format)
)

df_display["Puntos en Contra"] = (
    df_display["Puntos en Contra"]
    .map("{:,}".format)
)


# ------------------------
# KPIs
# ------------------------

leader = str(df.iloc[0]["Equipo"])

best_attack = str(df.loc[df["Puntos a Favor"].idxmax(), "Equipo"])

best_defense = str(df.loc[df["Puntos en Contra"].idxmin(), "Equipo"])
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="🏆 Líder",
        value=leader
    )

with col2:
    st.metric(
        label="🔥 Mejor ataque",
        value=best_attack
    )

with col3:
    st.metric(
        label="🛡️ Mejor defensa",
        value=best_defense
    )

# ------------------------
# SEPARADOR
# ------------------------
st.divider()

# ------------------------
# TABLA
# ------------------------

st.subheader("Clasificación")

st.dataframe(
    df_display,
    use_container_width=True,
    hide_index=True
)

pdf = generate_classification_pdf(df_display)

st.download_button(
    label="📄 Descargar clasificación en PDF",
    data=pdf,
    file_name="clasificacion_liga_endesa.pdf",
    mime="application/pdf"
)

# ------------------------
# SEPARADOR
# ------------------------
st.divider()

# ------------------------
# ZONA RESERVADA PARA EL GRÁFICO
# ------------------------
st.subheader("Visualización")

# ------------------------
# Gráfico diferencial (+/-)
# ------------------------

df_chart = df.sort_values("+/-", ascending=True)

fig, ax = plt.subplots(figsize=(5, 4.5))

bars = ax.barh(
    df_chart["Equipo"],
    df_chart["+/-"]
)

ax.set_title(
    "Diferencial de puntos por equipo",
    fontsize=10
)

ax.set_xlabel(
    "Diferencial (+/-)",
    fontsize=9
)

ax.set_ylabel("")

ax.tick_params(axis="x", labelsize=8)
ax.tick_params(axis="y", labelsize=8)

ax.grid(axis="x", alpha=0.3)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)


for bar in bars:
    width = bar.get_width()
    y = bar.get_y() + bar.get_height() / 2

    if width >= 0:
        ax.text(
            width + 5,
            y,
            f"{int(width)}",
            va="center",
            ha="left",
            fontsize=7
        )
    else:
        ax.text(
            width + 5,
            y,
            f"{int(width)}",
            va="center",
            ha="left",
            fontsize=7,
            color="white",
            fontweight="bold"
        )

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.pyplot(fig, use_container_width=False)

# st.divider()

st.subheader("¿Cómo imprimir la página actual?")

st.info(
    "Utiliza la opción de impresión del navegador (Ctrl+P en Windows o Cmd+P en macOS)."
)