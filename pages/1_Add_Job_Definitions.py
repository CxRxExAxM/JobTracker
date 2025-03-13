import streamlit as st
import sqlite3

st.title("Add Job Definitions")

# Database connection
conn = sqlite3.connect("jobDB.sqlite")
cursor = conn.cursor()

# Form
with st.form("add_job_definition"):
    dayforce_job_name = st.text_input("Dayforce Job Name", max_chars=100)
    is_exempt = st.checkbox("Is Exempt?")
    hourly_level = st.selectbox("Hourly Level (if not exempt)", [None, 1, 2, 3], index=0) if not is_exempt else None
    manager_level = st.selectbox("Manager Level (if exempt)", [None, 1, 2, 3, 4], index=0) if is_exempt else None
    # Dropdown for reports_to (optional)
    job_options = cursor.execute("SELECT dayforce_id, dayforce_job_name FROM dayforce_jobs").fetchall()
    reports_to = st.selectbox("Reports To (optional)", [None] + [f"{jid} - {jname}" for jid, jname in job_options], index=0)
    reports_to_id = None if reports_to is None else int(reports_to.split(" - ")[0])

    if st.form_submit_button("Add Job Definition"):
        if not dayforce_job_name:
            st.error("Job Name is required!")
        else:
            cursor.execute("""
                INSERT INTO dayforce_jobs (dayforce_job_name, is_exempt, hourly_level, manager_level, reports_to)
                VALUES (?, ?, ?, ?, ?)
            """, (dayforce_job_name, is_exempt, hourly_level, manager_level, reports_to_id))
            conn.commit()
            st.success(f"Added job: {dayforce_job_name}")

conn.close()