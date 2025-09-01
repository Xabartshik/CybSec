import math

# Модуль для арифметики классов вычетов
class Residue:
    def __init__(self, value, mod):
        self.mod = mod
        self.value = value % mod

    def __add__(self, other):
        if not isinstance(other, Residue) or self.mod != other.mod:
            raise ValueError("Operands must be Residue with same mod")
        return Residue((self.value + other.value) % self.mod, self.mod)

    def __sub__(self, other):
        if not isinstance(other, Residue) or self.mod != other.mod:
            raise ValueError("Operands must be Residue with same mod")
        return Residue((self.value - other.value) % self.mod, self.mod)

    def __mul__(self, other):
        if not isinstance(other, Residue) or self.mod != other.mod:
            raise ValueError("Operands must be Residue with same mod")
        return Residue((self.value * other.value) % self.mod, self.mod)

    def __truediv__(self, other):
        if not isinstance(other, Residue) or self.mod != other.mod:
            raise ValueError("Operands must be Residue with same mod")
        return self * other.inverse()

    def inverse(self):
        inv = mod_inverse(self.value, self.mod)
        return Residue(inv, self.mod)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"Residue({self.value}, {self.mod})"
# Расширенный алгоритм Евклида (НОД и коэффиценты)
def egcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = egcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        raise ValueError(f"No modular inverse for {a} mod {m}")
    return x % m

# Функции для шифрования и расшифрования (основная программа)
def affine_encrypt(text, a, b, alphabet):
    N = len(alphabet)
    if math.gcd(a, N) != 1:
        raise ValueError(f"gcd({a}, {N}) != 1, invalid a")
    result = ''
    mod = N
    A = Residue(a, mod)
    B = Residue(b, mod)
    char_to_index = {char: i for i, char in enumerate(alphabet)}
    for char in text.upper():
        if char in char_to_index:
            x = Residue(char_to_index[char], mod)
            y = (A * x + B).value
            result += alphabet[y]
        else:
            result += char
    return result

def affine_decrypt(ciphertext, a, b, alphabet):
    N = len(alphabet)
    if math.gcd(a, N) != 1:
        raise ValueError(f"gcd({a}, {N}) != 1, invalid a")
    result = ''
    mod = N
    A = Residue(a, mod)
    B = Residue(b, mod)
    A_inv = A.inverse()
    char_to_index = {char: i for i, char in enumerate(alphabet)}
    for char in ciphertext.upper():
        if char in char_to_index:
            y = Residue(char_to_index[char], mod)
            x = (A_inv * (y - B)).value
            result += alphabet[x]
        else:
            result += char
    return result




# Пример использования (выберу вариант 0)
if __name__ == "__main__":
    # В2
    alphabet = ['А', 'О', 'И', 'Н', 'Т', '_']
    original = "НАТА_ИННА_И_АНТОН"
    print(f"Алфавит: {alphabet}")
    print(f"Оригинал: {original}")

    a = 7
    b = 3
    encrypted = affine_encrypt(original, a, b, alphabet)
    print(f"Зашифровано (a={a}, b={b}): {encrypted}")
    decrypted = affine_decrypt(encrypted, a, b, alphabet)
    print(f"Расшифровано: {decrypted}")
