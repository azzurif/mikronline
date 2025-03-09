from paramiko import AutoAddPolicy, SSHClient


def connect(host, port, username, password):
    try:
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(host, port, username, password)
        return client
    except Exception as e:
        return e
