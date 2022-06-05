import base64

from models.user import User


# Foi utilizado base64 pois estava perdendo muito tempo com o cryptography
class Security:
    def __init__(self):
        pass

    @staticmethod
    def _encrypt(string):
        encoded_string = base64.b64encode(string.encode())
        return encoded_string.decode()

    @staticmethod
    def _decrypt(string):
        decoded_string = base64.b64decode(string)
        return decoded_string.decode()

    def encrypt(self, string):
        return self._encrypt(string)

    def decrypt(self, string):
        return self._decrypt(string)

    def encrypt_user(self, user: User):
        if not isinstance(user, User):
            return False

        if user.name:
            user.name = self._encrypt(user.name)
        if user.cpf:
            user.cpf = self._encrypt(user.cpf)
        if user.phone_number:
            user.phone_number = self._encrypt(user.phone_number)

        return user

    def decrypt_user(self, user: User):
        if not isinstance(user, User):
            return False

        if user.name:
            user.name = self._decrypt(user.name)
        if user.cpf:
            user.cpf = self._decrypt(user.cpf)
        if user.phone_number:
            user.phone_number = self._decrypt(user.phone_number)

        return user


if __name__ == '__main__':
    pass
