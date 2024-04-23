import json
import os
import shutil

def filter_transactions(input_folder, output_folder):
    # Ensure the output folder exists or create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through each JSON file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, filename)

            with open(input_file_path, "r") as input_file:
                data = json.load(input_file)

                # Check if all inputs have "scriptpubkey_type": "p2pkh"
                all_p2pkh = all(vin["prevout"]["scriptpubkey_type"] == "p2pkh" for vin in data["vin"])

                if all_p2pkh:
                    # Write the transaction to the output folder
                    shutil.copyfile(input_file_path, output_file_path)

# Define input and output folders
input_folder = "mempool"
output_folder = "categorized_scripts/p2pkh"

# Call the function to filter transactions
# filter_transactions(input_folder, output_folder)
