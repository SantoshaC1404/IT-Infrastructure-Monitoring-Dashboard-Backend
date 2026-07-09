import paramiko


class SSHService:

    @staticmethod
    def test_connection(
        hostname: str,
        port: int,
        username: str,
        password: str,
    ):

        ssh = paramiko.SSHClient()

        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:

            ssh.connect(
                hostname=hostname,
                port=port,
                username=username,
                password=password,
                timeout=5,
            )

            ssh.close()

            return True

        except Exception:
            return False
