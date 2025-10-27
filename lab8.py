import random
import math


def calculate_hamming_params(alphabet_size):
    """
    Вычисляет параметры кода Хэмминга для заданного размера алфавита.
    Возвращает (n, m, k) - общее количество бит, информационных бит и контрольных бит.
    """
    # Минимальное количество бит для кодирования алфавита
    m_required = math.ceil(math.log2(alphabet_size))

    # Подбираем k такое, что 2^k - 1 - k >= m_required
    k = 1
    while True:
        m = (2 ** k - 1) - k
        if m >= m_required:
            break
        k += 1

    n = 2 ** k - 1
    return n, m, k


def get_parity_bit_positions(n):
    """
    Возвращает позиции контрольных битов (степени двойки).
    """
    positions = []
    i = 0
    while 2 ** i <= n:
        positions.append(2 ** i)
        i += 1
    return positions


def encode_hamming(data_bits, n, k):
    """
    Кодирует информационные биты кодом Хэмминга.
    data_bits - список информационных битов.
    Возвращает закодированное сообщение длиной n.
    """
    # Инициализируем массив для закодированного сообщения
    encoded = [0] * (n + 1)  # Индексация с 1

    # Позиции контрольных битов
    parity_positions = get_parity_bit_positions(n)

    # Заполняем информационные биты
    data_index = 0
    for i in range(1, n + 1):
        if i not in parity_positions:
            encoded[i] = data_bits[data_index]
            data_index += 1

    # Вычисляем контрольные биты
    for parity_pos in parity_positions:
        parity = 0
        for i in range(1, n + 1):
            # Проверяем, контролирует ли данный контрольный бит позицию i
            if i & parity_pos:
                parity ^= encoded[i]
        encoded[parity_pos] = parity

    # Возвращаем без нулевого индекса
    return encoded[1:]


def decode_hamming(received, n, k):
    """
    Декодирует и исправляет ошибки в сообщении, закодированном кодом Хэмминга.
    Возвращает (corrected_message, error_position).
    """
    received = [0] + received  # Добавляем нулевой индекс для удобства

    # Вычисляем синдром
    syndrome = 0
    parity_positions = get_parity_bit_positions(n)

    for parity_pos in parity_positions:
        parity = 0
        for i in range(1, n + 1):
            if i & parity_pos:
                parity ^= received[i]
        if parity != 0:
            syndrome += parity_pos

    # Если синдром не равен 0, исправляем ошибку
    if syndrome != 0:
        received[syndrome] ^= 1  # Инвертируем ошибочный бит
        error_position = syndrome
    else:
        error_position = 0

    # Извлекаем информационные биты
    parity_positions_set = set(parity_positions)
    data_bits = []
    for i in range(1, n + 1):
        if i not in parity_positions_set:
            data_bits.append(received[i])

    return data_bits, error_position


def introduce_error(encoded_list, symbol_index, bit_position):
    """
    Вносит ошибку в закодированное сообщение.
    symbol_index - индекс символа в списке.
    bit_position - позиция бита для инверсии (1-indexed).
    """
    if 0 <= symbol_index < len(encoded_list):
        if 0 <= bit_position - 1 < len(encoded_list[symbol_index]):
            encoded_list[symbol_index][bit_position - 1] ^= 1
            return True
    return False


def main():
    # Входные данные
    alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ "
    message = "Я ТАК СКУЧАЮ"

    print(f"Алфавит: {alphabet}")
    print(f"Размер алфавита: {len(alphabet)}")
    print(f"Исходное сообщение: {message}")
    print()

    # 1. Подбираем параметры кода Хэмминга
    n, m, k = calculate_hamming_params(len(alphabet))
    print(f"Параметры кода Хэмминга: ({n}, {m})")
    print(f"Информационных бит: {m}, Контрольных бит: {k}")
    print()

    # 2. Создаем таблицу кодирования символов
    bits_per_symbol = math.ceil(math.log2(len(alphabet)))
    symbol_to_code = {}
    for idx, char in enumerate(alphabet):
        binary = format(idx, f'0{bits_per_symbol}b')
        # Дополняем нулями до m бит
        binary = binary.ljust(m, '0')
        symbol_to_code[char] = [int(b) for b in binary]

    print("Таблица кодирования (первые 5 символов):")
    for i, char in enumerate(alphabet[:5]):
        print(f"  {char}: {''.join(map(str, symbol_to_code[char]))}")
    print()

    # 3. Кодируем сообщение
    encoded_message = []
    for char in message:
        if char in symbol_to_code:
            data_bits = symbol_to_code[char]
            encoded = encode_hamming(data_bits, n, k)
            encoded_message.append(encoded)

    print("Закодированное сообщение:")
    for i, enc in enumerate(encoded_message):
        print(f"  {message[i]}: {''.join(map(str, enc))}")
    print()

    # 4. Вносим случайные ошибки
    errors_introduced = []
    num_errors = random.randint(1, min(3, len(encoded_message)))  # Вносим 1-3 ошибки

    for _ in range(num_errors):
        symbol_idx = random.randint(0, len(encoded_message) - 1)
        bit_pos = random.randint(1, n)
        if introduce_error(encoded_message, symbol_idx, bit_pos):
            errors_introduced.append((symbol_idx, bit_pos))

    print(f"Внесено ошибок: {len(errors_introduced)}")
    for sym_idx, bit_pos in errors_introduced:
        print(f"  Символ '{message[sym_idx]}' (индекс {sym_idx}), позиция бита: {bit_pos}")
    print()

    print("Сообщение с ошибками:")
    for i, enc in enumerate(encoded_message):
        print(f"  {message[i]}: {''.join(map(str, enc))}")
    print()

    # 5. Декодируем и исправляем ошибки
    decoded_message = []
    errors_detected = []

    # Обратная таблица для декодирования
    code_to_symbol = {tuple(code): char for char, code in symbol_to_code.items()}

    for i, encoded in enumerate(encoded_message):
        data_bits, error_pos = decode_hamming(encoded, n, k)

        if error_pos != 0:
            errors_detected.append((i, error_pos))

        # Находим символ по информационным битам
        data_bits_tuple = tuple(data_bits)
        if data_bits_tuple in code_to_symbol:
            decoded_message.append(code_to_symbol[data_bits_tuple])
        else:
            decoded_message.append('?')

    decoded_text = ''.join(decoded_message)

    print("Обнаруженные и исправленные ошибки:")
    for sym_idx, bit_pos in errors_detected:
        print(f"  Символ '{message[sym_idx]}' (индекс {sym_idx}), позиция бита: {bit_pos}")
    print()

    print(f"Раскодированное сообщение: {decoded_text}")
    print()

    if decoded_text == message:
        print("✓ Сообщение успешно восстановлено!")
    else:
        print("✗ Ошибка при восстановлении сообщения")


if __name__ == "__main__":
    main()
