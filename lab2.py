# Алфавит: русский алфавит из 33 букв (верхний и нижний регистр)
upper_alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
lower_alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
alphabet_size = len(upper_alphabet)


def vigenere_encrypt(text, key):
    result = ''
    key_index = 0
    for char in text:
        if char in upper_alphabet:
            key_char = key[key_index % len(key)]
            if key_char in upper_alphabet:
                shift = upper_alphabet.index(key_char)
                index = (upper_alphabet.index(char) + shift) % alphabet_size
                result += upper_alphabet[index]
                key_index += 1
            else:
                result += char
        elif char in lower_alphabet:
            key_char = key[key_index % len(key)]
            if key_char in upper_alphabet:
                shift = upper_alphabet.index(key_char)
                index = (lower_alphabet.index(char) + shift) % alphabet_size
                result += lower_alphabet[index]
                key_index += 1
            else:
                result += char
        else:
            result += char
    return result


def vigenere_decrypt(ciphertext, key):
    result = ''
    key_index = 0
    for char in ciphertext:
        if char in upper_alphabet:
            # Цикличное движение по ключу
            key_char = key[key_index % len(key)]
            if key_char in upper_alphabet:
                shift = upper_alphabet.index(key_char)
                index = (upper_alphabet.index(char) - shift) % alphabet_size
                result += upper_alphabet[index]
                key_index += 1
            else:
                result += char
        elif char in lower_alphabet:
            key_char = key[key_index % len(key)]
            if key_char in upper_alphabet:
                shift = upper_alphabet.index(key_char)
                index = (lower_alphabet.index(char) - shift) % alphabet_size
                result += lower_alphabet[index]
                key_index += 1
            else:
                result += char
        else:
            result += char
    return result


if __name__ == "__main__":
    original = "А знаете, какая фраза часто повторялась в немецких шифровках ВМВ, что позволяла взломать шифры?"
    key = "ЗАЦЕНЗУРЕНО"
    encrypted = vigenere_encrypt(original, key)
    print(f"Зашифровано (верхний, ключ '{key}'): {encrypted}")
    # Расшифрование (верхний регистр)
    decrypted = vigenere_decrypt(encrypted, key)
    print(f"Расшифровано (верхний): {decrypted}")
