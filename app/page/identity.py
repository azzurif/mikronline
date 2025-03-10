import streamlit as st

from lib.command import command

identity, host, username = (
    command("/system identity print", show_success=False),
    st.session_state["host"],
    st.session_state["username"],
)
identity = command("/system identity print", show_success=False)

st.session_state.connection = f":material/router: {identity} _{host}@{username}_"
st.write(st.session_state.connection)
st.header("Router's Name", divider="red")
name = st.text_input("Name", value=identity)

_, right = st.columns([6, 1])
confirm = right.button("Confirm", type="primary")
if confirm:
    st.success("yes changed.")
    command(f"/system identity set name={name}")
