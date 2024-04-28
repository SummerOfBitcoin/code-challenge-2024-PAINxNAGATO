# Solution for Assignment

## Assignment Flowchart
The design approach involves several key steps to construct a valid block from the transactions in the mempool. The overview of the Whole Assignemnt Created :

1. **Filtering Transactions**: The program filters transactions based on their script type, segregating them into separate folders for P2PKH and P2WPKH scripts.

2. **Script Evaluation**: Transaction scripts are verfied for validity, ensuring that they are in accordance with the specified script format and  signature verification holds.

3. **Transaction Header Generation**: Transaction headers are generated for both P2PKH and P2WPKH transaction types, facilitating Merkle root hash computation for the block as an whole.

4. **Merkle Root Calculation**: The Merkle root hash is computed from the list of transaction hashes in the "verified_transactions" folder.

5. **Coinbase Transaction Creation**: The Coinbase transaction, including the mining fees and witness commitment, is generated as the first transaction in the valid block.

6. **Mining**: A simple mining algorithm is employed to find a valid block header given the current block data with the provided difficukty target of `0000ffff00000000000000000000000000000000000000000000000000000000`.

7. **Block Header Creation**: The block header is constructed using the mined nonce, previous block header, Merkel Root and Mining Time.

8. **Valid Block Creation**: The valid block, containing the valid block header, the Coinbase transaction, the coinbase Txid and other verified transactions txids, is created.

9. **Output Generation**: The block header and transaction IDs are written to the output.txt file.

## Implementation Logic
Here's a breakdown of the implementation details for each step:

1. **Filtering Transactions**
    - The `filter_transactions` function reads JSON files from the mempool folder, filters transactions based on their script type, and copies valid transactions to the "verified_transactions" folder.

    - Input: Path to the input folder containing mempool transactions.

    - Output: Path to the output folder for verified transactions.

2. **Script Evaluation**
    - The `op_codes` module contains various opcodes for script verification, such as `hash160`, `double_sha256`, and `serialize_outpoint`.
    - ECDSA signature verification is performed using the `sig_verification` module.

    - Input: Transaction data, script signature, and public key hash.

    - Output: Boolean indicating script validity.

3. **Transaction Header Generation**
    - Functions `transaction_header_p2pkh` and `transaction_header_p2wpkh` generate transaction headers for P2PKH and P2WPKH transactions, respectively.

    - Input: Transaction data.

    - Output: Transaction header hash.

4. **Merkle Root Calculation**
    - The `return_merkelhash` function computes the Merkle root hash from the list of transaction IDs in the "verified_transactions" folder.
    - Input: None.

    - Output: Merkle root hash.


5. **Coinbase Transaction Creation**
    - The `coinbase_tx` function calculates the mining fees and constructs the Coinbase transaction, including the witness commitment.

    - Input: Path to the folder containing verified transactions.

    - Output: Coinbase transaction string.

6. **Mining**
    - The `mining` function implements a simple mining algorithm to find a valid block header given the current block data.

    - Input: None.

    - Output: Valid block header hash.

7. **Block Header Creation**
    - The block header is constructed using the mined nonce, Merkle root hash, and other relevant information.

    - Input: Mined nonce, Merkle root hash, and block data.

    - Output: Block header string.

8. **Valid Block Creation**
    - The valid block is created by combining the block header and the Coinbase transaction with other verified transactions.

    - Input: Block header, Coinbase transaction, and list of transaction IDs.

    - Output: Valid block string.

9. **Output Generation**
    - The block header and transaction IDs are written to the output.txt file.

    - Input: Block header, Coinbase transaction, and list of transaction IDs.

    - Output: Output.txt file containing the block data.

## Results and Performance
The program efficiently constructs valid Bitcoin transactions and blocks, ensuring script execution. Performance may vary depending on the number and complexity of transactions,But the solution tries to tackle all those conditions and creates an valid block with `2746` transactions with a mining fees of `13267862` satoshis excluding the block fees of `6.25` bitcoin with an weight of `2348636`.

## Conclusion
The provided solution offers an implementation for constructing an single block of valid Bitcoin transactions. It demonstrates the process of evaluating transaction scripts, calculating mining fees, computing the Merkle root hash, mining a valid block header, and creating a valid block. 
## References
- Bitcoin Technical Documentation: [learn me a bitcoin](https://learnmeabitcoin.com/)
- Bitcoin Script: [Bitcoin Wiki - Script](https://en.bitcoin.it/wiki/Script)
- ECDSA Python Library: [Python ECDSA Library](https://github.com/warner/python-ecdsa)

