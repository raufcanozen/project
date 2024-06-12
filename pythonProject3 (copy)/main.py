from hashlib import md5
from base64 import b64decode
from base64 import b64encode

from Crypto import Random
from Crypto.Cipher import AES




BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


def Encrypt(password,string):
    password = md5(password.encode('utf8')).hexdigest()
    string = pad(string)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(password, AES.MODE_CBC, iv)
    return b64encode(iv + cipher.encrypt(string))

def Decrypt(password,string):
    password = md5(password.encode('utf8')).hexdigest()
    string = b64decode(string)
    iv = string[:16]
    cipher = AES.new(password, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(string[16:])).decode('utf8')

msg = Encrypt("BuCokGizliBirSifre","Selam")
print(msg)
msg2 = Decrypt("BuCokGizliBirSifre",msg)
print(msg2)