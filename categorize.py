# imports  

import os
import json
import shutil

# Creating an separate folder for p2wpkh transaction json for the purpose of verification and txid or wtxid generation 

def p2wpkh_single(input_folder, output_folder):

    # To Ensure the output directory exists or create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through each JSON file in the mempool directory 
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            input_file_path = os.path.join(input_folder, filename)
            
            with open(input_file_path, "r") as f:
                data = json.load(f)
                
                if len(data.get("vin", [])) == 1 and data.get("vin")[0].get("prevout", {}).get("scriptpubkey_type") == "v0_p2wpkh":
                    shutil.copyfile(input_file_path, os.path.join(output_folder, filename))
                    
# sciprt to merge the two directories together 

def merge_folders(source_folder1, source_folder2, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for item in os.listdir(source_folder1):
        source_item = os.path.join(source_folder1, item)
        destination_item = os.path.join(destination_folder, item)
        
        if os.path.isdir(source_item):
            shutil.copytree(source_item, destination_item)
        else:
            shutil.copy2(source_item, destination_item)

    for item in os.listdir(source_folder2):
        source_item = os.path.join(source_folder2, item)
        destination_item = os.path.join(destination_folder, item)
        
        if os.path.isdir(source_item):
            shutil.copytree(source_item, destination_item)
        else:
            shutil.copy2(source_item, destination_item)

