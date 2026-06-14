import math
import random
import copy

# ==========================================
# 1. UNINFORMED SEARCH (Baseline Backtracking)
# ==========================================
def solve_backtracking(csp):
    empty = csp.find_empty_location()
    if not empty: return True
        
    row, col = empty
    for num in range(1, 10):
        csp.states_explored += 1
        if csp.is_safe(row, col, num):
            csp.update_board(row, col, num)
            if solve_backtracking(csp): return True
            csp.update_board(row, col, 0)
            csp.backtracks += 1
    return False

# ==========================================
# 2. CONSTRAINT PROPAGATION (Forward Checking)
# ==========================================
def solve_forward_checking(csp):
    empty = csp.find_empty_location()
    if not empty: return True
        
    row, col = empty
    for num in range(1, 10):
        csp.states_explored += 1
        if csp.is_safe(row, col, num):
            csp.update_board(row, col, num)
            if not _has_empty_domain(csp):
                if solve_forward_checking(csp): return True
            csp.update_board(row, col, 0)
            csp.backtracks += 1
    return False

def _has_empty_domain(csp):
    for r in range(9):
        for c in range(9):
            if csp.board[r][c] == 0:
                possible = sum(1 for v in range(1, 10) if csp.is_safe(r, c, v))
                if possible == 0: return True
    return False

# ==========================================
# 3. INFORMED SEARCH (AC-3 + MRV)
# ==========================================
def solve_mrv(csp):
    """
    Combines Arc Consistency (AC-3) for domain pruning 
    with Minimum Remaining Values (MRV) heuristic.
    """
    empty = _get_best_mrv_cell(csp)
    if not empty: return True
        
    row, col = empty
    
    # Get valid domain for this cell based on current board
    domain = [n for n in range(1, 10) if csp.is_safe(row, col, n)]
    
    for num in domain:
        csp.states_explored += 1
        csp.update_board(row, col, num)
        
        # Run AC-3 to check if this placement breaks arc consistency elsewhere
        if _ac3(csp, row, col):
            if solve_mrv(csp): return True
            
        csp.update_board(row, col, 0)
        csp.backtracks += 1
        
    return False

def _get_best_mrv_cell(csp):
    min_options = 10
    best_cell = None
    for r in range(9):
        for c in range(9):
            if csp.board[r][c] == 0:
                options = sum(1 for v in range(1, 10) if csp.is_safe(r, c, v))
                if options == 0: return (r, c)
                if options < min_options:
                    min_options = options
                    best_cell = (r, c)
    return best_cell

def _ac3(csp, placed_row, placed_col):
    """
    Simplified AC-3 algorithm. 
    Checks if placing a number at (placed_row, placed_col) causes any of its 
    neighbors (arcs) to have a domain of 0.
    """
    queue = _get_neighbors(placed_row, placed_col)
    
    while queue:
        r, c = queue.pop(0)
        if csp.board[r][c] == 0:
            valid_options = sum(1 for v in range(1, 10) if csp.is_safe(r, c, v))
            # If a neighbor has NO valid options left, AC-3 fails (inconsistent)
            if valid_options == 0:
                return False
    return True

def _get_neighbors(row, col):
    """Returns all cells in the same row, col, and 3x3 box."""
    neighbors = set()
    for x in range(9):
        if x != col: neighbors.add((row, x))
        if x != row: neighbors.add((x, col))
    
    start_r, start_c = row - row % 3, col - col % 3
    for i in range(3):
        for j in range(3):
            if (start_r + i != row) or (start_c + j != col):
                neighbors.add((start_r + i, start_c + j))
    return list(neighbors)

# ==========================================
# 4. LOCAL SEARCH (Simulated Annealing)
# ==========================================
def solve_local_search(csp):
    fixed_cells = [[csp.board[r][c] != 0 for c in range(9)] for r in range(9)]
    
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            missing_nums = [n for n in range(1, 10) if not _num_in_box(csp, box_row, box_col, n)]
            random.shuffle(missing_nums)
            for r in range(3):
                for c in range(3):
                    if not fixed_cells[box_row + r][box_col + c]:
                        csp.update_board(box_row + r, box_col + c, missing_nums.pop())

    temperature = 1.0
    cooling_rate = 0.9999
    current_cost = _calculate_cost(csp)
    
    for i in range(100000):
        csp.states_explored += 1
        if current_cost == 0: return True

        box_r = random.choice([0, 3, 6])
        box_c = random.choice([0, 3, 6])
        cells = [(r, c) for r in range(3) for c in range(3) if not fixed_cells[box_r + r][box_c + c]]
        if len(cells) < 2: continue
        
        c1, c2 = random.sample(cells, 2)
        r1, col1 = box_r + c1[0], box_c + c1[1]
        r2, col2 = box_r + c2[0], box_c + c2[1]

        val1, val2 = csp.board[r1][col1], csp.board[r2][col2]
        csp.update_board(r1, col1, val2)
        csp.update_board(r2, col2, val1)
        
        new_cost = _calculate_cost(csp)
        cost_diff = new_cost - current_cost

        if cost_diff < 0:
            current_cost = new_cost
        else:
            probability = math.exp(-cost_diff / temperature) if temperature > 0 else 0
            if random.random() < probability:
                current_cost = new_cost
                csp.backtracks += 1 
            else:
                csp.update_board(r1, col1, val1)
                csp.update_board(r2, col2, val2)

        temperature *= cooling_rate
    return current_cost == 0

def _num_in_box(csp, start_row, start_col, num):
    for i in range(3):
        for j in range(3):
            if csp.board[start_row + i][start_col + j] == num: return True
    return False

def _calculate_cost(csp):
    cost = 0
    for i in range(9):
        row_nums = [csp.board[i][j] for j in range(9)]
        cost += (9 - len(set(row_nums))) 
        col_nums = [csp.board[j][i] for j in range(9)]
        cost += (9 - len(set(col_nums)))
    return cost