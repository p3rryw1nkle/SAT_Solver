from copy import deepcopy
import time
import sys
import os

class SATSolver():
    def __init__(self, input_file):
        self.puzzle_file = input_file
        self.file_name = os.path.basename(input_file)
        self.puzzle_dimension = 1
        self.clauses, self.all_literals = self.read_input(input_file)
        self.solution_folder = f"{self.puzzle_dimension}x{self.puzzle_dimension}"
        self.sol_file = ""
        self.solution = set()
        self.back_tracks = 0


    def read_input(self, input_file):

        '''
        Reads in input files and converts to a set of clauses
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
        
    
    def simplify_clauses(self, clauses, assignment):
        simplified_clauses = set()
        for clause in clauses:
            new_clause = []
            clause_satisfied = False

            for literal in clause:
                stripped_literal = literal.replace('-', '')
                if stripped_literal in assignment:
                    # literal satisfaction check
                    if (assignment[stripped_literal] == ('-' not in literal)):
                        # if clause is satisfied, we can toss it out
                        clause_satisfied = True
                        break
                else:
                    # if the literal is not in the assignment, keep it in the clause
                    new_clause.append(literal)

            # keep clause if it hasn't been satisfied yet or if it is empty
            if not clause_satisfied:
                simplified_clauses.add(tuple(new_clause))

        return simplified_clauses


    def solve_dpll(self):
        '''
        Implement the DPLL algorithm
        '''
        self.back_tracks = 0

        def recursive_solve(partial_assignment, clauses):
            
            # if all clauses have been solved
            if len(clauses) == 0:
                self.solution = partial_assignment
                assert self.check_partial_assignment(self.solution, self.clauses) == True
                return True
            
            # if there are any empty clauses, return false
            for clause in clauses:
                if len(clause) == 0:
                    self.back_tracks += 1
                    return False
                
            # if there are unit clauses
            for clause in clauses:
                if len(clause) == 1:
                    # add literal to partial assigment
                    (lit,) = clause

                    # stripped literal
                    strp_lit = lit.replace('-','')

                    # assign the literal its appropriate value
                    partial_assignment[strp_lit] = ('-' not in lit)

            # add all the literals in the remaining clauses to a set
            pure_literals = set()

            for clause in clauses:
                for literal in clause:
                   strp_lit = literal.replace('-','')
                   if strp_lit not in partial_assignment:
                        pure_literals.add(literal)    

            for literal in pure_literals:
                # reversed literal (with '-' if without and vice versa)
                rev_lit = self.rev_literal(literal)
                strp_lit = literal.replace('-','')
                if (rev_lit not in pure_literals):
                    partial_assignment[strp_lit] = ('-' not in literal)

            # go through each clause, only keep those that have not been satisfied
            new_clauses = self.simplify_clauses(clauses, partial_assignment)

            assigned_literals = set(partial_assignment.keys())
            unassigned_literals = self.all_literals.difference(assigned_literals)

            # if there are no more literals to assign
            if len(unassigned_literals) == 0:
                return recursive_solve(partial_assignment.copy(), new_clauses.copy())

            # get the next literal from unassigned literals
            next_literal = sorted(unassigned_literals).pop(0)

            partial_assignment[next_literal] = False
            if recursive_solve(partial_assignment.copy(), new_clauses.copy()):
                return True
            else:
                partial_assignment[next_literal] = True
                return recursive_solve(partial_assignment.copy(), new_clauses.copy())

        return recursive_solve({}, self.clauses.copy())

    def solve_heuristic_1(self):
        """
        Implement first heuristic
        """
        self.back_tracks = 0

        def recursive_solve(partial_assignment, clauses):

            # if all clauses have been solved
            if len(clauses) == 0:
                self.solution = partial_assignment
                return True

            # if there is an empty clause, the formula is false so return false
            for clause in clauses:
                if len(clause) == 0:
                    self.back_tracks += 1
                    return False

            for clause in clauses:
                if len(clause) == 1:
                    (lit,) = clause
                    stripped_literal = lit.replace('-', '')
                    # print(f"adding unit clause: {clause} to partial assignment")
                    partial_assignment[stripped_literal] = ('-' not in lit)
                    assert partial_assignment[stripped_literal] == ('-' not in lit)

            # clauses = simplify_clauses(clauses, partial_assignment)

            # if not self.check_partial_assignment(partial_assignment, clauses):
            #     raise Exception("PA not valid after unit clause assignment!")

            # add all the literals in the remaining clauses to a set
            pure_literals = set()

            for clause in clauses:
                for literal in clause:
                   strp_lit = literal.replace('-','')
                   if strp_lit not in partial_assignment:
                        pure_literals.add(literal)    

            for literal in pure_literals:
                # reversed literal (with '-' if without and vice versa)
                rev_lit = self.rev_literal(literal)
                strp_lit = literal.replace('-','')
                if (rev_lit not in pure_literals):
                    partial_assignment[strp_lit] = ('-' not in literal)

            # if not self.check_partial_assignment(partial_assignment, clauses):
            #     raise Exception("PA not valid after pure literal assignment!")
            
            # clauses = simplify_clauses(clauses, partial_assignment)

            # if not self.check_partial_assignment(partial_assignment, clauses):
            #     raise Exception("PA not valid after simplification!")

            # choose the literal with the highest frequency
            literal_frequency = {}
            for clause in clauses:
                for literal in clause:
                    if literal not in partial_assignment:
                        literal_frequency[literal] = literal_frequency.get(literal, 0) + 1

            if len(literal_frequency) == 0:
                print(f"literal frequency is 0, partial assignment: {len(partial_assignment)}")

            # if all literals have already been assigned
            if not literal_frequency:
                if self.check_partial_assignment(partial_assignment, clauses):
                    self.solution = partial_assignment
                    return True
                else:
                    self.back_tracks += 1
                    return False
            
            # choose the literal with the highest frequency to break ties
            next_literal = max(literal_frequency, key=literal_frequency.get)

            stripped_literal = next_literal.replace('-', '')

            # Try assigning False, then True
            for value in [False, True]:
                # new_partial_assignment[stripped_literal] = value if '-' not in next_literal else not value
                partial_assignment[stripped_literal] = value
                new_clauses = simplify_clauses(clauses, partial_assignment)

                # Recurse with the new partial assignment and simplified clauses
                if recursive_solve(partial_assignment.copy(), new_clauses):
                    return True
            
            self.back_tracks += 1
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
                        if ((('-' in literal) and assignment[stripped_literal] == False) or
                                (('-' not in literal) and assignment[stripped_literal] == True)):
                            # if clause is satisfied, we can toss it out
                            clause_satisfied = True
                            break
                    else:
                        # if the literal is not in the assignment, keep it in the clause
                        new_clause.append(literal)

                # keep clause if it hasn't been satisfied yet or if it is empty
                if not clause_satisfied:
                    simplified_clauses.add(tuple(new_clause))

            return simplified_clauses

        # solve puzzle
        if not recursive_solve({}, self.clauses.copy()):
            print("No solution found")
            self.solution = {}
        # self.write_output()

    def solve_heuristic_2(self):
        """
        Implement first heuristic
        """

        def recursive_solve(partial_assignment, clauses, last_literal_assigned):

            # if not self.check_partial_assignment(partial_assignment, clauses):
                # raise Exception("PA not valid after unit clause assignment!")

            # if all clauses have been solved
            if len(clauses) == 0:
                self.solution = partial_assignment
                return True

            # if there is an empty clause, the formula is false so return false
            for clause in clauses:
                if len(clause) == 0:
                    self.back_tracks += 1
                    return False

            # add unit clauses to partial assignment
            for clause in clauses:
                if len(clause) == 1:
                    (lit,) = clause
                    stripped_literal = lit.replace('-', '')
                    partial_assignment[stripped_literal] = ('-' not in lit)
                    assert partial_assignment[stripped_literal] == ('-' not in lit)
                    last_literal_assigned = stripped_literal                                

            # assign pure literals
            literal_counts = {}
            for clause in clauses:
                for literal in clause:
                    literal_counts[literal] = literal_counts.get(literal, 0) + 1

            for literal in literal_counts.keys():
                rev_literal = self.rev_literal(literal)
                if rev_literal not in literal_counts:
                    stripped_literal = literal.replace('-', '')
                    partial_assignment[stripped_literal] = ('-' not in literal)
                    assert partial_assignment[stripped_literal] == ('-' not in literal)
                    last_literal_assigned = stripped_literal

            # if not self.check_partial_assignment(partial_assignment, clauses):
            #     raise Exception("PA not valid after pure literal assignment!")

            # choose the neighboring literal with the highest frequency
            nei_literal_frequency = {}
            for clause in clauses:
                rev_last_literal_assigned = self.rev_literal(last_literal_assigned)
                if (last_literal_assigned in clause) or (rev_last_literal_assigned in clause):
                    for neighbor in clause:                          #all of these literals are  neighbors
                        if (neighbor != last_literal_assigned) and (neighbor != rev_last_literal_assigned):
                            if neighbor not in nei_literal_frequency:
                                nei_literal_frequency[neighbor] = 0
                            nei_literal_frequency[neighbor] += 1

            # if not self.check_partial_assignment(partial_assignment, clauses):
            #     raise Exception("PA not valid after simplification!")

            next_literal = None

            # if there are no neighboring literals of the last literal assigned
            if not nei_literal_frequency:
                # check to see if there are literals still left to assign
                assigned_literals = set(partial_assignment.keys())
                unassigned_literals = self.all_literals.difference(assigned_literals)  

                if len(unassigned_literals) == 0:
                    print("no neighbors to choose from!")
                    if self.check_partial_assignment(partial_assignment, clauses):
                        self.solution = partial_assignment
                        return True
                    else:
                        self.back_tracks += 1
                        return False
                else:
                    # if there are, just choose the first one
                    next_literal = sorted(unassigned_literals).pop(0)
            else:           
                # if there are neighboring literals, choose the closest literal
                next_literal = max(nei_literal_frequency, key=nei_literal_frequency.get)

            assert next_literal != None

            stripped_literal = next_literal.replace('-', '')

            # Try assigning False, then True
            for value in [False, True]:
                # new_partial_assignment[stripped_literal] = value if '-' not in next_literal else not value
                partial_assignment[stripped_literal] = value
                last_literal_assigned = stripped_literal
                new_clauses = self.simplify_clauses(clauses, partial_assignment)

                # Recurse with the new partial assignment and simplified clauses
                if recursive_solve(partial_assignment.copy(), new_clauses, deepcopy(last_literal_assigned)):
                    return True
                
            self.back_tracks += 1
            return False

        # solve puzzle
        if not recursive_solve({}, self.clauses.copy(), None):
            print("No solution found")
            self.solution = {}
        self.write_output()


    def write_output(self):
        '''
        Write output to file in DIMAC format
        '''
        self.sol_file = f"solutions/{self.solution_folder}/sol_{self.file_name}"

        with open(self.sol_file, "w") as f:
            f.write(f"p {len(self.all_literals)} {len(self.solution)}\n")
            sorted_solution = sorted(self.solution)
            for assignment in sorted_solution:
                if self.solution[assignment] == True:
                    f.write(f"{assignment} 0\n")
            for assignment in sorted_solution:
                if self.solution[assignment] == False:
                    f.write(f"-{assignment} 0\n")


    def check_partial_assignment(self, pa, clauses):
        for clause in clauses:
            clause_satisfied = False
            for literal in clause:
                strp_literal = literal.replace('-','')
                if (strp_literal not in pa) or ((strp_literal in pa) and (pa[strp_literal] == ('-' not in literal))):
                    clause_satisfied = True
                    continue
            if not clause_satisfied:
                print(f"Clause {clause} not satisfied!")
                print(pa)
                return False
        return True


    def verify_solution(self, puzzle_file=None, sol_file=None):
        if not puzzle_file:
            puzzle_file = self.puzzle_file
            if not puzzle_file:
                raise Exception("Error, no puzzle file provided to verify solution!")

        if not sol_file:
            sol_file = self.sol_file
            if sol_file == "":
                raise Exception("Error, no solution file provided to verify solution!")
            
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
            print("The above clauses were not followed!")
            return False
        else:
            print("Solution is valid!")
            return True


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
    
    if algo_number != 4:
        solver.write_output()
        solver.verify_solution()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")

    if algo_number != 4:
        solver.write_output()