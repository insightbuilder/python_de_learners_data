from passlib.utils import pbkdf2
import binascii
import sys

arguments_counter = len(sys.argv) - 1

if arguments_counter != 2:
    raise TypeError("The function takes exactly 2 arguments (%d passed)" % arguments_counter)

password = sys.argv[1]
ssid = sys.argv[2]

var = pbkdf2.pbkdf2(str.encode(password), str.encode(ssid), 4096, 32)

print(binascii.hexlify(var).decode("utf-8"))