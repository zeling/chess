import chess

def respond_to(fen):
  # This is very stupid
  board = chess.Board(fen)
  import random
  return str(random.choice(list(board.legal_moves)))
  
