import streamlit as st
import re
from lib.command import command

if "show_form" not in st.session_state:
    st.session_state.show_form = False
if "edit_route" not in st.session_state:
    st.session_state.edit_route = None
if "config_success" not in st.session_state:
    st.session_state.config_success = False

route_data_raw = command("/ip route print terse")
route_lines = route_data_raw.strip().split("\n")

data = []
for idx, line in enumerate(route_lines):
    id_match = re.search(r'^\s*(\d+)', line) 
    gateway_match = re.search(r'gateway=([\d\.]+)', line)

    if id_match and gateway_match:
        route_id = id_match.group(1) 
        gateway = gateway_match.group(1)

        data.append({
            "No.": idx + 1,
            "ID": route_id,
            "Gateway": gateway
        })

st.write(st.session_state.get("connection", "Not Connected"))

if st.session_state.config_success:
    st.success("Konfigurasi berhasil!")
    st.session_state.config_success = False 

left, right = st.columns([6, 1], vertical_alignment="bottom")
left.header("Routes Lists (Gateway Only)")

if right.button("Add", type="primary", use_container_width=True):
    st.session_state.show_form = True
    st.session_state.edit_route = None 

if st.session_state.show_form:

    gateway_value = st.session_state.edit_route["Gateway"] if st.session_state.edit_route else ""
    route_id = st.session_state.edit_route["ID"] if st.session_state.edit_route else None

    gateway = st.text_input("Gateway", value=gateway_value, placeholder="eg. 192.168.88.1")

    _, cancel, submit = st.columns([5, 1, 1])
    
    if submit.button("Confirm", type="primary", use_container_width=True):
        if st.session_state.edit_route: 
            command(f"/ip route set {route_id} gateway={gateway}") 
        else:
            command(f"/ip route add gateway={gateway}") 

        st.session_state.config_success = True 
        st.session_state.show_form = False
        st.session_state.edit_route = None
        st.rerun()

    if cancel.button("Cancel", use_container_width=True):
        st.session_state.show_form = False
        st.session_state.edit_route = None
        st.rerun()

for row in data:
    col1, col2, col3, col4, col5 = st.columns([1, 2, 4, 1, 1])
    col1.write(row["No."])
    col2.write(row["ID"]) 
    col3.write(row["Gateway"])

    edit_btn = col4.button("✏️", key=f"edit_{row['No.']}")
    delete_btn = col5.button("🗑️", key=f"delete_{row['No.']}")

    if edit_btn:
        st.session_state.show_form = True
        st.session_state.edit_route = row 
        st.rerun()

    if delete_btn:
        command(f"/ip route remove {row['ID']}") 
        st.session_state.config_success = True 
        st.rerun() 
