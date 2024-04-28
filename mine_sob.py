# important imports.

import hashlib
import struct
import merkelroot
import time

# An some miners algorithm implemented.

def mining():
    ver = bytes.fromhex("00000020")
    prev_block = "0000000000000000000000000000000000000000000000000000000000000000"
    mrkl_root = merkelroot.return_merkelhash()

    # Taking unix current time while mining the block

    current_unix_time = int(time.time())

    time_ = int(hex(current_unix_time),16)
    
    # difficulty bits.

    bits = 0x1f00ffff 

    # Calculating the target from bits
    exp = bits >> 24
    mant = bits & 0xffffff
    target_hexstr = '%064x' % (mant * (1<<(8*(exp - 3))))
   
    target_bin = bytes.fromhex(target_hexstr)

    # nonce for mining looping from 0 
    
    nonce = 0
    
    # mining iteratively
    
    while nonce < 0x100000000:
        header = (
             ver + 
            bytes.fromhex(prev_block)[::-1] + 
            bytes.fromhex(mrkl_root)[::-1] + 
            struct.pack("<LLL", time_, bits, nonce)
        )
    
        hash = hashlib.sha256(hashlib.sha256(header).digest()).digest()

        if hash[::-1] < target_bin:
            break
        nonce += 1
    
    # returning the successful header to be pushed in the block header.

    return header.hex()
