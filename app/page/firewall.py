import streamlit as st
from page.identity import identity
from lib.command import command
from lib.interfaces import interfaces

data = [
    {"No.": 1, "Interface": "Ethernet0", "Value": "Up"},
    {"No.": 2, "Interface": "Ethernet1", "Value": "Down"},
    {"No.": 3, "Interface": "Ethernet2", "Value": "Up"},
]
st.write(identity)

left, right = st.columns([6, 1], vertical_alignment="bottom")
left.header("Firewall NAT Lists")
add = right.button("Add", type="primary", use_container_width=True)
if add:
    interface = st.selectbox(
        "Interfaces",
        interfaces,
        index=None,
        placeholder="Select interface",
    )
    flag = st.selectbox(
        "Interfaces",
        interfaces,
        index=None,
        placeholder="Select out interface",
    )

    _, cancel, submit = st.columns([5, 1, 1])
    confirm = submit.button("Confirm", type="primary", use_container_width=True)
    cancel.button("Cancel", use_container_width=True)

    # if confirm:
    #     command(
    #         f"/ip firewall nat add chain=srcnat {flag}={interface} action=masquerade"
    #     )

st.dataframe(data, hide_index=True)
