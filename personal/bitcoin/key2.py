import bitcoin

# valid_random_key = False

# while valid_random_key is not True:
#   random_key = bitcoin.random_key()
#   decoded_key = bitcoin.decode_privkey(random_key, "hex")
#   valid_random_key = 0 < decoded_key < bitcoin.N

# print(type(random_key), random_key)
# print(type(decoded_key), decoded_key)

private_key = "1E99423A4ED27608A15A2616A2B0E9E52CED330AC530EDCC32C8FFC6A526AEDD"
decoded_key = bitcoin.decode_privkey(private_key, "hex")
print(0 < decoded_key < bitcoin.N)

print(private_key)
print(decoded_key)
