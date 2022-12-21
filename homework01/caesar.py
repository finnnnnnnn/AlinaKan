import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for i in plaintext:
        if i.isalpha():
            ciphertext += shif(i, shift)
        else:
            ciphertext += i
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = encrypt_caesar(ciphertext, -shift)
    return plaintext


def shif(a : str, shift: int) -> str:
    if a.isupper():
        lef = ord('A')
        rig = ord('Z')
    else:
        lef = ord('a')
        rig = ord('z')

    if lef <= ord(a) + shift <= rig:
        return chr(ord(a) + shift)
    elif shift > 0:
        return chr(lef + (ord(a) + shift - rig) - 1)
    else:
        return chr(rig - (lef - (ord(a) + shift)) + 1)
