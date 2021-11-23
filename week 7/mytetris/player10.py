from os import scandir
from types import SimpleNamespace
from board import Direction, Rotation, Action
from random import Random
import time


class Player:
    def choose_action(self, board):
        raise NotImplementedError


class RandomPlayer(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)



    def score_highestposition(self, board):
        miny = 24
        for (x,y) in board.cells:
            if y < miny:
                miny = y
        return miny
    
    def score_touched(self, board):
        count = 0
        for (x,y) in board.cells:
            count += y
        return count



    def choose_action(self, board):
        xpos = board.falling.left
        bestx = 0
        bestscore = 0
        bestscore2 = 0
        bestmoves = []
        if self.random.random() > 0.976:
            return self.random.choice([
                Action.Discard,
                Action.Bomb,
            ])  
        else:
            for rotation in range(0, 4):
                for x in range(0,10):
                    sandbox = board.clone() 
                    moves = []
                    landed = False 
                    number1 = len(sandbox.cells)
                    if rotation == 0:
                        moves = []
                    elif rotation == 1:
                        sandbox.rotate(Rotation.Clockwise)
                        moves.append(Rotation.Clockwise)
                    elif rotation == 2:
                        sandbox.rotate(Rotation.Clockwise)
                        sandbox.rotate(Rotation.Clockwise)
                        moves.append(Rotation.Clockwise)
                        moves.append(Rotation.Clockwise)
                    else:                      
                        sandbox.rotate(Rotation.Anticlockwise)
                        moves.append(Rotation.Anticlockwise)
                    if x < 5:
                        xpos = sandbox.falling.left
                        while xpos > x and landed == False:
                            sandbox.move(Direction.Left)
                            moves.append(Direction.Left)
                            if sandbox.falling is not None: 
                                xpos = sandbox.falling.left
                            else:
                                landed = True
                                break
                        while xpos < x and landed == False:
                            sandbox.move(Direction.Right)
                            moves.append(Direction.Right)
                            if sandbox.falling is not None:                   
                                xpos = sandbox.falling.left
                            else:
                                landed = True
                                break
                        if landed == False:                   
                            sandbox.move(Direction.Drop)
                            moves.append(Direction.Drop)    
                    if x >= 5:
                        xpos = sandbox.falling.right
                        while xpos > x and landed == False:
                            sandbox.move(Direction.Left)
                            moves.append(Direction.Left)
                            if sandbox.falling is not None: 
                                xpos = sandbox.falling.right
                            else:
                                landed = True
                                break
                        while xpos < x and landed == False:
                            sandbox.move(Direction.Right)
                            moves.append(Direction.Right)
                            if sandbox.falling is not None:                   
                                xpos = sandbox.falling.right
                            else:
                                landed = True
                                break
                        if landed == False:             
                            sandbox.move(Direction.Drop)
                            moves.append(Direction.Drop) 
                    number2 = len(sandbox.cells) 
                    score1 = self.score_highestposition(sandbox)
                    score2 = self.score_touched(sandbox)
                    number3 = number1 + 4 - number2
                    score = score1 + score2 + 23 * number3
                    if score > bestscore:
                        bestscore = score
                        bestx = x
                        bestmoves = moves
        return bestmoves


SelectedPlayer = RandomPlayer


