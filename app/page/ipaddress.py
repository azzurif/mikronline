import streamlit as st
import re
from lib.command import command
from lib.interfaces import interfaces

if "show_form" not in st.session_state:
    st.session_state.show_form = False

ip_data_raw = command("/ip address print terse")
ip_lines = ip_data_raw.strip().split("\n")

data = []
for idx, line in enumerate(ip_lines):
    ip_match = re.search(r'address=([\d./]+)', line)  
    iface_match = re.search(r'interface=([\w-]+)', line)  

    if ip_match and iface_match:
        ip_address = ip_match.group(1)
        interface = iface_match.group(1)
        data.append({"No.": idx + 1, "Interface": interface, "Ip Address": ip_address})

st.write(st.session_state.get("connection", "Not Connected"))

left, right = st.columns([6, 1], vertical_alignment="bottom")
left.header("IP Addresses List")

if right.button("Add", type="primary", use_container_width=True):
    st.session_state.show_form = True

if st.session_state.show_form:
    left, right = st.columns(2, vertical_alignment="bottom")
    ip = left.text_input("IP Address", placeholder="eg. 192.168.88.1")
    interface = right.selectbox(
        "Interfaces",
        interfaces,
        index=None,
        placeholder="Select interface",
    )

    _, cancel, submit = st.columns([5, 1, 1])
    
    if submit.button("Confirm", type="primary", use_container_width=True):
        command(f"/ip address add address={ip} interface={interface}")
        st.session_state.show_form = False
    
    if cancel.button("Cancel", use_container_width=True):
        st.session_state.show_form = False
        

st.dataframe(data, hide_index=True)