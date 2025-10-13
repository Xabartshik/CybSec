

from typing import Tuple, List

# ---------------- Базовые процедуры ----------------

def egcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Расширенный алгоритм Евклида: возвращает (g, x, y) такие, что ax + by = g = gcd(a, b). 
    """
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = egcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)

def modinv(e: int, phi: int) -> int:
    """
    d такое, что (d * e) % phi == 1, используется для d ≡ e^{-1} (mod φ(n)) 
    """
    g, x, _ = egcd(e, phi)
    if g != 1:
        raise ValueError("Обратного элемента не существует (e и φ(n) не взаимно просты)")
    return x % phi  # Нормируем в [0, φ(n)-1]

def gcd(a: int, b: int) -> int:
    """
    Обычный НОД для проверки взаимной простоты gcd(e, φ(n)) = 1 
    """
    while b:
        a, b = b, a % b
    return a

# ---------------- Генерация ключей ----------------

def generate_keys(p: int, q: int, e: int | None = None) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Генерация ключей RSA:
      - n = p * q
      - φ(n) = (p - 1) * (q - 1)
      - выбрать e: 1 < e < φ(n), gcd(e, φ(n)) = 1
      - d = e^{-1} mod φ(n)
      - открыть: (e, n), закрыть: (d, n)
    """
    if p == q:
        raise ValueError("p и q должны быть различными простыми")
    n = p * q
    phi = (p - 1) * (q - 1)

    if e is None:
        e = 23  # небольшой простой показатель
    if not (1 < e < phi) or gcd(e, phi) != 1:
        raise ValueError("e должно быть в (1, φ(n)) и взаимно просто с φ(n)")

    d = modinv(e, phi)
    public_key = (e, n)
    private_key = (d, n)
    return public_key, private_key

# ---------------- Шифрование/расшифрование целых ----------------

def encrypt_int(m: int, public_key: Tuple[int, int]) -> int:
    """
    Шифрование целого: c ≡ m^e (mod n), где 1 ≤ m ≤ n-1 
    """
    e, n = public_key
    if not (1 <= m <= n - 1):
        raise ValueError("m должно быть в диапазоне [1, n-1]")
    return pow(m, e, n)

def decrypt_int(c: int, private_key: Tuple[int, int]) -> int:
    """
    Расшифрование целого: m ≡ c^d (mod n) 
    """
    d, n = private_key
    if not (1 <= c <= n - 1):
        raise ValueError("c должно быть в диапазоне [1, n-1]")
    return pow(c, d, n)

# ---------------- Работа со строками (покоординатно по символам) ----------------

def encrypt_text(text: str, public_key: Tuple[int, int]) -> List[int]:
    """
    шифруем каждый символ отдельно как ord(ch) ^ e mod n.
    """
    e, n = public_key
    cipher = []
    for ch in text:
        m = ord(ch)  # Преобразуем символ в код Unicode
        if m >= n:
            raise ValueError("n слишком мало для данного символа; выберите большие p, q или ограничьте алфавит")
        cipher.append(pow(m, e, n))  # c = m^e mod n
    return cipher

def decrypt_text(cipher: List[int], private_key: Tuple[int, int]) -> str:
    """
    Обратное преобразование: каждый элемент расшифровываем и превращаем в символ chr(m)
    """
    d, n = private_key
    chars = []
    for c in cipher:
        m = pow(c, d, n)  # m = c^d mod n
        chars.append(chr(m))  # Восстанавливаем символ
    return "".join(chars)  # Собираем строку

# ---------------- Демонстрация ----------------

if __name__ == "__main__":
    p, q, e = 43, 47, 37
    pub, priv = generate_keys(p, q, e)
    print(f"Открытый ключ (e, n): {pub}")
    print(f"Закрытый ключ (d, n): {priv}")

    m = 42
    c = encrypt_int(m, pub)
    m_back = decrypt_int(c, priv)
    print(f"m = {m} -> c = {c} -> m' = {m_back}")


    text = "Закрытый ключ переломлен пополам, а наш батюшка сеньор, совсем усоп, он разложился на сессию и липовый прод"
    cipher_list = encrypt_text(text, pub)
    text_back = decrypt_text(cipher_list, priv)
    print(f"text = {text!r}\ncipher = {cipher_list}\ntext' = {text_back!r}") 
