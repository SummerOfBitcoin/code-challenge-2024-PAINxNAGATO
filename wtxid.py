# important imports.

import txid_hashes
import merkelroot
import op_codes
import os
import json
import compactSize
import struct

# Wtxid of legacy is the same as the txid. 

# Function to create the Witness Root Hash.

def witness_roothash(folder_path):

    wtxids = extract_wtxids_from_folder(folder_path)

    wtxids = ["0000000000000000000000000000000000000000000000000000000000000000"] + wtxids

    wit_roothash = merkelroot.merkle(wtxids)

    return bytes.fromhex(wit_roothash)[::-1].hex()

# Function to create the Witness Commitment through the witness Roothash and witness reserved value. 

def wtxid_commitment(wit_roothash,wit_reserved_value):

    message = wit_roothash + wit_reserved_value

    message = bytes.fromhex(message)

    wtxid_commit = op_codes.double_sha256(message)

    return wtxid_commit.hex()

# Function to create Wtxid from Jsons.

def extract_wtxids_from_folder(folder_path):
    txids = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)
                if(data["vin"][0]["prevout"]["scriptpubkey_type"] == "p2pkh"):
                    txid = txid_hashes.transaction_header_p2pkh(data)
                    if txid:
                        txids.append(txid)
                elif(data["vin"][0]["prevout"]["scriptpubkey_type"] == "v0_p2wpkh"):
                    txid = wtxid_p2wpkh(data)
                    if txid:
                        txids.append(txid)
    return txids

# Function to create Wtxid from Jsons.

def wtxid_p2wpkh(data):
    message = ''

    version = data['version']

    if(version == 1):
        version = "01000000"
    else :
        version = "02000000"

    message += version

    message += "00" 

    message += "01" 

    message += compactSize.compact_size_calculator(len(data['vin']))

    for vin in data['vin']:
        big_endian_txid = vin['txid']
        little_endian_txid = ''.join(reversed([big_endian_txid[i:i+2] for i in range(0, len(big_endian_txid), 2)]))

        message += little_endian_txid

        vout = vin["vout"]
        vout_bytes = struct.pack('<I', int(vout))
        message += vout_bytes.hex()

        message += "00" 
        
        message += "" 
        sequence = vin["sequence"]
        sequence_bytes = struct.pack('<I', sequence).hex()
        message += sequence_bytes

    message += compactSize.compact_size_calculator(len(data['vout']))

    for vout in data['vout']:
        message += struct.pack('<Q', vout['value']).hex()
        size_pubkey = len(vout["scriptpubkey"])
        message += compactSize.compact_size_calculator(int(size_pubkey/2))
        message += vout["scriptpubkey"]

    for vin in data['vin']:
        message += "02"
        size_sigscript = len(vin["witness"][0])
        message += compactSize.compact_size_calculator(int(size_sigscript/2))
        message  += vin["witness"][0]
        size_pubkey_out = len(vin["witness"][1])
        message += compactSize.compact_size_calculator(int(size_pubkey_out/2))
        message += vin["witness"][1]
    
    locktime = struct.pack('<I', int(data["locktime"])).hex()

    message += locktime

    message_hash = op_codes.double_sha256(bytes.fromhex(message))

    return message_hash[::-1].hex()


