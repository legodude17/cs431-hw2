from connect4 import find_win

"""
Connect Four Player using Negamax search with alpha-beta pruning
"""
__author__ = "Joshua Bennett"
__license__ = "MIT"
__date__ = "2024-02-25"

class ComputerPlayer:
    _id: int; # player id
    _maxDepth: int; # maximum depth, aka difficulty level
    _prune: bool = True; # whether or not to use alpha-beta pruning
    # really big number for the max calculations to start at,
    # also used to represent a winning state
    _INFINITY = 999999999;
    _rack: list[list[int]]; # store the rack here so everything has access to it

    def __init__(self, id: int, difficulty_level: int):
        """
        Constructor, takes a difficulty level (likely the # of plies to look
        ahead), and a player ID that's either 1 or 2 that tells the player what
        its number is.
        """
        self._id = id
        self._maxDepth = difficulty_level

    def pick_move(self, rack):
        """
        Pick the move to make. It will be passed a rack with the current board
        layout, column-major. A 0 indicates no token is there, and 1 or 2
        indicate discs from the two players. Column 0 is on the left, and row 0 
        is on the bottom. It must return an int indicating in which column to 
        drop a disc. The player current just pauses for half a second (for 
        effect), and then chooses a random valid move.
        """
        # convert the rack to a list so we can modify it
        # while lists use more memory than tuples, we only store one rack,
        # so it doesn't matter much in the grand scheme of things
        self._rack = list([list(column) for column in rack])
        # alpha starts at -Inf and beta starts at Inf
        alpha = -self._INFINITY
        beta = self._INFINITY

        move = -1
        best = -self._INFINITY

        # Go through each column we can drop into
        for c in range(len(self._rack)):
            # If there's something in the top row in this colum, it's full, skip it
            if rack[c][-1] != 0:
                continue
            # We do the move, get it's score, then undo it
            self._do_move(c, self._id)
            # -1 means min, since the top node is max the next one is min
            score = self._calc_move(-1, 1, alpha, beta)
            self._undo_move(c)
            # if this score is better, or we don't have a move
            # the latter is for the case where the only move gaurantees a loss,
            # we still need to take it, since otherwise we'll return -1
            # and crash the runner
            if score > best or move == -1:
                move = c
                best = score
        
        return move

    def _calc_move(self, mult: int, depth: int, alpha: int, beta: int):
        """
        Calculate the score of a move, with mult indicating if this is a max (1) or min (-1) node 
        """
        # If we've reached the maximum depth,
        # then the score is whatever the evaluation function says
        if depth >= self._maxDepth:
            return self._eval()
        
        rack = self._rack
        best = -self._INFINITY
        # Go through each column we can drop into
        for c in range(len(rack)):
            # If there's something in the top row in this colum, it's full, skip it
            if rack[c][-1] != 0:
                continue
            # Do this move, then check how good it is, then undo it
            # player: If we are in a max node (mult==1), then the current player is us
            # otherwise, it's the other player
            self._do_move(c, self._id if mult == 1 else 3 - self._id)
            # If this state is winning for either player, then just evaluate it. Otherwise, recurse
            # This is because if we recurse into winning states we may get the wrong evaluation
            # if the move after the winning one also "wins"
            # Since the evaluation function doesn't stop when it finds four in a row
            # This also helps a bit with performance, especially near the end of the game
            # where nearly every state leads to a win in a few plies
            # Note: I was unsure if we're allowed to import helpers from the connect4 program,
            # but I figured if I didn't import it I'd just end up copying it, which accomplishes the same thing
            if find_win(rack, c):
                score = mult * self._eval()
            else:
                # Recurse into the next ply, flip mult so we alternate min and max nodes
                # We also increase the depth and pass alpha and beta for the pruning
                score = mult * self._calc_move(-mult, depth + 1, alpha, beta)
            self._undo_move(c)
            # Update the best score if this one is better
            if score > best:
                best = score
            # Pruning
            if self._prune:
                # If we are in a max node, update alpha and check beta
                if mult == 1:
                    if score > alpha:
                        alpha = score
                    if score >= beta:
                        break # beta cutoff
                # Otherwise, update beta and check alpha
                else:
                    if -score < beta:
                        beta = -score
                    if -score <= alpha:
                        break # alpha cutoff

        return mult * best
            
    def _do_move(self, c, player):
        """
        Execute a move, aka drop a tile for player into column c
        """
        rack = self._rack
        # Find the lowest unoccupied place in column c, put player into it
        # We could speed this up by caching the top of each "stack",
        # but the rack generally isn't going to be tall enough
        # to make this take a large amount of time
        # In addition, the vast majority of the time is spent
        # on the evaluation function anyway, not doing and undoing moves
        for i in range(len(rack[c])):
            if rack[c][i] == 0:
                rack[c][i] = player
                return

    def _undo_move(self, c):
        """
        Undo a move, basically just remove the top disk in column c
        """
        rack = self._rack
        # We could speed this up by caching the top of each "stack",
        # but the rack generally isn't going to be tall enough
        # to make this take a large amount of time
        # In addition, the vast majority of the time is spent
        # on the evaluation function anyway, not doing and undoing moves
        for i in range(len(rack[c]) - 1, -1, -1):
            if rack[c][i] != 0:
                rack[c][i] = 0
                return

    def _eval(self):
        """
        Evaluate the current rack, by finding all the quartets,
        evaluating them, and summing up all the scores
        """
        score = 0
        rack = self._rack

        # Vertical quartets
        for column in rack:
            for i in range(len(column) - 3):
                score += self._checkQuartet(column[i:i+4])

        # Horizontal quartets
        for c in range(len(rack) - 3):
            for i in range(len(rack[c])):
                score += self._checkQuartet([row[i] for row in rack[c:c+4]])

        # Diagonal quartets (up-right)
        for c in range(len(rack) - 3):
            for r in range(len(rack[c]) - 3):
                quartet = []
                for i in range(4):
                    quartet.append(rack[c + i][r + i])
                score += self._checkQuartet(quartet)

        # Diagonal quartets (down-right)
        for c in range(len(rack) - 3):
            for r in range(len(rack[c]) - 1, 2, -1):
                quartet = []
                for i in range(4):
                    quartet.append(rack[c + i][r - i])
                score += self._checkQuartet(quartet)

        return score
    
    def _checkQuartet(self, quartet):
        """
        Check a quartet for how it impacts the score
        """

        # Count the number of disks for me and the opponent
        mine = 0
        enemy = 0
        for v in quartet:
            if v == self._id:
                mine += 1
            elif v != 0:
                enemy += 1

        # If neither player or both player has disks here, it's worthless
        if mine == 0 and enemy == 0:
            return 0
        if mine > 0 and enemy > 0:
            return 0
        
        # Here, we assume only one player has disks, since we already checked that
        mult = 1
        count = mine
        # If the enemy has disks, then we count theirs and then negate the result
        if enemy > 0:
            mult = -1
            count = enemy

        score = 0
        if count == 4:
            # 4 in a row means you win, so infinite value
            score = self._INFINITY
        elif count == 3:
            score = 100
        elif count == 2:
            score = 10
        elif count == 1:
            score = 1

        return mult * score
