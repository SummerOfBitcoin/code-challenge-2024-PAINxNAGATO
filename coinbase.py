import os
import json
import struct

version = "01000000"

marker =  "00"

flag = "01"

inputcount = "01"

txid = "0000000000000000000000000000000000000000000000000000000000000000"

vout = "ffffffff"

scriptsigsize = "1b"

scriptsig = "0300000004f15ccf5609013803062b9b5a0100072f425443432f20"

sequence = "ffffffff"

outputcount = "01"

# amount = "will look later"

scriptpubkeysize = "19"

scriptpubkey = "76a914e1b3cbb1e09432b44976c49e979dbf0d07b0c0a488ac"

locktime = "00000000"

amount_newblock = 625000000

def calculate_sum_of_differences(folder_path):
    differences = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)
                vin_sum = sum([vin['prevout']['value'] for vin in data['vin']])
                vout_sum = sum([vout['value'] for vout in data['vout']])
                difference = vin_sum - vout_sum
                differences.append(difference)
    return sum(differences)

# Example usage:
# folder_path = "verified_transactions"

# sum_of_differences = calculate_sum_of_differences(folder_path)

# block_fees = amount_newblock + sum_of_differences

# bf_hex = struct.pack('<Q', block_fees).hex()

# print(bf_hex)

def coinbase_tx(folder_path):
    sum_of_differences = calculate_sum_of_differences(folder_path)

    block_fees = amount_newblock + sum_of_differences

    bf_hex = struct.pack('<Q', block_fees).hex()

    message = version + marker + flag + inputcount + txid + vout + scriptsigsize + scriptsig + sequence + outputcount + bf_hex + scriptpubkeysize + scriptpubkey + locktime

    # print(message)

    return message

# coinbase_tx()
def extract_txids_from_folder(folder_path):
    txids = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)
                vin = data.get('vin', [])
                for item in vin:
                    txid = item.get('txid')
                    if txid:
                        txids.append(txid)
    return txids

# print(extract_txids_from_folder(folder_path))

