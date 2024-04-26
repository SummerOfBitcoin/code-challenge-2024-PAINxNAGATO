import os
import json
import shutil
import op_codes

def p2sh(input_folder, output_folder):
    # input_folder = "categorized_scripts/v0_p2wpkh"
    # output_folder = "p2wpkh_one"

    # Ensure the output folder exists or create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through each JSON file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            input_file_path = os.path.join(input_folder, filename)
            
            # Open and load JSON data
            with open(input_file_path, "r") as f:
                data = json.load(f)
                
                # Check if there's only one input in "vin" array and its hash script type is "p2wpkh"
                if len(data.get("vin", [])) == 1 and data.get("vin")[0].get("prevout", {}).get("scriptpubkey_type") == "p2sh":
                    # Copy the file to the output folder
                    shutil.copyfile(input_file_path, os.path.join(output_folder, filename))

    print("Files copied to 'p2wpkh_one' folder.")

p2sh("mempool","p2sh")

# json_data = '''
# {
#   "version": 2,
#   "locktime": 834458,
#   "vin": [
#     {
#       "txid": "26add75d9ce9fc37214345e3239dc2cbd5bfa249b2848ade0e1e92d310f16844",
#       "vout": 0,
#       "prevout": {
#         "scriptpubkey": "a914b6bb3d1ec1f6610ba14865e73436b5e139fb385187",
#         "scriptpubkey_asm": "OP_HASH160 OP_PUSHBYTES_20 b6bb3d1ec1f6610ba14865e73436b5e139fb3851 OP_EQUAL",
#         "scriptpubkey_type": "p2sh",
#         "scriptpubkey_address": "3JMDD2tTHi8PSnqZ4Py9pQ89WzJMWrCz5r",
#         "value": 261468834
#       },
#       "scriptsig": "160014f62420cb38636c38450ec0b3525f54e21f040c3f",
#       "scriptsig_asm": "OP_PUSHBYTES_22 0014f62420cb38636c38450ec0b3525f54e21f040c3f",
#       "witness": [
#         "304402200145213cacd9de8335be935688cc7e4e5003d401d19019570be139b51a8ca86a02206c6f87bc806de4811abfe211394d8af727e005fb1f5871456415b8afb321dd1701",
#         "02959aad959e4d4a101ff592d85fba749cd0c5dd5f8bf531d67b866d7267197169"
#       ],
#       "is_coinbase": false,
#       "sequence": 4294967293,
#       "inner_redeemscript_asm": "OP_0 OP_PUSHBYTES_20 f62420cb38636c38450ec0b3525f54e21f040c3f"
#     }
#   ],
#   "vout": [
#     {
#       "scriptpubkey": "a914169e3805cbc3d49689bf953075f40fde3f9040ff87",
#       "scriptpubkey_asm": "OP_HASH160 OP_PUSHBYTES_20 169e3805cbc3d49689bf953075f40fde3f9040ff OP_EQUAL",
#       "scriptpubkey_type": "p2sh",
#       "scriptpubkey_address": "33kcL13n56JcPQCkAA42TAohAmx3LPJ5LC",
#       "value": 40000000
#     },
#     {
#       "scriptpubkey": "a9142a8e737b02fa9d1321b6a02c0cbb2dbbd955f0fd87",
#       "scriptpubkey_asm": "OP_HASH160 OP_PUSHBYTES_20 2a8e737b02fa9d1321b6a02c0cbb2dbbd955f0fd OP_EQUAL",
#       "scriptpubkey_type": "p2sh",
#       "scriptpubkey_address": "35a2xGyfidMJzwPCBD96RM32Ea2WgTrg3L",
#       "value": 221466494
#     }
#   ]
# }
# '''

# redeem = "00201c9457a046ded217b1773703d1987a8d6e5e1459fad731b205d1678495d8155e"

# redeem_hash = op_codes.hash160(redeem)

# print(redeem_hash)

