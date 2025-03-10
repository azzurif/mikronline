import streamlit as st

def command(command, show_success=True):
    client = st.session_state.get("client")

    if client is None:
        st.error("❌ Tidak ada koneksi ke MikroTik! Silakan login terlebih dahulu.")
        return "No Connection"

    try:
        _, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()

        if error:
            st.error("❌ Konfigurasi gagal: " + error)
            return None
        elif show_success:
            st.success("✅ Konfigurasi berhasil!")

        return output

    except Exception as e:
        st.error(f"⚠️ Gagal menjalankan perintah: {command}, Error: {e}")
        return None
