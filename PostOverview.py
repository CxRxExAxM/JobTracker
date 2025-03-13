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
