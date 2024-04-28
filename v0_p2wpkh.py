# important imports. 

import op_codes
import sig_verification

# scipt for p2wpkh transaction json verifcation.

def execute_script_V0p2wpkh(data,scriptsig,pubkey,pubkey_hash):
   
    try_pubkeyhash = op_codes.hash160(pubkey)
    if(try_pubkeyhash == pubkey_hash):
       message = op_codes.message_serilization_p2wpkh(data,scriptsig,pubkey,pubkey_hash)
       is_valid = sig_verification.ecdsa_check(pubkey,scriptsig,message)
       
    else :
       print("dup_wrong")
       is_valid = False
       
    return is_valid
