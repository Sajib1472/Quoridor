# 🎮 Quoridor AI Battle

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

*An intelligent Quoridor game implementation featuring two AI players with advanced algorithms*

[Features](#-features) • [Installation](#-installation) • [How to Play](#-how-to-play) • [AI Architecture](#-ai-architecture) • [Project Structure](#-project-structure)

</div>

---

## 📖 About

Quoridor is a strategic board game where players race to reach the opposite side of the board while placing walls to block their opponent's path. This implementation features:

- **Two Sophisticated AI Players** with distinct personalities and strategies
- **Beautiful Pygame GUI** with modern design and smooth animations
- **Advanced Pathfinding** using A* algorithm
- **Fuzzy Logic Decision Making** for human-like gameplay
- **Expectimax Algorithm** for intelligent move evaluation

---

## ✨ Features

### 🤖 Dual AI System
- **AI Player 1**: Conservative & Strategic (Minimax + Fuzzy Logic)
  - Balanced playstyle with emphasis on caution
  - Defensive wall placement
  - Aggression: 0.5 | Caution: 0.6

- **AI Player 2**: Aggressive & Opportunistic (Expectimax + Fuzzy Logic)
  - Bold offensive moves
  - Risk-taking behavior
  - Aggression: 0.7 | Caution: 0.4 | Risk Tolerance: 0.6

### 🎯 Core Gameplay
- **9x9 Board** with authentic Quoridor rules
- **Jump Mechanics** including straight and L-shaped jumps
- **Wall Validation** ensuring both players always have a path to victory
- **Real-time Path Visualization** showing optimal routes
- **Turn-based AI Battle** with strategic decision-making

### 🎨 Modern UI
- Clean, modern color palette
- Smooth player movement
- Visual indicators for legal moves
- Wall placement preview
- Real-time game statistics
- Turn indicators and wall counters

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/quoridor-ai-battle.git
   cd quoridor-ai-battle
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install pygame
   ```

4. **Run the game**
   ```bash
   python quoridor.py
   ```

---

## 🎮 How to Play

### Game Rules

1. **Objective**: Be the first player to reach the opposite side of the board
   - Player 1 (Yellow) starts at the bottom, aims for the top (row 0)
   - Player 2 (Blue) starts at the top, aims for the bottom (row 8)

2. **Movement**:
   - Move one square in any cardinal direction (up, down, left, right)
   - Cannot move through walls
   - Special jumping rules when adjacent to opponent

3. **Wall Placement**:
   - Each player has 10 walls
   - Walls block movement between two squares
   - Walls must be placed on grid lines (horizontal or vertical)
   - Cannot completely block a player's path to their goal
   - Walls cannot overlap or cross each other

4. **Jumping**:
   - **Straight Jump**: Jump directly over adjacent opponent if path is clear
   - **L-Shaped Jump**: If straight jump is blocked, jump diagonally to either side

### Controls

The current implementation features **AI vs AI** gameplay. The game runs automatically, showcasing the battle between two intelligent agents.

To watch the game:
- Run `python quoridor.py`
- Watch as AI players compete using advanced strategies
- Observe wall placements, path optimization, and tactical decisions

---

## 🧠 AI Architecture

### AI Player 1: Strategic Defender

**Algorithm Stack**:
- **Minimax with Limited Depth** (depth = 3)
- **Fuzzy Logic Decision System**
- **A* Pathfinding**

**Characteristics**:
```python
Aggression:     0.5  (Moderate)
Caution:        0.6  (High)
Playstyle:      Balanced with defensive bias
Wall Strategy:  Conservative, blocks opponent strategically
```

**Decision Process**:
1. Calculate path distances using A*
2. Fuzzify game state (path difference, walls remaining)
3. Apply fuzzy rules to determine move vs wall preference
4. Use Minimax to evaluate pawn moves
5. Strategic wall placement along opponent's optimal path

---

### AI Player 2: Aggressive Opportunist

**Algorithm Stack**:
- **Expectimax Algorithm** (depth = 3)
- **Enhanced Fuzzy Logic**
- **A* Pathfinding with Path Following**

**Characteristics**:
```python
Aggression:       0.7  (High)
Caution:          0.4  (Low)
Risk Tolerance:   0.6  (Moderate-High)
Playstyle:        Bold and offensive
Wall Strategy:    Opportunistic, creates immediate obstacles
```

**Decision Process**:
1. Emergency detection (opponent 1-2 moves from winning)
2. Fuzzy logic evaluation for normal gameplay
3. A* optimal path following as primary strategy
4. Expectimax fallback for complex positions
5. Anti-repetition mechanisms to avoid loops

**Special Features**:
- Position history tracking (last 6 moves)
- Urgency-based wall search optimization
- Critical situation handling (exhaustive wall search when losing)

---

## 🏗️ Project Structure

```
quoridor-ai-battle/
│
├── quoridor.py              # Main game loop and Pygame GUI
├── game_rules.py            # Core game logic and rules
│   ├── Board class          # Game state management
│   ├── is_blocked()         # Wall collision detection
│   ├── get_legal_moves()    # Move validation with jump rules
│   └── is_valid_wall()      # Wall placement validation
│
├── ai/
│   ├── ai_player1.py        # Strategic AI (Minimax + Fuzzy)
│   │   ├── FuzzySystem      # Fuzzy logic decision engine
│   │   └── AIPlayer1        # Conservative AI implementation
│   │
│   ├── ai_player2.py        # Aggressive AI (Expectimax + Fuzzy)
│   │   ├── FuzzySystem2     # Enhanced fuzzy logic
│   │   └── AIPlayer2        # Opportunistic AI implementation
│   │
│   └── pathfinding.py       # A* pathfinding algorithm
│       └── AStarPathfinder  # Optimal path calculation
│
└── README.md                # This file
```

---

## 🔍 Technical Deep Dive

### Pathfinding (A* Algorithm)

Located in `ai/pathfinding.py`, this module provides:

```python
class AStarPathfinder:
    - find_path_length()    # Returns shortest distance to goal
    - find_path()           # Returns full path as list of positions
    - manhattan_heuristic() # Admissible heuristic function
```

**Key Features**:
- Guarantees shortest path (optimal)
- Considers walls and legal moves dynamically
- Used for both AI evaluation and wall validation
- Efficient priority queue implementation with `heapq`

### Wall Validation System

Multi-layered validation ensures legal wall placement:

1. **Boundary Check**: Wall must fit within 8x8 wall grid
2. **Duplicate Prevention**: No identical walls
3. **Crossing Prevention**: H and V walls can't occupy same cell
4. **Overlap Detection**: Same-orientation walls can't overlap
5. **Intersection Prevention**: Perpendicular walls can't cross
6. **Path Validation**: Both players must retain a path to goal

### Fuzzy Logic System

Converts numeric game state into linguistic variables:

**Input Fuzzification**:
- Path Difference: `very_close`, `close`, `ahead`, `behind`, `far_ahead`, `far_behind`
- Wall Count: `very_low`, `low`, `medium`, `high`, `very_high`

**Rule Application**:
- Offensive Rules: Favor moving when ahead
- Defensive Rules: Favor walls when behind
- Risk-Taking Rules: Context-dependent bold moves
- Personality Modifiers: Adjust based on aggression/caution

**Output Defuzzification**:
- Produces `move_strength` and `wall_strength` values
- Compared to make final decision

---

## 🎯 Game Mechanics

### Move Generation

Legal moves are calculated considering:
- Board boundaries (9x9 grid)
- Wall obstacles (using `is_blocked()`)
- Opponent position (special jump rules)
- Current player position

### Jump Rules Implementation

**Straight Jump**:
```
Before:          After:
[ ]              [P1]
[P2]     →       [P2]
[P1]             [ ]
```

**L-Shaped Jump** (when straight jump blocked):
```
Wall blocks straight:
[ ][A][ ]
[ ][P2][ ]
[ ][P1][B]
[=][=][=]

P1 can jump to A or B
```

### Wall Mechanics

Walls are represented as tuples: `(row, col, orientation, player)`

- **Horizontal (H)**: Blocks vertical movement at specified row
- **Vertical (V)**: Blocks horizontal movement at specified column
- Each wall spans 2 cells
- Maximum 10 walls per player

---

## 📊 Performance Characteristics

| Component | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| A* Pathfinding | O(b^d) | O(b^d) |
| Minimax (depth 3) | O(b^3) | O(b × d) |
| Expectimax (depth 3) | O(b^3) | O(b × d) |
| Wall Validation | O(n) | O(1) |
| Move Generation | O(1) | O(1) |

*Where b = branching factor (~4 for moves, ~128 for walls), d = depth, n = number of existing walls*

---

## 🛠️ Customization

### Adjusting AI Difficulty

**In `ai/ai_player1.py`**:
```python
def __init__(self, player_id, max_depth=3):  # Increase depth for stronger AI
    self.aggression = 0.5    # 0.0-1.0 (higher = more aggressive)
    self.caution = 0.6       # 0.0-1.0 (higher = more defensive)
```

**In `ai/ai_player2.py`**:
```python
def __init__(self, player_id, max_depth=3):
    self.aggression = 0.7
    self.caution = 0.4
    self.risk_tolerance = 0.6  # Unique to AI Player 2
```

### Modifying Visual Theme

**In `quoridor.py`**, adjust color constants:
```python
# Player Colors
P1_COLOR = (241, 196, 15)  # Yellow
P2_COLOR = (52, 152, 219)   # Blue

# Wall Colors
WALL_COLOR_P1 = (230, 126, 34)  # Orange
WALL_COLOR_P2 = (155, 89, 182)  # Purple
```

### Game Speed

Adjust AI thinking time in main game loop:
```python
pygame.time.delay(500)  # Milliseconds between moves
```

---

## 🐛 Known Issues & Future Enhancements

### Potential Improvements
- [ ] Add human player mode with mouse controls
- [ ] Implement move history and undo functionality
- [ ] Add game replay system
- [ ] Create tournament mode (best of N games)
- [ ] Implement Monte Carlo Tree Search (MCTS) AI
- [ ] Add difficulty levels for casual players
- [ ] Network multiplayer support
- [ ] Save/load game state
- [ ] Performance profiling and optimization
- [ ] Unit tests for game rules

---

## 📚 Algorithm References

### A* Pathfinding
- **Paper**: Hart, P. E., Nilsson, N. J., & Raphael, B. (1968). "A Formal Basis for the Heuristic Determination of Minimum Cost Paths"
- **Heuristic**: Manhattan Distance (admissible and consistent)

### Minimax Algorithm
- **Concept**: Von Neumann, J., & Morgenstern, O. (1944). "Theory of Games and Economic Behavior"
- **Application**: Two-player zero-sum game tree search

### Expectimax Algorithm
- **Extension**: Minimax with chance nodes for uncertain opponent behavior
- **Use Case**: Models probabilistic opponent decisions

### Fuzzy Logic
- **Foundation**: Zadeh, L. A. (1965). "Fuzzy Sets"
- **Application**: Linguistic variable mapping for decision-making

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide for Python code
- Add docstrings to new functions and classes
- Test AI changes against both existing AI players
- Update README if adding new features

---

## 📄 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

- Quoridor board game by Mirko Marchesi
- Pygame community for excellent documentation
- AI algorithm implementations inspired by academic research
- Thanks to the open-source community

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Known Issues](#-known-issues--future-enhancements) section
2. Search existing GitHub issues
3. Create a new issue with detailed description and steps to reproduce

---

<div align="center">

**⭐ Star this repository if you found it helpful!**

Made with ❤️ and ☕

</div>
