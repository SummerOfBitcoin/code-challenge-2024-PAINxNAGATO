import op_codes
import sig_verification
import json 
def execute_script_V0p2wpkh(data,scriptsig,pubkey,pubkey_hash):
   #  is_valid = True
    try_pubkeyhash = op_codes.hash160(pubkey)
    if(try_pubkeyhash == pubkey_hash):
       message = op_codes.message_serilization_p2wpkh(data,scriptsig,pubkey,pubkey_hash)
    #    print(message)
       is_valid = sig_verification.ecdsa_check(pubkey,scriptsig,message)
    #    print(is_valid)
    else :
       print("dup_wrong")
       is_valid = False
    return is_valid

# json_data = '''
# {
#   "version": 1,
#   "locktime": 0,
#   "vin": [
#     {
#       "txid": "3b7dc918e5671037effad7848727da3d3bf302b05f5ded9bec89449460473bbb",
#       "vout": 16,
#       "prevout": {
#         "scriptpubkey": "0014f8d9f2203c6f0773983392a487d45c0c818f9573",
#         "scriptpubkey_asm": "OP_0 OP_PUSHBYTES_20 f8d9f2203c6f0773983392a487d45c0c818f9573",
#         "scriptpubkey_type": "v0_p2wpkh",
#         "scriptpubkey_address": "bc1qlrvlygpudurh8xpnj2jg04zupjqcl9tnk5np40",
#         "value": 37079526
#       },
#       "scriptsig": "",
#       "scriptsig_asm": "",
#       "witness": [
#         "30440220780ad409b4d13eb1882aaf2e7a53a206734aa302279d6859e254a7f0a7633556022011fd0cbdf5d4374513ef60f850b7059c6a093ab9e46beb002505b7cba0623cf301",
#         "022bf8c45da789f695d59f93983c813ec205203056e19ec5d3fbefa809af67e2ec"
#       ],
#       "is_coinbase": false,
#       "sequence": 4294967295
#     }
#   ],
#   "vout": [
#     {
#       "scriptpubkey": "76a9146085312a9c500ff9cc35b571b0a1e5efb7fb9f1688ac",
#       "scriptpubkey_asm": "OP_DUP OP_HASH160 OP_PUSHBYTES_20 6085312a9c500ff9cc35b571b0a1e5efb7fb9f16 OP_EQUALVERIFY OP_CHECKSIG",
#       "scriptpubkey_type": "p2pkh",
#       "scriptpubkey_address": "19oMRmCWMYuhnP5W61ABrjjxHc6RphZh11",
#       "value": 100000
#     },
#     {
#       "scriptpubkey": "0014ad4cc1cc859c57477bf90d0f944360d90a3998bf",
#       "scriptpubkey_asm": "OP_0 OP_PUSHBYTES_20 ad4cc1cc859c57477bf90d0f944360d90a3998bf",
#       "scriptpubkey_type": "v0_p2wpkh",
#       "scriptpubkey_address": "bc1q44xvrny9n3t5w7lep58egsmqmy9rnx9lt6u0tc",
#       "value": 36977942
#     }
#   ]
# }
# '''

# data = json.loads(json_data)

# sigscript = "30440220780ad409b4d13eb1882aaf2e7a53a206734aa302279d6859e254a7f0a7633556022011fd0cbdf5d4374513ef60f850b7059c6a093ab9e46beb002505b7cba0623cf301"

# pubkey = "022bf8c45da789f695d59f93983c813ec205203056e19ec5d3fbefa809af67e2ec"

# pubkeyhash = "f8d9f2203c6f0773983392a487d45c0c818f9573"


# print(execute_script_V0p2wpkh(data,sigscript,pubkey,pubkeyhash))


# #01000000000101bb3b4760944489ec9bed5d5fb002f33b3dda278784d7faef371067e518c97d3b1000000000ffffffff02a0860100000000001976a9146085312a9c500ff9cc35b571b0a1e5efb7fb9f1688ac163d340200000000160014ad4cc1cc859c57477bf90d0f944360d90a3998bf024730440220780ad409b4d13eb1882aaf2e7a53a206734aa302279d6859e254a7f0a7633556022011fd0cbdf5d4374513ef60f850b7059c6a093ab9e46beb002505b7cba0623cf30121022bf8c45da789f695d59f93983c813ec205203056e19ec5d3fbefa809af67e2ec00000000

# # 02473044022008f4f37e2d8f74e18c1b8fde2374d5f28402fb8ab7fd1cc5b786aa40851a70cb022032b1374d1a0f125eae4f69d1bc0b7f896c964cfdba329f38a952426cf427484c012103eed0d937090cae6ffde917de8a80dc6156e30b13edd5e51e2e50d52428da1c87

# # 02473044022008f4f37e2d8f74e18c1b8fde2374d5f28402fb8ab7fd1cc5b786aa40851a70cb022032b1374d1a0f125eae4f69d1bc0b7f896c964cfdba329f38a952426cf427484c012103eed0d937090cae6ffde917de8a80dc6156e30b13edd5e51e2e50d52428da1c87