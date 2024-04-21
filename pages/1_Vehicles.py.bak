import streamlit as st
import time

def genId():
    return str(hex(int(time.time() * 10000000))[2:])

st.set_page_config(page_title="Konnekt - Vehicles", page_icon=":car:", layout="wide")

st.title("Vehicles")

# Define vehicle types and corresponding emojis
vehicle_types = {
    "Personal Car": "🚗",
    "Cargo Transport": "🚛",
    "Train": "🚄",
}

vehicle_conditions = {
    20: "poor",
    40: "average",
    60: "good",
    80: "very Good",
    100: "excellent",
}

# Initialize an empty list to store vehicles
vehicles = st.session_state.get("vehicles", [])

# Create a form for adding vehicles
add_form_space, vehicle_space = st.columns([2, 3])
with add_form_space:
    with st.form(key='vehicle_form'):
        st.header("Add a Vehicle")
        name = st.text_input("Name")
        vehicle_type = st.selectbox("Type", list(vehicle_types.keys()))
        kms_driven = st.number_input("Kilometers Driven", min_value=0)
        age = st.number_input("Age", min_value=0)
        condition = st.slider("Condition", min_value=0, max_value=100)

        submit_button = st.form_submit_button(label='Add Vehicle')

        # If the form is submitted, add the vehicle to the list
        if submit_button:
            vehicles.append({
                "id": genId(), # Add a unique id to each vehicle
                "name": name,
                "type": vehicle_type,
                "kms": kms_driven,
                "age": age,
                "condition": condition,
            })
            st.session_state.vehicles = vehicles

with vehicle_space:
    col_count = 3
    cols = st.columns(col_count)
    for i, vehicle in enumerate(vehicles):
        col = cols[i % col_count]
        with col:
            with st.container(border=True):
                st.header(vehicle_types[vehicle['type']])
                st.subheader(vehicle['name'])
                condition = "unknown"
                for key in vehicle_conditions:
                    if vehicle['condition'] >= key:
                        condition = vehicle_conditions[key]
                st.markdown(f"{vehicle['kms']}kms, {vehicle['age']} years old, {condition} condition")
                remove_button = st.button(label='Remove', key=f"remove_{vehicle['id']}")

                if remove_button:
                    st.toast(f"Removed {vehicle['name']} [{vehicle['id']}]", icon="🔥")
