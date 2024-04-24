import txid_hashes
import merkelroot
import op_codes
# wtxid of legacy is the same as the txid 
def witness_roothash(folder_path):
    wtxids = txid_hashes.extract_txids_from_folder(folder_path)

    wtxids = ["0000000000000000000000000000000000000000000000000000000000000000"] + wtxids

    wit_roothash = merkelroot.merkle(wtxids)

    return bytes.fromhex(wit_roothash)[::-1].hex()

def wtxid_commitment(wit_roothash,wit_reserved_value):

    message = wit_roothash + wit_reserved_value

    # print(message)

    message = bytes.fromhex(message)

    wtxid_commit = op_codes.double_sha256(message)

    return wtxid_commit.hex()

# roothash = "dbee9a868a8caa2a1ddf683af1642a88dfb7ac7ce3ecb5d043586811a41fdbf2"

# rs = "0000000000000000000000000000000000000000000000000000000000000000"

# print(wtxid_commitment(roothash,rs).hex())







