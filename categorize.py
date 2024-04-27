import os
import json
import shutil

# 

def p2wpkh_single(input_folder, output_folder):

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
                if len(data.get("vin", [])) == 1 and data.get("vin")[0].get("prevout", {}).get("scriptpubkey_type") == "v0_p2wpkh":
                    # Copy the file to the output folder
                    shutil.copyfile(input_file_path, os.path.join(output_folder, filename))

    # print("Files copied to 'p2wpkh_one' folder.")

def merge_folders(source_folder1, source_folder2, destination_folder):
    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Iterate through the contents of source_folder1
    for item in os.listdir(source_folder1):
        source_item = os.path.join(source_folder1, item)
        destination_item = os.path.join(destination_folder, item)
        
        # Copy each item from source_folder1 to the destination folder
        if os.path.isdir(source_item):
            shutil.copytree(source_item, destination_item)
        else:
            shutil.copy2(source_item, destination_item)

    # Iterate through the contents of source_folder2
    for item in os.listdir(source_folder2):
        source_item = os.path.join(source_folder2, item)
        destination_item = os.path.join(destination_folder, item)
        
        # Copy each item from source_folder2 to the destination folder
        if os.path.isdir(source_item):
            shutil.copytree(source_item, destination_item)
        else:
            shutil.copy2(source_item, destination_item)


# input_folder = "mempool"
# output_folder = "p2wpkh_one"

# p2wpkh_single(input_folder,output_folder)