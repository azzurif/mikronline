import streamlit as st
import re
from lib.command import command
from lib.interfaces import interfaces

if "show_form" not in st.session_state:
    st.session_state.show_form = False
if "config_success" not in st.session_state:
    st.session_state.config_success = False

nat_data_raw = command("/ip firewall nat print terse")
nat_lines = nat_data_raw.strip().split("\n")

data = []
for idx, line in enumerate(nat_lines):
    id_match = re.search(r'^\s*(\d+)', line) 
    out_iface_match = re.search(r'out-interface=([\w\d-]+)', line)

    if id_match and out_iface_match:
        nat_id = id_match.group(1) 
        out_interface = out_iface_match.group(1)

        data.append({
            "No.": idx + 1,
            "ID": nat_id,
            "Out Interface": out_interface
        })

st.write(st.session_state.get("connection", "Not Connected"))

if st.session_state.config_success:
    st.success("Konfigurasi berhasil!")
    st.session_state.config_success = False 

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
        st.session_state.config_success = True 
        st.session_state.show_form = False
        st.rerun()

    if cancel.button("Cancel", use_container_width=True):
        st.session_state.show_form = False
        st.rerun()

for row in data:
    col1, col2, col3, col4 = st.columns([1, 2, 5, 1])
    col1.write(row["No."])
    col2.write(row["ID"]) 
    col3.write(row["Out Interface"])

    delete_btn = col4.button("🗑️", key=f"delete_{row['No.']}")

    if delete_btn:
        command(f"/ip firewall nat remove {row['ID']}") 
        st.session_state.config_success = True 
        st.rerun() 
