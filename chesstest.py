
import chess
import random
import numpy as np

positions = {}

class Tree:
    def __init__(self, data):
        self.children = []
        self.data = data

def return_move_tree(fen, depth, cur):
    board = chess.Board(fen)
    legal_moves = list(board.legal_moves)
    if depth == 0:
        return
    i = 0
    for move in legal_moves:
        board.push(move)
        next_fen = board.fen()
        board.pop()
        cur.children.append(Tree(move))
        return_move_tree(next_fen, depth-1, cur.children[i])
        i+=1
    

def generate_tree(fen):
    board = chess.Board(fen)
    legal_moves = list(board.legal_moves)
    if fen in positions:
        positions[fen]+=legal_moves
    else:
        positions[fen] = legal_moves
    
    #for move in legal_moves:
        #board.push(move)
        #next_fen = board.fen()
        #board.pop()

        #generate_tree(next_fen)

def make_random_move(fen):
    board = chess.Board(fen) 
    legal_moves = list(board.legal_moves)
    if fen in positions:
        positions[fen]+=legal_moves
    else:
        positions[fen] = legal_moves
    to_move = random.randint(0,len(legal_moves)-1)
    board.push(legal_moves[to_move])
    return board

def get_score_white(fen):
    status = fen.split()[0]
    pieces = ['R','N','B','Q','P']
    values = [5,3,3,9,1]
    score = 0
    piece_num = 0
    for piece in pieces:
        for i in status:
            if i==piece:
                score += values[piece_num]
        piece_num +=1

    return score

def get_score_black(fen):
    status = fen.split()[0]
    pieces = ['r','n','b','q','p']
    values = [5,3,3,9,1]
    score = 0
    piece_num = 0
    for piece in pieces:
        for i in status:
            if i==piece:
                score += values[piece_num]
        piece_num +=1

    return score

def get_rel_score(fen):
    white_score = get_score_white(fen)
    black_score = get_score_black(fen)
    return white_score-black_score

# Evaluate the score of each branch
# Among the top scoring, choose a random branch
def engine1(curnode, scores, curbranch):
    if(curnode.children == []):
        curbranch.append(curnode.data)
        board = chess.Board()
        for move in curbranch:
            board.push(move)
        topush = curbranch.copy()
        scores.append([get_rel_score(board.fen()), topush])
    else:
        if(curnode.data == 'root'):
            pass
        else:
            curbranch.append(curnode.data)
        for cnode in curnode.children:
            engine1(cnode, scores, curbranch)
            curbranch.pop()

random.seed(2)
try:
    #Initialize board
    board = chess.Board()
    board_fen = board.fen()
    i = 0
    while(not (board.is_checkmate() or board.is_stalemate())):
        print("Move %i" % i)
        get_score_white(board_fen)
        top = Tree("root")
        depth = 3
        move_tree = return_move_tree(board_fen,depth,top)
        #print(top.data,"->",top.children[0].data,"->",top.children[0].children[0].data)
        scores = []
        engine1(top,scores,[])
        arr = np.array(scores)
        for move in scores[2953][1]:
            board.push(move)
        print(board)


        board = make_random_move(board.fen())
        print(board,"\n")
        #input()
        i = i+1
        if i==100:
            break
    print(board.fen())
except RecursionError:
    print(len(positions) + sum(len(p) for p in positions))
