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

        clauses = set()
        all_literals = set()

        with open(input_file, "r") as f:
            for line in f:
                if line.startswith("p"):
                    continue
                # remove trailing zero
                line = line.replace('0\n', '')
                line = line.strip()
                literals = line.split(' ')
                clause = tuple(literals)
                for literal in literals:
                    literal = literal.replace('-', '')
                    all_literals.add(literal)
                if len(clause) == 0:
                    continue
                clauses.add(clause)

        self.puzzle_dimension = round(len(all_literals)**(1/3))
        print(f"Puzzle dimension: {self.puzzle_dimension}")

        return clauses, all_literals

    @staticmethod
    def rev_literal(literal):
        """
        Reverse a literal so it returns its opposite
        """
        if '-' in literal:
            return literal.replace('-','')
        else:
            return f"-{literal}"


    def solve_dpll(self):
        '''
        Implement the DPLL algorithm
        '''
        def recursive_solve(partial_assignment, clauses):
            
            # if all clauses have been solved
            if len(clauses) == 0:
                self.solution = partial_assignment
                return True
            
            # make a copy so we can modify clauses while we iterate through
            cur_clauses = clauses.copy()

            # we will know what literals are pure after we have iterated through all of the clauses
            pure_literals = {}

            for clause in clauses:
                # if there is an empty clause, the formula is false so return false
                if len(clause) == 0:
                    return False
                
                # if it is a unit clause
                if len(clause) == 1:

                    # add literal to partial assigment
                    (lit,) = clause

                    # stripped literal
                    strp_lit = lit.replace('-','')

                    # assign the literal its appropriate value
                    if '-' in lit:
                        partial_assignment[strp_lit] = False
                    else:
                        partial_assignment[strp_lit] = True

                    # we can remove this clause since it is a unit clause          
                    cur_clauses.remove(clause)
                    return recursive_solve(partial_assignment.copy(), cur_clauses.copy())     

                # if it's not a unit clause or the empty clause, we will iterate through each literal
                # we may remove false literals from the clause as we go, so we create a new_clause variable
                new_clause = list(clause)
                clause_satisfied = False

                # go through each literal in each clause
                for literal in clause:
                    # stripped literal
                    strp_lit = literal.replace('-', '')

                    # reversed literal
                    rev_lit = self.rev_literal(literal)

                    # if the opposite literal is also in the clause, then this clause is a tautology and we can remove it
                    if (literal in clause) and (rev_lit in clause):
                        if clause in cur_clauses:
                            cur_clauses.remove(clause)
                        return recursive_solve(partial_assignment.copy(), cur_clauses.copy())

                    if strp_lit in partial_assignment:
                        # if the literal in the clause matches its assignment
                        if (('-' in literal) and partial_assignment[strp_lit] == False) or \
                            (('-' not in literal) and partial_assignment[strp_lit] == True):

                            clause_satisfied = True
                            # this clause is satisfied, we can remove it
                            if clause in cur_clauses:
                                cur_clauses.remove(clause)  
                        else:
                            lit_val = False
                            if "-" not in literal:
                                lit_val = True

                            assert partial_assignment[strp_lit] != lit_val

                            print(f"Removing literal {literal} from clause {clause}")
                            # shorten clause (literal is false so we only care about the rest of the clause)
                            new_clause.remove(literal)
                
                new_clause = tuple(new_clause)

                if new_clause != clause and not clause_satisfied:
                    # print(f"Shortening old clause: {clause} to new clause: {new_clause}")
                    cur_clauses.remove(clause)
                    cur_clauses.add(tuple(new_clause))

            pure_literals = {}

            for clause in clauses:
                for literal in clause:
                    # if the literal has already been assigned, its purity in the remaining clauses is irrelevant
                    if literal not in partial_assignment:
                        # reverse literal
                        rev_lit = self.rev_literal(literal)

                        if literal not in pure_literals:
                            pure_literals[literal] = True
                        # otherwise if both the literal and its negation are in the remaining clauses, set both purities to false
                        if (literal in pure_literals) and (rev_lit in pure_literals):
                            pure_literals[literal] = False
                            pure_literals[rev_lit] = False

            # add all pure literals to partial_assignment
            for literal in pure_literals:
                strp_lit = literal.replace('-','')
                if pure_literals[literal] == True and (strp_lit not in partial_assignment):
                    rev_lit = self.rev_literal(literal)
                    
                    for clause in clauses:
                        if rev_lit in clause:
                            raise Exception("Literal is not actually pure!")

                    if "-" in literal:
                        partial_assignment[strp_lit] = False
                    else:                    
                        partial_assignment[strp_lit] = True

            assigned_literals = set(partial_assignment.keys())
            unassigned_literals = self.all_literals.difference(assigned_literals)

            # if there are no more literals to assign
            if len(unassigned_literals) == 0:
                # this should return True
                return recursive_solve(partial_assignment.copy(), cur_clauses.copy())

            # get the next literal from unassigned literals
            next_literal = sorted(unassigned_literals).pop(0)

            partial_assignment[next_literal] = False
            if recursive_solve(partial_assignment.copy(), cur_clauses.copy()):
                return True
            else:
                # try true value next
                partial_assignment[next_literal] = True
                return recursive_solve(partial_assignment.copy(), cur_clauses.copy())

        return recursive_solve({}, self.clauses.copy())
    

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
                if self.solution[assignment] == False:
                    continue
                    f.write(f"-{assignment} 0\n")
                else:
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