import struct
import op_codes
import json
import os

# json_
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
                txid = transaction_header(data)
                if txid:
                    txids.append(txid)
                # vin = data.get('vin', [])
                # for item in vin:
                #     txid = item.get('txid')
                #     if txid:
                #         txids.append(txid)
    return txids

# json_data = '''
# {
#   "version": 2,
#   "locktime": 0,
#   "vin": [
#     {
#       "txid": "fb7fe37919a55dfa45a062f88bd3c7412b54de759115cb58c3b9b46ac5f7c925",
#       "vout": 1,
#       "prevout": {
#         "scriptpubkey": "76a914286eb663201959fb12eff504329080e4c56ae28788ac",
#         "scriptpubkey_asm": "OP_DUP OP_HASH160 OP_PUSHBYTES_20 286eb663201959fb12eff504329080e4c56ae287 OP_EQUALVERIFY OP_CHECKSIG",
#         "scriptpubkey_type": "p2pkh",
#         "scriptpubkey_address": "14gnf7L2DjBYKFuWb6iftBoWE9hmAoFbcF",
#         "value": 433833
#       },
#       "scriptsig": "4830450221008f619822a97841ffd26eee942d41c1c4704022af2dd42600f006336ce686353a0220659476204210b21d605baab00bef7005ff30e878e911dc99413edb6c1e022acd012102c371793f2e19d1652408efef67704a2e9953a43a9dd54360d56fc93277a5667d",
#       "scriptsig_asm": "OP_PUSHBYTES_72 30450221008f619822a97841ffd26eee942d41c1c4704022af2dd42600f006336ce686353a0220659476204210b21d605baab00bef7005ff30e878e911dc99413edb6c1e022acd01 OP_PUSHBYTES_33 02c371793f2e19d1652408efef67704a2e9953a43a9dd54360d56fc93277a5667d",
#       "is_coinbase": false,
#       "sequence": 4294967295
#     }
#   ],
#   "vout": [
#     {
#       "scriptpubkey": "76a9141ef7874d338d24ecf6577e6eadeeee6cd579c67188ac",
#       "scriptpubkey_asm": "OP_DUP OP_HASH160 OP_PUSHBYTES_20 1ef7874d338d24ecf6577e6eadeeee6cd579c671 OP_EQUALVERIFY OP_CHECKSIG",
#       "scriptpubkey_type": "p2pkh",
#       "scriptpubkey_address": "13pjoLcRKqhzPCbJgYW77LSFCcuwmHN2qA",
#       "value": 387156
#     },
#     {
#       "scriptpubkey": "76a9142e391b6c47778d35586b1f4154cbc6b06dc9840c88ac",
#       "scriptpubkey_asm": "OP_DUP OP_HASH160 OP_PUSHBYTES_20 2e391b6c47778d35586b1f4154cbc6b06dc9840c OP_EQUALVERIFY OP_CHECKSIG",
#       "scriptpubkey_type": "p2pkh",
#       "scriptpubkey_address": "15DQVhQ7PU6VPsTtvwLxfDsTP4P6A3Z5vP",
#       "value": 37320
#     }
#   ]
# }
# '''

extract_txids_from_folder("verified_transactions")
# data = json.loads(json_data) 

#020000000125c9f7c56ab4b9c358cb159175de542b41c7d38bf862a045fa5da51979e37ffb010000006b4830450221008f619822a97841ffd26eee942d41c1c4704022af2dd42600f006336ce686353a0220659476204210b21d605baab00bef7005ff30e878e911dc99413edb6c1e022acd012102c371793f2e19d1652408efef67704a2e9953a43a9dd54360d56fc93277a5667dffffffff0254e80500000000001976a9141ef7874d338d24ecf6577e6eadeeee6cd579c67188acc8910000000000001976a9142e391b6c47778d35586b1f4154cbc6b06dc9840c88ac00000000

#020000000125c9f7c56ab4b9c358cb159175de542b41c7d38bf862a045fa5da51979e37ffb010000006b4830450221008f619822a97841ffd26eee942d41c1c4704022af2dd42600f006336ce686353a0220659476204210b21d605baab00bef7005ff30e878e911dc99413edb6c1e022acd012102c371793f2e19d1652408efef67704a2e9953a43a9dd54360d56fc93277a5667dffffffff0254e80500000000001976a9141ef7874d338d24ecf6577e6eadeeee6cd579c67188acc8910000000000001976a9142e391b6c47778d35586b1f4154cbc6b06dc9840c88ac00000000

# print(transaction_header(data)) 

#896aeeb4d8af739da468ad05932455c639073fa3763d3256ff3a2c86122bda4e

#896aeeb4d8af739da468ad05932455c639073fa3763d3256ff3a2c86122bda4e