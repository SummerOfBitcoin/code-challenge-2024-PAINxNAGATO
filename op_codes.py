import hashlib
from Crypto.Hash import RIPEMD160
import json
import hashlib
import struct
# import ecdsa
import sig_verification


#---------------------------------------------#
def double_sha256(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()

def serialize_outpoint(txid, vout):
    # Serialize txid in little-endian and vout as little-endian integer
    txid_bytes = bytes.fromhex(txid)[::-1]  # Reverse txid to little-endian
    vout_bytes = struct.pack('<I', vout)    # Pack vout as little-endian unsigned int
    return txid_bytes + vout_bytes

def serialize_sequence(sequence):
    # Sequence numbers are serialized as little-endian unsigned integers
    return struct.pack('<I', sequence)

def serialize_script_length(script_hex):
    # Calculate the length of the script
    script_length = len(bytes.fromhex(script_hex))
    # Serialize the length in big-endian format (using 2 bytes)
    return struct.pack('>H', script_length)


def op_pushbytes_(op,tokens,stack,i):
    # Extract the number of bytes to push
    num_bytes =  2 * int(op[13:])
    i += 1  # Move to the data part
    data_to_push = tokens[i][:num_bytes]  # Slice the data up to the specified bytes
    stack.append(data_to_push)  # Push to stack
    return stack, i

def op_dup(stack):
    if stack:
        stack.append(stack[-1])
    return stack

def op_hash160(stack):
    sha256_val = hashlib.sha256(bytes.fromhex(stack.pop())).digest()
    ripemd_hash = RIPEMD160.new(sha256_val).digest()
    stack.append(ripemd_hash.hex())

    return stack

def op_equalverify(stack):
    if len(stack) >= 2:
        a = stack.pop()
        b = stack.pop()
        if a != b:
            return True, stack
        else :
            # print("OP_equalverified")
            return False, stack

def op_checksig(stack,data,l):
    if len(stack) >= 2:
        pubkey = stack.pop()
        sig = stack.pop()
        message_hash = message_serilization(data,sig,l)
        # print(sig_hash)
        is_valid = sig_verification.ecdsa_check(pubkey,sig,message_hash)
        return is_valid


def message_serilization(data,sig,l):

    message = ''

    version = data['version']

    if(version == 1):
        version = "01000000"
    else :
        version = "02000000"

    message += version

    message += "{:02d}".format(len(data['vin']))


    
    # vin 
    k = 1
    for vin in data['vin']:
        big_endian_txid = vin['txid']
        little_endian_txid = ''.join(reversed([big_endian_txid[i:i+2] for i in range(0, len(big_endian_txid), 2)]))

        message += little_endian_txid

        vout = vin["vout"]
        vout_bytes = struct.pack('<I', int(vout))
        message += vout_bytes.hex()

        length_pubkey = len(vin["prevout"]["scriptpubkey"])
        # compact_size = encode_compact_size(length_pubkey)
        if(k == l):
            message += hex(int(length_pubkey/2))[2:]
            message += vin["prevout"]["scriptpubkey"]
        else :
            message += "00"
            message += ""
        sequence = vin["sequence"]
        sequence_bytes = struct.pack('<I', sequence).hex()
        message += sequence_bytes
        # print(sequence_bytes)
        k += 1
    
# vout
    message += "{:02d}".format(len(data['vout']))
    for vout in data['vout']:
        message += struct.pack('<Q', vout['value']).hex()
        size_pubkey = len(vout["scriptpubkey"])
        message += hex(int(size_pubkey/2))[2:]
        message += vout["scriptpubkey"]

    message += struct.pack('<I',data['locktime']).hex()
    sig_flag = sig[-2:]
    if(sig_flag == "01") :
        sighash = struct.pack('<I', int(sig_flag)).hex()
    elif(sig_flag == "02") :
        sighash = struct.pack('<I', int(sig_flag)).hex()
    elif(sig_flag == "03") :
        sighash = struct.pack('<I', int(sig_flag)).hex()
    else:
        sighash = struct.pack('<I', int("00")).hex()

    message += sighash

    if(len(message) % 2 == 0):
        bytes.fromhex(message)
    else : 
        message += "0"

    message_hash = double_sha256(bytes.fromhex(message))

    return message_hash.hex()

