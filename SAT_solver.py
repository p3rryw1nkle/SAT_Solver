import sys

class SATSolver():
    def __init__(self, input_file):
        self.clauses = self.read_input(input_file)

    def read_input(self):
        pass

    def solve_dpll(self):
        '''
        Implement the DPLL algorithm
        '''
        pass

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
    algo_number = sys.argv[1]
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