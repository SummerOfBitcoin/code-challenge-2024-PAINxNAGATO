import ecdsa

def ecdsa_check(public_key_hex,signature_hex,message_hex) :
# Convert hex strings to bytes
    signature_hex = signature_hex[:-2]

    public_key_bytes = bytes.fromhex(public_key_hex)
    signature_bytes = bytes.fromhex(signature_hex)
    message_bytes = bytes.fromhex(message_hex)

    try:
        # Create an ECDSA verifier
        vk = ecdsa.VerifyingKey.from_string(public_key_bytes, curve=ecdsa.SECP256k1)

        # Verify the signature
        is_valid = vk.verify_digest(signature_bytes, message_bytes, sigdecode=ecdsa.util.sigdecode_der)
        if is_valid:
            # print("Signature is valid")
            result = True
        else:
            # print("Signature is invalid")
            result = False

    except Exception as e:
        # print("Error occurred during verification:", e)
        result = False

    return result

