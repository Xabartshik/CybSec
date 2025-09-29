import random

class StreamCipher:
    def __init__(self):
        self.KEY = []
        self.GEN = []

    def create_key(self):
        # 1. Создание ключа как перестановки чисел 0-255
        self.KEY = list(range(256))
        random.shuffle(self.KEY)

    def init_generator(self):
        # 2. Инициализация генератора GEN на основе ключа
        self.GEN = list(self.KEY)  # Исходное состояние - ключ
        j = 0
        for i in range(256):
            j = (j + self.GEN[i] + self.KEY[i]) % 256
            self.GEN[i], self.GEN[j] = self.GEN[j], self.GEN[i]

    def get_gamma(self, message_length):
        # 3. Генерация гаммы GAMMA равной длине сообщения
        GAMMA = [0] * message_length
        i = 0
        j = 0
        for k in range(message_length):
            i = (i + 1) % 256
            j = (j + self.GEN[i]) % 256
            self.GEN[i], self.GEN[j] = self.GEN[j], self.GEN[i]
            t = (self.GEN[i] + self.GEN[j]) % 256
            GAMMA[k] = self.GEN[t]
        return GAMMA

    def encrypt(self, message_bytes):
        # 4. Шифрование: XOR с гаммой
        GAMMA = self.get_gamma(len(message_bytes))
        output = bytearray(len(message_bytes))
        for k in range(len(message_bytes)):
            output[k] = message_bytes[k] ^ GAMMA[k]
        return output

    def decrypt(self, ciphertext_bytes):
        # 5. Расшифрование: то же самое, XOR с гаммой (поскольку XOR обратим)
        return self.encrypt(ciphertext_bytes)

# Пример использования
if __name__ == "__main__":
    cipher = StreamCipher()
    cipher.create_key()
    cipher.init_generator()


    plaintext = "ЙЦУКЕНГШЩЗХЪфывапролджэЯЧСМИТЬБЮ."
    message_bytes = plaintext.encode('utf-8')


    ciphertext = cipher.encrypt(message_bytes)
    print("Шифртекст (в hex):", ciphertext.hex())


    cipher_dec = StreamCipher()
    cipher_dec.KEY = cipher.KEY
    cipher_dec.init_generator()


    decrypted_bytes = cipher_dec.decrypt(ciphertext)
    decrypted_text = decrypted_bytes.decode('utf-8')
    print("Расшифрованный текст:", decrypted_text)
