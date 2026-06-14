import random
import copy

class PuzzleGenerator:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solutions_found = 0 # Used to ensure uniqueness

    def generate_puzzle(self, difficulty):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self._fill_diagonal()
        self._solve_to_generate()

        puzzle = copy.deepcopy(self.board)
        
        # Difficulties: target number of cells to ACTUALLY remove
        if difficulty.lower() == "easy":
            target = 30
        elif difficulty.lower() == "medium":
            target = 40
        elif difficulty.lower() == "hard":
            target = 50
        else: # Expert
            target = 58 # 58 is safely achievable, 60 might loop infinitely

        # Smart removal: Ensuring uniquely solvable!
        cells_removed = 0
        attempts = 0
        max_attempts = 300 # Safety net so the app doesn't freeze

        while cells_removed < target and attempts < max_attempts:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            
            if puzzle[row][col] != 0:
                backup = puzzle[row][col]
                puzzle[row][col] = 0
                
                # Check if it still has EXACTLY 1 solution
                self.solutions_found = 0
                self._count_solutions(puzzle)
                
                if self.solutions_found != 1:
                    # Removing this broke the uniqueness! Put it back.
                    puzzle[row][col] = backup
                else:
                    cells_removed += 1
                
            attempts += 1

        return puzzle

    def _fill_diagonal(self):
        for i in range(0, 9, 3):
            self._fill_box(i, i)

    def _fill_box(self, row_start, col_start):
        for i in range(3):
            for j in range(3):
                while True:
                    num = random.randint(1, 9)
                    if self._is_safe_in_box(row_start, col_start, num):
                        self.board[row_start + i][col_start + j] = num
                        break

    def _is_safe_in_box(self, row_start, col_start, num):
        for i in range(3):
            for j in range(3):
                if self.board[row_start + i][col_start + j] == num:
                    return False
        return True

    def _solve_to_generate(self):
        empty = self._find_empty(self.board)
        if not empty: return True
        row, col = empty
        
        # RANDOMIZE choices to destroy the "Golden Path" Generation Bias!
        nums = list(range(1, 10))
        random.shuffle(nums)
        
        for num in nums:
            if self._is_safe_gen(self.board, row, col, num):
                self.board[row][col] = num
                if self._solve_to_generate(): return True
                self.board[row][col] = 0
        return False

    def _count_solutions(self, grid):
        """Helper to guarantee unique solution exist"""
        if self.solutions_found > 1:
            return
            
        empty = self._find_empty(grid)
        if not empty:
            self.solutions_found += 1
            return
            
        row, col = empty
        for num in range(1, 10):
            if self._is_safe_gen(grid, row, col, num):
                grid[row][col] = num
                self._count_solutions(grid)
                grid[row][col] = 0

    def _find_empty(self, grid):
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0: return (i, j)
        return None

    def _is_safe_gen(self, grid, row, col, num):
        for x in range(9):
            if grid[row][x] == num or grid[x][col] == num: return False
        start_row, start_col = row - row % 3, col - col % 3
        for i in range(3):
            for j in range(3):
                if grid[i + start_row][j + start_col] == num: return False
        return True
