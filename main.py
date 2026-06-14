# # main.py
# import time
# from generator import PuzzleGenerator
# from csp_base import SudokuCSP
# from algorithms import solve_backtracking, solve_forward_checking, solve_mrv, solve_local_search

# def test_algorithm(algorithm_func, algorithm_name, puzzle):
#     print(f"\nRunning {algorithm_name}...")
    
#     # 1. Create a fresh CSP object from the puzzle
#     csp = SudokuCSP(puzzle)
    
#     # 2. Start timer
#     start_time = time.time()
    
#     # 3. Run the algorithm
#     success = algorithm_func(csp)
    
#     # 4. Stop timer
#     end_time = time.time()
#     time_taken = end_time - start_time
    
#     # 5. Print Metrics
#     if success:
#         print(f"✅ Solved successfully in {time_taken:.4f} seconds!")
#         print(f"📊 States Explored: {csp.states_explored}")
#         print(f"🔄 Backtracks: {csp.backtracks}")
#     else:
#         print(f"❌ Failed to solve. (Usually means Local Search timed out)")

#     return time_taken, csp.states_explored, csp.backtracks

# if __name__ == "__main__":
#     print("=== Sudoku AI Benchmarking Suite ===")
    
#     # Generate one puzzle to test all algorithms fairly
#     gen = PuzzleGenerator()
#     difficulty = "hard" # Change this to 'easy', 'medium', 'hard', or 'expert'
#     print(f"\nGenerating a {difficulty.upper()} puzzle...\n")
    
#     puzzle = gen.generate_puzzle(difficulty)
    
#     # Print original puzzle
#     original_csp = SudokuCSP(puzzle)
#     original_csp.print_board()
#     print("\n------------------------------------")

#     # Run Uninformed Search (Baseline)
#     test_algorithm(solve_backtracking, "Uninformed (Basic Backtracking)", puzzle)

#     # Run Forward Checking
#     test_algorithm(solve_forward_checking, "Constraint Propagation (Forward Checking)", puzzle)

#     # Run Informed Search
#     test_algorithm(solve_mrv, "Informed Search (MRV + Degree Heuristic)", puzzle)
    
#     # Run Local Search
#     # Note: Local search struggles on "hard" and "expert", which is great for your report's analysis!
#     test_algorithm(solve_local_search, "Local Search (Simulated Annealing)", puzzle)
# main.py
from ui_visualizer import SudokuGUI

if __name__ == "__main__":
    app = SudokuGUI()
    app.main_menu() # Starts the interactive application!