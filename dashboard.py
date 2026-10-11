"""Dashboard for Madrid job offers."""

import pandas as pd
import streamlit as st
from psycopg.rows import dict_row

from careerpulse.database import get_connection

st.set_page_config(
    page_title="CareerPulse AI · Madrid",
    page_icon="📊",
    layout="wide",
)

st.title("CareerPulse AI · Ofertas tecnológicas en Madrid")
st.caption(
    "Ofertas obtenidas de Adzuna y de un CSV de ejemplo, "
    "transformadas y guardadas en PostgreSQL."
)

with get_connection() as connection, connection.cursor(row_factory=dict_row) as cursor:
    cursor.execute(
        """
        SELECT job_id, title, company, location, technology,
               salary_min, salary_max, remote, source
        FROM jobs
        WHERE LOWER(location) LIKE '%madrid%'
        ORDER BY job_id DESC
        """
    )
    jobs = pd.DataFrame(cursor.fetchall())

if jobs.empty:
    st.info("Todavía no hay ofertas de Madrid en la base de datos.")
    st.stop()

source_column, technology_column, remote_column = st.columns(3)

with source_column:
    source = st.selectbox(
        "Origen",
        ["Todos", *sorted(jobs["source"].dropna().unique())],
    )

with technology_column:
    technology = st.selectbox(
        "Tecnología",
        ["Todas", *sorted(jobs["technology"].dropna().unique())],
    )

with remote_column:
    remote = st.selectbox("Trabajo remoto", ["Todos", "Sí", "No"])

search = st.text_input(
    "Buscar por puesto o empresa",
    placeholder="Por ejemplo: Python",
).strip()

visible_jobs = jobs.copy()

if source != "Todos":
    visible_jobs = visible_jobs[visible_jobs["source"] == source]

if technology != "Todas":
    visible_jobs = visible_jobs[visible_jobs["technology"] == technology]

if remote != "Todos":
    visible_jobs = visible_jobs[
        visible_jobs["remote"] == (remote == "Sí")
    ]

if search:
    matches_title = visible_jobs["title"].str.contains(
        search, case=False, regex=False, na=False
    )
    matches_company = visible_jobs["company"].str.contains(
        search, case=False, regex=False, na=False
    )
    visible_jobs = visible_jobs[matches_title | matches_company]

if visible_jobs.empty:
    st.info("No hay ofertas que coincidan con esos filtros.")
    st.stop()

total_column, remote_metric_column, salary_column = st.columns(3)

with total_column:
    st.metric("Ofertas mostradas", len(visible_jobs))

with remote_metric_column:
    st.metric("Marcadas como remotas", int(visible_jobs["remote"].sum()))

with salary_column:
    st.metric(
        "Con salario mínimo informado",
        int(visible_jobs["salary_min"].notna().sum()),
    )

st.subheader("Ofertas por perfil")

titles = visible_jobs["title"].fillna("")
profiles = pd.Series("Otros perfiles", index=visible_jobs.index)

profiles.loc[titles.str.contains("data analyst", case=False, regex=False)] = (
    "Data Analyst"
)
profiles.loc[titles.str.contains("data engineer", case=False, regex=False)] = (
    "Data Engineer"
)
profiles.loc[titles.str.contains("data architect", case=False, regex=False)] = (
    "Data Architect"
)
profiles.loc[titles.str.contains("data scientist", case=False, regex=False)] = (
    "Data Scientist"
)

st.bar_chart(profiles.value_counts())

st.subheader("Tecnologías identificadas")
known_technologies = visible_jobs.loc[
    visible_jobs["technology"] != "Unknown", "technology"
]

if known_technologies.empty:
    st.info("No se identificaron tecnologías en estas ofertas.")
else:
    st.bar_chart(known_technologies.value_counts())

st.subheader("Detalle de las ofertas")
st.dataframe(visible_jobs, hide_index=True, use_container_width=True)

st.caption(
    "La etiqueta «Unknown» indica que no se identificó una tecnología. "
    "El indicador de trabajo remoto se deduce del texto de la oferta. "
    "Es una muestra pequeña y no representa todo el mercado laboral de Madrid."
)