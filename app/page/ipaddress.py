import streamlit as st
from lib.command import command
from lib.interfaces import interfaces

data = [
    {"No.": 1, "Interface": "Ethernet0", "Ip Address": "192.168.88.1/24"},
    {"No.": 2, "Interface": "Ethernet1", "Ip Address": "192.168.88.2/24"},
    {"No.": 3, "Interface": "Ethernet2", "Ip Address": "192.168.88.3/24"},
]


st.write(st.session_state.connection)

left, right = st.columns([6, 1], vertical_alignment="bottom")
left.header("Ip Addresses Lists")
add = right.button("Add", type="primary", use_container_width=True)

if add:
    st.session_state.show_form = True

if st.session_state.show_form:
    left, right = st.columns(2, vertical_alignment="bottom")
    ip = left.text_input("Ip Address", placeholder="eg. 192.168.88.1")
    interface = right.selectbox(
        "Interfaces",
        interfaces,
        index=None,
        placeholder="Select interface",
    )

    _, cancel, submit = st.columns([5, 1, 1])
    confirm = submit.button("Confirm", type="primary", use_container_width=True)
    cancel = cancel.button("Cancel", use_container_width=True)
    if cancel:
        st.session_state.show_form = False

    # if confirm:
    #     command(f"/ip address add address={ip} interface={interface}")
    # st.session_state.show_form = False

st.dataframe(data, hide_index=True)
