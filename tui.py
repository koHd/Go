# tui.py

import curses
from constants import STONE_ICONS

class GoTUI:
    def __init__(self, stdscr, game):
        self.stdscr = stdscr
        self.game   = game
        size = game.board.size
        self.cursor = (size * size) // 2

        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
        self._compute_dimensions()

    def run(self):
        size = self._size  # safe because draw() was called once

        while True:
            self.draw()
            self.game.message = None
            key = self.stdscr.getch()

            # Navigation
            if key in (curses.KEY_RIGHT, ord("l")) and (self.cursor + 1) % size:
                self.cursor += 1
            elif key in (curses.KEY_LEFT, ord("h")) and self.cursor % size:
                self.cursor -= 1
            elif key in (curses.KEY_UP, ord("k")) and self.cursor >= size:
                self.cursor -= size
            elif key in (curses.KEY_DOWN, ord("j")) and self.cursor < size * (size - 1):
                self.cursor += size

            # Commands
            elif key in (ord(" "), ord("\n"), 10, 13):
                self.game.place(self.cursor)
            elif key in (ord("p"), ord("P")):
                if self.game.pass_turn():
                    break
            elif key in (ord("q"), ord("Q")):
                break

        # Final screen (could also be refactored similarly)
        b_score, w_score, winner = self.game.final_result()
        self.stdscr.clear()
        lines = [
            "Game Over!",
            f"Black score: {b_score}",
            f"White score: {w_score}",
            f"Winner: {winner}",
            "Press any key to exit."
        ]
        for i, line in enumerate(lines):
            y = self._h // 2 - 2 + i
            x = (self._w - len(line)) // 2
            self.stdscr.addstr(y, x, line)
        self.stdscr.refresh()
        self.stdscr.getch()

    def draw(self):
        self.stdscr.clear()
        self._draw_title()
        self._draw_column_labels()
        self._draw_scores()
        self._draw_board()
        self._draw_turn_indicator()
        self.stdscr.refresh()

    def _compute_dimensions(self):
        """Calculate and stash screen + board geometry once."""
        h, w = self.stdscr.getmaxyx()
        size   = self.game.board.size
        cell_w = 3
        board_w = (cell_w + 1) * size - 1
        board_h = 2 * size - 1
        start_y = (h // 2) - (board_h // 2)
        start_x = (w // 2) - (board_w // 2)

        self._h, self._w        = h, w
        self._size              = size
        self._cell_w            = cell_w
        self._board_h, self._board_w = board_h, board_w
        self._start_y, self._start_x = start_y, start_x

    def _draw_title(self):
        title = f"GO ({self._size}×{self._size}) – Arrows to move, Space/Enter to place, P to pass, Q to quit"
        y = self._start_y - 3
        x = max((self._w - len(title)) // 2, 0)
        self.stdscr.addstr(y, x, title)

    def _draw_column_labels(self):
        labels = [chr(ord("A") + i) for i in range(self._size)]
        y = self._start_y - 1
        for i, ch in enumerate(labels):
            x = self._start_x + i * (self._cell_w + 1) + (self._cell_w // 2)
            self.stdscr.addstr(y, x, ch)

    def _draw_scores(self):
        terr     = self.game.board.calculate_territory()
        caps     = self.game.board.captures
        black_s  = terr["X"] + caps["O"]
        white_s  = terr["O"] + caps["X"] + self.game.komi

        lines = [
            f"Black {STONE_ICONS['X']}: {black_s:.1f}  (T:{terr['X']}, C:{caps['O']})",
            f"White {STONE_ICONS['O']}: {white_s:.1f}  (T:{terr['O']}, C:{caps['X']}, K:{self.game.komi})"
        ]
        for i, line in enumerate(lines):
            x = self._w - len(line) - 2
            self.stdscr.addstr(i, x, line)

    def _draw_board(self):
        size, cw = self._size, self._cell_w
        sy, sx    = self._start_y, self._start_x

        for row in range(size):
            y = sy + row * 2
            # row label
            label = str(row + 1).rjust(2)
            self.stdscr.addstr(y, sx - 4, label)

            for col in range(size):
                idx   = row * size + col
                sym   = self.game.board.cells[idx]
                stone = STONE_ICONS.get(sym, " ")
                disp  = f"[{stone}]" if idx == self.cursor else f" {stone} "
                disp  = disp.ljust(cw)

                x = sx + col * (cw + 1)
                self.stdscr.addstr(y, x, disp)
                if col < size - 1:
                    self.stdscr.addstr(y, x + cw, "|")

            # horizontal separator
            if row < size - 1:
                sep = "+".join(["-" * cw] * size)
                self.stdscr.addstr(y + 1, sx, sep)

    def _draw_turn_indicator(self):
        y = self._start_y + self._board_h + 1
        player = self.game.current_player()
        icon   = STONE_ICONS[player.symbol]
        msg    = f"{player.name}'s turn ({icon})"
        x = (self._w - len(msg)) // 2
        self.stdscr.addstr(y, x, msg)

    def _draw_message(self):
        if not self.game.message:
            return
        y = self._start_y + self._board_h + 3
        x = (self._w - len(self.game.message)) // 2
        self.stdscr.addstr(y, x, self.game.message)


