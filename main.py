# important imports

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
# Fucntion defination :
#---------------------------------------------------------------------#

def execute_script_p2pkh(evaluate, stack, data,l):
    global c
    tokens = evaluate.split(" ")
    stack = []
    is_valid = True
    i = 0
    while i < len(tokens):
        op = tokens[i]
        
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

# stack generator for scripts 

def stack_evalute(data):
  l = 1
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

# parse json into the evaluator from the directories .

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
            json_str = json.dumps(data)
            data_size = len(json_str.encode('utf-8'))
            if(data_size != 94429):
                result = stack_evalute(data)
                
                if(result):
                    cnt_valid += 1
                    verified_filepath = os.path.join(verified_folder, filename)
                    shutil.copy(filepath, verified_filepath)
                    
    return cnt_valid

# function to generate the ouput.txt for final evaluation. 

def write_to_txt(block_header, coinbase_txn, txid_list, output_file):
    with open(output_file, 'w') as file:
        file.write(block_header + '\n')
        
        file.write(coinbase_txn)
        
        for txid in txid_list:
            file.write('\n' + txid)

# To reverse the bytes for representational purposes.

def reverse_byte_order(txid):
    return txid[::-1]

#--------------------------------------------------------------------------#

input_folder = "mempool"

output_folder_p2pkh = "categorized_scripts/p2pkh"

output_folder_p2wpkh = "categorized_scripts/v0_p2wpkh"

output_merged = "merged_folder"

UniqueScript.filter_transactions(input_folder, output_folder_p2pkh)

categorize.p2wpkh_single(input_folder,output_folder_p2wpkh)

categorize.merge_folders(output_folder_p2pkh,output_folder_p2wpkh,output_merged)

valid_count = parse_json_files_in_folder(output_merged)

block_header = mine_sob.mining()

coinbase_hash = coinbase.coinbase_tx("verified_transactions")

txid_list = txid_hashes.extract_txids_from_folder("verified_transactions")

txid_list = ["0000000000000000000000000000000000000000000000000000000000000000"] + txid_list

output_file = "output.txt"

write_to_txt(block_header, coinbase_hash, txid_list, output_file)