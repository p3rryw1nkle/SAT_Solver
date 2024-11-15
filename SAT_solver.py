import time
import sys
import os

class SATSolver():
    def __init__(self, input_file):
        self.file_name = os.path.basename(input_file)
        self.puzzle_dimension = 1
        self.clauses, self.all_literals = self.read_input(input_file)
        self.solution_folder = f"{self.puzzle_dimension}x{self.puzzle_dimension}"
        self.solution = set()

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
                if len(clause) == 0:
                    continue
                clauses.append(clause)

        self.puzzle_dimension = round(len(all_literals)**(1/3))
        print(f"Puzzle dimension: {self.puzzle_dimension}")

        return clauses, all_literals


    def solve_dpll(self):
        '''
        Implement the DPLL algorithm
        '''
        sorted_literals = sorted(self.all_literals)
        # partial assignment
        pa = set()

        def recursive_solve(partial_assignment, unassigned_literals):
            # for each of the clauses, check to see if it is unsatisfied by partial assigment
            # we know a clause is false when each variable has been assigned, but the clause is still false
            for clause in self.clauses:

                # assume clause is unsatisfied until proven True
                satisfied = False
                
                # how many variables in the clause have been assigned
                assigned = 0

                for variable in clause:
                    ### clause e.g. 122 222 322 422
                    ### so it will iterate through variables 122, 222, 322, and 422

                    # if the variable is in the partial assignment we know this clause is satisfied
                    if variable in partial_assignment:
                        satisfied = True
                    
                    # if the variable is not in the partial assigment, check to see if its inverse is in the PA
                    t_var = variable.replace('-', '')
                    f_var = f"-{t_var}"

                    # if either true or false literal is in the pa, we know this literal has been assigned but clause is not positive (yet)
                    if t_var in partial_assignment or f_var in partial_assignment:
                        assigned += 1

                # if all variables in this clause have been assigned and it is still not satisfied, we know for sure this PA won't work
                if assigned == len(clause) and not satisfied:
                    return False
                
            # if all literals have been assigned and no clauses are unsatisfied, return true
            if len(partial_assignment) == len(self.all_literals):
                self.solution = partial_assignment
                return True
            
            # get this next literal from unassigned literals
            next_literal = unassigned_literals.pop(0)

            # try the false value first
            false_literal = f"-{next_literal}"
            partial_assignment.add(false_literal)
            if recursive_solve(partial_assignment.copy(), unassigned_literals.copy()):
                return True
            else:
                # try true value next
                partial_assignment.remove(false_literal)
                partial_assignment.add(next_literal)
                return recursive_solve(partial_assignment.copy(), unassigned_literals.copy())

        return recursive_solve(pa, sorted_literals)

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

    def write_output(self):
        '''
        Write output to file in DIMAC format
        '''

        with open(f"solutions/{self.solution_folder}/sol_{self.file_name}", "w") as f:
            f.write(f"p {len(self.all_literals)} {len(self.solution)}\n")
            for assignment in sorted(self.solution):
                f.write(f"{assignment} 0\n")


if __name__ == "__main__":
    algo_number = int(sys.argv[1])
    input_file = sys.argv[2]
    solver = SATSolver(input_file)

    start_time = time.time()

    match algo_number:
        case 1:
            solver.solve_dpll()
        case 2:
            solver.solve_heuristic_1()
        case 3:
            solver.solve_heuristic_2()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")

    solver.write_output()

# prioritizing literals by how often we've seen them

# focus on row, columns, and boxes that have the fewest empty variables left
