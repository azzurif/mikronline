import streamlit as st
import re
from lib.command import command
from lib.interfaces import interfaces

if "show_form" not in st.session_state:
    st.session_state.show_form = False

route_data_raw = command("/ip route print terse")

route_lines = route_data_raw.strip().split("\n")
data = []
for idx, line in enumerate(route_lines):
    gateway_match = re.search(r'gateway=([\d\.]+)', line) 

    if gateway_match:
        gateway = gateway_match.group(1)
        data.append({"No.": idx + 1, "Gateway": gateway})

st.write(st.session_state.get("connection", "Not Connected"))

left, right = st.columns([6, 1], vertical_alignment="bottom")
left.header("Routes Lists (Gateway Only)")

if right.button("Add", type="primary", use_container_width=True):
    st.session_state.show_form = True

if st.session_state.show_form:
    gateway = st.text_input("Gateway", placeholder="eg. 192.168.88.1")

    _, cancel, submit = st.columns([5, 1, 1])
    
    if submit.button("Confirm", type="primary", use_container_width=True):
        command(f"/ip route add gateway={gateway}")
        st.session_state.show_form = False
    
    if cancel.button("Cancel", use_container_width=True):
        st.session_state.show_form = False

st.dataframe(data, hide_index=True)
