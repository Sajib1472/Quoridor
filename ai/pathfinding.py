import heapq

class AStarPathfinder:
    def __init__(self, get_legal_moves_func):
        # Reference to Board.get_legal_moves(player)
        self.get_legal_moves = get_legal_moves_func

    def manhattan_heuristic(self, position, goal_row):
        return abs(position[0] - goal_row)

    def find_path_length(self, board, player):
        result = self._astar_search(board, player, return_path=False)
        return result  # Returns distance or None

    def find_path(self, board, player):
        result = self._astar_search(board, player, return_path=True)
        return result  # Returns path list or None

    def _astar_search(self, board, player, return_path=False):
        start_list = board.get_pawn_position(player)
        if start_list is None:
            return None
        start = tuple(start_list)

        # Goal row depends on player
        goal_row = 0 if player == 1 else board.size - 1

        h_start = self.manhattan_heuristic(start, goal_row)
        open_set = [(h_start, 0, start)]
        
        # Track visited nodes and their g_scores
        g_scores = {start: 0}
        
        # For path reconstruction
        came_from = {}

        while open_set:
            # Get node with lowest f_score
            f_current, g_current, current = heapq.heappop(open_set)
            row, col = current

            # Goal check
            if row == goal_row:
                if return_path:
                    # Reconstruct path
                    path = [current]
                    while current in came_from:
                        current = came_from[current]
                        path.append(current)
                    path.reverse()
                    return path
                else:
                    return g_current  # Path length

            # Explore neighbors
            for neigh in self.get_legal_moves(player=player, override_pos=list(current)):
                neighbor = tuple(neigh)
                tentative_g = g_current + 1  # Cost to move is always 1

                # If this path to neighbor is better than any previous one
                if neighbor not in g_scores or tentative_g < g_scores[neighbor]:
                    # Update path
                    came_from[neighbor] = current
                    g_scores[neighbor] = tentative_g
                    
                    # Calculate f_score and add to open set
                    h_score = self.manhattan_heuristic(neighbor, goal_row)
                    f_score = tentative_g + h_score
                    heapq.heappush(open_set, (f_score, tentative_g, neighbor))

        # No path found
        return None


# Backward compatibility alias
BFSPathfinder = AStarPathfinder