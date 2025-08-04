import random
import sys
import time

class Connect4AIvAI:
    def __init__(self):
        self.rows = 6
        self.cols = 7
        self.board = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_player = 'X'
        self.ai1_player = 'X'
        self.ai2_player = 'O'
        self.ai1_depth = 4  # AI 1 lookahead depth
        self.ai2_depth = 4  # AI 2 lookahead depth
        self.move_delay = 1  # Delay between moves in seconds
        
    def display_board(self):
        print("\n" + "=" * 29)
        print("    CONNECT 4 - AI vs AI")
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
        opponent = self.ai2_player if player == self.ai1_player else self.ai1_player
        
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
    
    def minimax(self, depth, alpha, beta, maximizing_player, ai_player):
        """Minimax algorithm with alpha-beta pruning"""
        valid_cols = self.get_valid_columns()
        
        # Terminal state checks
        if depth == 0 or self.is_terminal_state():
            if self.is_terminal_state():
                # Check who won
                temp_player = self.current_player
                self.current_player = ai_player
                if self.check_winner():
                    self.current_player = temp_player
                    return (None, 1000000)
                opponent = self.ai2_player if ai_player == self.ai1_player else self.ai1_player
                self.current_player = opponent
                if self.check_winner():
                    self.current_player = temp_player
                    return (None, -1000000)
                self.current_player = temp_player
                return (None, 0)  # Tie
            else:
                # Depth limit reached, evaluate position
                return (None, self.score_position(ai_player))
        
        if maximizing_player:
            value = -sys.maxsize
            best_col = random.choice(valid_cols) if valid_cols else None
            
            for col in valid_cols:
                # Make move
                row = self.get_next_open_row(col)
                self.board[row][col] = ai_player
                opponent = self.ai2_player if ai_player == self.ai1_player else self.ai1_player
                self.current_player = opponent
                
                # Recursive call
                _, score = self.minimax(depth - 1, alpha, beta, False, ai_player)
                
                # Undo move
                self.board[row][col] = ' '
                self.current_player = ai_player
                
                if score > value:
                    value = score
                    best_col = col
                
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            
            return best_col, value
        
        else:  # Minimizing player
            value = sys.maxsize
            best_col = random.choice(valid_cols) if valid_cols else None
            
            for col in valid_cols:
                # Make move
                opponent = self.ai2_player if ai_player == self.ai1_player else self.ai1_player
                row = self.get_next_open_row(col)
                self.board[row][col] = opponent
                self.current_player = ai_player
                
                # Recursive call
                _, score = self.minimax(depth - 1, alpha, beta, True, ai_player)
                
                # Undo move
                self.board[row][col] = ' '
                self.current_player = opponent
                
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
    
    def get_ai_move(self, ai_player, depth):
        """Get the AI's move using minimax"""
        col, _ = self.minimax(depth, -sys.maxsize, sys.maxsize, True, ai_player)
        return col
    
    def play(self):
        """Main game loop for AI vs AI"""
        print("\nWelcome to Connect 4 - AI vs AI!")
        print("AI 1 is Player X (depth: {})".format(self.ai1_depth))
        print("AI 2 is Player O (depth: {})".format(self.ai2_depth))
        print("Press Ctrl+C to stop the game\n")
        
        move_count = 0
        
        try:
            while True:
                self.display_board()
                
                # Determine which AI is playing
                if self.current_player == self.ai1_player:
                    print(f"\nAI 1 (X) is thinking...")
                    col = self.get_ai_move(self.ai1_player, self.ai1_depth)
                    ai_name = "AI 1 (X)"
                else:
                    print(f"\nAI 2 (O) is thinking...")
                    col = self.get_ai_move(self.ai2_player, self.ai2_depth)
                    ai_name = "AI 2 (O)"
                
                if col is not None:
                    self.drop_piece(col)
                    move_count += 1
                    print(f"{ai_name} drops piece in column {col + 1}")
                    print(f"Move #{move_count}")
                    
                    # Check for winner
                    if self.check_winner():
                        self.display_board()
                        print(f"\n{ai_name} wins after {move_count} moves!")
                        break
                    
                    # Check for tie
                    if self.is_board_full():
                        self.display_board()
                        print(f"\nIt's a tie after {move_count} moves! The board is full.")
                        break
                    
                    # Switch to other AI
                    self.switch_player()
                    
                    # Add delay to make it watchable
                    time.sleep(self.move_delay)
                else:
                    print("AI error: No valid moves available")
                    break
                    
        except KeyboardInterrupt:
            print("\n\nGame interrupted by user!")
            print(f"Game ended after {move_count} moves.")
    
    def play_with_options(self):
        """Play with customizable options"""
        print("\nConnect 4 - AI vs AI Setup")
        print("=" * 30)
        
        # Get AI depths
        try:
            depth1 = input("Enter AI 1 (X) difficulty (1-6, default=4): ").strip()
            self.ai1_depth = int(depth1) if depth1 else 4
            self.ai1_depth = max(1, min(6, self.ai1_depth))
            
            depth2 = input("Enter AI 2 (O) difficulty (1-6, default=4): ").strip()
            self.ai2_depth = int(depth2) if depth2 else 4
            self.ai2_depth = max(1, min(6, self.ai2_depth))
            
            delay = input("Enter delay between moves in seconds (default=1): ").strip()
            self.move_delay = float(delay) if delay else 1.0
            
        except ValueError:
            print("Invalid input. Using default settings.")
            self.ai1_depth = 4
            self.ai2_depth = 4
            self.move_delay = 1.0
        
        self.play()


def main():
    game = Connect4AIvAI()
    game.play_with_options()


if __name__ == "__main__":
    main()
