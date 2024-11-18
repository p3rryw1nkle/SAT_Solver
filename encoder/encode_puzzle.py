
class PuzzleEncoder():
    def __init__(self, input_file, dimension):
        self.input_file = input_file
        self.dimension = dimension
        self.puzzle_rules = []
        with open(f"rules/sudoku-rules-{dimension}x{dimension}.txt", "r") as f:
            self.puzzle_rules = f.readlines()[1::]

    def encode_sudoku_line(self, line, file_index):
        clauses = []
        n = self.dimension # nxn Sudoku
        for i, char in enumerate(line.strip()):
            if char.isdigit():  # Only process known digits
                row = i // n + 1
                col = i % n + 1
                value = char
                # Construct the clause in the form "rowcolvalue 0"
                clause = f"{row}{col}{value} 0"
                clauses.append(clause)
        
        # Write the clauses to a file
        with open(f"test_sets/encoded/{n}x{n}_sudokus/{self.input_file.replace(".txt", "")}_sudoku_{file_index}.txt", "w") as f:
            f.write("\n".join(clauses) + "\n")
            f.write("".join(self.puzzle_rules))

    def process_sudoku_file(self):
        with open(f"test_sets/unencoded/{self.input_file}", "r") as f:
            lines = f.readlines()
        
        for index, line in enumerate(lines):
            self.encode_sudoku_line(line, index + 1)


if __name__ == "__main__":
    encoder = PuzzleEncoder(input_file="9set.txt", dimension=9)
    encoder.process_sudoku_file()