def encode_sudoku_line(line, file_index):
    clauses = []
    n = 4  # 4x4 Sudoku
    for i, char in enumerate(line.strip()):
        if char.isdigit():  # Only process known digits
            row = i // n + 1
            col = i % n + 1
            value = char
            # Construct the clause in the form "rowcolvalue 0"
            clause = f"{row}{col}{value} 0"
            clauses.append(clause)
    
    # Write the clauses to a file
    with open(f"sudoku_{file_index}.txt", "w") as f:
        f.write("\n".join(clauses) + "\n")

def process_sudoku_file(input_file):
    with open(input_file, "r") as f:
        lines = f.readlines()
    
    for index, line in enumerate(lines):
        encode_sudoku_line(line, index + 1)

# Process the provided file
process_sudoku_file("smallset.txt")
