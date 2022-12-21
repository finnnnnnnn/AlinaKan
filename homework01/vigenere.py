from caesar import encrypt_caesar
from caesar import decrypt_caesar

def keyword_lenght(keyword, word):
    if len(word) > len(keyword):
        for i in range(len(word)):
            keyword += keyword[i]
    return keyword.upper()


def encrypt_vigenere(word, keyword):
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    keyword = keyword_lenght(keyword, word)
    for i in range(len(word)):
        ch = word[i]
        shift = ord(keyword[i]) - ord('A')
        ciphertext += encrypt_caesar(ch, shift)
    return ciphertext


def decrypt_vigenere(word, keyword):
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    keyword = keyword_lenght(keyword, word)
    for i in range(len(word)):
        ch = word[i]
        shift = ord(keyword[i]) - ord('A')
        plaintext += decrypt_caesar(ch, shift)
    return plaintext
