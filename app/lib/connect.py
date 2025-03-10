from paramiko import AutoAddPolicy, SSHClient, AuthenticationException, SSHException

def connect(host, port, username, password):
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())

    try:
        client.connect(hostname=host, port=port, username=username, password=password)
        return client

    except AuthenticationException:
        print("❌ Gagal login! Periksa username/password.")
        return None
    except SSHException as e:
        print(f"⚠️ SSH error: {e}")
        return None
    except Exception as e:
        print(f"🚨 Error lainnya: {e}")
        return None
