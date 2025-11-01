from ai.pathfinding import BFSPathfinder
import copy

class Board:
    def __init__(self):
        self.size = BOARD_SIZE
        self.p1_pos = [self.size - 1, self.size // 2]
        self.p2_pos = [0, self.size // 2]
        self.walls = []
        self.p1_walls_remaining = 10
        self.p2_walls_remaining = 10

    def get_pawn_position(self, player):
        return self.p1_pos if player == 1 else self.p2_pos

    def get_opponent_position(self, player):
        return self.p2_pos if player == 1 else self.p1_pos

    def get_legal_moves(self, player, override_pos=None):
        pos = override_pos or self.get_pawn_position(player)
        opp = self.get_opponent_position(player)
        return get_legal_moves(pos, opp, self.walls)

    def is_valid_wall(self, row, col, orientation):
        if not is_valid_wall(row, col, orientation, self.walls):
            return False
        # Temporarily add wall and check if paths to goals still exist for both players
        temp_walls = self.walls + [(row, col, orientation, 0)]
        def temp_legal(player, override_pos=None):
            pos = override_pos or self.get_pawn_position(player)
            opp = self.get_opponent_position(player)
            return get_legal_moves(pos, opp, temp_walls)
        bfs = BFSPathfinder(temp_legal)
        if bfs.find_path_length(self, 1) is None or bfs.find_path_length(self, 2) is None:
            return False
        return True

    def place_wall(self, player, row, col, orientation):
        if self.is_valid_wall(row, col, orientation):
            self.walls.append((row, col, orientation, player))
            if player == 1:
                self.p1_walls_remaining -= 1
            else:
                self.p2_walls_remaining -= 1
            return True
        return False

    def get_walls_remaining(self, player):
        return self.p1_walls_remaining if player == 1 else self.p2_walls_remaining

    def apply_move(self, player, move):
        if player == 1:
            self.p1_pos = list(move)
        else:
            self.p2_pos = list(move)

    def clone(self):
        return copy.deepcopy(self)

BOARD_SIZE = 9

def is_blocked(r1, c1, r2, c2, walls):
    """
    Check if movement from (r1,c1) to (r2,c2) is blocked by a wall.
    
    FIXED: Corrected wall blocking logic
    
    H wall at (row, col):
      - Blocks vertical movement crossing the horizontal line at row
      - Affects columns col and col+1
    
    V wall at (row, col):
      - Blocks horizontal movement crossing the vertical line at col
      - Affects rows row and row+1
    """
    for (wall_row, wall_col, orientation, _) in walls:
        if orientation == 'H':
            # H wall blocks vertical movement
            if abs(r1 - r2) == 1 and c1 == c2:  # Vertical move
                # Moving down (r2 > r1) or up (r2 < r1)
                crossing_row = max(r1, r2)  # The row boundary being crossed
                if crossing_row == wall_row:
                    # Check if the column is affected by this wall
                    if c1 == wall_col or c1 == wall_col + 1:
                        return True
        elif orientation == 'V':
            # V wall blocks horizontal movement
            if abs(c1 - c2) == 1 and r1 == r2:  # Horizontal move
                # Moving right (c2 > c1) or left (c2 < c1)
                crossing_col = max(c1, c2)  # The column boundary being crossed
                if crossing_col == wall_col:
                    # Check if the row is affected by this wall
                    if r1 == wall_row or r1 == wall_row + 1:
                        return True
    return False

def get_legal_moves(pawn_pos, opponent_pos, walls):
    moves = []
    r, c = pawn_pos
    r2, c2 = opponent_pos

    directions = [(1,0), (-1,0), (0,1), (0,-1)]  # down, up, right, left
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
            if not is_blocked(r, c, nr, nc, walls):
                if [nr, nc] == opponent_pos:
                    # Adjacent to opponent - jump rules apply
                    jr, jc = nr + dr, nc + dc
                    # Check straight jump
                    straight_jump_possible = (0 <= jr < BOARD_SIZE and 0 <= jc < BOARD_SIZE 
                                             and not is_blocked(nr, nc, jr, jc, walls))
                    
                    if straight_jump_possible:
                        # Straight jump over opponent
                        moves.append([jr, jc])
                    else:
                        # L-shaped jump: perpendicular moves from opponent's position
                        perp_dirs = [(0,1), (0,-1)] if dc == 0 else [(1,0), (-1,0)]
                        for pdr, pdc in perp_dirs:
                            side_r, side_c = nr + pdr, nc + pdc
                            if 0 <= side_r < BOARD_SIZE and 0 <= side_c < BOARD_SIZE:
                                if not is_blocked(nr, nc, side_r, side_c, walls):
                                    moves.append([side_r, side_c])
                else:
                    # Normal move (no opponent in the way)
                    moves.append([nr, nc])
    return moves

def is_valid_wall(row, col, orientation, walls):
    """
    FIXED: Correct wall validation to prevent overlapping and intersecting walls
    """
    # Check boundaries
    if row < 0 or row >= BOARD_SIZE - 1 or col < 0 or col >= BOARD_SIZE - 1:
        return False

    for (wr, wc, wo, _) in walls:
        # 1. Check for EXACT duplicate (same position and orientation)
        if wr == row and wc == col and wo == orientation:
            return False
        
        # 2. Check for CROSSING at same position (H and V at same cell)
        if wr == row and wc == col and wo != orientation:
            return False
        
        # 3. FIXED: Check for overlapping adjacent walls of SAME orientation
        if orientation == 'H' and wo == 'H':
            # Both horizontal walls
            # H wall at (row, col) occupies space between cols [col, col+2)
            # Check if they're on same row and overlap
            if wr == row:
                # Check if segments overlap
                # Wall 1: [col, col+2), Wall 2: [wc, wc+2)
                if not (col + 2 <= wc or wc + 2 <= col):
                    # Segments overlap!
                    return False
        
        elif orientation == 'V' and wo == 'V':
            # Both vertical walls
            # V wall at (row, col) occupies space between rows [row, row+2)
            # Check if they're on same column and overlap
            if wc == col:
                # Check if segments overlap
                # Wall 1: [row, row+2), Wall 2: [wr, wr+2)
                if not (row + 2 <= wr or wr + 2 <= row):
                    # Segments overlap!
                    return False
        
        # 4. FIXED: Check for perpendicular intersection (H crosses V)
        elif orientation == 'H' and wo == 'V':
            # New H wall at (row, col) spans columns [col, col+2) at row boundary
            # Existing V wall at (wr, wc) spans rows [wr, wr+2) at col boundary
            # They intersect if:
            # - V wall's column (wc) is within H wall's column range
            # - H wall's row is within V wall's row range
            if col < wc < col + 2 and wr < row < wr + 2:
                return False
        
        elif orientation == 'V' and wo == 'H':
            # New V wall at (row, col) spans rows [row, row+2) at col boundary
            # Existing H wall at (wr, wc) spans columns [wc, wc+2) at row boundary
            # They intersect if:
            # - H wall's column (wc) is within V wall's column range
            # - V wall's row is within H wall's row range
            if wc < col < wc + 2 and row < wr < row + 2:
                return False
    
    return True

def apply_move(pawn_pos, move):
    return [move[0], move[1]]

def apply_wall(walls, wall_action):
    new_walls = walls.copy()
    new_walls.append(wall_action)
    return new_walls