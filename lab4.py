import numpy as np
import math

# ------------- Алфавит и исходные данные -------------

alphabet = ['А', 'О', 'И', 'Н', 'Т', '_']
N = len(alphabet)
m = 3  # длина блока
text = "НАТА_ИННА_И_АНТОН"

# ------------- Вспомогательные функции -------------

def pad_text(text, block_size, pad_char):
    pad_len = (-len(text)) % block_size
    return text + pad_char * pad_len

def text_to_vectors(text, alphabet, block_size):
    char_to_idx = {c: i for i, c in enumerate(alphabet)}
    vecs = []
    for i in range(0, len(text), block_size):
        block = text[i:i+block_size]
        vecs.append([char_to_idx[char] for char in block])
    return vecs

def vectors_to_text(vectors, alphabet):
    return ''.join(''.join(alphabet[idx] for idx in vec) for vec in vectors)

# --------------- Генерация обратимой матрицы -------------

def find_invertible_matrix(n, m):
    while True:
        A = np.random.randint(0, n, size=(m, m))
        det = int(round(np.linalg.det(A)))
        if math.gcd(det, n) == 1:
            return A

def matrix_mod_inv(A, n):
    det = int(round(np.linalg.det(A)))
    det_inv = pow(det, -1, n)
    adj = np.round(det * np.linalg.inv(A)).astype(int) % n
    return (det_inv * adj) % n

# ------------ Шифрование и расшифрование ------------

def hill_encrypt(text, A, H, alphabet):
    padded_text = pad_text(text, A[0].shape[0], alphabet[-1])
    vectors = text_to_vectors(padded_text, alphabet, A[0].shape[0])
    encrypted_vecs = []
    for X in vectors:
        Y = (np.dot(X, A) + H) % N
        encrypted_vecs.append(Y.astype(int).tolist())
    return vectors_to_text(encrypted_vecs, alphabet)

def hill_decrypt(ciphertext, A, H, alphabet):
    vecs = text_to_vectors(ciphertext, alphabet, A[0].shape[0])
    A_inv = matrix_mod_inv(A, N)
    decrypted_vecs = []
    for Y in vecs:
        X = np.dot((np.array(Y) - H) % N, A_inv) % N
        decrypted_vecs.append(np.round(X).astype(int).tolist())
    return vectors_to_text(decrypted_vecs, alphabet)

# ----------- Пример использования ------------------

if __name__ == "__main__":
    print(f"Алфавит: {alphabet}")
    print(f"Оригинал: {text}")

    # Генерация ключей (матрица и вектор)
    A = find_invertible_matrix(N, m)
    H = np.random.randint(0, N, size=m)

    print(f"Матрица A:\n{A}")
    print(f"Вектор H: {H}")

    encrypted = hill_encrypt(text, A, H, alphabet)
    print(f"Зашифровано: {encrypted}")

    decrypted = hill_decrypt(encrypted, A, H, alphabet)
    print(f"Расшифровано: {decrypted}")
