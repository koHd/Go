class Board:
    def __init__(self, size=9):
        self.size = size
        self.cells = [" "] * (size * size)
        self.previous_state = None  # for Ko rule
        self.captures = {"X": 0, "O": 0}

    def place_stone(self, index, symbol):
        if self.cells[index] != " ":
            return False  # Illegal: cell already occupied

        current_state = self.cells.copy()  # Save current state for comparison

        self.cells[index] = symbol  # Tentatively place the stone

        # Check and remove captured enemy stones
        for neighbor in self.get_adjacent_indices(index):
            if self.cells[neighbor] not in [" ", symbol]:  # Opponent stone
                group = self.get_group(neighbor)
                if self.get_liberties(group) == 0:
                    self.remove_group(group)

        # ! Suicide check: the place stone must not die immediately
        group = self.get_group(index)
        if self.get_liberties(group) == 0:
            self.cells = current_state # revert move
            return False

        # Ko check: if resulting state == previous state, it's an illegal move
        if self.previous_state and self.cells == self.previous_state:
            self.cells = current_state  # Revert
            return False  # Ko violation

        self.previous_state = current_state  # Save state for next Ko check
        return True  # Move successful

    def get_adjacent_indices(self, index):
        row, col = divmod(index, self.size)
        neighbors = []
        if row > 0:
            neighbors.append(index - self.size)
        if row < self.size - 1:
            neighbors.append(index + self.size)
        if col > 0:
            neighbors.append(index - 1)
        if col < self.size - 1:
            neighbors.append(index + 1)
        return neighbors

    def get_group(self, index):
        symbol = self.cells[index]
        visited = set()
        to_visit = [index]

        while to_visit:
            current = to_visit.pop()
            if current not in visited:
                visited.add(current)
                for neighbor in self.get_adjacent_indices(current):
                    if self.cells[neighbor] == symbol and neighbor not in visited:
                        to_visit.append(neighbor)
        return visited

    def get_liberties(self, group):
        liberties = set()
        for idx in group:
            for neighbor in self.get_adjacent_indices(idx):
                if self.cells[neighbor] == " ":
                    liberties.add(neighbor)
        return len(liberties)

    def remove_group(self, group):
        if not group:
            return
        symbol = self.cells[next(iter(group))]
        for idx in group:
            self.cells[idx] = " "
        self.captures[symbol] += len(group)

    def is_full(self):
        return " " not in self.cells

    def calculate_territory(self):
        visited = set()
        territory = {"X": 0, "O": 0}

        for idx in range(len(self.cells)):
            if self.cells[idx] != " " or idx in visited:
                continue

            region = self.get_empty_region(idx)
            border_symbols = set()

            for cell in region:
                visited.add(cell)
                for neighbor in self.get_adjacent_indices(cell):
                    if self.cells[neighbor] in ["X", "O"]:
                        border_symbols.add(self.cells[neighbor])

            if len(border_symbols) == 1:
                owner = border_symbols.pop()
                territory[owner] += len(region)

        return territory

    def get_empty_region(self, start):
        to_visit = [start]
        region = set()

        while to_visit:
            idx = to_visit.pop()
            if idx not in region and self.cells[idx] == " ":
                region.add(idx)
                to_visit.extend(
                        neighbor for neighbor in self.get_adjacent_indices(idx)
                        if neighbor not in region
                )

        return region

    def get_scores(self, komi):
        territory = self.calculate_territory()
        captures = self.captures

        black = territory["X"] + captures["O"]
        white = territory["O"] + captures["X"] + komi

        return black, white

    def get_final_result(self, komi):
        """
        Returns (black_score, white_score, winner_str)
        where winner_str is "Black", "White", or "Draw".
        """
        b, w = self.get_scores(komi)
        if b > w:
            winner = "Black"
        elif w > b:
            winner = "White"
        else:
            winner = "Draw"
        return b, w, winner

