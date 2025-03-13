import streamlit as st
import sqlite3

st.title("Add Sources")

conn = sqlite3.connect("jobdb.sqlite")
cursor = conn.cursor()

with st.form("add_source"):
    posting_options = cursor.execute("SELECT posting_id FROM posting_tracker").fetchall()
    posting_id = st.selectbox("Posting ID", [p[0] for p in posting_options])
    source_name = st.selectbox("Source", ["Indeed", "LinkedIn", "SmartRecruiters", "Corp Website", "Hotel Site", "Referral", "Other"])
    source_details = st.text_input("Details (optional)") if source_name == "Other" else None
    referral_emp_id = st.number_input("Referral emp_id (required for Referral)", min_value=0, step=1) if source_name == "Referral" else None

    if st.form_submit_button("Add Source"):
        if source_name == "Referral" and not referral_emp_id:
            st.error("Referral requires an employee ID!")
        else:
            cursor.execute("INSERT INTO sources (posting_id, source_name, source_details, referral_emp_id) VALUES (?, ?, ?, ?)",
                          (posting_id, source_name, source_details, referral_emp_id))
            conn.commit()
            st.success(f"Source '{source_name}' added!")

conn.close()