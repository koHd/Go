# audio.py
import curses

class Audio:
    def handle_event(self, event_name, **kwargs):
        """
        Called by Game whenever a named event occurs.
        """
        if event_name == "illegal_move":
            curses.beep()
