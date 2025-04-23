import streamlit as st
import re
from lib.command import command
from lib.interfaces import interfaces

if "show_form" not in st.session_state:
    st.session_state.show_form = False
if "config_success" not in st.session_state:
    st.session_state.config_success = False
if "gateway" not in st.session_state:
    st.session_state.gateway = ""

dhcp_data_raw = command("/ip dhcp-server print terse")
dhcp_lines = dhcp_data_raw.strip().split("\n")

data = []
for idx, line in enumerate(dhcp_lines):
    id_match = re.search(r"^\s*(\d+)", line)
    iface_match = re.search(r"interface=([\w-]+)", line)
    status_match = re.search(r"disabled=(yes|no)", line)

    if id_match and iface_match:
        dhcp_id = id_match.group(1)
        interface = iface_match.group(1)
        status = "Up" if status_match and status_match.group(1) == "no" else "Down"

        data.append(
            {"No.": idx + 1, "ID": dhcp_id, "Interface": interface, "Status": status}
        )

st.write(st.session_state.get("connection", "Not Connected"))

if st.session_state.config_success:
    st.success("Konfigurasi berhasil!")
    st.session_state.config_success = False

left, right = st.columns([6, 1], vertical_alignment="bottom")
left.header("DHCP Server List")

if right.button("Add", type="primary", use_container_width=True):
    st.session_state.show_form = True

if st.session_state.show_form:
    left, right = st.columns(2, vertical_alignment="bottom")
    bottomLeft, bottomRight = st.columns(2, vertical_alignment="bottom")

    interface = left.selectbox(
        "Interfaces",
        interfaces,
        index=None,
        placeholder="Select interface",
    )
    address = right.text_input("Network", placeholder="eg. 192.168.88.0/24")
    gateway = bottomLeft.text_input("Gateway", placeholder="eg. 192.168.88.1")
    num_ips = bottomRight.number_input(
        "Pool",
        min_value=1,
        max_value=254,
        value=100,
        placeholder="eg. 100",
        help="Number of IP addresses to allocate starting from .1",
    )
    network_prefix = address.split("/")[0].rsplit(".", 1)[0]
    pool_range = f"{network_prefix}.2-{network_prefix}.{num_ips}"
    _, cancel, submit = st.columns([5, 1, 1])

    if submit.button("Confirm", type="primary", use_container_width=True):

        command(f"/ip pool add name=dhcp_pool_{interface} ranges={pool_range}")
        command(
            f"/ip dhcp-server network add address={address} gateway={gateway} dns-server=8.8.8.8"
        )
        command(
            f"/ip dhcp-server add interface={interface} address-pool=dhcp_pool_{interface} disabled=no"
        )
        st.session_state.config_success = True
        st.session_state.show_form = False
        st.session_state.gateway = gateway

        st.rerun()

    if cancel.button("Cancel", use_container_width=True):
        st.session_state.show_form = False
        st.rerun()

for row in data:
    col1, col2, col3, col4, col5 = st.columns([1, 2, 4, 4, 1])
    col1.write(row["No."])
    col2.write(row["ID"])
    col3.write(row["Interface"])
    col4.write(row["Status"])

    delete_btn = col5.button("🗑️", key=f"delete_{row['No.']}")

    if delete_btn:
        print(st.session_state.gateway)
        command(f"/ip dhcp-server remove {row['ID']}")
        command(f"/ip pool remove [find name=dhcp_pool_{row['Interface']}]")
        command(
            f"/ip dhcp-server network remove [ find gateway={st.session_state.gateway} ]"
        )

        st.session_state.config_success = True
        st.rerun()
