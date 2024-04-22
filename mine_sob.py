import hashlib
import struct
import merkelroot
import time
def mining():
    ver = bytes.fromhex("00000020")
    prev_block = "0000000000000000000000000000000000000000000000000000000000000000"
    mrkl_root,txhash = merkelroot.return_merkelhash()
# 8a97295a2747b4f1a0b3948df3990344c0e19fa6b2b92b3a19c8e6badc141787
# time_ = 0x53058b35  # 2014-02-20 04:57:25
    current_unix_time = int(time.time())
# int(hex_string, 16)
    time_ = int(hex(current_unix_time),16)
# print(time_) 
    bits = 0x1f00ffff # constant(difficult) (do not change).

# Calculating the target from bits
    exp = bits >> 24
    mant = bits & 0xffffff
    target_hexstr = '%064x' % (mant * (1<<(8*(exp - 3))))
    # print("target difficult :",target_hexstr)
# target_hexstr = "0000ffff00000000000000000000000000000000000000000000000000000000"
    target_bin = bytes.fromhex(target_hexstr)

    nonce = 1 # success : 77585 (0x12f11). 
    while nonce < 0x100000000:
        header = (
             ver + 
            bytes.fromhex(prev_block)[::-1] + 
            bytes.fromhex(mrkl_root) + 
            struct.pack("<LLL", time_, bits, nonce)
        )
    # print(header.hex())
    # header hash .
        hash = hashlib.sha256(hashlib.sha256(header).digest()).digest()

    # print(nonce, hash[::-1].hex())

        if hash[::-1] < target_bin:
            # print(header.hex())
            # print('success')
            break
        nonce += 1
    return header.hex()

