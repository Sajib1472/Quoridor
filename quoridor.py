import pygame, sys
from game_rules import get_legal_moves, is_valid_wall, Board

from ai.ai_player1 import AIPlayer1
from ai.ai_player2 import AIPlayer2

pygame.init()

ai1 = AIPlayer1(1)
ai2 = AIPlayer2(2)

CELL_SIZE = 60
BOARD_SIZE = 9
MARGIN = 60
WIDTH = HEIGHT = BOARD_SIZE * CELL_SIZE + 2 * MARGIN

# Modern Color Palette
BG_COLOR = (245, 245, 250)
BOARD_COLOR = (52, 73, 94)
CELL_COLOR = (236, 240, 241)
CELL_HOVER = (189, 195, 199)
GRID_LINE_COLOR = (127, 140, 141)

# Player Colors
P1_COLOR = (241, 196, 15)
P1_BORDER = (243, 156, 18)
P2_COLOR = (52, 152, 219)
P2_BORDER = (41, 128, 185)

# Wall Colors
WALL_COLOR_P1 = (230, 126, 34)
WALL_COLOR_P1_SHADOW = (211, 84, 0)
WALL_COLOR_P2 = (155, 89, 182)
WALL_COLOR_P2_SHADOW = (142, 68, 173)

# UI Colors
TEXT_COLOR = (44, 62, 80)
HIGHLIGHT_COLOR = (46, 204, 113)
SHADOW_COLOR = (0, 0, 0, 30)
PANEL_BG = (236, 240, 241)

# UI Layout
INFO_PANEL_HEIGHT = 100
TOTAL_HEIGHT = HEIGHT + INFO_PANEL_HEIGHT

screen = pygame.display.set_mode((WIDTH, TOTAL_HEIGHT))
pygame.display.set_caption("Quoridor - AI Battle")

def draw_board(board):
    screen.fill(BG_COLOR)
    
    board_rect = pygame.Rect(MARGIN, MARGIN, BOARD_SIZE * CELL_SIZE, BOARD_SIZE * CELL_SIZE)
    pygame.draw.rect(screen, BOARD_COLOR, board_rect)

    # Draw grid cells
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            cell_rect = pygame.Rect(MARGIN + col * CELL_SIZE + 6, MARGIN + row * CELL_SIZE + 6, 
                                   CELL_SIZE - 12, CELL_SIZE - 12)
            pygame.draw.rect(screen, CELL_COLOR, cell_rect)
            
            if row < BOARD_SIZE - 1:
                line_y = MARGIN + (row + 1) * CELL_SIZE
                pygame.draw.line(screen, GRID_LINE_COLOR, (MARGIN + 6, line_y), 
                               (MARGIN + BOARD_SIZE * CELL_SIZE - 6, line_y), 1)
            if col < BOARD_SIZE - 1:
                line_x = MARGIN + (col + 1) * CELL_SIZE
                pygame.draw.line(screen, GRID_LINE_COLOR, (line_x, MARGIN + 6), 
                               (line_x, MARGIN + BOARD_SIZE * CELL_SIZE - 6), 1)

    # Draw walls (removed labels for cleaner look)
    for (row, col, orientation, player) in board.walls:
        color = WALL_COLOR_P1 if player == 1 else WALL_COLOR_P2
        
        if orientation == 'H':
            x = MARGIN + col * CELL_SIZE
            y = MARGIN + row * CELL_SIZE - 6
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE * 2, 12))
            
        elif orientation == 'V':
            x = MARGIN + col * CELL_SIZE - 6
            y = MARGIN + row * CELL_SIZE
            pygame.draw.rect(screen, color, (x, y, 12, CELL_SIZE * 2))

    # Draw player pawns
    font_small = pygame.font.Font(None, 24)
    
    # Player 1
    p1_x = MARGIN + board.p1_pos[1] * CELL_SIZE + CELL_SIZE // 2
    p1_y = MARGIN + board.p1_pos[0] * CELL_SIZE + CELL_SIZE // 2
    pygame.draw.circle(screen, P1_BORDER, (p1_x, p1_y), CELL_SIZE // 3 + 2)
    pygame.draw.circle(screen, P1_COLOR, (p1_x, p1_y), CELL_SIZE // 3)
    label = font_small.render("1", True, TEXT_COLOR)
    label_rect = label.get_rect(center=(p1_x, p1_y))
    screen.blit(label, label_rect)

    # Player 2
    p2_x = MARGIN + board.p2_pos[1] * CELL_SIZE + CELL_SIZE // 2
    p2_y = MARGIN + board.p2_pos[0] * CELL_SIZE + CELL_SIZE // 2
    pygame.draw.circle(screen, P2_BORDER, (p2_x, p2_y), CELL_SIZE // 3 + 2)
    pygame.draw.circle(screen, P2_COLOR, (p2_x, p2_y), CELL_SIZE // 3)
    label = font_small.render("2", True, (255, 255, 255))
    label_rect = label.get_rect(center=(p2_x, p2_y))
    screen.blit(label, label_rect)

def draw_info_panel(board, current_turn):
    """Draw information panel with player stats"""
    panel_y = HEIGHT
    
    panel_rect = pygame.Rect(0, panel_y, WIDTH, INFO_PANEL_HEIGHT)
    pygame.draw.rect(screen, PANEL_BG, panel_rect)
    pygame.draw.line(screen, GRID_LINE_COLOR, (0, panel_y), (WIDTH, panel_y), 2)
    
    font_large = pygame.font.Font(None, 42)
    font_medium = pygame.font.Font(None, 32)
    font_small = pygame.font.Font(None, 24)
    
    # Player 1 Section
    p1_x = 50
    p1_y = panel_y + 25
    
    pygame.draw.circle(screen, P1_BORDER if current_turn == 1 else (200, 200, 200), 
                      (p1_x, p1_y + 10), 20)
    pygame.draw.circle(screen, P1_COLOR, (p1_x, p1_y + 10), 16)
    if current_turn == 1:
        pygame.draw.circle(screen, P1_BORDER, (p1_x, p1_y + 10), 24, 3)
    
    p1_name = font_large.render("AI Player 1", True, TEXT_COLOR if current_turn == 1 else (150, 150, 150))
    screen.blit(p1_name, (p1_x + 35, p1_y - 5))
    
    walls_text = font_small.render(f"Walls: {board.p1_walls_remaining}", True, TEXT_COLOR)
    screen.blit(walls_text, (p1_x + 35, p1_y + 30))
    
    for i in range(board.p1_walls_remaining):
        wall_x = p1_x + 115 + i * 12
        wall_y = p1_y + 32
        pygame.draw.rect(screen, WALL_COLOR_P1, (wall_x, wall_y, 8, 16))
    
    # Player 2 Section
    p2_x = WIDTH - 50
    p2_y = panel_y + 25
    
    pygame.draw.circle(screen, P2_BORDER if current_turn == 2 else (200, 200, 200), 
                      (p2_x, p2_y + 10), 20)
    pygame.draw.circle(screen, P2_COLOR, (p2_x, p2_y + 10), 16)
    if current_turn == 2:
        pygame.draw.circle(screen, P2_BORDER, (p2_x, p2_y + 10), 24, 3)
    
    p2_name = font_large.render("AI Player 2", True, TEXT_COLOR if current_turn == 2 else (150, 150, 150))
    p2_name_rect = p2_name.get_rect(right=p2_x - 35, top=p2_y - 5)
    screen.blit(p2_name, p2_name_rect)
    
    walls_text = font_small.render(f"Walls: {board.p2_walls_remaining}", True, TEXT_COLOR)
    walls_rect = walls_text.get_rect(right=p2_x - 35, top=p2_y + 30)
    screen.blit(walls_text, walls_rect)
    
    for i in range(board.p2_walls_remaining):
        wall_x = p2_x - 127 - i * 12
        wall_y = p2_y + 32
        pygame.draw.rect(screen, WALL_COLOR_P2, (wall_x, wall_y, 8, 16))
    
    # Center - VS
    center_x = WIDTH // 2
    center_y = panel_y + INFO_PANEL_HEIGHT // 2
    
    vs_text = font_medium.render("VS", True, GRID_LINE_COLOR)
    vs_rect = vs_text.get_rect(center=(center_x, center_y))
    screen.blit(vs_text, vs_rect)
    
    arrow_color = HIGHLIGHT_COLOR
    arrow_y = panel_y + 15
    
    if current_turn == 1:
        arrow_x = vs_rect.left - 50
        arrow_points = [
            (arrow_x - 15, arrow_y),
            (arrow_x, arrow_y - 12),
            (arrow_x, arrow_y + 12)
        ]
    else:
        arrow_x = vs_rect.right + 50
        arrow_points = [
            (arrow_x + 15, arrow_y),
            (arrow_x, arrow_y - 12),
            (arrow_x, arrow_y + 12)
        ]
    
    pygame.draw.polygon(screen, arrow_color, arrow_points)
    pygame.draw.polygon(screen, TEXT_COLOR, arrow_points, 2)
    
    turn_label = font_small.render("TURN", True, arrow_color)
    turn_label_rect = turn_label.get_rect(center=(arrow_x, arrow_y + 25))
    screen.blit(turn_label, turn_label_rect)


def main():
    board = Board()
    turn = 1
    clock = pygame.time.Clock()
    first_frame = True
    game_over = False
    winner = None
    show_winner_modal = False
    move_count = 0
    max_moves = 500

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_board(board)
        draw_info_panel(board, turn)
        
        if show_winner_modal:
            # Darken background
            overlay = pygame.Surface((WIDTH, TOTAL_HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(overlay, (0, 0, 0, 180), overlay.get_rect())
            screen.blit(overlay, (0, 0))
            
            # Winner box
            box_width = 500
            box_height = 200
            box_x = (WIDTH - box_width) // 2
            box_y = (HEIGHT - box_height) // 2
            
            box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
            pygame.draw.rect(screen, (255, 255, 255), box_rect)
            
            winner_color = P1_COLOR if winner == 1 else P2_COLOR
            border_color = P1_BORDER if winner == 1 else P2_BORDER
            pygame.draw.rect(screen, border_color, box_rect, 5)
            
            font_title = pygame.font.Font(None, 74)
            font_sub = pygame.font.Font(None, 42)
            title = font_title.render(f"AI Player {winner} Wins!", True, winner_color)
            subtitle = font_sub.render(f"Game completed in {move_count} moves!", True, border_color)
            
            title_rect = title.get_rect(center=(WIDTH // 2, box_y + 70))
            subtitle_rect = subtitle.get_rect(center=(WIDTH // 2, box_y + 130))
            
            screen.blit(title, title_rect)
            screen.blit(subtitle, subtitle_rect)
            
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()
        
        pygame.display.flip()
        
        if game_over and not show_winner_modal:
            pygame.time.wait(2000)
            show_winner_modal = True
            continue

        if first_frame:
            first_frame = False
            clock.tick(1)
            continue

        if game_over:
            continue

        # Safety check
        if move_count >= max_moves:
            print(f"\n⚠️ Safety limit reached ({max_moves} moves)")
            from ai.pathfinding import AStarPathfinder
            pathfinder = AStarPathfinder(board.get_legal_moves)
            p1_dist = pathfinder.find_path_length(board, 1)
            p2_dist = pathfinder.find_path_length(board, 2)
            if p1_dist is not None and p2_dist is not None:
                winner = 1 if p1_dist < p2_dist else 2
            elif p1_dist is not None:
                winner = 1
            elif p2_dist is not None:
                winner = 2
            else:
                winner = 1
            print(f"Winner by distance: Player {winner}")
            game_over = True
            continue

        # Get current AI
        ai = ai1 if turn == 1 else ai2

        move = ai.choose_move(board, return_fuzzy=False)

        if move is None:
            winner = 3 - turn
            print(f"Player {turn} has no valid actions! Player {winner} wins!")
            game_over = True
            continue

        action_type, action = move
        move_count += 1
        
        if action_type == "move":
            board.apply_move(turn, action)
            print(f"Move {move_count}: Player {turn} moved to {action}")
            
        elif action_type == "wall":
            row, col, orient = action
            success = board.place_wall(turn, row, col, orient)
            if success:
                print(f"Move {move_count}: Player {turn} placed {orient} wall at ({row},{col})")

        # Check for win
        if action_type == "move":
            current_pos = board.p1_pos if turn == 1 else board.p2_pos
            
            if turn == 1 and current_pos[0] == 0:
                print(f"\n🎉 AI Player 1 WINS in {move_count} moves!")
                game_over = True
                winner = 1
            elif turn == 2 and current_pos[0] == board.size - 1:
                print(f"\n🎉 AI Player 2 WINS in {move_count} moves!")
                game_over = True
                winner = 2

        turn = 3 - turn
        clock.tick(1)

if __name__ == "__main__":
    main()