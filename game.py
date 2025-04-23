# game.py

from board import Board
from player import Player
from constants import KOMI, STONE_ICONS

class Game:
    def __init__(self, size=9):
        self.board             = Board(size)
        self.players           = [ Player("Black", "X"), Player("White", "O") ]
        self.to_move           = 0        # index into self.players
        self.passes            = 0        # consecutive passes
        self.komi              = KOMI
        self.message           = None     # last feedback
        self._listeners = [] # simple pub/sub list

    def add_listener(self, fn):
        """Register a callback(fn) to receive (event_name, **kwargs)."""
        self._listeners.append(fn)

    def _notify(self, event_name, **kwargs):
        for fn in self._listeners:
            fn(event_name, **kwargs)

    def current_player(self):
        return self.players[self.to_move]

    def place(self, index):
        """
        Try to place a stone for the current player at `index`.
        Returns True if successful, False if illegal.
        Sets self.message on failure.
        """
        symbol = self.current_player().symbol
        if not self.board.place_stone(index, symbol):
            self.message = "Illegal move: Ko, suicide, or occupied spot"
            self._notify("illegal_move")
            return False

        # successful move
        self.message = None
        self.passes  = 0
        self.to_move = 1 - self.to_move
        return True

    def pass_turn(self):
        """
        Current player passes.
        Returns True if this was the second consecutive pass (game over).
        """
        self.passes += 1
        if self.passes >= 2:
            return True

        self.message   = "Player passed"
        self.to_move   = 1 - self.to_move
        return False

    def final_result(self):
        """
        Returns (black_score, white_score, winner_str).
        """
        return self.board.get_final_result(self.komi)

