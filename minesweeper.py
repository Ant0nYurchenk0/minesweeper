import itertools
import random
import copy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count
        self.safes = set()
        self.mines = set()
    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        return self.mines

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        return self.safes

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        self.cells.remove(cell)
        self.mines.add(cell)
        self.count=-1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        self.cells.remove(cell)
        self.safes.add(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def neighbors(self, cell):
        neighbors = set()
        for i in range (-1, 2):
            for j in range (-1, 2):
                if cell[0]+i < 0 or cell[0]+i>self.width:
                    continue 
                if cell[1]+j < 0 or cell[1]+j>self.height:
                    continue
                if i == 0 and j == 0:
                    continue
                neighbors.add((cell[0] + i, cell[1]+j))
        return neighbors
    
    def check(self, cells, count):
        new_sentence = Sentence(cells, count)
        if count == 0:
            self.safes.update(cells)
        elif len(cells) == count:
            self.mines.update(cells)
        elif not new_sentence in self.knowledge:
            self.knowledge.append(Sentence(cells, count))

    def update_knowledge(self):
        for know1 in self.knowledge:
            for know2 in self.knowledge:
                print("1")#endless cycle here!!!!!!!!
                if know1.count == 0:
                    self.safes.update(know1.cells)
                if len(know1.cells) == know1.count:
                    self.mines.update(know1.cells)
                if not know1 is know2:
                    count = 0 if know1.count-know2.count < 0 else know1.count-know2.count
                    cells = (know1.cells).difference(know2.cells)
                    self.check(cells, count)
                    count = abs(know1.count-know2.count)
                    cells = (know1.cells).intersection(know2.cells)
                    self.check(cells, count)
        if len(self.mines) != 0:
           self.knowledge.append(Sentence(self.mines, len(self.mines)))
        self.knowledge.append(Sentence(self.safes, 0))





    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.safes.add(cell)
        self.knowledge.append(Sentence(self.neighbors(cell), count)) 
        self.update_knowledge()
        a=10

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for i in range (0, self.width):
            for j in range (0, self.height):
                if not (i, j) in self.moves_made:
                    if (i, j) in self.safes:
                        self.moves_made.add((i,j))
                        return (i, j)

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possible_turns = set()
        for i in range (0, self.width-1):
            for j in range (0, self.height-1):
                if not (i, j) in self.moves_made:
                    if not (i, j) in self.mines:
                        possible_turns.add((i, j))
        turn = random.sample(possible_turns, 1)[0]
        self.moves_made.add(turn)
        return turn