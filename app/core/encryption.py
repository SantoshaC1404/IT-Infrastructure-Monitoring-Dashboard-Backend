from cryptography.fernet import Fernet

from app.core.config import settings


class EncryptionService:
    def __init__(self):
        """Initialize the EncryptionService with a Fernet key."""
        self.key = Fernet(settings.ENCRYPTION_KEY.encode())

    def encrypt(self, value: str) -> str:
        """Encrypt the given value using Fernet encryption.
        Args:
            value (str): The value to be encrypted.
        Returns:
            str: The encrypted value as a string.
        """
        return self.key.encrypt(value.encode()).decode()

    def decrypt(self, value: str) -> str:
        """Decrypt the given value using Fernet decryption.
        Args:
            value (str): The value to be decrypted.
        Returns:
            str: The decrypted value as a string.
        """
        return self.key.decrypt(value.encode()).decode()


encryption_service = EncryptionService()
