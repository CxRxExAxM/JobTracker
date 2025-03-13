import streamlit as st
import sqlite3

st.title("Add Posted Jobs")

conn = sqlite3.connect("jobDB.sqlite")
cursor = conn.cursor()

with st.form("add_posted_job"):
    dayforce_options = cursor.execute("SELECT dayforce_id, dayforce_job_name FROM dayforce_jobs").fetchall()
    dayforce_id = st.selectbox("Dayforce Job", [f"{jid} - {jname}" for jid, jname in dayforce_options])
    dayforce_id = int(dayforce_id.split(" - ")[0])
    posted_job_name = st.text_input("Posted Job Name", max_chars=100)

    if st.form_submit_button("Add Posted Job"):
        if not posted_job_name:
            st.error("Posted Job Name is required!")
        else:
            cursor.execute("INSERT INTO posted_jobs (dayforce_id, posted_job_name) VALUES (?, ?)",
                          (dayforce_id, posted_job_name))
            conn.commit()
            st.success(f"Added posted job: {posted_job_name}")

conn.close()