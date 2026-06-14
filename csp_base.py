# csp_base.py
import copy

class SudokuCSP:
    def __init__(self, board):
        """
        Initialize the Sudoku Constraint Satisfaction Problem (CSP).
        'board' is a 9x9 2D list. 0 represents an empty cell.
        """
        # Deepcopy ensures we don't accidentally modify the original puzzle
        self.board = copy.deepcopy(board)
        
        # Performance Metrics (Required for Evaluation Rubric)
        self.states_explored = 0
        self.backtracks = 0
        self.history = []  #Records every move for the GUI animation!

    def is_safe(self, row, col, num):
        """
        CONSTRAINT CHECK: Checks if placing 'num' at (row, col) is valid.
        It must not violate Sudoku rules (Row, Column, and 3x3 Box).
        """
        # 1. Check Row Constraint
        for x in range(9):
            if self.board[row][x] == num:
                return False

        # 2. Check Column Constraint
        for x in range(9):
            if self.board[x][col] == num:
                return False

        # 3. Check 3x3 Box Constraint
        start_row = row - (row % 3)
        start_col = col - (col % 3)
        for i in range(3):
            for j in range(3):
                if self.board[i + start_row][j + start_col] == num:
                    return False

        # If it passes all 3 checks, it's safe!
        return True

    def find_empty_location(self):
        """
        Finds the first empty cell (value 0) on the board.
        Returns a tuple (row, col). If no empty cells, returns None.
        """
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

    def update_board(self, row, col, num):
        """NEW: Updates the board and saves the move for the GUI"""
        self.board[row][col] = num
        self.history.append((row, col, num))

    def print_board(self):
        """Helper function to beautifully print the Sudoku board to the terminal."""
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - - - - ")
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    print(" | ", end="")
                if j == 8:
                    print(self.board[i][j])
                else:
                    print(str(self.board[i][j]) + " ", end="")
