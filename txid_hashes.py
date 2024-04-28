# important imports

import struct
import op_codes
import json
import os
import compactSize

# Function to create the Txids from the jsons

def transaction_header_p2pkh(data):

    message = ''

    version = data['version']

    if(version == 1):
        version = "01000000"
    else :
        version = "02000000"

    message += version

    message += compactSize.compact_size_calculator(len(data['vin']))

    for vin in data['vin']:
        big_endian_txid = vin['txid']
        little_endian_txid = ''.join(reversed([big_endian_txid[i:i+2] for i in range(0, len(big_endian_txid), 2)]))

        message += little_endian_txid

        vout = vin["vout"]
        vout_bytes = struct.pack('<I', int(vout))
        message += vout_bytes.hex()

        length_pubkey = len(vin["scriptsig"])
        message += compactSize.compact_size_calculator(int(length_pubkey/2))
        message += vin["scriptsig"]
        sequence = vin["sequence"]
        sequence_bytes = struct.pack('<I', sequence).hex()
        message += sequence_bytes
    
    message += compactSize.compact_size_calculator(len(data['vout']))

    for vout in data['vout']:
        message += struct.pack('<Q', vout['value']).hex()
        size_pubkey = len(vout["scriptpubkey"])
        message += compactSize.compact_size_calculator(int(size_pubkey/2))
        message += vout["scriptpubkey"]

    locktime = struct.pack('<I', int(data["locktime"])).hex()

    message += locktime

    message_hash = op_codes.double_sha256(bytes.fromhex(message))

    return message_hash[::-1].hex()

# Function to switch between Txids for different scripts.

def extract_txids_from_folder(folder_path):
    txids = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)
                if(data["vin"][0]["prevout"]["scriptpubkey_type"] == "p2pkh"):
                    txid = transaction_header_p2pkh(data)
                    if txid:
                        txids.append(txid)
                elif(data["vin"][0]["prevout"]["scriptpubkey_type"] == "v0_p2wpkh"):
                    txid = transaction_header_p2wpkh(data)
                    if txid:
                        txids.append(txid)
    return txids

# Function to create the Txids from the jsons.

def transaction_header_p2wpkh(data):

    message = ""

    version = data['version']

    if(version == 1):
        version = "01000000"
    elif(version == 2):
        version = "02000000"

    message += version

    message += compactSize.compact_size_calculator(len(data['vin']))

    for vin in data['vin']:
        big_endian_txid = vin['txid']
        little_endian_txid = ''.join(reversed([big_endian_txid[i:i+2] for i in range(0, len(big_endian_txid), 2)]))

        message += little_endian_txid

        vout = vin["vout"]
        vout_bytes = struct.pack('<I', vout)
        message += vout_bytes.hex()

        message += "00" 

        sequence = vin["sequence"]
        sequence_bytes = struct.pack('<I', sequence).hex()
        message += sequence_bytes

    message += compactSize.compact_size_calculator(len(data['vout']))

    for vout in data['vout']:
        message += struct.pack('<Q', vout['value']).hex()
        size_pubkey = len(vout["scriptpubkey"])
        message += compactSize.compact_size_calculator(int(size_pubkey/2))
        message += vout["scriptpubkey"]

    locktime = struct.pack('<I', data["locktime"]).hex()

    message += locktime

    message_hash = op_codes.double_sha256(bytes.fromhex(message))

    return message_hash[::-1].hex()
