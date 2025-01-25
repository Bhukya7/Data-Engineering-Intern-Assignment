import streamlit as st
import requests

st.title("Log Analyzer")

log_level = st.selectbox("Select Log Level", ["INFO", "ERROR", "WARN"])
start_time = st.text_input("Start Time (YYYY-MM-DD HH:mm:ss)")
end_time = st.text_input("End Time (YYYY-MM-DD HH:mm:ss)")

if st.button("Fetch Logs"):
    response = requests.get("http://localhost:8000/logs", params={"log_level": log_level, "start_time": start_time, "end_time": end_time})
    
    if response.status_code == 200:
        logs = response.json().get("logs", [])
        st.write(logs)