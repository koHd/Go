# tui.py

import curses
from constants import STONE_ICONS

class GoTUI:
    def __init__(self, stdscr, game):
        self.stdscr = stdscr
        self.game   = game
        # start cursor in roughly the center
        size = game.board.size
        self.cursor = (size * size) // 2

        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)

    def draw(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()

        size        = self.game.board.size
        cell_w      = 3
        board_w     = (cell_w + 1) * size - 1
        board_h     = 2 * size - 1
        start_y     = (h // 2) - (board_h // 2)
        start_x     = (w // 2) - (board_w // 2)

        # ── COLUMN LABELS ────────────────────────────────────────────────
        # e.g.   A   B   C   … above the top row of cells
        col_labels = [chr(ord("A") + i) for i in range(size)]
        label_row = start_y - 1
        for idx, ch in enumerate(col_labels):
            # center the label over the cell
            x = start_x + idx * (cell_w + 1) + (cell_w // 2)
            self.stdscr.addstr(label_row, x, ch)

            # --- live score display ---
            terr    = self.game.board.calculate_territory()
            caps    = self.game.board.captures
            black_s = terr["X"] + caps["O"]
            white_s = terr["O"] + caps["X"] + self.game.komi

        score_lines = [
            f"Black {STONE_ICONS['X']}: {black_s:.1f} (T:{terr['X']},C:{caps['O']})",
            f"White {STONE_ICONS['O']}: {white_s:.1f} (T:{terr['O']},C:{caps['X']},K:{self.game.komi})"
        ]
        for i, line in enumerate(score_lines):
            self.stdscr.addstr(i, w - len(line) - 2, line)

        # --- title ---
        title = f"GO ({size}x{size}) – Arrows to move, Space/Enter to place, P to pass, Q to quit"
        self.stdscr.addstr(start_y - 3, max((w - len(title)) // 2, 0), title)

        # --- board drawing ---
        for row in range(size):
            y = start_y + row * 2
            row_label = str(row + 1)
            self.stdscr.addstr(y, start_x - 3, row_label.rjust(2))

            for col in range(size):
                idx    = row * size + col
                sym    = self.game.board.cells[idx]
                stone  = STONE_ICONS.get(sym, " ")
                if idx == self.cursor:
                    disp = f"[{stone}]"
                else:
                    disp = f" {stone} "
                disp = disp.ljust(cell_w)

                x = start_x + col * (cell_w + 1)
                self.stdscr.addstr(y, x, disp)
                if col < size - 1:
                    self.stdscr.addstr(y, x + cell_w, "|")

            if row < size - 1:
                sep = "+".join(["-" * cell_w] * size)
                self.stdscr.addstr(start_y + row * 2 + 1, start_x, sep)

        # --- turn indicator ---
        player   = self.game.current_player()
        turn_icon = STONE_ICONS[player.symbol]
        turn_msg  = f"{player.name}'s turn ({turn_icon})"
        self.stdscr.addstr(start_y + board_h + 1,
                           (w - len(turn_msg)) // 2,
                           turn_msg)

        # --- optional message ---
        msg = self.game.message
        if msg:
            self.stdscr.addstr(start_y + board_h + 3,
                               (w - len(msg)) // 2,
                               msg)

        self.stdscr.refresh()

    def run(self):
        while True:
            self.draw()
            self.game.message = None

            key = self.stdscr.getch()
            size = self.game.board.size

            # navigation
            if key in (curses.KEY_RIGHT, ord("l")) and (self.cursor + 1) % size:
                self.cursor += 1
            elif key in (curses.KEY_LEFT, ord("h")) and (self.cursor % size):
                self.cursor -= 1
            elif key in (curses.KEY_UP, ord("k")) and self.cursor >= size:
                self.cursor -= size
            elif key in (curses.KEY_DOWN, ord("j")) and self.cursor < size * (size - 1):
                self.cursor += size

            # commands
            elif key in (ord(" "), ord("\n"), 10, 13):
                self.game.place(self.cursor)
            elif key in (ord("p"), ord("P")):
                if self.game.pass_turn():
                    break
            elif key in (ord("q"), ord("Q")):
                break

        # final screen
        b_score, w_score, winner = self.game.final_result()
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        lines = [
            "Game Over!",
            f"Black score: {b_score}",
            f"White score: {w_score}",
            f"Winner: {winner}",
            "Press any key to exit."
        ]
        for i, line in enumerate(lines):
            self.stdscr.addstr(h//2 - 2 + i, (w - len(line))//2, line)
        self.stdscr.refresh()
        self.stdscr.getch()

