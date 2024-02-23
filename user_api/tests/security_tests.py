from models.user import User

from utils.security import Security


def test_basic_encrypt():
    encrypted_string = Security().encrypt('This is a simple encrypt test...')
    assert encrypted_string == 'VGhpcyBpcyBhIHNpbXBsZSBlbmNyeXB0IHRlc3QuLi4='


def test_basic_decrypt():
    decrypted_string = Security().decrypt('VGhpcyBpcyBhIHNpbXBsZSBkZWNyeXB0IHRlc3QuLi4=')
    assert decrypted_string == 'This is a simple decrypt test...'


def test_basic_encrypt_user():
    user = User()
    user.name = 'Bruno Baehr'
    user.cpf = '123.456.789-00'
    user.phone_number = '(47) 996060607'
    Security().encrypt_user(user)

    assert user.name == 'QnJ1bm8gQmFlaHI='
    assert user.cpf == 'MTIzLjQ1Ni43ODktMDA='
    assert user.phone_number == 'KDQ3KSA5OTYwNjA2MDc='


def test_basic_decrypt_user():
    user = User(name='', cpf='', phone_number='')
    user.name = 'QnJ1bm8gQmFlaHI='
    user.cpf = 'MTIzLjQ1Ni43ODktMDA='
    user.phone_number = 'KDQ3KSA5OTYwNjA2MDc='

    decrypted_user = Security().decrypt_user(user)

    assert decrypted_user.name == 'Bruno Baehr'
    assert decrypted_user.cpf == '123.456.789-00'
    assert decrypted_user.phone_number == '(47) 996060607'
