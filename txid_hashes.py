import struct
import op_codes
import json
import os
import compactSize

# json_
def transaction_header_p2pkh(data):

    message = ''

    version = data['version']

    if(version == 1):
        version = "01000000"
    else :
        version = "02000000"

    message += version

    # compact size 
    message += compactSize.compact_size_calculator(len(data['vin']))
    # message += "{:02d}".format(len(data['vin']))

    for vin in data['vin']:
        big_endian_txid = vin['txid']
        little_endian_txid = ''.join(reversed([big_endian_txid[i:i+2] for i in range(0, len(big_endian_txid), 2)]))

        message += little_endian_txid

        vout = vin["vout"]
        vout_bytes = struct.pack('<I', int(vout))
        message += vout_bytes.hex()

        length_pubkey = len(vin["scriptsig"])
        # message += hex(int(length_pubkey/2))[2:]
        message += compactSize.compact_size_calculator(int(length_pubkey/2))
        message += vin["scriptsig"]
        sequence = vin["sequence"]
        sequence_bytes = struct.pack('<I', sequence).hex()
        message += sequence_bytes
        # print(sequence_bytes)
    
# vout
    # compact size
    message += compactSize.compact_size_calculator(len(data['vout']))
    # message += "{:02d}".format(len(data['vout']))

    for vout in data['vout']:
        # print(struct.pack('<Q', vout['value']).hex())
        message += struct.pack('<Q', vout['value']).hex()
        size_pubkey = len(vout["scriptpubkey"])
        # message += hex(int(size_pubkey/2))[2:]
        message += compactSize.compact_size_calculator(int(size_pubkey/2))
        message += vout["scriptpubkey"]

    locktime = struct.pack('<I', int(data["locktime"])).hex()

    # print(locktime)

    message += locktime

    # return message

    message_hash = op_codes.double_sha256(bytes.fromhex(message))

    return message_hash[::-1].hex()

def extract_txids_from_folder(folder_path):
    txids = []
    # print(os.listdir(folder_path))
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
                    # print(file)
                    txid = transaction_header_p2wpkh(data)
                    if txid:
                        txids.append(txid)
    return txids

def transaction_header_p2wpkh(data):

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

        # length_pubkey = len(vin["scriptsig"])
        # message += hex(int(length_pubkey/2))[2:]
        message += "00" # scriptsig_size
        # message += vin["scriptsig"]
        message += "" # sciprtsig
        sequence = vin["sequence"]
        sequence_bytes = struct.pack('<I', sequence).hex()
        message += sequence_bytes
        # print(sequence_bytes)


    
# vout
    # compact size
    message += compactSize.compact_size_calculator(len(data['vout']))
    # message += "{:02d}".format(len(data['vout']))

    # print("{:02d}".format(len(data['vout'])))

    for vout in data['vout']:
        # print(struct.pack('<Q', vout['value']).hex())
        message += struct.pack('<Q', vout['value']).hex()
        size_pubkey = len(vout["scriptpubkey"])
        message += compactSize.compact_size_calculator(int(size_pubkey/2))
        # message += hex(int(size_pubkey/2))[2:]
        message += vout["scriptpubkey"]

    # for vin in data['vin']:
    #     message += "02"

    #     size_sigscript = len(vin["witness"][0])

    #     message += hex(int(size_sigscript/2))[2:]

    #     message  += vin["witness"][0]

    #     size_pubkey_out = len(vin["witness"][1])

    #     message  += hex(int(size_pubkey_out/2))[2:]

    #     message += vin["witness"][1]
    

    locktime = struct.pack('<I', int(data["locktime"])).hex()

    # print(locktime)

    message += locktime

    # print(message)

    message_hash = op_codes.double_sha256(bytes.fromhex(message))

    return message_hash[::-1].hex()

# def extract_txids_from_folder(folder_path):
#     txids = []
#     for filename in os.listdir(folder_path):
#         if filename.endswith('.json'):
#             filepath = os.path.join(folder_path, filename)
#             with open(filepath, 'r') as file:
#                 data = json.load(file)
#                 txid = transaction_header(data)
#                 if txid:
#                     txids.append(txid)
#                 # vin = data.get('vin', [])
#                 # for item in vin:
#                 #     txid = item.get('txid')
#                 #     if txid:
#                 #         txids.append(txid)
#     return txids'

# def extract_txids_from_folder(folder_path):
#     txids = []
#     # print(os.listdir(folder_path))
#     for filename in os.listdir(folder_path):
#         if filename.endswith('.json'):
#             filepath = os.path.join(folder_path, filename)
#             with open(filepath, 'r') as file:
#                 data = json.load(file)
#                 txid = transaction_header(data)
#                 if txid:
#                     txids.append(txid)
#                 # vin = data.get('vin', [])
#                 # for item in vin:
#                 #     txid = item.get('txid')
#                 #     if txid:
#                 #         txids.append(txid)
#     return txids


#02000000014f7efa32f4cb24fdd1334af21de6e6bf8d3f39e1fc4bf415ba88fbe05775453c0100000000fdffffff02011c0000000000001600146ede86efa7b4f5beae851ebff27bdf96a0733d4de02d0700000000001600143a6fd353ebcb81b6729bbd64354bb651ab0826a000000000

#02000000013a53de6e1fe821452674c5435e3989eecdf35cb1de1c8bafb674f543a55d658c3600000000fdffffff01599aea0400000000160014cfbd92a6337e8b6043552d6fc5c35c7e5062281e00000000