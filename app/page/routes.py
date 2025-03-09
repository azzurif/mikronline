import streamlit as st
from lib.command import command
from lib.interfaces import interfaces

data = [
    {"No.": 1, "Interface": "Ethernet0", "Gateway": "Up"},
    {"No.": 2, "Interface": "Ethernet1", "Gateway": "Down"},
    {"No.": 3, "Interface": "Ethernet2", "Gateway": "Up"},
]
st.write(st.session_state.connection)

left, right = st.columns([6, 1], vertical_alignment="bottom")
left.header("Routes Lists")
add = right.button("Add", type="primary", use_container_width=True)
if add:
    st.session_state.show_form = True

if st.session_state.show_form:
    left, right = st.columns(2, vertical_alignment="bottom")
    interface = left.selectbox(
        "Interfaces",
        interfaces,
        index=None,
        placeholder="Select interface",
    )
    gateway = right.text_input("Gateway", placeholder="eg. 192.168.88.1")

    _, cancel, submit = st.columns([5, 1, 1])
    confirm = submit.button("Confirm", type="primary", use_container_width=True)
    if cancel.button("Cancel", use_container_width=True):
        st.session_state.show_form = False

    # if confirm:
    #     command(f"/ip route add gateway={gateway}")
    #  st.session_state.show_form = False

st.dataframe(data, hide_index=True)
