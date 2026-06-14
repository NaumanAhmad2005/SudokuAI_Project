# ui_visualizer.py
import pygame
import time
import sys
from generator import PuzzleGenerator
from csp_base import SudokuCSP
from algorithms import solve_backtracking, solve_forward_checking, solve_mrv, solve_local_search
from dashboard import run_benchmark_dashboard

# ==========================================
# BEAUTIFUL MINIMALIST THEMES (Light & Dark)
# ==========================================
THEMES = [
    {
        "id": "wood",
        "name": "Zen Wood",
        "bg": (251, 249, 244),
        "panel": (242, 238, 229),
        "text_main": (60, 48, 40),
        "text_sub": (140, 125, 115),
        "primary": (115, 155, 117),    # Sage Green
        "secondary": (210, 125, 105),  # Terracotta
        "grid": (220, 215, 205),
        "grid_thick": (130, 115, 105),
        "btn_bg": (235, 230, 220),
    },
    {
        "id": "light",
        "name": "Light Mode",
        "bg": (250, 250, 250),
        "panel": (240, 240, 240),
        "text_main": (17, 24, 39),
        "text_sub": (107, 114, 128),
        "primary": (59, 130, 246),     # Clean Blue
        "secondary": (16, 185, 129),   # Clean Green
        "grid": (229, 231, 235),
        "grid_thick": (156, 163, 175),
        "btn_bg": (243, 244, 246),
    },
    {
        "id": "dark",
        "name": "Dark Mode",
        "bg": (17, 24, 39),
        "panel": (31, 41, 55),
        "text_main": (249, 250, 251),
        "text_sub": (156, 163, 175),
        "primary": (96, 165, 250),     # Soft Blue
        "secondary": (52, 211, 153),   # Soft Green
        "grid": (55, 65, 81),
        "grid_thick": (107, 114, 128),
        "btn_bg": (55, 65, 81),
    }
]

class SudokuGUI:
    def __init__(self):
        pygame.init()
        self.width = 600   # Restored exact width
        self.height = 750  # Kept compact so it NEVER flows under the screen
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Sudoku AI Benchmarking Suite")
        
        # Clean, modern typography
        self.font_title = pygame.font.SysFont("segoeui", 38, bold=True)
        self.font_header = pygame.font.SysFont("segoeui", 18, bold=True)
        self.font_grid = pygame.font.SysFont("segoeui", 34, bold=False)
        self.font_btn = pygame.font.SysFont("segoeui", 16, bold=True)
        self.font_small = pygame.font.SysFont("segoeui", 14, bold=True)

        self.theme_idx = 0

    @property
    def theme(self):
        return THEMES[self.theme_idx]

    def main_menu(self):
        running = True
        selected_diff = "easy"
        selected_algo = "backtracking"
        selected_speed = "normal" 

        # --- Layout Engine ---
        # Difficulty
        btn_easy = pygame.Rect(40, 100, 110, 40)
        btn_med = pygame.Rect(170, 100, 110, 40)
        btn_hard = pygame.Rect(300, 100, 110, 40)
        btn_exp = pygame.Rect(430, 100, 110, 40)

        # Algorithms
        btn_uninformed = pygame.Rect(40, 190, 520, 40)
        btn_forward = pygame.Rect(40, 240, 520, 40)
        btn_mrv = pygame.Rect(40, 290, 520, 40)
        btn_local = pygame.Rect(40, 340, 520, 40)

        # Speed
        btn_vslow = pygame.Rect(40, 430, 90, 40)
        btn_slow = pygame.Rect(145, 430, 90, 40)
        btn_normal = pygame.Rect(250, 430, 90, 40)
        btn_fast = pygame.Rect(355, 430, 90, 40)
        btn_instant = pygame.Rect(460, 430, 100, 40)

        # Actions
        btn_start = pygame.Rect(50, 530, 500, 50)
        btn_benchmark = pygame.Rect(50, 595, 500, 50) 
        btn_race = pygame.Rect(50, 660, 500, 50)

        # Theme Toggle (Restored to extreme top right!)
        btn_theme = pygame.Rect(470, 15, 110, 30)

        while running:
            t = self.theme
            self.win.fill(t["bg"])
            mouse_pos = pygame.mouse.get_pos()

            # --- Draw Header ---
            title = self.font_title.render("AI SUDOKU BENCHMARK", True, t["primary"])
            self.win.blit(title, (40, 20))
            
            # Draw Theme Toggle at Top Right
            self._draw_btn(btn_theme, f"{t['name'].upper()}", mouse_pos, False, self.font_small, override_bg=t["panel"], override_fg=t["text_main"])

            # --- Section Headers ---
            self.win.blit(self.font_header.render("1. PUZZLE DIFFICULTY", True, t["text_main"]), (40, 70))
            self.win.blit(self.font_header.render("2. ALGORITHM TO ANIMATE", True, t["text_main"]), (40, 160))
            self.win.blit(self.font_header.render("3. ANIMATION SPEED", True, t["text_main"]), (40, 400)) 

            # --- Draw Config Buttons ---
            self._draw_btn(btn_easy, "Easy", mouse_pos, selected_diff == "easy")
            self._draw_btn(btn_med, "Medium", mouse_pos, selected_diff == "medium")
            self._draw_btn(btn_hard, "Hard", mouse_pos, selected_diff == "hard")
            self._draw_btn(btn_exp, "Expert", mouse_pos, selected_diff == "expert")

            self._draw_btn(btn_uninformed, "Basic Backtracking (Uninformed DFS)", mouse_pos, selected_algo == "backtracking")
            self._draw_btn(btn_forward, "Forward Checking (Constraint Propagation)", mouse_pos, selected_algo == "forward")
            self._draw_btn(btn_mrv, "AC3 + MRV + Degree (Informed Search)", mouse_pos, selected_algo == "mrv")
            self._draw_btn(btn_local, "Simulated Annealing (Local Search)", mouse_pos, selected_algo == "local")

            self._draw_btn(btn_vslow, "V. Slow", mouse_pos, selected_speed == "v_slow", font=self.font_small)
            self._draw_btn(btn_slow, "Slow", mouse_pos, selected_speed == "slow", font=self.font_small)
            self._draw_btn(btn_normal, "Normal", mouse_pos, selected_speed == "normal", font=self.font_small)
            self._draw_btn(btn_fast, "Fast", mouse_pos, selected_speed == "fast", font=self.font_small)
            self._draw_btn(btn_instant, "Instant", mouse_pos, selected_speed == "instant", font=self.font_small)

            # --- Draw Action Panel ---
            pygame.draw.rect(self.win, t["panel"], (0, 500, self.width, 250))
            pygame.draw.line(self.win, t["grid"], (0, 500), (self.width, 500), 2)

            self._draw_btn(btn_start, "ANIMATE SINGLE SOLVER", mouse_pos, False, override_bg=t["primary"])
            self._draw_btn(btn_benchmark, "RUN FULL BENCHMARK SUITE", mouse_pos, False, override_bg=t["text_main"])
            self._draw_btn(btn_race, "START 4-WAY LIVE RACE", mouse_pos, False, override_bg=t["secondary"])

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if btn_theme.collidepoint(mouse_pos):
                        self.theme_idx = (self.theme_idx + 1) % len(THEMES)
                    
                    if btn_easy.collidepoint(mouse_pos): selected_diff = "easy"
                    if btn_med.collidepoint(mouse_pos): selected_diff = "medium"
                    if btn_hard.collidepoint(mouse_pos): selected_diff = "hard"
                    if btn_exp.collidepoint(mouse_pos): selected_diff = "expert"

                    if btn_uninformed.collidepoint(mouse_pos): selected_algo = "backtracking"
                    if btn_forward.collidepoint(mouse_pos): selected_algo = "forward"
                    if btn_mrv.collidepoint(mouse_pos): selected_algo = "mrv"
                    if btn_local.collidepoint(mouse_pos): selected_algo = "local"

                    if btn_vslow.collidepoint(mouse_pos): selected_speed = "v_slow"
                    if btn_slow.collidepoint(mouse_pos): selected_speed = "slow"
                    if btn_normal.collidepoint(mouse_pos): selected_speed = "normal"
                    if btn_fast.collidepoint(mouse_pos): selected_speed = "fast"
                    if btn_instant.collidepoint(mouse_pos): selected_speed = "instant"

                    if btn_start.collidepoint(mouse_pos):
                        self.process_and_animate(selected_diff, selected_algo, selected_speed) 

                    if btn_benchmark.collidepoint(mouse_pos):
                        self.win.fill(t["bg"])
                        loading = self.font_title.render("Running Benchmarks...", True, t["primary"])
                        self.win.blit(loading, (self.width//2 - loading.get_width()//2, self.height//2))
                        pygame.display.update()
                        run_benchmark_dashboard(selected_diff)

                    if btn_race.collidepoint(mouse_pos):
                        self.process_and_race(selected_diff, selected_speed)

    def _draw_btn(self, rect, text, mouse_pos, is_selected, font=None, override_bg=None, override_fg=None):
        if font is None: font = self.font_btn
        t = self.theme
            
        if override_bg:
            bg_color = override_bg
            fg_color = override_fg if override_fg else t["bg"] 
            if rect.collidepoint(mouse_pos):
                # Lighten/Darken effect
                bg_color = (min(255, bg_color[0]+15), min(255, bg_color[1]+15), min(255, bg_color[2]+15))
        else:
            if is_selected:
                bg_color = t["primary"]
                fg_color = t["bg"]
            elif rect.collidepoint(mouse_pos):
                bg_color = t["btn_bg"]
                fg_color = t["primary"]
            else:
                bg_color = t["btn_bg"]
                fg_color = t["text_main"]

        # Clean minimalist rounded corners
        pygame.draw.rect(self.win, bg_color, rect, border_radius=6)
        
        # Soft subtle border for unselected buttons
        if not override_bg and not is_selected:
            pygame.draw.rect(self.win, t["grid_thick"], rect, width=1, border_radius=6)

        txt_surf = font.render(text, True, fg_color)
        self.win.blit(txt_surf, (rect.x + (rect.width - txt_surf.get_width())//2, rect.y + (rect.height - txt_surf.get_height())//2))

    def process_and_animate(self, difficulty, algo_key, speed):
        t = self.theme
        self.win.fill(t["bg"])
        loading = self.font_title.render(f"Generating {difficulty.upper()} Puzzle...", True, t["primary"])
        self.win.blit(loading, (self.width//2 - loading.get_width()//2, self.height//2))
        pygame.display.update()

        gen = PuzzleGenerator()
        puzzle = gen.generate_puzzle(difficulty)
        csp = SudokuCSP(puzzle)

        algo_name = ""
        start_time = time.perf_counter()
        
        if algo_key == "backtracking":
            algo_name = "Basic Backtracking"
            solve_backtracking(csp)
        elif algo_key == "forward":
            algo_name = "Forward Checking"
            solve_forward_checking(csp)
        elif algo_key == "mrv":
            algo_name = "MRV + Degree Heuristic"
            solve_mrv(csp)
        elif algo_key == "local":
            algo_name = "Simulated Annealing"
            solve_local_search(csp)

        end_time = time.perf_counter()
        time_taken = end_time - start_time

        self.animate_solution(puzzle, csp.history, algo_name, csp.states_explored, csp.backtracks, time_taken, speed)

    def animate_solution(self, original_board, history, algo_name, final_states, final_backs, time_taken, speed):
        current_board = [[original_board[i][j] for j in range(9)] for i in range(9)]
        running = True
        step = 0
        total_steps = len(history)
        solved = False
        paused = False

        delay = 0       
        skip_frames = 1 
        
        if speed == "v_slow": delay = 700  
        elif speed == "slow": delay = 250  
        elif speed == "normal": delay = 190   
        elif speed == "fast": delay = 15; skip_frames = 1 
        elif speed == "instant": skip_frames = total_steps + 1 

        grid_size = 500
        offset_x = (self.width - grid_size) // 2
        offset_y = 30

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    if event.key == pygame.K_SPACE:
                        if solved: return 
                        else: paused = not paused

            t = self.theme
            self.win.fill(t["bg"])
            frames_to_process = skip_frames if not solved else 1
            
            if not paused:
                for _ in range(frames_to_process):
                    if step < total_steps:
                        row, col, num = history[step]
                        current_board[row][col] = num
                        step += 1
                    else:
                        solved = True
                        break

            self._draw_grid(offset_x, offset_y, grid_size)
            self._draw_numbers(current_board, original_board, offset_x, offset_y, grid_size)
            
            current_states = int((step / total_steps) * final_states) if total_steps > 0 else final_states
            current_backs = int((step / total_steps) * final_backs) if total_steps > 0 else final_backs
            if solved:
                current_states = final_states
                current_backs = final_backs

            self._draw_info(algo_name, current_states, current_backs, time_taken, solved, paused)

            pygame.display.update()
            if delay > 0 and not solved:
                pygame.time.delay(delay)

    def _draw_grid(self, offset_x, offset_y, size):
        t = self.theme
        gap = size / 9
        pygame.draw.rect(self.win, t["btn_bg"], (offset_x, offset_y, size, size))
        
        for i in range(10):
            color = t["grid_thick"] if i % 3 == 0 else t["grid"]
            thick = 3 if i % 3 == 0 else 1
            pygame.draw.line(self.win, color, (offset_x, offset_y + i * gap), (offset_x + size, offset_y + i * gap), thick)
            pygame.draw.line(self.win, color, (offset_x + i * gap, offset_y), (offset_x + i * gap, offset_y + size), thick)

    def _draw_numbers(self, board, original_board, offset_x, offset_y, size):
        t = self.theme
        gap = size / 9
        for i in range(9):
            for j in range(9):
                if board[i][j] != 0:
                    color = t["text_sub"] if original_board[i][j] != 0 else t["primary"]
                    text = self.font_grid.render(str(board[i][j]), True, color)
                    x = offset_x + (j * gap) + (gap / 2 - text.get_width() / 2)
                    y = offset_y + (i * gap) + (gap / 2 - text.get_height() / 2)
                    self.win.blit(text, (x, y))

    def _draw_info(self, algo_name, states, backtracks, time_taken, solved, paused=False):
        t = self.theme
        panel_y = 560
        pygame.draw.rect(self.win, t["panel"], (0, panel_y, self.width, self.height - panel_y))
        pygame.draw.line(self.win, t["grid"], (0, panel_y), (self.width, panel_y), 2)
        
        status_color = t["primary"] if solved else (t["secondary"] if paused else t["text_sub"])
        status_text = "COMPLETED" if solved else ("PAUSED" if paused else "SEARCHING...")
        
        text_algo = self.font_title.render(f"{algo_name}", True, t["text_main"])
        text_status = self.font_btn.render(f"{status_text}", True, status_color)
        
        text_states = self.font_header.render(f"States: {states:,}", True, t["text_sub"])
        text_backs = self.font_header.render(f"Backtracks: {backtracks:,}", True, t["text_sub"])
        
        time_formatted = f"{time_taken * 1000:.2f} ms" if time_taken < 1 else f"{time_taken:.3f} s"
        text_time = self.font_header.render(f"Time: {time_formatted}" if solved else "Time: ---", True, t["text_sub"])

        self.win.blit(text_algo, (30, panel_y + 30))
        self.win.blit(text_status, (30, panel_y + 70))
        
        self.win.blit(text_states, (30, panel_y + 115))
        self.win.blit(text_backs, (230, panel_y + 115))
        self.win.blit(text_time, (420, panel_y + 115))

    def process_and_race(self, difficulty, speed):
        t = self.theme
        self.win.fill(t["bg"])
        loading = self.font_title.render(f"Generating {difficulty.upper()} Puzzle...", True, t["primary"])
        self.win.blit(loading, (self.width//2 - loading.get_width()//2, self.height//2))
        pygame.display.update()

        gen = PuzzleGenerator()
        puzzle = gen.generate_puzzle(difficulty)

        self.win.fill(t["bg"])
        loading = self.font_title.render("Running Algorithms for Race...", True, t["primary"])
        self.win.blit(loading, (self.width//2 - loading.get_width()//2, self.height//2))
        pygame.display.update()

        algos = [
            ("Backtracking", solve_backtracking),
            ("Forward Check", solve_forward_checking),
            ("MRV + Degree", solve_mrv),
            ("Local Search", solve_local_search)
        ]

        race_data = []
        for name, func in algos:
            csp = SudokuCSP(puzzle)
            start_time = time.perf_counter()
            func(csp)
            end_time = time.perf_counter()
            race_data.append({
                "name": name,
                "history": csp.history,
                "states": csp.states_explored,
                "backs": csp.backtracks,
                "time": end_time - start_time
            })

        self.width_race = 750
        self.height_race = 750
        self.win = pygame.display.set_mode((self.width_race, self.height_race))
        
        self.animate_race(puzzle, race_data, speed)
        self.win = pygame.display.set_mode((self.width, self.height))

    def animate_race(self, original_board, race_data, speed):
        current_boards = [[[original_board[i][j] for j in range(9)] for i in range(9)] for _ in range(4)]
        steps = [0] * 4
        total_steps = [len(data["history"]) for data in race_data]
        solved = [False] * 4
        running = True
        paused = False
        
        delay = 0       
        skip_frames = 1 
        if speed == "v_slow": delay = 700
        elif speed == "slow": delay = 250
        elif speed == "normal": delay = 190
        elif speed == "fast": delay = 15; skip_frames = 1
        elif speed == "instant": skip_frames = max(total_steps) + 1 

        grid_size = 300
        # Beautiful padding for 4 distinct quadrants (fits exactly in 750x750)
        offsets = [(40, 50), (410, 50), (40, 420), (410, 420)]

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    if event.key == pygame.K_SPACE:
                        if all(solved): return 
                        else: paused = not paused

            t = self.theme
            self.win.fill(t["bg"])
            frames_to_process = skip_frames if not all(solved) else 1
            
            if not paused:
                for _ in range(frames_to_process):
                    for i in range(4):
                        if steps[i] < total_steps[i]:
                            row, col, num = race_data[i]["history"][steps[i]]
                            current_boards[i][row][col] = num
                            steps[i] += 1
                        else:
                            solved[i] = True

            for i in range(4):
                self._draw_grid(offsets[i][0], offsets[i][1], grid_size)
                self._draw_numbers(current_boards[i], original_board, offsets[i][0], offsets[i][1], grid_size)
                
                curr_states = int((steps[i] / total_steps[i]) * race_data[i]["states"]) if total_steps[i] > 0 else race_data[i]["states"]
                curr_backs = int((steps[i] / total_steps[i]) * race_data[i]["backs"]) if total_steps[i] > 0 else race_data[i]["backs"]
                if solved[i]: 
                    curr_states = race_data[i]["states"]
                    curr_backs = race_data[i]["backs"]
                
                status_color = t["primary"] if solved[i] else (t["secondary"] if paused else t["text_main"])
                
                # Title
                title_text = f"{race_data[i]['name']} [PAUSED]" if paused and not solved[i] else f"{race_data[i]['name']}"
                title_surf = self.font_header.render(title_text, True, status_color)
                self.win.blit(title_surf, (offsets[i][0], offsets[i][1] - 30))
                
                # Subtitle (Metrics)
                time_formatted = f"{race_data[i]['time'] * 1000:.2f}ms" if race_data[i]['time'] < 1 else f"{race_data[i]['time']:.3f}s"
                time_str = time_formatted if solved[i] else "---"
                metrics_surf = self.font_small.render(f"States: {curr_states:,}   Backs: {curr_backs:,}   Time: {time_str}", True, t["text_sub"])
                self.win.blit(metrics_surf, (offsets[i][0], offsets[i][1] + grid_size + 10))

            pygame.display.update()
            if delay > 0 and not all(solved):
                pygame.time.delay(delay)