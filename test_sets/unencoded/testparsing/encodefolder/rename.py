import os

def rename_files_in_folder(folder_path):
    # List and sort files in the folder to ensure correct ordering
    files = sorted([f for f in os.listdir(folder_path) if f.endswith('.txt_encoded.txt')])
    
    # Rename each file in the specified format
    for i, filename in enumerate(files, start=1):
        old_path = os.path.join(folder_path, filename)
        new_filename = f"sudoku_4x4_{i}.txt"
        new_path = os.path.join(folder_path, new_filename)
        
        # Rename the file
        os.rename(old_path, new_path)
        print(f"Renamed '{filename}' to '{new_filename}'")

# Usage
folder_path = "./"  # Replace with the actual path
rename_files_in_folder(folder_path)
