from unittest.mock import MagicMock
from app.utils import encrypt_message, decrypt_message


def test_encrypt_message():
    # Создаем mock для cipher_suite
    mock_cipher_suite = MagicMock()
    mock_cipher_suite.encrypt.return_value = b"encrypted_data"

    # Проверяем, что функция возвращает правильный результат
    encrypted_message = encrypt_message("Hello", mock_cipher_suite)
    assert encrypted_message == "encrypted_data"  # Сравниваем строку напрямую

    # Убедимся, что метод encrypt был вызван с правильным аргументом
    mock_cipher_suite.encrypt.assert_called_with(b"Hello")


def test_decrypt_message():
    # Создаем mock для cipher_suite
    mock_cipher_suite = MagicMock()
    mock_cipher_suite.decrypt.return_value = b"decrypted_data"

    # Проверяем, что функция возвращает правильный результат
    decrypted_message = decrypt_message("encrypted_data", mock_cipher_suite)
    assert decrypted_message == "decrypted_data"  # Сравниваем строку напрямую

    # Убедимся, что метод decrypt был вызван с правильным аргументом
    mock_cipher_suite.decrypt.assert_called_with(b"encrypted_data")
