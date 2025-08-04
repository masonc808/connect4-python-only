import random
import sys

class Connect4:
    def __init__(self):
        self.rows = 6
        self.cols = 7
        self.board = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_player = 'X'
        self.human_player = 'X'
        self.ai_player = 'O'
        self.max_depth = 4  # AI lookahead depth
        
    def display_board(self):
        print("\n" + "=" * 29)
        print("      CONNECT 4 GAME")
        print("=" * 29)
        
        # Display column numbers
        print("  ", end="")
        for col in range(self.cols):
            print(f" {col + 1} ", end="")
        print()
        
        # Display board
        print("  " + "-" * (self.cols * 4 - 1))
        for row in range(self.rows):
            print("  |", end="")
            for col in range(self.cols):
                print(f" {self.board[row][col]} |", end="")
            print()
            print("  " + "-" * (self.cols * 4 - 1))
    
    def drop_piece(self, col):
        """Drop a piece in the specified column"""
        if col < 0 or col >= self.cols:
            return False
        
        # Check if column is full
        if self.board[0][col] != ' ':
            return False
        
        # Find the lowest empty row
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][col] == ' ':
                self.board[row][col] = self.current_player
                return True
        
        return False
    
    def check_winner(self):
        """Check if there's a winner"""
        # Check horizontal
        for row in range(self.rows):
            for col in range(self.cols - 3):
                if (self.board[row][col] == self.current_player and
                    self.board[row][col + 1] == self.current_player and
                    self.board[row][col + 2] == self.current_player and
                    self.board[row][col + 3] == self.current_player):
                    return True
        
        # Check vertical
        for row in range(self.rows - 3):
            for col in range(self.cols):
                if (self.board[row][col] == self.current_player and
                    self.board[row + 1][col] == self.current_player and
                    self.board[row + 2][col] == self.current_player and
                    self.board[row + 3][col] == self.current_player):
                    return True
        
        # Check diagonal (top-left to bottom-right)
        for row in range(self.rows - 3):
            for col in range(self.cols - 3):
                if (self.board[row][col] == self.current_player and
                    self.board[row + 1][col + 1] == self.current_player and
                    self.board[row + 2][col + 2] == self.current_player and
                    self.board[row + 3][col + 3] == self.current_player):
                    return True
        
        # Check diagonal (bottom-left to top-right)
        for row in range(3, self.rows):
            for col in range(self.cols - 3):
                if (self.board[row][col] == self.current_player and
                    self.board[row - 1][col + 1] == self.current_player and
                    self.board[row - 2][col + 2] == self.current_player and
                    self.board[row - 3][col + 3] == self.current_player):
                    return True
        
        return False
    
    def is_board_full(self):
        """Check if the board is full"""
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == ' ':
                    return False
        return True
    
    def switch_player(self):
        """Switch between players"""
        self.current_player = 'O' if self.current_player == 'X' else 'X'
    
    def get_valid_columns(self):
        """Get list of columns that aren't full"""
        valid_cols = []
        for col in range(self.cols):
            if self.board[0][col] == ' ':
                valid_cols.append(col)
        return valid_cols
    
    def evaluate_window(self, window, player):
        """Evaluate a window of 4 positions"""
        score = 0
        opponent = self.ai_player if player == self.human_player else self.human_player
        
        # Count pieces
        player_count = window.count(player)
        opponent_count = window.count(opponent)
        empty_count = window.count(' ')
        
        # Scoring based on patterns
        if player_count == 4:
            score += 100
        elif player_count == 3 and empty_count == 1:
            score += 10
        elif player_count == 2 and empty_count == 2:
            score += 2
        
        # Penalize opponent's opportunities
        if opponent_count == 3 and empty_count == 1:
            score -= 80
        elif opponent_count == 2 and empty_count == 2:
            score -= 2
            
        return score
    
    def score_position(self, player):
        """Score the entire board position"""
        score = 0
        
        # Score center column preference
        center_col = self.cols // 2
        for row in range(self.rows):
            if self.board[row][center_col] == player:
                score += 3
        
        # Score horizontal windows
        for row in range(self.rows):
            for col in range(self.cols - 3):
                window = [self.board[row][col + i] for i in range(4)]
                score += self.evaluate_window(window, player)
        
        # Score vertical windows
        for row in range(self.rows - 3):
            for col in range(self.cols):
                window = [self.board[row + i][col] for i in range(4)]
                score += self.evaluate_window(window, player)
        
        # Score diagonal windows (positive slope)
        for row in range(self.rows - 3):
            for col in range(self.cols - 3):
                window = [self.board[row + i][col + i] for i in range(4)]
                score += self.evaluate_window(window, player)
        
        # Score diagonal windows (negative slope)
        for row in range(3, self.rows):
            for col in range(self.cols - 3):
                window = [self.board[row - i][col + i] for i in range(4)]
                score += self.evaluate_window(window, player)
        
        return score
    
    def is_terminal_state(self):
        """Check if the game is over"""
        # Check if current player won
        if self.check_winner():
            return True
        # Check if board is full
        if self.is_board_full():
            return True
        return False
    
    def minimax(self, depth, alpha, beta, maximizing_player):
        """Minimax algorithm with alpha-beta pruning"""
        valid_cols = self.get_valid_columns()
        
        # Terminal state checks
        if depth == 0 or self.is_terminal_state():
            if self.is_terminal_state():
                # Check who won
                temp_player = self.current_player
                self.current_player = self.ai_player
                if self.check_winner():
                    self.current_player = temp_player
                    return (None, 1000000)
                self.current_player = self.human_player
                if self.check_winner():
                    self.current_player = temp_player
                    return (None, -1000000)
                self.current_player = temp_player
                return (None, 0)  # Tie
            else:
                # Depth limit reached, evaluate position
                return (None, self.score_position(self.ai_player))
        
        if maximizing_player:
            value = -sys.maxsize
            best_col = random.choice(valid_cols)
            
            for col in valid_cols:
                # Make move
                row = self.get_next_open_row(col)
                self.board[row][col] = self.ai_player
                self.current_player = self.human_player
                
                # Recursive call
                _, score = self.minimax(depth - 1, alpha, beta, False)
                
                # Undo move
                self.board[row][col] = ' '
                self.current_player = self.ai_player
                
                if score > value:
                    value = score
                    best_col = col
                
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            
            return best_col, value
        
        else:  # Minimizing player
            value = sys.maxsize
            best_col = random.choice(valid_cols)
            
            for col in valid_cols:
                # Make move
                row = self.get_next_open_row(col)
                self.board[row][col] = self.human_player
                self.current_player = self.ai_player
                
                # Recursive call
                _, score = self.minimax(depth - 1, alpha, beta, True)
                
                # Undo move
                self.board[row][col] = ' '
                self.current_player = self.human_player
                
                if score < value:
                    value = score
                    best_col = col
                
                beta = min(beta, value)
                if alpha >= beta:
                    break
            
            return best_col, value
    
    def get_next_open_row(self, col):
        """Get the next open row in a column"""
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][col] == ' ':
                return row
        return -1
    
    def get_ai_move(self):
        """Get the AI's move using minimax"""
        col, _ = self.minimax(self.max_depth, -sys.maxsize, sys.maxsize, True)
        return col
    
    def play(self):
        """Main game loop"""
        print("\nWelcome to Connect 4!")
        print("You are Player X (human)")
        print("Computer is Player O (AI)")
        print("Enter column number (1-7) to drop your piece")
        print("Enter 'q' to quit the game\n")
        
        while True:
            self.display_board()
            
            if self.current_player == self.human_player:
                # Human player's turn
                player_input = input(f"\nYour turn (X), enter column (1-7): ").strip()
                
                # Check if player wants to quit
                if player_input.lower() == 'q':
                    print("Thanks for playing!")
                    break
                
                # Validate input
                try:
                    col = int(player_input) - 1
                except ValueError:
                    print("Invalid input! Please enter a number between 1 and 7.")
                    continue
                
                # Make move
                if self.drop_piece(col):
                    # Check for winner
                    if self.check_winner():
                        self.display_board()
                        print(f"\nCongratulations! You win!")
                        break
                    
                    # Check for tie
                    if self.is_board_full():
                        self.display_board()
                        print("\nIt's a tie! The board is full.")
                        break
                    
                    # Switch to AI player
                    self.switch_player()
                else:
                    print("Invalid move! That column is full or doesn't exist.")
            
            else:
                # AI player's turn
                print("\nAI is thinking...")
                col = self.get_ai_move()
                
                if col is not None:
                    self.drop_piece(col)
                    print(f"AI drops piece in column {col + 1}")
                    
                    # Check for winner
                    if self.check_winner():
                        self.display_board()
                        print(f"\nAI wins! Better luck next time.")
                        break
                    
                    # Check for tie
                    if self.is_board_full():
                        self.display_board()
                        print("\nIt's a tie! The board is full.")
                        break
                    
                    # Switch back to human player
                    self.switch_player()
                else:
                    print("AI error: No valid moves available")
                    break


def main():
    game = Connect4()
    game.play()


if __name__ == "__main__":
    main()
