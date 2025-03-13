import streamlit as st
import re
from lib.command import command
from lib.interfaces import interfaces

if "show_form" not in st.session_state:
    st.session_state.show_form = False
if "edit_ip" not in st.session_state:
    st.session_state.edit_ip = None

def get_ip_data():
    ip_data_raw = command("/ip address print terse")
    ip_lines = ip_data_raw.strip().split("\n")
    
    parsed_data = []
    for idx, line in enumerate(ip_lines):
        id_match = re.search(r'^\s*(\d+)', line) 
        ip_match = re.search(r'address=([\d./]+)', line) 
        iface_match = re.search(r'interface=([\w-]+)', line) 
        
        if id_match and ip_match and iface_match:
            ip_id = id_match.group(1)
            ip_address = ip_match.group(1)
            interface = iface_match.group(1)
            parsed_data.append({
                "No.": idx + 1,
                "ID": ip_id,
                "Interface": interface,
                "IP Address": ip_address
            })
    return parsed_data

data = get_ip_data()

st.write(st.session_state.get("connection", "Not Connected"))

left, right = st.columns([6, 1], vertical_alignment="bottom")
left.header("IP Addresses List")

if right.button("Add", type="primary", use_container_width=True):
    st.session_state.show_form = True
    st.session_state.edit_ip = None 

if st.session_state.show_form:
    left, right = st.columns(2, vertical_alignment="bottom")


    ip_value = st.session_state.edit_ip["IP Address"] if st.session_state.edit_ip else ""
    interface_value = st.session_state.edit_ip["Interface"] if st.session_state.edit_ip else None
    ip_id = st.session_state.edit_ip["ID"] if st.session_state.edit_ip else None

    ip = left.text_input("IP Address", value=ip_value, placeholder="eg. 192.168.88.1")
    interface = right.selectbox(
        "Interfaces",
        interfaces,
        index=interfaces.index(interface_value) if interface_value in interfaces else None,
        placeholder="Select interface",
    )

    _, cancel, submit = st.columns([5, 1, 1])

    if submit.button("Confirm", type="primary", use_container_width=True):
        if st.session_state.edit_ip: 
            command(f"/ip address set {ip_id} address={ip} interface={interface}") 
        else:
            command(f"/ip address add address={ip} interface={interface}") 
        st.session_state.show_form = False
        st.session_state.edit_ip = None
        st.rerun() 

    if cancel.button("Cancel", use_container_width=True):
        st.session_state.show_form = False
        st.session_state.edit_ip = None
        st.rerun()

for row in data:
    col1, col2, col3, col4, col5, col6 = st.columns([1, 2, 4, 4, 1, 1])
    col1.write(row["No."])
    col2.write(row["ID"]) 
    col3.write(row["Interface"])
    col4.write(row["IP Address"])

    edit_btn = col5.button("✏️", key=f"edit_{row['No.']}")
    delete_btn = col6.button("🗑️", key=f"delete_{row['No.']}")

    if edit_btn:
        st.session_state.show_form = True
        st.session_state.edit_ip = row 
        st.rerun()

    if delete_btn:
        command(f"/ip address remove {row['ID']}") 
        st.rerun() 
