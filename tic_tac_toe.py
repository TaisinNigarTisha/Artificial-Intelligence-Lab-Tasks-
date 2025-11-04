from typing import List, Optional, Tuple
import copy

class TicTacToe:
    def __init__(self):
        self.board: List[List[Optional[str]]] = [[None]*3 for _ in range(3)]
        self.current_player: str = 'X'
        self.winner: Optional[str] = None
        self.moves_made: int = 0

    def make_move(self, row: int, col: int) -> bool:
        if self.board[row][col] is None and self.winner is None:
            self.board[row][col] = self.current_player
            self.moves_made += 1
            if self.check_winner(row, col):
                self.winner = self.current_player
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def check_winner(self, row: int, col: int) -> bool:
        b, p = self.board, self.current_player
        return (
            all(b[row][c] == p for c in range(3)) or
            all(b[r][col] == p for r in range(3)) or
            (row == col and all(b[i][i] == p for i in range(3))) or
            (row + col == 2 and all(b[i][2-i] == p for i in range(3)))
        )

    def is_draw(self) -> bool:
        return self.moves_made == 9 and self.winner is None

    def reset(self):
        self.__init__()

    def copy(self):
        return copy.deepcopy(self)


class AlphaBeta:
    def __init__(self, depth: int = 3):
        self.depth = depth

    def best_move(self, game: TicTacToe, player: str) -> Tuple[int, int]:
        best_val = float('-inf')
        move = (-1, -1)
        for r, c in self.get_children(game):
            new_game = game.copy()
            new_game.board[r][c] = player
            new_game.current_player = 'O' if player == 'X' else 'X'
            val = self.minimax(new_game, self.depth-1, float('-inf'), float('inf'), False, player)
            if val > best_val:
                best_val = val
                move = (r, c)
        return move

    def minimax(self, state: TicTacToe, depth: int, alpha: float, beta: float, maximizing_player: bool, player: str) -> float:
        if depth == 0 or self.is_terminal(state):
            return self.evaluate(state, player)

        if maximizing_player:
            max_eval = float('-inf')
            for r, c in self.get_children(state):
                new_state = state.copy()
                new_state.board[r][c] = player
                new_state.current_player = 'O' if player == 'X' else 'X'
                eval = self.minimax(new_state, depth-1, alpha, beta, False, player)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            opp = 'O' if player == 'X' else 'X'
            for r, c in self.get_children(state):
                new_state = state.copy()
                new_state.board[r][c] = opp
                new_state.current_player = player
                eval = self.minimax(new_state, depth-1, alpha, beta, True, player)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def is_terminal(self, state: TicTacToe) -> bool:
        return state.winner is not None or state.is_draw()

    def evaluate(self, state: TicTacToe, player: str) -> float:
        if state.winner == player:
            return 10
        elif state.winner is not None:
            return -10
        else:
            return 0

    def get_children(self, state: TicTacToe) -> List[Tuple[int,int]]:
        moves = []
        for r in range(3):
            for c in range(3):
                if state.board[r][c] is None:
                    moves.append((r, c))
        return moves

if __name__ == "__main__":
    game = TicTacToe()
    ai = AlphaBeta(depth=4)

    while not game.winner and not game.is_draw():
        game.print_board() if hasattr(game, 'print_board') else None
        if game.current_player == 'X':  # Human
            row, col = map(int, input("Enter row and col (0-2): ").split())
            game.make_move(row, col)
        else:  # AI
            r, c = ai.best_move(game, 'O')
            game.make_move(r, c)
    print("Game Over")
    game.print_board() if hasattr(game, 'print_board') else None
    if game.winner:
        print(f"Winner: {game.winner}")
    else:
        print("Draw")
