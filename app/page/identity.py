import streamlit as st
from lib.command import command

identity = command("/system identity print", show_success=False).strip().replace("name: ", "")
host = st.session_state.get("host", "Unknown")
username = st.session_state.get("username", "Unknown")

st.session_state.connection = f"⛓️‍💥 **Router:** `{identity}` \n👤 **User:** `{username}` \n🌐 **Host:** `{host}`"
st.markdown(st.session_state.connection)

st.header(f"Router's Name", divider="rainbow")

name = st.text_input("New Router Name", value=identity, max_chars=30, help="Enter a new name for your router")

_, right = st.columns([6, 2])
if right.button("Update Name", type="primary", use_container_width=True):
    if name.strip():
        command(f"/system identity set name={name.strip()}")
        st.success(f"✅ Router name updated to **{name}**")
        st.rerun()
    else:
        st.warning("⚠️ Router name cannot be empty!")
