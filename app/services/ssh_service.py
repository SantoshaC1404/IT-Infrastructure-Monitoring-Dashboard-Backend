from app.connections.ssh import SSHConnection


class SSHService(SSHConnection):
    """
    Backward compatibility.

    Will be removed after the project
    migrates completely to ConnectionFactory.
    """

    pass
