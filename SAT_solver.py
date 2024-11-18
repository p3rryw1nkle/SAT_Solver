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
                    # if the literal has already been assigned, skip over it
                    if literal not in partial_assignment:
                        # reverse literal
                        rev_lit = self.rev_literal(literal)

                        if literal not in pure_literals:
                            pure_literals[literal] = True
                        # if both the literal and its negation are in the remaining clauses, set both purities to false
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
                return recursive_solve(partial_assignment.copy(), cur_clauses.copy())

            # get the next literal from unassigned literals
            next_literal = sorted(unassigned_literals).pop(0)

            partial_assignment[next_literal] = False
            if recursive_solve(partial_assignment.copy(), cur_clauses.copy()):
                return True
            else:
                # try the true value next
                partial_assignment[next_literal] = True
                return recursive_solve(partial_assignment.copy(), cur_clauses.copy())

        return recursive_solve({}, self.clauses.copy())

    def solve_heuristic_1(self):
        """
        Implement first heuristic
        """

        def recursive_solve(partial_assignment, clauses):

            # if all clauses have been solved
            if len(clauses) == 0:
                self.solution = partial_assignment
                return True

            # if there is an empty clause, the formula is false so return false
            for clause in clauses:
                if len(clause) == 0:
                    return False

            # assign values to unit clauses
            unit_clauses = [clause for clause in clauses if len(clause) == 1]
            for unit in unit_clauses:
                (lit,) = unit
                stripped_literal = lit.replace('-', '')
                partial_assignment[stripped_literal] = '-' not in lit
                clauses = simplify_clauses(clauses, partial_assignment)

            # remove pure literals
            literal_counts = {}
            for clause in clauses:
                for literal in clause:
                    literal_counts[literal] = literal_counts.get(literal, 0) + 1

            for literal in list(literal_counts.keys()):
                rev_literal = self.rev_literal(literal)
                if rev_literal not in literal_counts:
                    stripped_literal = literal.replace('-', '')
                    partial_assignment[stripped_literal] = '-' not in literal
                    clauses = simplify_clauses(clauses, partial_assignment)

            # choose the literal with the highest frequency
            literal_frequency = {}
            for clause in clauses:
                for literal in clause:
                    if literal not in partial_assignment:
                        literal_frequency[literal] = literal_frequency.get(literal, 0) + 1

            if not literal_frequency:
                return False

            # choose the literal with the highest frequency to break ties
            next_literal = max(literal_frequency, key=literal_frequency.get)

            stripped_literal = next_literal.replace('-', '')

            for clause in clauses:
                if next_literal in clause or self.rev_literal(next_literal) in clause:
                    print(f"Removing literal {next_literal} from clause {clause}")

            # Try assigning False, then True
            for value in [False, True]:
                # Backup the partial assignment and the clauses before the decision
                new_partial_assignment = partial_assignment.copy()
                new_clauses = [tuple(clause) for clause in clauses]

                # Apply the literal assignment
                new_partial_assignment[stripped_literal] = value if '-' not in next_literal else not value
                updated_clauses = simplify_clauses(new_clauses, new_partial_assignment)

                # Recurse with the new partial assignment and simplified clauses
                success = recursive_solve(new_partial_assignment, updated_clauses)
                if success:
                    return True

            return False

        def simplify_clauses(clauses, assignment):
            simplified_clauses = set()
            for clause in clauses:
                new_clause = []
                clause_satisfied = False

                for literal in clause:
                    stripped_literal = literal.replace('-', '')
                    if stripped_literal in assignment:
                        # literal satisfaction check
                        if (('-' in literal and not assignment[stripped_literal]) or
                                ('-' not in literal and assignment[stripped_literal])):
                            clause_satisfied = True
                            break
                    else:
                        new_clause.append(literal)

                if not clause_satisfied and new_clause:
                    simplified_clauses.add(tuple(new_clause))

            return simplified_clauses

        # solve puzzle
        success = recursive_solve({}, self.clauses.copy())

        # write the output to file
        self.write_output()

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
            sorted_solution = sorted(self.solution)
            for assignment in sorted_solution:
                if self.solution[assignment] == True:
                    f.write(f"{assignment} 0\n")
            for assignment in sorted_solution:
                if self.solution[assignment] == False:
                    f.write(f"-{assignment} 0\n")


    def verify_solution(self, puzzle_file, sol_file):
        puzzle_clauses, _ = self.read_input(puzzle_file)
        sol_clauses, _ = self.read_input(sol_file)

        rules_broken = False

        for clause in puzzle_clauses:
            clause_satisfied = False
            for literal in clause:
                if (literal,) in sol_clauses:
                    clause_satisfied = True
                    continue
            if not clause_satisfied:
                rules_broken = True
                print(f"Clause {clause} not satisfied!")

        if rules_broken:
            print("Rules were not followed!")

if __name__ == "__main__":
    algo_number = int(sys.argv[1])
    input_file = sys.argv[2]
    solver = SATSolver(input_file)

    try:
        sol_file = sys.argv[3]
    except:
        sol_file = None

    start_time = time.time()

    match algo_number:
        case 1:
            solver.solve_dpll()
        case 2:
            solver.solve_heuristic_1()
        case 3:
            solver.solve_heuristic_2()
        case 4:
            solver.verify_solution(input_file, sol_file)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")

    if algo_number != 4:
        solver.write_output()