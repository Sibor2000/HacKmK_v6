import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Konnekt - Monitoring", page_icon=":car:", layout="wide")

st.title("Monitoring")

df = pd.read_csv("data/waaa_detailed.csv")

def getAudits():
    return [
        {
            "Location": "Berlin",
            "reasons": [
                "High number of complaints",
                "High number of late deliveries",
            ]
        }
    ]

complaint_emojis = {
    "Late": "🕒",
    "Damaged Product": "📦",
    "Missing Product": "❌",
    "Wrong product": "❓",
    # Palm tree because why not
    "Other": "🌴",
}

col1, col2 = st.columns([1, 1])

with col2:
    st.subheader("Complaints")
    # Sort the complaints by time, only select the middle 30
    for i, row in df.sort_values("Time").iloc[210:240].iterrows():
        emoji = complaint_emojis.get(row["Complaint"], "❓")
        with st.container(border=True):
            col11, col12 = st.columns([1, 6])
            with col11:
                st.header(emoji)
            with col12:
                st.write(f"**{row['Complaint']}** in {row['District']}\n\nat {row['Time']}")

with col1:
    st.subheader("Audit Events")
    # Show a progress spinner for 4 seconds
    with st.spinner("Loading audit events..."):
        time.sleep(4)

    audits = getAudits()
    st.warning(f"Found {len(audits)} unusual complaint patterns")
    for audit in audits:
        with st.expander(f"🔍 Audit for {audit['Location']} office"):
            st.write(f"An audit should be performed at {audit['Location']} because of the following reasons:")
            for reason in audit["reasons"]:
                st.write(f"- {reason}")