from cryptography.fernet import Fernet
from PyQt5.QtCore import QSettings
import base64


class SecureDataManager:
    def __init__(self):
        self.settings = QSettings("Dota2CounterApp", "SecureData")
        self.key = self._get_or_create_key()
        self.cipher = Fernet(self.key)
        
    def _get_or_create_key(self):
        # Try to get the encryption key from settings
        key_base64 = self.settings.value("encryption_key")
        
        if key_base64:
            # Key exists, decode it
            return base64.urlsafe_b64decode(key_base64.encode())
        else:
            # Generate a new key and store it
            key = Fernet.generate_key()
            self.settings.setValue("encryption_key", base64.urlsafe_b64encode(key).decode())
            return key
    
    def store_data(self, key, data):
        """Securely store data"""
        if data:
            encrypted_data = self.cipher.encrypt(data.encode())
            self.settings.setValue(key, base64.urlsafe_b64encode(encrypted_data).decode())
        else:
            self.settings.remove(key)
    
    def retrieve_data(self, key):
        """Retrieve securely stored data"""
        encrypted_data_base64 = self.settings.value(key)
        if encrypted_data_base64:
            try:
                encrypted_data = base64.urlsafe_b64decode(encrypted_data_base64.encode())
                return self.cipher.decrypt(encrypted_data).decode()
            except:
                # If decryption fails, return empty string
                return "", print("Error! Decryption failed")
        return ""