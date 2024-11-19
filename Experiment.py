import json
import sys
import os
from SAT_solver import SATSolver
import time


class SATExperiment():
    """
    Runs 3 heuristics against 2 different sets of problems
    Records how many times each heuristic returns false (i.e. has to backtrack)
    """
    def __init__(self):
        self.experiment_name = "test1"
        self.result_file = f"experiment_data/{self.experiment_name}.json"
        self.solvers = ["solve_dpll", "solve_heuristic_2", "solve_heuristic_1"]
        self.puzzle_sets = {
            "standard" : "test_sets/encoded/9x9_sudokus/standard",
            "hard" : "test_sets/encoded/9x9_sudokus/hard"
        }
        self.experiment_data = {solver : {} for solver in self.solvers}
        self.load_prev


    def load_prev(self):
        """
        Load in existing experiment data if it exists
        """
        if os.path.exists(self.result_file):
            print("reading in old experimental data...")
            with open(self.result_file, "r") as json_file:
                saved_data = json.load(json_file)
                self.experiment_data = saved_data
        else:
            print("old file does not exist... skipping")

    
    def gather_data(self):
        for algo in self.solvers:
            print(f"Starting to solve with algorithm: {algo}")

            for puzzle_set, dir_path in self.puzzle_sets.items():
                print(f"On puzzle set: {puzzle_set}")

                # add to dictionary
                if puzzle_set not in self.experiment_data[algo]:
                    self.experiment_data[algo][puzzle_set] = {}

                # Get a list of all filenames in the directory
                filenames = os.listdir(dir_path)

                # Filter out directories (optional)
                file_list = [os.path.join(dir_path, f) for f in filenames if os.path.isfile(os.path.join(dir_path, f))]

                for puzzle in file_list:
                    puzzle_name = os.path.basename(puzzle)

                    if puzzle_name in self.experiment_data[algo][puzzle_set]:
                        continue
                    else:
                        self.experiment_data[algo][puzzle_set][puzzle_name] = {}

                    print(f"On puzzle: {puzzle_name}")
                    print(f"Puzzle file path: {puzzle}")

                    start_time = time.time()

                    solver_instance = SATSolver(puzzle)
                    result = getattr(solver_instance, algo)()
                    solver_instance.write_output()
                    assert solver_instance.verify_solution() == True
                    print(result)

                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    back_tracks = solver_instance.back_tracks

                    self.experiment_data[algo][puzzle_set][puzzle_name]["time"] = elapsed_time
                    self.experiment_data[algo][puzzle_set][puzzle_name]["back_tracks"] = back_tracks
                    self.save_progress()

                    print(f"elapsed time: {elapsed_time}")

    def save_progress(self):
        """
        
        """
        with open(self.result_file, "w") as f:
            json.dump(self.experiment_data, f, indent=4)


    def stat_test(self):
        pass

    def create_graphs(self):
        pass

def main():
    experiment = SATExperiment()
    experiment.gather_data()
    experiment.stat_test()
    experiment.create_graphs()


if __name__ == "__main__":
    main()