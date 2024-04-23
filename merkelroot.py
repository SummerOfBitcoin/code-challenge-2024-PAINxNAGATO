import hashlib
import coinbase

# Hash pairs of items recursively until a single value is obtained
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
    # Reverse inputs before and after hashing
    # due to big-endian / little-endian nonsense
    a1 = bytes.fromhex(a)[::-1]
    # a1 = bytes.fromhex(a)
    b1 = bytes.fromhex(b)[::-1]
    # b1 = bytes.fromhex(b)
    h = hashlib.sha256(hashlib.sha256(a1+b1).digest()).digest()
    return h[::-1].hex()
    # return h.hex()

def reverse_byte_order(txid):
    # Assuming txid is a hexadecimal string
    return txid[::-1]
	
def return_merkelhash():
    txHashes = coinbase.extract_txids_from_folder("verified_transactions")
    txHashes = ["0000000000000000000000000000000000000000000000000000000000000000"] + txHashes
    txid_list_reversed = [reverse_byte_order(txid) for txid in txHashes]
    merkle_root = merkle(txid_list_reversed)
    # print("Merkle Root:", merkle_root)
    return merkle_root

# print(return_merkelhash())

