from app.connectors.ssh.ssh_connector import SSHConnector
from app.connectors.winrm.winrm_connector import WinRMConnector
from app.core.exceptions import (
    AuthenticationException,
    ConnectionTimeoutException,
    HostUnreachableException,
    ConnectionException,
)
from app.schemas.test_connection import (
    TestConnectionRequest,
    TestConnectionResponse,
)
from app.utils.enums import DeviceType


class TestConnectionService:

    def test(
        self,
        request: TestConnectionRequest,
    ) -> TestConnectionResponse:

        try:

            if request.device_type == DeviceType.LINUX:

                port = request.port or 22

                connector = SSHConnector(
                    hostname=request.ip_address,
                    port=port,
                    username=request.username,
                    password=request.password,
                )

            else:

                port = request.port or 5985

                connector = WinRMConnector(
                    hostname=request.ip_address,
                    port=port,
                    username=request.username,
                    password=request.password,
                )

            connector.connect()
            connector.disconnect()

            return TestConnectionResponse(
                success=True,
                message="Connection successful.",
            )

        except AuthenticationException:

            return TestConnectionResponse(
                success=False,
                message="Authentication failed.",
            )

        except HostUnreachableException:

            return TestConnectionResponse(
                success=False,
                message="Host unreachable.",
            )

        except ConnectionTimeoutException:

            return TestConnectionResponse(
                success=False,
                message="Connection timed out.",
            )

        except ConnectionException as ex:

            return TestConnectionResponse(
                success=False,
                message=str(ex),
            )
