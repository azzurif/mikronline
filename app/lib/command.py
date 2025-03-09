import streamlit as st

client = st.session_state.client


def command(command, show_success=True):
    stdin, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode()
    error = stderr.read().decode()
    if error:
        st.error("Configuration Failed: " + error)
    elif show_success:
        st.success("Configuration Successful")
    return output
