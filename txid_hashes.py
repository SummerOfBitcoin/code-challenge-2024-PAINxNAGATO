import struct
import op_codes
import json
import os


def transaction_header(data):

    message = ''

    version = data['version']

    if(version == 1):
        version = "01000000"
    else :
        version = "02000000"

    message += version

    message += "{:02d}".format(len(data['vin']))

    for vin in data['vin']:
        big_endian_txid = vin['txid']
        little_endian_txid = ''.join(reversed([big_endian_txid[i:i+2] for i in range(0, len(big_endian_txid), 2)]))

        message += little_endian_txid

        vout = vin["vout"]
        vout_bytes = struct.pack('<I', int(vout))
        message += vout_bytes.hex()

        length_pubkey = len(vin["scriptsig"])
        message += hex(int(length_pubkey/2))[2:]
        message += vin["scriptsig"]
        sequence = vin["sequence"]
        sequence_bytes = struct.pack('<I', sequence).hex()
        message += sequence_bytes
        # print(sequence_bytes)
    
# vout
    message += "{:02d}".format(len(data['vout']))

    for vout in data['vout']:
        # print(struct.pack('<Q', vout['value']).hex())
        message += struct.pack('<Q', vout['value']).hex()
        size_pubkey = len(vout["scriptpubkey"])
        message += hex(int(size_pubkey/2))[2:]
        message += vout["scriptpubkey"]

    locktime = struct.pack('<I', int(data["locktime"])).hex()

    # print(locktime)

    message += locktime

    # print(message)

    message_hash = op_codes.double_sha256(bytes.fromhex(message))

    return message_hash.hex()

def extract_txids_from_folder(folder_path):
    txids = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)
                txid = transaction_header(data)
                if txid:
                    txids.append(txid)
                # vin = data.get('vin', [])
                # for item in vin:
                #     txid = item.get('txid')
                #     if txid:
                #         txids.append(txid)
    return txids


