import random
# Принцип работы
# 1. Подготовить данные
# Переводим их в 2-ую форму, склеиваем вместе (в данном случае, 16 + 16 бит)
# 2. P-блок (Перестановка) -- перемешиваем все биты по какой-то фиксированной схеме
# [4, 7, 2, 21, 10, 5, 25, 15, где значения - значения позиции старых битов до перемешивания
# 3. S-блок (Замена) -- 32 делим на блоки по 4 бита (0-15), перестановка по ключу (если число 3, а ключ, допустим, (2 7 9), то 3 меняем на 9 )
# Обратно в 4 бита, объединить вместе
# 4. Второй Р-блок - перестановка 32 бит

# Расшифровка:
# Все то же самое, но наоборот

# Перестановка элементов списка 64 раза
def random_permutation(lst):
    lst = lst[:]
    for _ in range(64):
        i = random.randint(0, len(lst) - 1)
        j = random.randint(0, len(lst) - 1)
        lst[i], lst[j] = lst[j], lst[i]
    return lst

# Возвращает набор случайных перестановок
def generate_permutations(original, n):
    perms = []
    while len(perms) < n:
        perm = random_permutation(original)
        if perm != original:
            perms.append(perm)
    return perms

# Символ в двоичный код
def char_to_bin(c):
    return bin(ord(c))[2:].zfill(16)

# Строка в 32 битную двоичную строку
def string_to_bin(s):
    if len(s) != 2:
        raise ValueError("String must be exactly two characters.")
    return char_to_bin(s[0]) + char_to_bin(s[1])

# Возвращает обратную перестановку, меняя местами индексы и значения
def get_inverse_perm(perm):
    inverse = [0] * len(perm)
    for i, p in enumerate(perm):
        inverse[p] = i
    return inverse

# Получаем новую строку по перестановке
def p_block(bit_str, perm):
    return ''.join(bit_str[i] for i in perm)

def p_block_encrypt(bit_str, perm):
    return p_block(bit_str, perm)

def p_block_decrypt(bit_str, perm):
    inverse = get_inverse_perm(perm)
    return p_block(bit_str, inverse)


def bin_to_int(bin_str):
    return int(bin_str, 2)

def int_to_bin(num, width):
    return bin(num)[2:].zfill(width)

# Замена по перестановке десятичного числа, полученного из 4 битов
def s_block_encrypt(bits4, s_perm):
    val = bin_to_int(bits4)
    new_val = s_perm[val]
    return int_to_bin(new_val, 4)

def s_block_decrypt(bits4, s_perm):
    val = bin_to_int(bits4)
    inverse = get_inverse_perm(s_perm)
    orig_val = inverse[val]
    return int_to_bin(orig_val, 4)

def battery_encrypt(bit32, s_perm):
    # Разбивает на блоки по 4
    parts = [bit32[i:i+4] for i in range(0, 32, 4)]
    # S-шифрование
    enc_parts = [s_block_encrypt(part, s_perm) for part in parts]
    return ''.join(enc_parts)

def battery_decrypt(bit32, s_perm):
    # Разбивает на блоки по 4
    parts = [bit32[i:i+4] for i in range(0, 32, 4)]
    # S-дешифрование
    dec_parts = [s_block_decrypt(part, s_perm) for part in parts]
    return ''.join(dec_parts)

# Подготовка данных
def bin_to_string(bit32):
    b1 = bit32[0:16]
    b2 = bit32[16:32]
    c1 = chr(bin_to_int(b1))
    c2 = chr(bin_to_int(b2))
    return c1 + c2

# Генерация перестановок
random.seed("Black Magic")  # Для воспроизводимости
S_original = list(range(16))
P_original = list(range(32))
num_perms = 32  # 10-20
# Перестановочки
S_perms = generate_permutations(S_original, num_perms)
P_perms = generate_permutations(P_original, num_perms)

# Для S можно добавить перестановку, которая соответствует какому-то примеру, но поскольку в документе не указана конкретная, используем сгенерированные

if __name__ == "__main__":
    # Пример использования с номерами перестановок
    message = "東方"
    # Номера перестановок для использования
    p_num = 20
    s_num = 2

    print("========== Шифрование ==========")
    print("Исходное сообщение:", message)
    bits = string_to_bin(message)
    print("Битовая форма исходного сообщения:", bits)
    perm_p = P_perms[p_num]
    bits_p1 = p_block_encrypt(bits, perm_p)
    print("Зашифрованная p-блоком битовая форма:", bits_p1)
    perm_s = S_perms[s_num]
    bits_s = battery_encrypt(bits_p1, perm_s)
    print("Зашифрованная батареей s-блоков битовая форма:", bits_s)
    bits_p2 = p_block_encrypt(bits_s, perm_p)
    print("Зашифрованная p-блоком битовая форма:", bits_p2)
    encrypted = bin_to_string(bits_p2)
    print("Зашифрованное сообщение:", encrypted)

    print("========== Расшифрование ==========")
    print("Зашифрованное сообщение:", encrypted)
    bits_enc = string_to_bin(encrypted)
    bits_dp1 = p_block_decrypt(bits_enc, perm_p)
    print("Расшифрованная p-блоком битовая форма:", bits_dp1)
    bits_ds = battery_decrypt(bits_dp1, perm_s)
    print("Расшифрованная батареей s-блоков битовая форма:", bits_ds)
    bits_dp2 = p_block_decrypt(bits_ds, perm_p)
    print("Расшифрованная p-блоком битовая форма:", bits_dp2)
    decrypted = bin_to_string(bits_dp2)
    print("Расшифрованное сообщение:", decrypted)