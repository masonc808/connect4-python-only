# Connect 4 - Pure Python Implementation

A Connect 4 game implementation in Python using **only built-in libraries** - no external dependencies required!

## Features

- Classic Connect 4 gameplay on a 6x7 board
- Two game modes:
  - **Human vs AI** (`pythonGame.py`)
  - **AI vs AI** (`connect4pyAivAi.py`)
- Intelligent AI using minimax algorithm with alpha-beta pruning
- **Zero external dependencies** - uses only Python's standard library
- Clear ASCII-based visual interface
- Configurable AI difficulty levels

## Getting Started

1. Make sure you have Python 3.x installed on your system
2. Clone this repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/connect4-python-only.git
   cd connect4-python-only
   ```

## Game Modes

### Human vs AI
Run the human vs AI game:
```bash
python pythonGame.py
# or
python3 pythonGame.py
```

- You play as 'X' and the AI plays as 'O'
- Enter a column number (1-7) to drop your piece
- Connect 4 pieces in a row (horizontally, vertically, or diagonally) to win
- Enter 'q' to quit the game at any time

### AI vs AI
Watch two AI players compete:
```bash
python connect4pyAivAi.py
# or
python3 connect4pyAivAi.py
```

- Configure difficulty for each AI (1-6, where 6 is the smartest)
- Set delay between moves to watch the game unfold
- Press Ctrl+C to stop the game

## AI Strategy

The AI uses a minimax algorithm with alpha-beta pruning to:
- Look ahead up to 4-6 moves (configurable)
- Evaluate board positions based on potential winning patterns
- Block opponent's winning moves while setting up its own
- Prefer center column positions for strategic advantage

## Requirements

- Python 3.x
- No external libraries required! 🎉

## Files

- `pythonGame.py` - Human vs AI game
- `connect4pyAivAi.py` - AI vs AI game
- `README.md` - This file

## License

This project is open source and available under the MIT License.
