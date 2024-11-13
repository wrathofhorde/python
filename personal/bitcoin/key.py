import random
from bitcoin import *
from icecream import ic

bit256 = ""

for i in range(256):
  bit256 += str(random.randrange(0, 2))

ic(bit256)
ic(int(bit256, 2))
ic(hex(int(bit256, 2)))
ic(hex(int(bit256, 2))[2:])

private_key = hex(int(bit256, 2))[2:]

public_key = privtopub(private_key)
address = pubtoaddr(public_key)

words = entropy_to_words(bytes.fromhex(private_key))

print(private_key)
print(public_key)
print(address)
print(words)
