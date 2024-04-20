import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Konnekt - Monitoring", page_icon=":car:", layout="wide")

st.title("Monitoring")

df = pd.read_csv("data/waaa_detailed.csv")
dng = pd.read_csv("data/waaa_danger.csv")

def getAudits():
    cluster_boundaries = {
        0.13258585045228255: {'label': 'Safe', 'complaint_threshold': 4},
        0.22391832056115185: {'label': 'Low Risk', 'complaint_threshold': 8},
        0.32837354917314765: {'label': 'Medium Risk', 'complaint_threshold': 12},
        0.4309576057897442: {'label': 'Considerable Risk', 'complaint_threshold': 16},
        0.6960472349781424: {'label': 'High Risk', 'complaint_threshold': 20},
        1.0: {'label': 'Very High Risk', 'complaint_threshold': 24},
    }

    # Get unique locations
    locations = df["Location"].unique()
    # For each location, calculate the number of "Missing Product" complaints
    for location in locations:
        missing_product_count = df[(df["Location"] == location) & (df["Complaint"] == "Missing Product")].shape[0]
        # Get danger score for the location through sch association
        sch = df[df["Location"] == location]["sch"].values[0]
        danger_score = dng[dng["sch"] == sch]["danger_score"].values[0]
        # Find the cluster boundary that the danger score falls into
        cluster = None
        for boundary, cluster_data in cluster_boundaries.items():
            if danger_score <= boundary:
                cluster = cluster_data
                break
        
        # If the number of complaints is higher than the threshold for the cluster, add the location to the audit list
        if cluster and missing_product_count > cluster["complaint_threshold"]:
            yield {
                "Location": location,
                "reasons": [
                    f"High number of Missing Product complaints in a {cluster['label']} neighborhood",
                    f"New delivery drivers in the area",
                ]
            }

    # Also add a random audit
    yield {
        "Location": "Kreuzberg",
        "reasons": [
            "High number of recent complaints",
            "High number of Damaged Products reported",
            "Routine inspection due",
        ]
    }

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

    audits = [a for a in getAudits()]
    st.warning(f"Found {len(audits)} unusual complaint patterns!")
    for audit in audits:
        with st.expander(f"🔍 Audit for {audit['Location']} office", expanded=True):
            st.write(f"An audit should be performed at {audit['Location']} because of the following reasons:")
            for reason in audit["reasons"]:
                st.write(f"- {reason}")
            x, y = st.columns([3, 1])
            with y:
                st.button("Schedule Audit", key=f"audit_{audit['Location']}")