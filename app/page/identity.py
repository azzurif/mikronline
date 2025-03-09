import streamlit as st

from lib.command import command

if "identity" not in st.session_state:
    st.session_state.identity = None

identity = st.session_state.identity
# identity = command("/system identity print", show_success=False)

st.write(identity)
st.header("Router's Name", divider="red")
name = st.text_input("Name", value=identity)

_, right = st.columns([6, 1])
confirm = right.button("Confirm", type="primary")
if confirm:
    st.success("yes changed.")
    # command(f"/system identity set name={name}")
