import streamlit as st
from lib.command import command
from lib.interfaces import interfaces

data = [
    {"No.": 1, "Interface": "Ethernet0", "SSID": "Up", "Password": "password"},
    {"No.": 2, "Interface": "Ethernet1", "SSID": "Down", "Password": "password"},
    {"No.": 3, "Interface": "Ethernet2", "SSID": "Up", "Password": "password"},
]
st.write(st.session_state.connection)

left, right = st.columns([6, 1], vertical_alignment="bottom")
left.header("Wireless Lists")
add = right.button("Add", type="primary", use_container_width=True)
if add:
    st.session_state.show_form = True

if st.session_state.show_form:
    left, center, right = st.columns(3, vertical_alignment="bottom")
    ssid = left.text_input("SSID", placeholder="Mikrotik")
    password = center.text_input("Password", type="password", placeholder="Password")
    interface = right.selectbox(
        "Interfaces",
        interfaces,
        index=None,
        placeholder="Select interface",
    )

    _, cancel, submit = st.columns([5, 1, 1])
    confirm = submit.button("Confirm", type="primary", use_container_width=True)
    if cancel.button("Cancel", use_container_width=True):
        st.session_state.show_form = False

    # if confirm:
    # command(f"/interface wireless set [find default-name={interface}] ssid={ssid} mode=ap-bridge band=5ghz-b/g/n frequency=auto disabled=no")
    # command(f"/interface wireless security-profiles set [find default=yes] mode=dynamic-keys authentication-types=wpa2-psk wpa2-pre-shared-key={password}")
    #     command(
    #         f"/interface wireless set [ find default-name={interface} ] ssid={ssid} mode=ap-bridge band=2ghz-b/g/n frequency=auto wireless-protocol=802.11 security-profile=default"
    #     )
    #  st.session_state.show_form = False

st.dataframe(data, hide_index=True)
