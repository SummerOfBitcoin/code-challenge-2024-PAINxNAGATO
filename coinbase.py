# important imports  

import os
import json
import struct
import wtxid

# version 

version = "01000000"

# marker and flags

marker =  "00"

flag = "01"

# input count of the coinbase transactions

inputcount = "01"

# Txid of coinbase transaction 

txid = "0000000000000000000000000000000000000000000000000000000000000000"

# vout 

vout = "ffffffff"

# scriptsig for coinbase 

scriptsigsize = "1b"

scriptsig = "0300000004f15ccf5609013803062b9b5a0100072f425443432f20"

sequence = "ffffffff"

outputcount = "02"

scriptpubkeysize = "19"

scriptpubkey = "76a914e1b3cbb1e09432b44976c49e979dbf0d07b0c0a488ac"

amount_output2 = "0000000000000000"

fixed_header = "6a24aa21a9ed"

scriptpubkey_size_2 = "26" 

witness_stackitems = "01"

item_size = "20"

# witness reserved value 

item = "0000000000000000000000000000000000000000000000000000000000000000"

# locktime

locktime = "00000000"

amount_newblock = 625000000

# calculating the mining fees 

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

# function to create the coinbase transaction 

def coinbase_tx(folder_path):
    sum_of_differences = calculate_sum_of_differences(folder_path)

    wit_roothash = wtxid.witness_roothash(folder_path)
    
    # witness commitment 

    wtxid_commit = wtxid.wtxid_commitment(wit_roothash,item)
    
    # mining fees 

    block_fees = amount_newblock + sum_of_differences

    bf_hex = struct.pack('<Q', block_fees).hex()
    
    # coinbase to be added to output.txt

    message = version + marker + flag + inputcount + txid + vout + scriptsigsize + scriptsig + sequence + outputcount + bf_hex + scriptpubkeysize + scriptpubkey + amount_output2 + scriptpubkey_size_2 + fixed_header + wtxid_commit + witness_stackitems + item_size + item + locktime

    return message






