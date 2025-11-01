from collections import deque

class BFSPathfinder:
    """
    BFS pathfinding class used by both AIs.
    Calculates the shortest path length for a player's pawn
    from its current position to the opposite goal row.
    
    NOTE: This uses BFS (Breadth-First Search), not A*.
    """

    def __init__(self, get_legal_moves_func):
        # Reference to Board.get_legal_moves(player)
        self.get_legal_moves = get_legal_moves_func

    def find_path_length(self, board, player):
        """
        Returns the length of the shortest path from the player's
        pawn position to their goal side using BFS search.
        Returns None if no path is found.
        """
        start_list = board.get_pawn_position(player)
        if start_list is None:
            return None
        start = tuple(start_list)

        # Goal row depends on player
        goal_row = 0 if player == 1 else board.size - 1

        # Queue for BFS: (position, distance)
        queue = deque([(start, 0)])
        visited = set([start])

        while queue:
            current, dist = queue.popleft()
            row, col = current

            # Goal check
            if row == goal_row:
                return dist  # Path length

            # Explore neighbors
            for neigh in self.get_legal_moves(player=player, override_pos=list(current)):
                neighbor = tuple(neigh)
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))

        # No path found
        return None