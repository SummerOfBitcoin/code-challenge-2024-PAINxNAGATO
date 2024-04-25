import json
import os
import op_codes
import shutil
import coinbase
import mine_sob
import UniqueScript
import txid_hashes
import v0_p2wpkh
import categorize

#---------------------------------------------------------------------#
# fucntion defination :
#---------------------------------------------------------------------#
def execute_script_p2pkh(evaluate, stack, data,l):
    global c
    tokens = evaluate.split(" ")
    stack = []
    is_valid = True
    # Initialize a pointer to move through the tokens
    i = 0
    while i < len(tokens):
        op = tokens[i]
        # Check which operation and handle accordingly
        if op.startswith("OP_PUSHBYTES_"):
            stack, i = op_codes.op_pushbytes_(op,tokens,stack,i)
        elif op == "OP_DUP":
            stack = op_codes.op_dup(stack)
        elif op == "OP_HASH160":
            stack = op_codes.op_hash160(stack)
        elif op == "OP_EQUALVERIFY":
            is_valid, stack = op_codes.op_equalverify(stack)
        elif op == "OP_CHECKSIG":
            is_valid = op_codes.op_checksig(stack,data,l)
        else:
            is_valid = False
        
        i += 1

    return is_valid

# stack function
def stack_evalute(data):
  l = 1
#   script_result = True
  for vin in data['vin']:
    if vin["prevout"]["scriptpubkey_type"] == "p2pkh":
      evaluate = ''
      scriptsig_asm = vin.get('scriptsig_asm', '')
      scriptpubkey_asm = vin['prevout'].get('scriptpubkey_asm', '') if 'prevout' in vin else ''
      evaluate = scriptsig_asm + ' ' + scriptpubkey_asm
      stack = []
      if(not execute_script_p2pkh(evaluate,stack,data,l)):
         return False
      l+= 1
    elif vin["prevout"]["scriptpubkey_type"] == "v0_p2wpkh":
       scriptsig = vin["witness"][0]
       pubkey = vin["witness"][1]
       pubkey_hash = vin["prevout"]["scriptpubkey"][4:]
       if(not v0_p2wpkh.execute_script_V0p2wpkh(data,scriptsig,pubkey,pubkey_hash)):
          return False
  return True

# parse json
def parse_json_files_in_folder(folder_path):
    # c = 0
    cnt_valid = 0
    verified_folder = "verified_transactions"
    if not os.path.exists(verified_folder):
        os.makedirs(verified_folder)   
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
          filepath = os.path.join(folder_path, filename)
          with open(filepath, 'r') as file:
            data = json.load(file)
            # print(file)
            result = stack_evalute(data)
            # print(result)
            if(result):
               cnt_valid += 1
               verified_filepath = os.path.join(verified_folder, filename)
               shutil.copy(filepath, verified_filepath)
            # else :
            #    print(file)
            #    verified_filepath = os.path.join(verified_folder, filename)
            #    with open(verified_filepath, 'w') as verified_file:
            #       json.dump(data, verified_file)
    return cnt_valid

def write_to_txt(block_header, coinbase_txn, txid_list, output_file):
    with open(output_file, 'w') as file:
        # Write block header on the first row
        file.write(block_header + '\n')
        
        # Write coinbase transaction hash on input_folder = "mempool"
# output_folder = "categorized_scripts/p2pkh"the second row
        file.write(coinbase_txn)
        
        # Write txids on subsequent rows
        for txid in txid_list:
            file.write('\n' + txid)

# def reverse_byte_order(txid):
#     # Assuming txid is a hexadecimal string
#     return txid[::-1]

input_folder = "mempool"

output_folder_p2pkh = "categorized_scripts/p2pkh"

output_folder_p2wpkh = "categorized_scripts/v0_p2wpkh"

output_merged = "merged_folder"

UniqueScript.filter_transactions(input_folder, output_folder_p2pkh)

categorize.p2wpkh_single(input_folder,output_folder_p2wpkh)

categorize.merge_folders(output_folder_p2pkh,output_folder_p2wpkh,output_merged)

valid_count = parse_json_files_in_folder(output_merged)

# valid_count = parse_json_files_in_folder(output_folder_p2wpkh)

print(f"{valid_count}")



# print(coinbase_hash)

block_header = mine_sob.mining()

coinbase_hash = coinbase.coinbase_tx("verified_transactions")

txid_list = txid_hashes.extract_txids_from_folder("verified_transactions")

txid_list = ["0000000000000000000000000000000000000000000000000000000000000000"] + txid_list

# txid_list_reversed = [reverse_byte_order(txid) for txid in txid_list]

# print(txid_list_reversed)

# print(len(txid_list))

# Output file path
output_file = "output.txt"

# Write data to output file
write_to_txt(block_header, coinbase_hash, txid_list, output_file)