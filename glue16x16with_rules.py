import os
import shutil

# Define paths for the folders and files
file1_path = 'C:/Users/Vasja/Desktop/group24SATsolver/SAT_Solver/rules/sudoku-rules-16x16.txt'  # The first file that stays the same
input_folder = 'C:/Users/Vasja/Desktop/group24SATsolver/SAT_Solver/16x16_encoded_files_only10'  # Folder containing all second files (file2)
output_folder = 'C:/Users/Vasja/Desktop/group24SATsolver/SAT_Solver/16x16_encoded_concatenated'  # Folder to save the new concatenated files

# Ensure the output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Iterate through all files in the input folder
for file_name in os.listdir(input_folder):
    file2_path = os.path.join(input_folder, file_name)  # Full path to the current file2
    output_file_path = os.path.join(output_folder, file_name)  # Path for the output file

    # Skip directories, only process files
    if os.path.isdir(file2_path):
        continue

    # Open the first file in read mode and the current file2 in read mode
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        # Read the contents of both files
        file1_contents = file1.read()
        file2_contents = file2.read()

        # Concatenate the contents
        concatenated_contents = file1_contents + file2_contents

    # Write the concatenated content to a new file in the output folder
    with open(output_file_path, 'w') as output_file:
        output_file.write(concatenated_contents)

    print(f"File '{file_name}' has been processed and saved to '{output_file_path}'.")

print("All files have been processed and saved.")
