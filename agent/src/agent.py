import chess

def pop_count(i):
    s = 0
    while i:
        s += 1
        i &= i - 1
    return s

_p_scores = [0, 10, 30, 30, 50, 90, 900]
_max_score = 1290

def _evaluate(b, c):
    # could be optimized into a matrix mult, but I choose to belive in pypy's JIT
    score = 0
    for ptype in range(chess.PAWN, chess.KING + 1):
        mask = b.pieces_mask(ptype, c)
        score += pop_count(mask) * _p_scores[ptype]
    return score

def evaluate(b):
    return _evaluate(b, b.turn) - _evaluate(b, not b.turn)


def _minimax(b, d=3, mmin=-_max_score, mmax=_max_score, is_max_node=True):
    if not d: return evaluate(b)
    if is_max_node:
        score = mmin
        for move in b.legal_moves:
            b.push(move)
            score_prime = _minimax(b, d-1, score, mmax, False)
            b.pop()
            if score_prime > score:
                score = score_prime
            if score > mmax: return mmax
        return score
    else:
        score = mmax
        for move in b.legal_moves:
            b.push(move)
            score_prime = _minimax(b, d-1, mmin, score, True)
            b.pop()
            if score_prime < score:
                score = score_prime
            if score < mmin: return mmin
        return score

def respond_to(fen):
    b = chess.Board(fen)
    s = -_max_score
    bestmove = None
    for move in b.legal_moves:
        b.push(move)
        min_score = _minimax(b, d=3, mmin=s, is_max_node=False)
        b.pop()
        if min_score > s: 
            s = min_score
            bestmove = move
    return bestmove.uci()

if __name__ == '__main__':
    print(respond_to(chess.Board().fen()))
