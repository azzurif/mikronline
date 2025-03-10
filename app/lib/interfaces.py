import streamlit as st
import re
from lib.command import command

interfaces_raw = command("/interface print terse")
interface_lines = interfaces_raw.strip().split("\n")

interfaces = []
for line in interface_lines:
    match = re.search(r"name=([\w-]+)", line) 
    if match:
        interfaces.append(match.group(1))

st.session_state.interfaces = interfaces if interfaces else ["No interfaces found"]
