import streamlit as st

client = st.session_state.client

interfaces = ["Ethernet0", "Ethernet1", "Ethernet2"]
# stdin, stdout, stderr = client.exec_command("/interface print terse")
# interfaces = stdout.read().decode().strip().split("\n")
