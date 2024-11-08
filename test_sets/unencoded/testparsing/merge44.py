import os

def insert_file_after_first_line(first_file_path, folder_path):
    # Read the content of the first file (constant file)
    with open(first_file_path, 'r') as f1:
        first_file_lines = f1.readlines()

    # Ensure the output directory exists
    output_folder = os.path.join(folder_path, "merged_outputs")
    os.makedirs(output_folder, exist_ok=True)

    # Iterate over all text files in the folder (excluding the first file itself)
    for filename in os.listdir(folder_path):
        second_file_path = os.path.join(folder_path, filename)
        
        # Process only text files and skip the primary first file
        if filename.endswith('.txt') and second_file_path != first_file_path:
            # Read the content of the second file
            with open(second_file_path, 'r') as f2:
                second_file_content = f2.readlines()
            
            # Combine the lines: first line of first file, second file content, remaining lines of first file
            merged_content = [first_file_lines[0]] + second_file_content + first_file_lines[1:]
            
            # Create a new output file with "_merged" in the filename
            output_file_path = os.path.join(output_folder, f"{filename}_encoded.txt")
            with open(output_file_path, 'w') as output_file:
                output_file.writelines(merged_content)
    
    print(f"Merged files have been saved in: {output_folder}")

# Example usage
first_file_path = "sudoku-rules-4x4_reordered.txt"  # Replace with the path to the first (constant) file
folder_path = "./encodefolder"  # Replace with the path to the folder containing secondary files

insert_file_after_first_line(first_file_path, folder_path)
