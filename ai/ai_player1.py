# ai/ai_player1.py
import math
import random
from ai.pathfinding import AStarPathfinder

class FuzzySystem:

    def __init__(self):
        self.very_close_threshold = 1.5
        self.close_threshold = 3.5
        self.moderate_threshold = 6.0

        self.very_low_walls = 1
        self.low_walls = 3
        self.medium_walls = 6
        self.high_walls = 8

        self.aggression = 0.5
        self.caution = 0.6

    def fuzzify_path_diff(self, diff):
        very_close = max(0, 1 - abs(diff) / self.very_close_threshold)
        close = max(0, 1 - abs(diff) / self.close_threshold) if abs(diff) < self.close_threshold else 0

        if diff > 0:
            slightly_ahead = max(0, min(1, diff / 2.5))
            ahead = max(0, min(1, (diff - 2) / 4.0)) if diff > 2 else 0
            far_ahead = max(0, min(1, (diff - 5) / 3.0)) if diff > 5 else 0
        else:
            slightly_ahead = ahead = far_ahead = 0

        if diff < 0:
            slightly_behind = max(0, min(1, -diff / 2.5))
            behind = max(0, min(1, (-diff - 2) / 4.0)) if diff < -2 else 0
            far_behind = max(0, min(1, (-diff - 5) / 3.0)) if diff < -5 else 0
        else:
            slightly_behind = behind = far_behind = 0

        return {
            "very_close": very_close,
            "close": close,
            "slightly_ahead": slightly_ahead,
            "ahead": ahead,
            "far_ahead": far_ahead,
            "slightly_behind": slightly_behind,
            "behind": behind,
            "far_behind": far_behind
        }

    def fuzzify_walls(self, remaining):
        very_low = max(0, 1 - remaining / 2.0)
        low = max(0, min(1, (3 - remaining) / 3.0)) if remaining < 4 else 0
        medium = max(0, 1 - abs(remaining - 5) / 3.0)
        high = max(0, min(1, (remaining - 4) / 4.0)) if remaining > 4 else 0
        very_high = max(0, min(1, (remaining - 7) / 3.0)) if remaining > 7 else 0

        return {
            "very_low": very_low,
            "low": low,
            "medium": medium,
            "high": high,
            "very_high": very_high
        }

    def apply_rules(self, path_fuzzy, wall_fuzzy):
        move_strength = 0
        wall_strength = 0

        # DEFENSIVE RULES
        wall_strength = max(wall_strength,
                           min(path_fuzzy["far_behind"], wall_fuzzy["high"]) * 0.9)
        wall_strength = max(wall_strength, path_fuzzy["behind"] * 0.7)
        wall_strength = max(wall_strength,
                           min(path_fuzzy["slightly_behind"], wall_fuzzy["medium"]) * 0.5)

        # AGGRESSIVE RULES
        move_strength = max(move_strength,
                           min(path_fuzzy["far_ahead"], wall_fuzzy["high"]) * 0.85)
        move_strength = max(move_strength, path_fuzzy["ahead"] * 0.75)
        move_strength = max(move_strength, path_fuzzy["slightly_ahead"] * 0.6)

        # SITUATIONAL RULES
        move_strength = max(move_strength,
                           min(path_fuzzy["close"], wall_fuzzy["medium"]) * 0.65)
        move_strength = max(move_strength, wall_fuzzy["very_low"] * 0.8)
        wall_strength = max(wall_strength,
                           min(path_fuzzy["close"], wall_fuzzy["very_high"]) * 0.4)
        move_strength = max(move_strength, path_fuzzy["very_close"] * 0.5)

        move_strength *= (1.0 + self.aggression * 0.3)
        wall_strength *= (1.0 + self.caution * 0.2)

        return move_strength, wall_strength

    def decide_action(self, path_diff, walls_remaining):
        """Fuzzy decision with human-like uncertainty"""
        path_fuzzy = self.fuzzify_path_diff(path_diff)
        wall_fuzzy = self.fuzzify_walls(walls_remaining)
        move_strength, wall_strength = self.apply_rules(path_fuzzy, wall_fuzzy)

        diff = abs(move_strength - wall_strength)
        if diff < 0.2:
            uncertainty = random.uniform(-0.15, 0.15)
            move_strength += uncertainty

        action = "move" if move_strength >= wall_strength * 0.95 else "wall"
        return action, move_strength, wall_strength

class AIPlayer1:
    """
    AI Player 1 uses Minimax + Alpha-Beta Pruning + Fuzzy Logic + A* Pathfinding
    """

    def __init__(self, player_id, max_depth=3):
        self.player_id = player_id
        self.max_depth = max_depth
        self.pathfinder = AStarPathfinder(lambda p, **kwargs: [])
        self.fuzzy = FuzzySystem()
        self.recent_positions = []
        self.max_history = 6

    def choose_move(self, board, return_fuzzy=False):
        self.pathfinder.get_legal_moves = board.get_legal_moves
        p1_dist = self.pathfinder.find_path_length(board, 1)
        p2_dist = self.pathfinder.find_path_length(board, 2)

        # Handle None distances (no path found)
        if p1_dist is None:
            p1_dist = 999
        if p2_dist is None:
            p2_dist = 999

        path_diff = (p2_dist - p1_dist) if self.player_id == 1 else (p1_dist - p2_dist)
        walls_left = board.get_walls_remaining(self.player_id)

        opponent_id = 3 - self.player_id
        opponent_dist = p2_dist if self.player_id == 1 else p1_dist
        my_dist = p1_dist if self.player_id == 1 else p2_dist

        # CRITICAL: Opponent can win in 1 move
        if opponent_dist is not None and opponent_dist != 999 and opponent_dist == 1 and walls_left > 0:
            wall = self.choose_wall_placement(board)
            if wall is not None:
                fuzzy_value = (0.0, 1.0)
                if return_fuzzy:
                    return ("wall", wall), fuzzy_value
                else:
                    return ("wall", wall)
            else:
                legal_moves = board.get_legal_moves(self.player_id)
                if legal_moves:
                    goal_row = 0 if self.player_id == 1 else board.size - 1
                    winning_move = None
                    for m in legal_moves:
                        if m[0] == goal_row:
                            winning_move = m
                            break

                    if winning_move:
                        move = winning_move
                    else:
                        best_dist = float('inf')
                        best_move = legal_moves[0]
                        for m in legal_moves:
                            dist = abs(m[0] - goal_row)
                            if dist < best_dist:
                                best_dist = dist
                                best_move = m
                        move = best_move

                    fuzzy_value = (1.0, 0.0)
                    if return_fuzzy:
                        return ("move", move), fuzzy_value
                    else:
                        return ("move", move)
                else:
                    return None

        # URGENT: Opponent is 2 moves away
        if (opponent_dist is not None and opponent_dist != 999 and opponent_dist == 2 and walls_left > 0 and
            my_dist is not None and my_dist != 999 and my_dist >= opponent_dist):
            wall = self.choose_wall_placement(board)
            if wall is not None:
                fuzzy_value = (0.0, 1.0)
                if return_fuzzy:
                    return ("wall", wall), fuzzy_value
                else:
                    return ("wall", wall)
            else:
                # can't place a wall — continue to fuzzy decision below
                pass

        # Fuzzy decision
        action_type, move_strength, wall_strength = self.fuzzy.decide_action(path_diff, walls_left)
        fuzzy_value = (move_strength, wall_strength)

        move = None
        preferred_type = action_type
        for attempt in [preferred_type, "wall" if preferred_type == "move" else "move"]:
            if attempt == "move":
                legal_moves = board.get_legal_moves(self.player_id)
                if legal_moves:
                    pos = self.choose_pawn_move(board)
                    if pos is not None:
                        move = ("move", pos)
                        break
            elif attempt == "wall" and walls_left > 0:
                wall = self.choose_wall_placement(board)
                if wall is not None:
                    move = ("wall", wall)
                    break

        if move is None:
            return None

        if return_fuzzy:
            return move, fuzzy_value
        else:
            return move

    def choose_pawn_move(self, board):
        legal_moves = board.get_legal_moves(self.player_id)
        if not legal_moves:
            return None

        goal_row = 0 if self.player_id == 1 else board.size - 1
        
        # Check for immediate winning move
        for move in legal_moves:
            if move[0] == goal_row:
                return move

        current_pos = tuple(board.get_pawn_position(self.player_id))

        # Get the optimal path using A*
        self.pathfinder.get_legal_moves = board.get_legal_moves
        optimal_path = self.pathfinder.find_path(board, self.player_id)
        
        # If we have a clear optimal path, follow it
        if optimal_path and len(optimal_path) > 1:
            # The next position in the optimal path
            next_pos_in_path = list(optimal_path[1])
            
            # Check if this move is legal and not a recent repetition
            if next_pos_in_path in legal_moves:
                move_tuple = tuple(next_pos_in_path)
                # Allow following path unless we've been there very recently
                if move_tuple not in self.recent_positions[-2:]:
                    self.recent_positions.append(move_tuple)
                    if len(self.recent_positions) > self.max_history:
                        self.recent_positions.pop(0)
                    return next_pos_in_path

        # Fallback: Use minimax for complex situations or when path following isn't ideal
        best_score = -math.inf
        candidates = []
        for move in legal_moves:
            new_board = board.clone()
            new_board.apply_move(self.player_id, move)
            score = self.minimax(new_board, depth=self.max_depth - 1,
                             alpha=-math.inf, beta=math.inf,
                             maximizing=False)

            move_tuple = tuple(move)
            if move_tuple in self.recent_positions:
                repetition_penalty = 5 * (self.max_history - self.recent_positions.index(move_tuple))
                score -= repetition_penalty

            distance_to_goal = abs(move[0] - goal_row)
            current_distance = abs(current_pos[0] - goal_row)

            if distance_to_goal < current_distance:
                tiebreaker = 1.0
            elif distance_to_goal > current_distance:
                if current_distance <= 3:
                    tiebreaker = -3.0
                else:
                    tiebreaker = -1.5
            else:
                tiebreaker = -distance_to_goal * 0.05

            score += tiebreaker

            if score > best_score:
                best_score = score
                candidates = [move]
            elif score == best_score:
                candidates.append(move)

        if candidates:
            chosen_move = random.choice(candidates)
            self.recent_positions.append(tuple(chosen_move))
            if len(self.recent_positions) > self.max_history:
                self.recent_positions.pop(0)
            return chosen_move
        return None

    def choose_wall_placement(self, board):
        """Choose wall placement with improved urgency and blocking logic"""
        best_score = -math.inf
        candidates = []

        self.pathfinder.get_legal_moves = board.get_legal_moves
        opponent_id = 3 - self.player_id
        opponent_dist = self.pathfinder.find_path_length(board, opponent_id)
        my_dist = self.pathfinder.find_path_length(board, self.player_id)

        opp_pos = board.get_pawn_position(opponent_id)
        if opp_pos is None:
            return None

        opponent_goal_row = 0 if opponent_id == 1 else board.size - 1
        is_critical = opponent_dist is not None and opponent_dist != 999 and opponent_dist == 1
        is_urgent = opponent_dist is not None and opponent_dist != 999 and opponent_dist == 2

        if is_critical:
            opp_legal_moves = board.get_legal_moves(opponent_id)
            winning_moves = [m for m in opp_legal_moves if m[0] == opponent_goal_row]

            if winning_moves:
                for row in range(board.size - 1):
                    for col in range(board.size - 1):
                        for orient in ['H', 'V']:
                            if board.is_valid_wall(row, col, orient):
                                new_board = board.clone()
                                new_board.place_wall(self.player_id, row, col, orient)
                                self.pathfinder.get_legal_moves = new_board.get_legal_moves
                                new_opp_dist = self.pathfinder.find_path_length(new_board, opponent_id)

                                if new_opp_dist is not None and new_opp_dist > 1:
                                    score = 1000

                                    if score > best_score:
                                        best_score = score
                                        candidates = [(row, col, orient)]
                                    elif score == best_score:
                                        candidates.append((row, col, orient))

                if candidates:
                    chosen = random.choice(candidates)
                    return chosen
                else:
                    return None

        opponent_path = self._find_opponent_path(board, opponent_id)

        if is_urgent:
            search_positions = self._get_urgent_wall_positions(board, opp_pos, opponent_path)
        else:
            search_positions = self._get_strategic_wall_positions(board, opp_pos, opponent_path)

        min_path_increase = 0 if (is_critical or is_urgent) else 1

        for row, col in search_positions:
            for orient in ['H', 'V']:
                if board.is_valid_wall(row, col, orient):
                    new_board = board.clone()
                    new_board.place_wall(self.player_id, row, col, orient)
                    self.pathfinder.get_legal_moves = new_board.get_legal_moves
                    new_opp_dist = self.pathfinder.find_path_length(new_board, opponent_id)

                    if opponent_dist is None or new_opp_dist is None:
                        continue

                    path_increase = new_opp_dist - opponent_dist
                    if path_increase <= min_path_increase:
                        continue

                    score = path_increase * 10
                    if opponent_path and self._is_wall_on_path(row, col, orient, opponent_path):
                        score += 15

                    dist_to_opp = abs(row - opp_pos[0]) + abs(col - opp_pos[1])
                    if dist_to_opp <= 2:
                        score += 5

                    if is_urgent:
                        score *= 2

                    if score > best_score:
                        best_score = score
                        candidates = [(row, col, orient)]
                    elif score == best_score:
                        candidates.append((row, col, orient))

        if candidates:
            return random.choice(candidates)
        return None

    def _find_opponent_path(self, board, opponent_id):
        try:
            from collections import deque
            start = board.get_pawn_position(opponent_id)
            if not start:
                return None
            goal_row = 0 if opponent_id == 1 else board.size - 1
            queue = deque([(start, [start])])
            visited = {tuple(start)}
            while queue:
                pos, path = queue.popleft()
                if pos[0] == goal_row:
                    return path
                for next_pos in board.get_legal_moves(opponent_id, override_pos=pos):
                    next_tuple = tuple(next_pos)
                    if next_tuple not in visited:
                        visited.add(next_tuple)
                        queue.append((next_pos, path + [next_pos]))
            return None
        except:
            return None

    def _is_wall_on_path(self, row, col, orient, path):
        if not path or len(path) < 2:
            return False
        for i in range(len(path) - 1):
            pos1, pos2 = path[i], path[i + 1]
            if orient == 'H':
                if pos2[0] > pos1[0]:
                    if row == pos2[0] and col <= pos1[1] < col + 2:
                        return True
                elif pos2[0] < pos1[0]:
                    if row == pos1[0] and col <= pos1[1] < col + 2:
                        return True
            else:
                if pos2[1] > pos1[1]:
                    if col == pos2[1] and row <= pos1[0] < row + 2:
                        return True
                elif pos2[1] < pos1[1]:
                    if col == pos1[1] and row <= pos1[0] < row + 2:
                        return True
        return False

    def _get_urgent_wall_positions(self, board, opp_pos, opponent_path):
        positions = set()
        for dr in range(-2, 3):
            for dc in range(-2, 3):
                r, c = opp_pos[0] + dr, opp_pos[1] + dc
                if 0 <= r < board.size - 1 and 0 <= c < board.size - 1:
                    positions.add((r, c))
        if opponent_path:
            for pos in opponent_path[:5]:
                r, c = pos
                for dr in range(-1, 2):
                    for dc in range(-1, 2):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < board.size - 1 and 0 <= nc < board.size - 1:
                            positions.add((nr, nc))
        return list(positions)

    def _get_strategic_wall_positions(self, board, opp_pos, opponent_path):
        positions = set()
        if opponent_path:
            for pos in opponent_path:
                r, c = pos
                for dr in range(-1, 2):
                    for dc in range(-1, 2):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < board.size - 1 and 0 <= nc < board.size - 1:
                            positions.add((nr, nc))
        if len(positions) < 10:
            mid = board.size // 2
            for r in range(mid - 2, mid + 3):
                for c in range(mid - 2, mid + 3):
                    if 0 <= r < board.size - 1 and 0 <= c < board.size - 1:
                        positions.add((r, c))
        return list(positions)

    def minimax(self, board, depth, alpha, beta, maximizing):
        """Minimax with Alpha-Beta Pruning"""
        current_player = self.player_id if maximizing else 3 - self.player_id

        if depth == 0 or self.is_terminal(board):
            return self.evaluate(board)

        legal_moves = board.get_legal_moves(current_player)
        if not legal_moves:
            return self.evaluate(board)

        if maximizing:
            max_eval = -math.inf
            for move in legal_moves:
                new_board = board.clone()
                new_board.apply_move(current_player, move)
                eval_score = self.minimax(new_board, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for move in legal_moves:
                new_board = board.clone()
                new_board.apply_move(current_player, move)
                eval_score = self.minimax(new_board, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval

    def evaluate(self, board):
        """Fuzzy-inspired Evaluation"""
        self.pathfinder.get_legal_moves = board.get_legal_moves
        p1_dist = self.pathfinder.find_path_length(board, 1)
        p2_dist = self.pathfinder.find_path_length(board, 2)

        if p1_dist == 0:
            return math.inf if self.player_id == 1 else -math.inf
        if p2_dist == 0:
            return math.inf if self.player_id == 2 else -math.inf
        if p1_dist is None or p2_dist is None:
            return 0

        path_advantage = (p2_dist - p1_dist) if self.player_id == 1 else (p1_dist - p2_dist)
        wall_advantage = board.get_walls_remaining(self.player_id) - board.get_walls_remaining(3 - self.player_id)

        fuzzy_score = (0.7 * path_advantage) + (0.3 * wall_advantage)
        return fuzzy_score

    def is_terminal(self, board):
        pos1 = board.get_pawn_position(1)
        pos2 = board.get_pawn_position(2)
        if pos1 and pos1[0] == 0:
            return True
        if pos2 and pos2[0] == board.size - 1:
            return True
        return False
