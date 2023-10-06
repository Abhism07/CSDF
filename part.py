import os
import re

trash_path = "/home/admin1/.local/share/Trash/files"
info_path = "/home/admin1/.local/share/Trash/info"

# List the files in the trash folder
dir_list = os.listdir(trash_path)

# Create a dictionary to store the corresponding info file paths
info_files = {}

for fname in dir_list:
    # Check if the file name matches the input
    if fname.startswith(fname):
        info_file_path = os.path.join(info_path, fname + ".trashinfo")
        if os.path.exists(info_file_path):
            info_files[fname] = info_file_path

# Check if the input file name exists in the info files
if not info_files:
    print("No matching files found in trash.")
else:
    # Print a list of recoverable files
    print("Recoverable files:")
    for fname in info_files.keys():
        print(fname)

    input_fname = input("\nEnter the file name you want to recover: ")

    # Check if the input file name is in the info files
    if input_fname not in info_files:
        print("File not found in trash.")
    else:
        info_file_path = info_files[input_fname]

        with open(info_file_path, "r") as info_file:
            for line in info_file:
                if line.startswith("Path="):
                    dest_path = re.findall(r'Path=(.*)', line)
                    if dest_path:
                        dest_path = dest_path[0]

                        src_file_path = os.path.join(trash_path, input_fname)
                        dest_file_path = os.path.expanduser(dest_path)

                        # Copy the file from trash to the destination
                        try:
                            with open(src_file_path, "rb") as src_file, open(dest_file_path, "wb") as dest_file:
                                dest_file.write(src_file.read())

                            print("File recovered to:", dest_file_path)

                            # Remove the file from trash
                            os.remove(src_file_path)
                            os.remove(info_file_path)
                        except Exception as e:
                            print("Error recovering the file:", str(e))

