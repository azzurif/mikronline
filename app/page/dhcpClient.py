import streamlit as st
import re
from lib.command import command
from lib.interfaces import interfaces


if "show_form" not in st.session_state:
    st.session_state.show_form = False

dhcp_data_raw = command("/ip dhcp-client print terse")
dhcp_lines = dhcp_data_raw.strip().split("\n")

data = []
for idx, line in enumerate(dhcp_lines):
    iface_match = re.search(r'interface=([\w-]+)', line)  
    bound_match = re.search(r'address=([\d./]+)', line)  

    if iface_match:
        interface = iface_match.group(1)
        bound_address = bound_match.group(1) if bound_match else "Not Bound"
        data.append({"No.": idx + 1, "Interface": interface, "Bound": bound_address})

st.write(st.session_state.get("connection", "Not Connected"))

left, right = st.columns([6, 1], vertical_alignment="bottom")
left.header("DHCP Client Lists")

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
        st.session_state.show_form = False
    
    if cancel.button("Cancel", use_container_width=True):
        st.session_state.show_form = False

st.dataframe(data, hide_index=True)