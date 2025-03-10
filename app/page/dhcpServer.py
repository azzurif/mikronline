import streamlit as st
import re
from lib.command import command
from lib.interfaces import interfaces

if "show_form" not in st.session_state:
    st.session_state.show_form = False

dhcp_data_raw = command("/ip dhcp-server print terse")
dhcp_lines = dhcp_data_raw.strip().split("\n")

data = []
for idx, line in enumerate(dhcp_lines):
    iface_match = re.search(r'interface=([\w-]+)', line) 
    status_match = re.search(r'disabled=(yes|no)', line) 

    if iface_match:
        interface = iface_match.group(1)
        status = "Up" if status_match and status_match.group(1) == "no" else "Down"
        data.append({"No.": idx + 1, "Interface": interface, "Value": status})

st.write(st.session_state.get("connection", "Not Connected"))

left, right = st.columns([6, 1], vertical_alignment="bottom")
left.header("DHCP Server Lists")

if right.button("Add", type="primary", use_container_width=True):
    st.session_state.show_form = True

if st.session_state.show_form:
    left, right = st.columns(2, vertical_alignment="bottom")
    bottomLeft, bottomRight = st.columns(2, vertical_alignment="bottom")
    
    interface = left.selectbox(
        "Interfaces",
        interfaces,
        index=None,
        placeholder="Select interface",
    )
    pool = right.text_input(
        "Address pool", placeholder="eg. 192.168.88.1-192.168.88.254"
    )
    address = bottomLeft.text_input("Network", placeholder="eg. 192.168.88.1/24")
    gateway = bottomRight.text_input("Gateway", placeholder="eg. 192.168.88.1")

    _, cancel, submit = st.columns([5, 1, 1])
    
    if submit.button("Confirm", type="primary", use_container_width=True):
        command(f"/ip pool add name=dhcp_pool_{interface} ranges={pool}")
        command(f"/ip dhcp-server network add address={address} gateway={gateway} dns-server=8.8.8.8")
        command(f"/ip dhcp-server add interface={interface} address-pool=dhcp_pool_{interface}")
        st.session_state.show_form = False
    
    if cancel.button("Cancel", use_container_width=True):
        st.session_state.show_form = False

st.dataframe(data, hide_index=True)