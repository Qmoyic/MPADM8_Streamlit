# ACB Basketball Dashboard

Aplicación web desarrollada con **Streamlit** para visualizar información de la Liga Endesa mediante datos obtenidos desde la **API oficial de la ACB**.

## Funcionalidades

- Consulta de la clasificación de la Liga Endesa.
- Visualización de los partidos de la última jornada.
- Gráficos interactivos.
- Exportación de la clasificación a PDF.
- Autenticación de usuario.

## Tecnologías

- Python
- Streamlit
- Pandas
- Matplotlib
- Requests
- ReportLab

## Estructura del proyecto

```
MPADM8_Streamlit/
├── app.py
├── pages/
├── utils/
├── data/
├── assets/
└── requirements.txt
```

## Instalación

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Fuente de datos

- API oficial de la ACB.
- Archivos CSV como respaldo en caso de indisponibilidad de la API.

## Autor

Enrique Moya