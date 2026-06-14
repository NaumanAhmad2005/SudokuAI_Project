# console_visualizer.py
import time
import os

class ConsoleVisualizer:
    """Console-based Sudoku animation - no external dependencies needed!"""
    
    def __init__(self):
        self.clear_screen()
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def draw_board(self, board, original_board):
        """Draw the Sudoku board in the console"""
        self.clear_screen()
        print("\n" + "="*50)
        print("    AI Sudoku Solver Visualizer")
        print("="*50 + "\n")
        
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("    ------+-------+------")
            
            row_str = "    "
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    row_str += "| "
                
                cell = board[i][j]
                if cell == 0:
                    row_str += ". "
                else:
                    # Bold for original clues, normal for AI moves
                    if original_board[i][j] != 0:
                        row_str += f"\033[1m{cell}\033[0m "  # Bold
                    else:
                        row_str += f"\033[92m{cell}\033[0m "  # Green for AI moves
            
            print(row_str)
        
        print("\n" + "="*50)
    
    def animate_solution(self, original_board, history, algo_name, final_states, final_backs, speed_multiplier=1.0):
        """Play back the solution step by step in the console"""
        current_board = [[original_board[i][j] for j in range(9)] for i in range(9)]
        
        step = 0
        total_steps = len(history)
        
        print(f"\n🚀 Starting animation with {algo_name}...")
        print(f"📊 Total moves to animate: {total_steps}\n")
        time.sleep(2)
        
        for step, (row, col, num) in enumerate(history):
            current_board[row][col] = num
            
            # Update board display
            self.draw_board(current_board, original_board)
            
            # Show metrics
            print(f"\n📍 Move {step + 1} of {total_steps}")
            print(f"🔹 Placed {num} at position ({row}, {col})")
            
            current_states = int((step / total_steps) * final_states) if total_steps > 0 else final_states
            print(f"📊 States Explored: {current_states} / {final_states}")
            print(f"🔄 Backtracks: {int((step / total_steps) * final_backs)} / {final_backs}")
            
            # Animation speed - default is 0.2 seconds per move (SLOW for viewing)
            base_speed = 0.2  # Slow animation for clear viewing
            speed = base_speed * speed_multiplier
            time.sleep(speed)
        
        # Final display
        self.draw_board(current_board, original_board)
        print("\n" + "="*50)
        print("✅ PUZZLE SOLVED!")
        print("="*50)
        print(f"Algorithm: {algo_name}")
        print(f"Total States Explored: {final_states}")
        print(f"Total Backtracks: {final_backs}")
        print("="*50 + "\n")
