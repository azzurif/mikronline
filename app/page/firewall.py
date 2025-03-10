import streamlit as st
import re
from lib.command import command
from lib.interfaces import interfaces

if "show_form" not in st.session_state:
    st.session_state.show_form = False

nat_data_raw = command("/ip firewall nat print terse")

nat_lines = nat_data_raw.strip().split("\n")
data = []
for idx, line in enumerate(nat_lines):
    out_iface_match = re.search(r'out-interface=([\w\d-]+)', line) 

    if out_iface_match:
        out_interface = out_iface_match.group(1)
        data.append({"No.": idx + 1, "Out Interface": out_interface})

st.write(st.session_state.get("connection", "Not Connected"))

left, right = st.columns([6, 1], vertical_alignment="bottom")
left.header("Firewall NAT Lists (Out Interface Only)")

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
        command(f"/ip firewall nat add chain=srcnat out-interface={interface} action=masquerade")
        st.session_state.show_form = False

    if cancel.button("Cancel", use_container_width=True):
        st.session_state.show_form = False

st.dataframe(data, hide_index=True)