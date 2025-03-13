import streamlit as st
import re
from lib.command import command

# Inisialisasi session state
if "show_form" not in st.session_state:
    st.session_state.show_form = False
if "edit_form" not in st.session_state:
    st.session_state.edit_form = None
if "config_success" not in st.session_state:
    st.session_state.config_success = False

# Ambil data Wireless dari MikroTik
wireless_raw = command("/interface wireless print terse")
wireless_lines = wireless_raw.strip().split("\n")

# Parsing Data Wireless
data = []
for idx, line in enumerate(wireless_lines):
    fields = {}
    for part in line.split():
        key_val = part.split("=", 1)
        if len(key_val) == 2:
            fields[key_val[0]] = key_val[1]

    if "name" in fields and "ssid" in fields:
        status = "Enabled" if fields.get("disabled", "no") == "no" else "Disabled"
        data.append({
            "No.": idx + 1,
            "Interface": fields["name"],
            "SSID": fields["ssid"],
            "Status": status
        })

# Menampilkan status koneksi
st.write(st.session_state.get("connection", "Not Connected"))

if st.session_state.config_success:
    st.success("Konfigurasi berhasil!")
    st.session_state.config_success = False

# Header & Tombol Add
left, right = st.columns([6, 1], vertical_alignment="bottom")
left.header("Wireless Networks")

if right.button("Add", type="primary", use_container_width=True):
    st.session_state.show_form = True

# Form Tambah Wireless
if st.session_state.show_form:
    left, center, right = st.columns(3, vertical_alignment="bottom")
    ssid = center.text_input("SSID", placeholder="Enter WiFi Name")
    password = right.text_input("Password", type="password", placeholder="Enter Password")
    interface = left.text_input("Interface Name", placeholder="eg. wlan2")

    _, cancel, submit = st.columns([5, 1, 1])

    if submit.button("Confirm", type="primary", use_container_width=True):
        command(f"/interface wireless add name={interface} master-interface=wlan1 mode=ap-bridge disabled=no")
        command(f"/interface wireless security-profiles add name=profile_{interface} mode=dynamic-keys authentication-types=wpa2-psk wpa2-pre-shared-key={password}")
        command(f"/interface wireless set {interface} security-profile=profile_{interface} ssid={ssid}")
        st.session_state.config_success = True
        st.session_state.show_form = False
        st.rerun()

    if cancel.button("Cancel", use_container_width=True):
        st.session_state.show_form = False
        st.rerun()

# Menampilkan Data Wireless
for idx, row in enumerate(data):
    col1, col2, col3, col4, col5, col6 = st.columns([1, 3, 4, 2, 1, 1])
    col1.write(row["No."])
    col2.write(row["Interface"])
    col3.write(row["SSID"])
    col4.write(row["Status"])

    edit_key = f"edit_{idx}"
    delete_key = f"delete_{idx}"

    if col5.button("✏️", key=edit_key):
        st.session_state.edit_form = row["Interface"]

    if col6.button("🗑️", key=delete_key):
        command(f"/interface wireless remove [find name={row['Interface']}]") 
        command(f"/interface wireless security-profiles remove [find name=profile_{row['Interface']}]") 
        st.session_state.config_success = True
        st.rerun()

# Form Edit Wireless
if st.session_state.edit_form:
    left, center = st.columns([3, 3])
    ssid = left.text_input("New SSID", placeholder="Enter New WiFi Name")
    password = center.text_input("New Password", type="password", placeholder="Enter New Password")

    _, cancel, submit = st.columns([5, 1, 1])

    if submit.button("Save Changes", type="primary", use_container_width=True):
        interface = st.session_state.edit_form
        command(f"/interface wireless set [find name={interface}] ssid={ssid}")
        command(f"/interface wireless security-profiles set [find name=profile_{interface}] wpa2-pre-shared-key={password}")
        st.session_state.config_success = True
        st.session_state.edit_form = None
        st.rerun()

    if cancel.button("Cancel", use_container_width=True):
        st.session_state.edit_form = None
        st.rerun()
