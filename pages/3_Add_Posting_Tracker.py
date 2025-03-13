import streamlit as st
import sqlite3
from datetime import date

st.title("Add Job Posting")

conn = sqlite3.connect("../hr_database.db")
cursor = conn.cursor()

with st.form("jobdb.sqlite"):
    posted_options = cursor.execute("SELECT posted_name_id, posted_job_name FROM posted_jobs").fetchall()
    posted_name_id = st.selectbox("Posted Job Name", [f"{pid} - {pname}" for pid, pname in posted_options])
    posted_name_id = int(posted_name_id.split(" - ")[0])
    open_date = st.date_input("Open Date", value=date.today())
    close_date = st.date_input("Close Date (optional)", value=None)
    is_replacement = st.checkbox("Is Replacement?")
    replacing_whom = st.number_input("Replacing Whom (emp_id)", min_value=0, step=1) if is_replacement else None
    opened_by = st.number_input("Opened By (emp_id)", min_value=0, step=1)

    if st.form_submit_button("Add Posting"):
        cursor.execute("""
            INSERT INTO posting_tracker (posted_name_id, open_date, close_date, is_replacement, replacing_whom, opened_by)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (posted_name_id, open_date.isoformat(), close_date.isoformat() if close_date else None,
              is_replacement, replacing_whom, opened_by))
        conn.commit()
        st.success("Posting added!")

conn.close()