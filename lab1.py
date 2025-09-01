upper_alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
lower_alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
alphabet_size = len(upper_alphabet)

def caesar_encrypt(text, shift):
    result = ''
    shift = shift % alphabet_size
    for char in text:
        if char in upper_alphabet:
            index = (upper_alphabet.index(char) + shift) % alphabet_size
            result += upper_alphabet[index]
        elif char in lower_alphabet:
            index = (lower_alphabet.index(char) + shift) % alphabet_size
            result += lower_alphabet[index]
        else:
            result += char
    return result

def caesar_decrypt(ciphertext, shift):
    result = ''
    shift = shift % alphabet_size
    for char in ciphertext:
        if char in upper_alphabet:
            index = (upper_alphabet.index(char) - shift) % alphabet_size
            result += upper_alphabet[index]
        elif char in lower_alphabet:
            index = (lower_alphabet.index(char) - shift) % alphabet_size
            result += lower_alphabet[index]
        else:
            result += char
    return result


# Все варианты
def caesar_brute_force(ciphertext):
    results = []
    for shift in range(alphabet_size):
        decrypted = caesar_decrypt(ciphertext, shift)
        results.append(f"Сдвиг {shift}: {decrypted}")
    return results


if __name__ == "__main__":
    original = "А знаете, какая фраза часто повторялась в немецких шифровках ВМВ, что позволяла взломать шифры?"
    shift = 4
    encrypted = caesar_encrypt(original, shift)
    print(f"Зашифровано (сдвиг {shift}): {encrypted}")
    decrypted = caesar_decrypt(encrypted, shift)
    print(f"Расшифровано: {decrypted}")
    print("Варианты дешифрования перебором:")
    for variant in caesar_brute_force(encrypted):
        print(variant)