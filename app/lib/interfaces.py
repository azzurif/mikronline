import streamlit as st
import re
from lib.command import command

# Gunakan perintah lebih lengkap untuk mendapatkan semua interface
interfaces_raw = command("/interface print without-paging terse")
interface_lines = interfaces_raw.strip().split("\n")

interfaces = []
for line in interface_lines:
    match = re.search(r"name=([^\s]+)", line)  # Tangkap nama dengan karakter non-spasi
    if match:
        interfaces.append(match.group(1))

# Pastikan ada daftar interface, jika kosong beri pesan default
st.session_state.interfaces = interfaces if interfaces else ["No interfaces found"]
