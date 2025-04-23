# main.py

import curses
from game import Game
from tui import GoTUI
from audio import Audio

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    game = Game(size=9)
    audio = Audio()
    game.add_listener(audio.handle_event)
    tui = GoTUI(stdscr, game)
    tui.run()

if __name__ == "__main__":
    curses.wrapper(main)

