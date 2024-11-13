import bip32utils
from icecream import ic
from mnemonic import Mnemonic

mnemo = Mnemonic("english")
# words = mnemo.generate(strength=256)
# 5fdf86297346e72e2dd6d13e8679d940e1792b9dabd276f77346f519fca85089
# 04cacb01bd1d5137403f3c1e51f855105dbd773b5b752727fd770bfa9902aad51a190407b93437d442e222d05e6714cfae7bcf57765c8669c6d91956ea01cb6f9c
# 1Ma92vhGhcpmHdkntawGcTqJAnwbFqhTWo
initial = ['garlic', 'wire', 'medal', 'track','hover', \
         'novel', 'resemble', 'surface', 'direct', 'critic', \
          'iron', 'limb', 'bleak', 'noise', 'issue', \
            'kid', 'ivory', 'romance', 'spider', 'tuition', \
              'panther', 'feature', 'drama', 'camera']

words = " ".join(initial)

ic(words)
seed = mnemo.to_seed(words, passphrase="")
ic(seed)
# entropy = mnemo.to_entropy(words)
# ic(entropy)
ic(seed.hex())
root_key = bip32utils.BIP32Key.fromEntropy(seed)
root_address = root_key.Address()
ic(root_address)

