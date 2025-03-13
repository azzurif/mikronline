import streamlit as st
import re
from lib.command import command
from lib.interfaces import interfaces

if "show_form" not in st.session_state:
    st.session_state.show_form = False
if "config_success" not in st.session_state:
    st.session_state.config_success = False

dhcp_data_raw = command("/ip dhcp-client print terse")
dhcp_lines = dhcp_data_raw.strip().split("\n")

data = []
for idx, line in enumerate(dhcp_lines):
    id_match = re.search(r'^\s*(\d+)', line) 
    iface_match = re.search(r'interface=([\w-]+)', line)  
    bound_match = re.search(r'address=([\d./]+)', line)  

    if id_match and iface_match:
        dhcp_id = id_match.group(1) 
        interface = iface_match.group(1)
        bound_address = bound_match.group(1) if bound_match else "Not Bound"

        data.append({
            "No.": idx + 1,
            "ID": dhcp_id,
            "Interface": interface,
            "Bound": bound_address
        })

st.write(st.session_state.get("connection", "Not Connected"))

if st.session_state.config_success:
    st.success("Konfigurasi berhasil!")
    st.session_state.config_success = False 

left, right = st.columns([6, 1], vertical_alignment="bottom")
left.header("DHCP Client List")

if right.button("Add", type="primary", use_container_width=True):
    st.session_state.show_form = True

if st.session_state.show_form:
    interface = st.selectbox(
        "Interfaces",
        interfaces,
        index=None,
        placeholder="Select interface",
    )

    _, cancel, submit = st.columns([5, 1, 1])
    
    if submit.button("Confirm", type="primary", use_container_width=True):
        command(f"/ip dhcp-client add interface={interface}")
        st.session_state.config_success = True 
        st.session_state.show_form = False
        st.rerun()
    
    if cancel.button("Cancel", use_container_width=True):
        st.session_state.show_form = False
        st.rerun()

for row in data:
    col1, col2, col3, col4, col5 = st.columns([1, 2, 4, 4, 1])
    col1.write(row["No."])
    col2.write(row["ID"]) 
    col3.write(row["Interface"])
    col4.write(row["Bound"])

    delete_btn = col5.button("🗑️", key=f"delete_{row['No.']}")

    if delete_btn:
        command(f"/ip dhcp-client remove {row['ID']}") 
        st.session_state.config_success = True 
        st.rerun() 
