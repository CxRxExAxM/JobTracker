import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect('JobDB.sqlite')
df = pd.read_sql_query("""
    SELECT pt.posting_id, pj.posted_job_name, pt.open_date, pt.close_date,
           CASE WHEN pt.close_date IS NULL THEN 'Open' ELSE 'Closed' END AS status
    FROM posting_tracker pt
    JOIN posted_jobs pj ON pt.posted_name_id = pj.posted_name_id
""", conn)

st.subheader('Job Postings Overview')
st.dataframe(df)
st.download_button('Export to CSV', df.to_csv(index=False), 'postings.csv')
conn.close()


st.subheader("Add New Job Posting")
with st.form("add_posting"):
    job_options = pd.read_sql_query("SELECT posted_name_id, posted_job_name FROM posted_jobs", conn)["posted_job_name"].tolist()
    posted_job_name = st.selectbox("Job Name", job_options)
    open_date = st.date_input("Open Date")
    close_date = st.date_input("Close Date (optional)", value=None)
    is_replacement = st.checkbox("Is Replacement?")
    replacing_whom = st.number_input("Replacing Whom (emp_id)", min_value=0, step=1) if is_replacement else None
    if st.form_submit_button("Save"):
        # Insert logic here
        st.success("Posting added!")
