"""Local dashboard for Madrid job offers."""

import pandas as pd
import streamlit as st
from psycopg.rows import dict_row

from careerpulse.database import get_connection

st.set_page_config(page_title="CareerPulse AI", page_icon="📊")
st.title("CareerPulse AI · Madrid")
st.caption("Exploración de las ofertas guardadas en PostgreSQL.")

with get_connection() as connection, connection.cursor(row_factory=dict_row) as cursor:
    cursor.execute(
        """
        SELECT job_id, title, company, location, technology,
               salary_min, salary_max, remote, source
        FROM jobs
        WHERE LOWER(location) LIKE '%madrid%'
        ORDER BY job_id
        """
    )
    jobs = pd.DataFrame(cursor.fetchall())

if jobs.empty:
    st.info("Todavía no hay ofertas de Madrid en la base de datos.")
    st.stop()

source = st.selectbox(
    "Origen de las ofertas",
    ["Todos", *sorted(jobs["source"].unique())],
)

visible_jobs = jobs if source == "Todos" else jobs[jobs["source"] == source]

st.metric("Ofertas mostradas", len(visible_jobs))
st.dataframe(visible_jobs, hide_index=True)

st.subheader("Ofertas por tecnología")
st.bar_chart(visible_jobs["technology"].value_counts())
st.caption(
    "Unknown indica que no se identificó una tecnología. "
    "Estos datos son una muestra pequeña, no una estimación del mercado."
)