# important imports.

import hashlib
import txid_hashes

# merkel root creation 

def merkle(hashList):
    if len(hashList) == 1:
        return hashList[0]
    newHashList = []

    # Process pairs. For odd length, the last is skipped
    
    for i in range(0, len(hashList)-1, 2):
        newHashList.append(hash2(hashList[i], hashList[i+1]))
    if len(hashList) % 2 == 1: # odd, hash last item twice
        newHashList.append(hash2(hashList[-1], hashList[-1]))
    return merkle(newHashList)

def hash2(a, b):
    a1 = bytes.fromhex(a)[::-1]
    
    b1 = bytes.fromhex(b)[::-1]

    h = hashlib.sha256(hashlib.sha256(a1+b1).digest()).digest()
    
    return h[::-1].hex()

# bytes reversing functionality

def reverse_byte_order(txid):
    return txid[::-1]

# merkel root hash creation.
	
def return_merkelhash():
    txHashes = txid_hashes.extract_txids_from_folder("verified_transactions")
    txHashes = ["0000000000000000000000000000000000000000000000000000000000000000"] + txHashes
    merkle_root = merkle(txHashes)
    return merkle_root


