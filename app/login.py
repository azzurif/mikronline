import streamlit as st
from lib.connect import connect


if "client" not in st.session_state:
    st.session_state.client = None


def login():
    st.header("Mikroline", divider="red")

    host = st.text_input("Host", placeholder="192.168.88.1")
    username = st.text_input("Username", placeholder="admin")
    password = st.text_input("Password", type="password", placeholder="Password")
    port = st.number_input("Port", value=None, placeholder="22", min_value=0, step=1)

    _, right = st.columns([4, 1])
    submit = right.button("Connect", type="primary", use_container_width=True)

    if submit:
        st.session_state.client = "ada"
        # st.session_state.client = connect(host, port, username, password)
        st.rerun()


def logout():
    st.session_state.client = None
    st.rerun()


loginPage = st.Page(login, title="Log In", icon=":material/login:")
logoutPage = st.Page(logout, title="Log out", icon=":material/logout:")
namePage = st.Page(
    "page/identity.py",
    title="Router Identity",
    icon=":material/bug_report:",
    default=True,
)
ipsPage = st.Page(
    "page/ipaddress.py", title="Ip Addresses", icon=":material/dashboard:"
)
dhcpClientPage = st.Page(
    "page/dhcpClient.py", title="DHCP Client", icon=":material/notification_important:"
)
dhcpServerPage = st.Page(
    "page/dhcpServer.py", title="DHCP Server", icon=":material/notification_important:"
)
routesPage = st.Page("page/routes.py", title="Routes", icon=":material/bug_report:")
wirelessPage = st.Page(
    "page/wireless.py", title="Wireless", icon=":material/bug_report:"
)
firewallPage = st.Page(
    "page/firewall.py", title="Firewall NAT", icon=":material/bug_report:"
)


if st.session_state.client:
    pg = st.navigation(
        {
            "Configs": [
                namePage,
                ipsPage,
                dhcpClientPage,
                dhcpServerPage,
                routesPage,
                wirelessPage,
                firewallPage,
            ],
            "Account": [logoutPage],
        }
    )
else:
    pg = st.navigation([loginPage])

pg.run()
