import sys

class SATSolver():
    def __init__(self, input_file):
        self.clauses, self.all_literals = self.read_input(input_file)

    def read_input(self, input_file):

        '''
        111 112 113 114 115 116 117 118 119  0
        121 122 123 124 125 126 127 128 129  0
        131 132 133 134 135 136 137 138 139  0
        141 142 143 144 145 146 147 148 149  0
        151 152 153 154 155 156 157 158 159  0
                
        '''

        clauses = []
        all_literals = set()

        with open(input_file, "r") as f:
            for line in f:
                if line.startswith("p"):
                    continue
                # remove trailing zero
                line = line.replace('0\n', '')
                line = line.strip()
                literals = line.split(' ')
                clause = set(literals)
                for literal in literals:
                    literal = literal.replace('-', '')
                    all_literals.add(literal)
                clauses.append(clause)


        return clauses, all_literals


    def solve_dpll(self):
        '''
        Implement the DPLL algorithm
        '''
        # partial assignment
        pa = []
        sorted_literals = sorted(self.all_literals)

        def recursive_solve(partial_assignment):
            if len(partial_assignment) == len(self.all_literals):
                return
            
            next = sorted_literals.pop(0)
            recursive_solve(partial_assignment.append(next))
  
        return recursive_solve(pa)

    def solve_heuristic_1(self):
        '''
        Implement first hueristic
        '''
        pass

    def solve_heuristic_2(self):
        '''
        Implement second heuristic
        '''
        pass

    def write_output(seflf):
        '''
        Write output to file in DIMAC format
        '''
        pass

if __name__ == "__main__":
    algo_number = int(sys.argv[1])
    input_file = sys.argv[2]
    solver = SATSolver(input_file)

    match algo_number:
        case 1:
            solver.solve_dpll()
        case 2:
            solver.solve_heuristic_1()
        case 3:
            solver.solve_heuristic_2()

    solver.write_output()