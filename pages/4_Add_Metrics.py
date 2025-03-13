import streamlit as st
import sqlite3
from datetime import date

st.title("Add Metrics")

conn = sqlite3.connect("jobdb.sqlite")
cursor = conn.cursor()

with st.form("add_metrics"):
    posting_options = cursor.execute("SELECT posting_id FROM posting_tracker").fetchall()
    posting_id = st.selectbox("Posting ID", [p[0] for p in posting_options])
    applicant_total = st.number_input("Total Applicants", min_value=0, step=1)
    applicants_called = st.number_input("Applicants Called", min_value=0, step=1)
    applicants_interviewed = st.number_input("Applicants Interviewed", min_value=0, step=1)

    if st.form_submit_button("Add Metrics"):
        cursor.execute("""
            INSERT INTO posting_metrics (posting_id, applicant_total, applicants_called, applicants_interviewed, recorded_date)
            VALUES (?, ?, ?, ?, ?)
        """, (posting_id, applicant_total, applicants_called, applicants_interviewed, date.today().isoformat()))
        conn.commit()
        st.success("Metrics added!")

conn.close()