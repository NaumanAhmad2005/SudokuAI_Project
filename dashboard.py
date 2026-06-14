# dashboard.py
import time
import matplotlib.pyplot as plt
from generator import PuzzleGenerator
from csp_base import SudokuCSP
from algorithms import solve_backtracking, solve_forward_checking, solve_mrv, solve_local_search

def run_benchmark_dashboard(difficulty):
    gen = PuzzleGenerator()
    puzzle = gen.generate_puzzle(difficulty)

    # 4 Search Techniques Required by Assignment
    algorithms = [
        ("Uninformed\n(Backtracking)", solve_backtracking),
        ("Constraint Prop\n(Forward Check)", solve_forward_checking),
        ("Informed\n(MRV + Degree)", solve_mrv),
        ("Local Search\n(Sim. Anneal)", solve_local_search)
    ]

    names, times, states, backtracks, table_data = [], [], [], [], []

    for name, func in algorithms:
        csp = SudokuCSP(puzzle)
        start_time = time.time()
        success = func(csp)
        end_time = time.time()
        
        time_taken = round(end_time - start_time, 4)
        
        names.append(name)
        times.append(time_taken)
        states.append(csp.states_explored)
        backtracks.append(csp.backtracks)
        
        status = "Solved" if success else "Timeout/Local Optima"
        # Format names for table specifically to avoid newlines breaking layout
        table_name = name.replace('\n', ' ')
        table_data.append([table_name, status, f"{time_taken}s", f"{csp.states_explored:,}", f"{csp.backtracks:,}"])

    # ==========================================
    # DISPLAY BEAUTIFUL METRICS DASHBOARD
    # ==========================================
    # Use a professional font style for matplotlib
    plt.style.use('ggplot')
    
    fig = plt.figure(figsize=(12, 7))
    fig.canvas.manager.set_window_title(f'Sudoku AI Benchmark - {difficulty.upper()} Difficulty')
    
    # 1. TABLE (Top Half)
    ax1 = plt.subplot(2, 1, 1)
    ax1.axis('off')
    ax1.set_title(f"Algorithm Performance Comparison ({difficulty.upper()} Puzzle)", fontsize=16, fontweight='bold', pad=20)
    
    columns = ('Algorithm Strategy', 'Solution Status', 'Time Taken (Sec)', 'States Explored', 'Backtracks')
    table = ax1.table(cellText=table_data, colLabels=columns, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 2.0) # Tall rows for readability

    colors = ['#FF6666', '#66B2FF', '#99FF99', '#FFCC66'] # Red, Blue, Green, Yellow

    # 2. BAR CHART: STATES EXPLORED (Bottom Left)
    ax2 = plt.subplot(2, 2, 3)
    bars2 = ax2.bar(names, states, color=colors)
    ax2.set_title('Total States Explored', fontweight='bold')
    ax2.set_ylabel('States (Log Scale)')
    ax2.set_yscale('log') # Log scale because Backtracking is massive compared to MRV

    # 3. BAR CHART: TIME TAKEN (Bottom Right)
    ax3 = plt.subplot(2, 2, 4)
    bars3 = ax3.bar(names, times, color=colors)
    ax3.set_title('Time Taken to Solve', fontweight='bold')
    ax3.set_ylabel('Seconds')

    plt.tight_layout()
    plt.show()