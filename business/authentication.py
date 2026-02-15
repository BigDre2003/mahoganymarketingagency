import hashlib
import os
import hmac
from data.database import Database
import random


class AuthenticationService:
    def __init__(self):
        pass
        self.db = Database()

    def hash_password(self, password):
        salt = os.urandom(16)
        password_bytes = password.encode('utf-8')
        hash_password = hashlib.sha256(salt +  password_bytes).digest()
        return salt.hex(), hash_password.hex()


    def new_user(self, lName: str, password: str) -> tuple[bool, str]:
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        salt_password, hash_password = self.hash_password(password)


        for _ in range(5):
            letter = random.choice(letters)
            numbers = "".join(str(random.randint(0, 9)) for _ in range(4))
            username = letter + lName + numbers
            success = self.db.create_user(username, hash_password, salt_password, 'employee')
            if success:
                return True, username
        return False, "Error! Please try again."

    def login(self, username: str, password: str, role: str) -> tuple[bool, str]:
        success = self.db.verify_user(username)
        if success:
            if role == 'a':
                stored_salt, stored_hash, user_role = success
                if user_role == "admin":
                    password_bytes = password.encode('utf-8')
                    enter_hash = hashlib.sha256(bytes.fromhex(stored_salt) + password_bytes).hexdigest()

                    if hmac.compare_digest(enter_hash, stored_hash):
                        return True, "Login Successful"
                    else:
                        return False, "Incorrect Password"
                else:
                    return False, "Don't have correct authorization!"
            else:
                stored_salt, stored_hash, user_role = success
                password_bytes = password.encode('utf-8')
                enter_hash = hashlib.sha256(bytes.fromhex(stored_salt) + password_bytes).hexdigest()

                if hmac.compare_digest(enter_hash, stored_hash):
                    return True, "Login Successful"
                else:
                    return False, "Incorrect Password"
        else:
            return False, "Invalid Credentials"