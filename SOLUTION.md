# Solution for Assignment

## Assignment Flowchart
The design approach involves several important steps to construct a valid block from the transactions jsons in the mempool. The overview of the whole Assignemnt is as follows :

1. **Filtering Transactions**: The program filters transactions based on their script type, separating them into separate folders for `p2pkh` and `p2wpkh` scripts.

2. **Script Evaluation**: Transaction jsons are verfied for validity, ensuring that the proper script format and  signature verification holds.

3. **Transaction Header Generation**: Transaction headers are generated for both `p2pkh` and `p2wpkh`.

4. **Merkle Root Calculation**: The Merkle root hash is generated from the list of Txids of the `verified` transaction jsons.

5. **Coinbase Transaction Creation**: The Coinbase transaction, including the mining fees and witness commitment, is generated as the first transaction in the valid block.

6. **Mining**: An mining algorithm is used to find a valid block header given the current block data with the provided difficulty target of `0000ffff00000000000000000000000000000000000000000000000000000000`.

7. **Block Header Creation**: The block header is constructed using the mined nonce, previous block header, Merkel Root and Mining Time.

8. **Valid Block Creation**: The valid block, containing the valid block header, the Coinbase transaction, the coinbase TxID and other verified transactions TxIDs, is created.

9. **Output Generation**: The block header, the coinbase transactions and  TxIDs of verified transactions are written to the output.txt file.

## Implementation Details
The implementation details for each step is given as follows:

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
    - Functions `transaction_header_p2pkh` and `transaction_header_p2wpkh` generate transaction headers for `p2pkh` and `p2wpkh` transactions, respectively.

    - Input: Transaction data.

    - Output: Transaction header hash.

4. **Merkle Root Calculation**
    - The `return_merkelhash` function computes the Merkle root hash from the list of transaction IDs in the "verified_transactions" folder.
    - Input: Valid TxIDs.

    - Output: Merkle root hash.


5. **Coinbase Transaction Creation**
    - The `coinbase_tx` function calculates the mining fees and constructs the Coinbase transaction, including the witness commitment.

    - Input: Path to the folder containing verified transactions.

    - Output: Coinbase transaction.

6. **Mining**
    - The `mining` function implements an mining algorithm to find a valid block header given the current block data.

    - Input: Previous block header, merkel root hash, nonce, Unix time.

    - Output: Valid block header hash.

7. **Block Header Creation**
    - The block header is constructed using the mined nonce, merkle root hash, and other relevant information.

    - Input: mined nonce, merkle root hash, and block data.

    - Output: Block header.

8. **Valid Block Creation**
    - The valid block is created by combining the block header and the Coinbase transaction with other verified transactions.

    - Input: Block header, Coinbase transaction, and list of TxIDs.

    - Output: Valid block.

9. **Output Generation**
    - The block header, the coinbase transactions and TxIDs are written to the output.txt file.

    - Input: Block header, Coinbase transaction, coinbase Txid and list of TxIDs.

    - Output: Output.txt file.

## Results and Performance
The program constructs valid Bitcoin transactions and blocks. Performance may vary depending on the number and complexity of transactions,But the solution tries to tackle all those conditions and creates an valid block with `2746` transactions with a mining fees of `13267862` satoshis excluding the block fees of `6.25` bitcoin with an weight of `2348636`.

## Conclusion
The provided solution outlines an implementation for constructing a single block of valid Bitcoin transactions. It demonstrates the process of evaluating transaction scripts, calculating mining fees, computing the merkle root hash, mining a valid block header, and creating a valid block that is ready to be pushed into the network.
## References
- Bitcoin Technical Documentation: [learn me a bitcoin](https://learnmeabitcoin.com/)
- ECDSA Python Library: [Python ECDSA Library](https://github.com/warner/python-ecdsa)