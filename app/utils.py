from flask import abort, flash, session


def login_checker():
    if session.get("login") is not True:
        flash(
            "Вы должны войти в систему для просмотра этой страницы!", "danger"
        )
        abort(403)


def encrypt_message(message: str, cipher_suite) -> str:
    """Шифрование текста сообщения."""
    encrypted_message = cipher_suite.encrypt(message.encode())
    return encrypted_message.decode()


def decrypt_message(encrypted_message: str, cipher_suite) -> str:
    """Расшифровка текста сообщения."""
    decrypted_message = cipher_suite.decrypt(encrypted_message.encode())
    return decrypted_message.decode()
