"""
PLEASE READ THE COMMENTS BELOW AND THE HOMEWORK DESCRIPTION VERY CAREFULLY BEFORE YOU START CODING

 The file where you will need to create the GUI which should include (i) drawing the grid, (ii) call your Minimax/Negamax functions
 at each step of the game, (iii) allowing the controls on the GUI to be managed (e.g., setting board size, using 
                                                                                 Minimax or Negamax, and other options)
 In the example below, grid creation is supported using pygame which you can use. You are free to use any other 
 library to create better looking GUI with more control. In the __init__ function, GRID_SIZE (Line number 36) is the variable that
 sets the size of the grid. Once you have the Minimax code written in multiAgents.py file, it is recommended to test
 your algorithm (with alpha-beta pruning) on a 3x3 GRID_SIZE to see if the computer always tries for a draw and does 
 not let you win the game. Here is a video tutorial for using pygame to create grids http://youtu.be/mdTeqiWyFnc
 
 
 PLEASE CAREFULLY SEE THE PORTIONS OF THE CODE/FUNCTIONS WHERE IT INDICATES "YOUR CODE BELOW" TO COMPLETE THE SECTIONS
 
"""
import pygame
import numpy as np
from GameStatus_5120 import GameStatus
from multiAgents import minimax, negamax

mode = "player_vs_ai"  # default mode for playing the game (player vs AI)


class RandomBoardTicTacToe:
    """
    RandomBoardTicTacToe

    This is the main GUI/controller class. It connects:
    - Pygame drawing + input handling
    - `GameStatus` game state transitions
    - `minimax` / `negamax` AI move selection

    Board encoding:
    - 0  empty
    - 1  X
    - -1 O

    Turn encoding (matches `GameStatus.get_new_state`):
    - `turn_O == True`  -> next move placed is X (1)
    - `turn_O == False` -> next move placed is O (-1)
    """
    def __init__(self, size=(700, 850)):
        """
        Initialize pygame and all controller state.

        Creates:
        - Window sizing and drawing constants
        - Button state (mode, algorithm, board size)
        - Match flow state (game_over, settings lock)
        - Running series counters
        """

        self.size = self.width, self.height = size

        # Define some colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 200, 0)
        self.RED = (200, 0, 0)
        self.GRAY = (180, 180, 180)
        self.DARK_GRAY = (60, 60, 60)
        self.BLUE = (80, 120, 255)
        self.LIGHT_BLUE = (140, 170, 255)

        self.CIRCLE_COLOR = (140, 146, 172)
        self.CROSS_COLOR = (140, 146, 172)

        # GUI layout — tall enough for title, info, rule, result, series, and buttons row
        self.TOP_PANEL_HEIGHT = 175
        self.BOARD_PIXELS = 700

        # Grid Size
        self.GRID_SIZE = 4
        self.OFFSET = 5
        self.win_length = 4  # kept for board setup /compatibility; larger-board scoring is handled in GameStatus

        # This sets the WIDTH and HEIGHT of each grid location
        self.WIDTH = self.BOARD_PIXELS / self.GRID_SIZE - self.OFFSET
        self.HEIGHT = self.BOARD_PIXELS / self.GRID_SIZE - self.OFFSET

        # This sets the margin between each cell
        self.MARGIN = 5

        # Game settings
        self.algorithm = "minimax"
        self.mode = "player_vs_ai"
        self.game_over = False
        self.settings_locked = False
        self.result_text = "Choose options, then click a cell to start"
        self.final_score = 0
        self.series = {"X": 0, "O": 0, "Draw": 0}
        self.scores = {"X": 0, "O": 0}  # cumulative board scores across rounds

        # Button placeholders
        self.buttons = {}

        # Initialize pygame ONCE here (not inside draw_game)
        pygame.init()
        self.font = pygame.font.SysFont(None, 28)
        self.small_font = pygame.font.SysFont(None, 22)
        self.big_font = pygame.font.SysFont(None, 34)

        # Create screen ONCE here
        self.screen = pygame.display.set_mode(self.size)

        self.game_reset()

    def draw_game(self):
        """
        Render the entire UI frame (top panel + buttons + empty board grid).

        This redraws a fresh background and UI chrome. It does NOT re-draw existing marks;
        marks are drawn at move time by `draw_cross` / `draw_circle`.
        """
        # FIX: removed pygame.init() and display.set_mode() from here — calling them
        # every frame was re-initializing pygame and swallowing input events.
        pygame.display.set_caption("Tic Tac Toe GUI")
        self.screen.fill(self.BLACK)

        # Top control panel
        pygame.draw.rect(self.screen, self.DARK_GRAY, (0, 0, self.width, self.TOP_PANEL_HEIGHT))

        title = self.big_font.render("Multi-Agent Tic Tac Toe", True, self.WHITE)
        self.screen.blit(title, (20, 10))

        info_text = f"Mode: {self.mode}   |   Algorithm: {self.algorithm}   |   Board: {self.GRID_SIZE}x{self.GRID_SIZE}"
        info_surface = self.small_font.render(info_text, True, self.WHITE)
        self.screen.blit(info_surface, (20, 45))

        # Rule text should match the actual game logic
        if self.GRID_SIZE == 3:
            rule_text = "Rule: First 3-in-a-row wins."
        else:
            rule_text = "Rule: Board fills completely; winner is based on total matching triplets."
        
        rule_surface = self.small_font.render(rule_text, True, self.WHITE)
        self.screen.blit(rule_surface, (20, 70))

        result_surface = self.small_font.render(
            self.result_text,
            True,
            self.GREEN if not self.game_over else self.RED
        )
        self.screen.blit(result_surface, (20, 95))

        # Series: wins per player | Scores: cumulative board score per player
        series_text = (f"Series: X={self.series['X']}  O={self.series['O']}  "
                       f"Draw={self.series['Draw']}   |   "
                       f"Score — X: {self.scores['X']}  O: {self.scores['O']}")
        series_surface = self.small_font.render(series_text, True, self.WHITE)
        self.screen.blit(series_surface, (20, 120))

        mouse_pos = pygame.mouse.get_pos()

        # Buttons row at y=148, safely below all text rows (panel height = 175)
        self.buttons = {
            "minimax": pygame.Rect(20,  148, 100, 22),
            "negamax": pygame.Rect(128, 148, 100, 22),
            "pvai":    pygame.Rect(236, 148, 110, 22),
            "pvp":     pygame.Rect(354, 148, 120, 22),
            "size3":   pygame.Rect(484, 148, 48,  22),
            "size4":   pygame.Rect(538, 148, 48,  22),
            "size5":   pygame.Rect(592, 148, 48,  22),
            "reset":   pygame.Rect(self.width - 90, 8, 78, 26),
        }

        def draw_button(key, label, selected=False):
            rect = self.buttons[key]
            hovered = rect.collidepoint(mouse_pos)
            # Visual feedback: selected > hovered > normal.
            fill = self.BLUE if selected else (self.LIGHT_BLUE if hovered else self.GRAY)
            pygame.draw.rect(self.screen, fill, rect)
            pygame.draw.rect(self.screen, self.WHITE, rect, 2)
            txt = self.small_font.render(label, True, self.BLACK)
            txt_rect = txt.get_rect(center=rect.center)
            self.screen.blit(txt, txt_rect)

        draw_button("minimax", "Minimax", selected=(self.algorithm == "minimax"))
        draw_button("negamax", "Negamax", selected=(self.algorithm == "negamax"))
        draw_button("pvai", "Human vs AI", selected=(self.mode == "player_vs_ai"))
        draw_button("pvp", "Human vs Human", selected=(self.mode == "player_vs_human"))
        draw_button("size3", "3x3", selected=(self.GRID_SIZE == 3))
        draw_button("size4", "4x4", selected=(self.GRID_SIZE == 4))
        draw_button("size5", "5x5", selected=(self.GRID_SIZE == 5))
        draw_button("reset", "Reset", selected=False)

        # Board
        cell_w = self.BOARD_PIXELS / self.GRID_SIZE
        cell_h = self.BOARD_PIXELS / self.GRID_SIZE

        for r in range(self.GRID_SIZE):
            for c in range(self.GRID_SIZE):
                rect_x = c * cell_w
                rect_y = self.TOP_PANEL_HEIGHT + r * cell_h
                pygame.draw.rect(self.screen, self.WHITE, (rect_x, rect_y, cell_w, cell_h), 2)

        pygame.display.update()

    def change_turn(self):
        """
        Update the window title to show whose turn is next.

        Note: in this codebase, `turn_O=True` means the next placed value is X (1),
        and `turn_O=False` means the next placed value is O (-1).
        """
        if self.game_state.turn_O:
            # get_new_state: 1 if turn_O else -1, so True -> X's turn
            pygame.display.set_caption("Tic Tac Toe - X's turn")
        else:
            pygame.display.set_caption("Tic Tac Toe - O's turn")

    def draw_circle(self, x, y):
        """
        YOUR CODE HERE TO DRAW THE CIRCLE FOR THE NOUGHTS PLAYER
        """
        radius = int(self.WIDTH // 3)
        pygame.draw.circle(self.screen, self.CIRCLE_COLOR, (int(x), int(y)), radius, 5)
        pygame.display.update()

    def draw_cross(self, x, y):
        """
        YOUR CODE HERE TO DRAW THE CROSS FOR THE CROSS PLAYER AT THE CELL THAT IS SELECTED VIA THE gui
        """
        offset_x = int(self.WIDTH // 3)
        offset_y = int(self.HEIGHT // 3)
        top_left = (int(x) - offset_x, int(y) - offset_y)
        bottom_right = (int(x) + offset_x, int(y) + offset_y)
        top_right = (int(x) + offset_x, int(y) - offset_y)
        bottom_left = (int(x) - offset_x, int(y) + offset_y)
        pygame.draw.line(self.screen, self.CROSS_COLOR, top_left, bottom_right, 5)
        pygame.draw.line(self.screen, self.CROSS_COLOR, top_right, bottom_left, 5)
        pygame.display.update()

    def redraw_marks(self):
        """Re-draw all marks currently on the board (needed after draw_game wipes the screen)."""
        cell_w = self.BOARD_PIXELS / self.GRID_SIZE
        cell_h = self.BOARD_PIXELS / self.GRID_SIZE
        for r in range(self.GRID_SIZE):
            for c in range(self.GRID_SIZE):
                val = self.game_state.board_state[r][c]
                if val == 0:
                    continue
                px = c * cell_w + cell_w // 2
                py = self.TOP_PANEL_HEIGHT + r * cell_h + cell_h // 2
                if val == 1:
                    self.draw_cross(px, py)
                else:
                    self.draw_circle(px, py)

    def is_game_over(self):
        """
        YOUR CODE HERE TO SEE IF THE GAME HAS TERMINATED AFTER MAKING A MOVE. YOU SHOULD USE THE IS_TERMINAL()
        FUNCTION FROM GAMESTATUS_5120.PY FILE (YOU WILL FIRST NEED TO COMPLETE IS_TERMINAL() FUNCTION)

        YOUR RETURN VALUE SHOULD BE TRUE OR FALSE TO BE USED IN OTHER PARTS OF THE GAME
        """
        """
        Wrapper around `GameStatus.is_terminal()`.

        Returns:
            True if the match has ended, else False.
        """
        result = self.game_state.is_terminal()
        return result

    def move(self, move):
        """
        Apply a move to the current match by transitioning to a new `GameStatus`.

        Args:
            move: (row, col)
        """
        self.game_state = self.game_state.get_new_state(move)
        self.board_state = self.game_state.board_state

    def play_ai(self):
        """
        YOUR CODE HERE TO CALL MINIMAX OR NEGAMAX DEPENDEING ON WHICH ALGORITHM SELECTED FROM THE GUI
        ONCE THE ALGORITHM RETURNS THE BEST MOVE TO BE SELECTED, YOU SHOULD DRAW THE NOUGHT (OR CIRCLE DEPENDING
        ON WHICH SYMBOL YOU SELECTED FOR THE AI PLAYER)

        THE RETURN VALUES FROM YOUR MINIMAX/NEGAMAX ALGORITHM SHOULD BE THE SCORE, MOVE WHERE SCORE IS AN INTEGER
        NUMBER AND MOVE IS AN X,Y LOCATION RETURNED BY THE AGENT
        """
        """
        Compute and apply the AI move (when in Human vs AI mode).

        - Human is X (1)
        - AI is O (-1)
        So for minimax, the AI calls the minimizing branch.
        """
        if self.mode == "player_vs_ai":
            # Scale depth down for larger boards to keep search time reasonable
            depth = 9 if self.GRID_SIZE == 3 else (2 if self.GRID_SIZE == 4 else 1)
            if self.algorithm == "negamax":
                # negamax base case already handles perspective in GameStatus.get_negamax_scores()
                _, ai_move = negamax(self.game_state, depth, 1)
            else:
                # AI plays O (-1), so it should minimize the score (score is positive for X, negative for O).
                _, ai_move = minimax(self.game_state, depth, False)

            if ai_move is not None:
                # AI is always the next player, so draw based on whose turn it is BEFORE applying the move.
                placing_o = not self.game_state.turn_O
                self.move(ai_move)
                cell_w = self.BOARD_PIXELS / self.GRID_SIZE
                cell_h = self.BOARD_PIXELS / self.GRID_SIZE
                px = ai_move[1] * cell_w + cell_w // 2
                py = self.TOP_PANEL_HEIGHT + ai_move[0] * cell_h + cell_h // 2
                # Convert (row, col) move into pixel center for drawing.
                if placing_o:
                    self.draw_circle(px, py)
                else:
                    self.draw_cross(px, py)

        self.change_turn()
        pygame.display.update()
        terminal = self.game_state.is_terminal()
        """ USE self.game_state.get_scores(terminal) HERE TO COMPUTE AND DISPLAY THE FINAL SCORES """
        self.game_state.get_scores(terminal)

    def game_reset(self):
        """
        Reset the board for a new match and unlock settings.

        This does not reset the series counters.
        """
        self.draw_game()
        """
        YOUR CODE HERE TO RESET THE BOARD TO VALUE 0 FOR ALL CELLS AND CREATE A NEW GAME STATE WITH NEWLY INITIALIZED
        BOARD STATE
        """
        fresh_board = np.zeros((self.GRID_SIZE, self.GRID_SIZE), dtype=int)
        self.board_state = fresh_board
        # Start with X (value 1) as the human player.
        self.game_state = GameStatus(fresh_board, True, self.win_length)
        self.game_over = False
        self.settings_locked = False
        self.result_text = "Game reset. Choose options, then click a cell to start."
        self.scores = {"X": 0, "O": 0}  # reset cumulative scores on full reset

        pygame.display.update()

    def start_next_round(self):
        """
        Start the next match using the same selected settings.

        This clears the board and keeps settings locked (until Reset is clicked).
        """
        fresh_board = np.zeros((self.GRID_SIZE, self.GRID_SIZE), dtype=int)
        self.board_state = fresh_board
        self.game_state = GameStatus(fresh_board, True, self.win_length)
        self.game_over = False
        self.result_text = "New round. Click a cell to start."
        self.draw_game()

    def play_game(self, mode="player_vs_ai"):
        """
        Main pygame loop.

        Handles:
        - Button clicks (algorithm/mode/size selection, reset)
        - Board clicks (human move + optional AI response)
        - Game-over detection and series score tracking
        """
        done = False

        clock = pygame.time.Clock()

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

                # FIX: moved game-over detection inside MOUSEBUTTONDOWN so it only
                # triggers once on a click, not every frame. Previously it was a
                # floating check that ran every loop tick, causing repeated redraws
                # and effectively freezing input.

                if event.type == pygame.MOUSEBUTTONDOWN and not done:
                    click_x, click_y = pygame.mouse.get_pos()

                    # Button clicks
                    if self.buttons["reset"].collidepoint(click_x, click_y):
                        self.game_reset()
                        continue

                    # Settings buttons are locked once a match starts.
                    # Only block top-panel button clicks — board clicks must still fall through.
                    if self.settings_locked and click_y < self.TOP_PANEL_HEIGHT:
                        continue  # ignore settings button clicks mid-game

                    if self.buttons["minimax"].collidepoint(click_x, click_y):
                        self.algorithm = "minimax"
                        self.result_text = "Algorithm set to Minimax"
                        self.draw_game()
                        continue

                    if self.buttons["negamax"].collidepoint(click_x, click_y):
                        self.algorithm = "negamax"
                        self.result_text = "Algorithm set to Negamax"
                        self.draw_game()
                        continue

                    if self.buttons["pvai"].collidepoint(click_x, click_y):
                        self.mode = "player_vs_ai"
                        self.result_text = "Mode set to Human vs AI"
                        self.draw_game()
                        continue

                    if self.buttons["pvp"].collidepoint(click_x, click_y):
                        self.mode = "player_vs_human"
                        self.result_text = "Mode set to Human vs Human"
                        self.draw_game()
                        continue

                    if self.buttons["size3"].collidepoint(click_x, click_y):
                        self.GRID_SIZE = 3
                        self.win_length = 3
                        self.WIDTH = self.BOARD_PIXELS / self.GRID_SIZE - self.OFFSET
                        self.HEIGHT = self.BOARD_PIXELS / self.GRID_SIZE - self.OFFSET
                        self.game_reset()
                        continue

                    if self.buttons["size4"].collidepoint(click_x, click_y):
                        self.GRID_SIZE = 4
                        self.win_length = 4
                        self.WIDTH = self.BOARD_PIXELS / self.GRID_SIZE - self.OFFSET
                        self.HEIGHT = self.BOARD_PIXELS / self.GRID_SIZE - self.OFFSET
                        self.game_reset()
                        continue

                    if self.buttons["size5"].collidepoint(click_x, click_y):
                        self.GRID_SIZE = 5
                        self.win_length = 5
                        self.WIDTH = self.BOARD_PIXELS / self.GRID_SIZE - self.OFFSET
                        self.HEIGHT = self.BOARD_PIXELS / self.GRID_SIZE - self.OFFSET
                        self.game_reset()
                        continue

                    # Ignore clicks in the top panel
                    if click_y < self.TOP_PANEL_HEIGHT:
                        continue

                    # Board clicks
                    if self.game_over:
                        self.start_next_round()
                        continue

                    # First board click locks settings until Reset.
                    self.settings_locked = True

                    # FIX: use cell_w/cell_h (full cell size) for coordinate math,
                    # not self.WIDTH/HEIGHT which have OFFSET subtracted and give wrong cells.
                    cell_w = self.BOARD_PIXELS / self.GRID_SIZE
                    cell_h = self.BOARD_PIXELS / self.GRID_SIZE

                    # Translate screen coordinates into board indices.
                    board_y = click_y - self.TOP_PANEL_HEIGHT
                    grid_row = int(board_y // cell_h)
                    grid_col = int(click_x // cell_w)

                    if 0 <= grid_row < self.GRID_SIZE and 0 <= grid_col < self.GRID_SIZE:
                        if self.game_state.board_state[grid_row][grid_col] == 0:
                            # Which symbol is being placed (get_new_state: 1 if turn_O else -1, so turn_O=True -> X, False -> O)
                            placing_o = not self.game_state.turn_O

                            self.move((grid_row, grid_col))

                            draw_x = grid_col * cell_w + cell_w // 2
                            draw_y = self.TOP_PANEL_HEIGHT + grid_row * cell_h + cell_h // 2

                            if placing_o:
                                self.draw_circle(draw_x, draw_y)
                            else:
                                self.draw_cross(draw_x, draw_y)

                            self.change_turn()

                            if self.is_game_over():
                                terminal = True
                                final = self.game_state.get_scores(terminal)
                                self.final_score = final
                                # Accumulate scores per player: positive = X points, negative = O points
                                if final > 0:
                                    self.scores["X"] += final
                                elif final < 0:
                                    self.scores["O"] += abs(final)
                                winner = self.game_state.winner
                                self.result_text = f"Game Over | Winner: {winner} | X score: {self.scores['X']}  O score: {self.scores['O']}"
                                pygame.display.set_caption(f"Game Over — {winner} wins!")
                                if winner in self.series:
                                    self.series[winner] += 1
                                # FIX: set game_over BEFORE draw_game so the settings_locked
                                # guard correctly allows the next board click to start a new round.
                                self.game_over = True
                                self.draw_game()
                                self.redraw_marks()  # draw_game wipes screen; restore marks
                            else:
                                # FIX: only call play_ai when mode is player_vs_ai
                                # Previously AI ran in Human vs Human mode too.
                                if self.mode == "player_vs_ai":
                                    self.play_ai()
                                    if self.is_game_over():
                                        terminal = True
                                        final = self.game_state.get_scores(terminal)
                                        self.final_score = final
                                        # Accumulate scores per player
                                        if final > 0:
                                            self.scores["X"] += final
                                        elif final < 0:
                                            self.scores["O"] += abs(final)
                                        winner = self.game_state.winner
                                        self.result_text = f"Game Over | Winner: {winner} | X score: {self.scores['X']}  O score: {self.scores['O']}"
                                        pygame.display.set_caption(f"Game Over — {winner} wins!")
                                        if winner in self.series:
                                            self.series[winner] += 1
                                        # FIX: same ordering fix — flag before draw, then restore marks
                                        self.game_over = True
                                        self.draw_game()
                                        self.redraw_marks()

            pygame.display.update()
            clock.tick(60)

        pygame.quit()


tictactoegame = RandomBoardTicTacToe()
"""
YOUR CODE HERE TO SELECT THE OPTIONS VIA THE GUI CALLED FROM THE ABOVE LINE
AFTER THE ABOVE LINE, THE USER SHOULD SELECT THE OPTIONS AND START THE GAME. 
YOUR FUNCTION PLAY_GAME SHOULD THEN BE CALLED WITH THE RIGHT OPTIONS AS SOON
AS THE USER STARTS THE GAME
"""
tictactoegame.play_game()