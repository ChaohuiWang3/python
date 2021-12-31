from board import Direction, Rotation, Action, Shape
from random import Random
from time import sleep
import sys



class Player:
    def choose_action(self, board):
        raise NotImplementedError


class RandomPlayer(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)
        self.blocknum = 0
        self.blocklist = []
        self.top = 24
        self.sequence = -1;

    def choose_action(self, board):
        self.blocknum += 1
        self.blocklist.append(board.falling.shape)
        if self.blocknum == 3:
            if self.blocklist[0] == Shape.J and self.blocklist[1] == Shape.Z \
                and self.blocklist[2] == Shape.T:
                self.sequence = 0
            elif self.blocklist[0] == Shape.J and self.blocklist[1] == Shape.S:
                self.sequence = 1
            elif self.blocklist[0] == Shape.S:
                self.sequence = 2
            elif self.blocklist[0] == Shape.Z:
                self.sequence = 3
            elif self.blocklist[0] == Shape.J and self.blocklist[1] == Shape.Z \
                and self.blocklist[2] == Shape.S:
                self.sequence = 4
        while True:
            if self.sequence == 0 and board.score >= 80:
                assert(False)
            elif self.sequence == 1 and board.score >= 120:
                assert(False)
            elif self.sequence == 2 and board.score >= 160:
                assert(False)
            elif self.sequence == 3 and board.score >= 200:
                assert(False)
            elif self.sequence == 4 and board.score >= 240:
                assert(False)
            yield self.random.choice([
                Direction.Left,
                Direction.Right,
                Rotation.Anticlockwise,
            ])
class Probeplayer(Player):
    def __init__(self, seed = 2):
        self.random = Random(seed)
        self.blocknum = 0
        self.map = {Shape.I : 1,
                    Shape.J : 2,
                    Shape.L : 3,
                    Shape.O : 4,
                    Shape.S : 5,
                    Shape.T : 6,
                    Shape.Z : 7}

        self.sequence = [2,2,4,7,2]
        self.sequence2 = [21,21,22,22,21]
        self.sequenc3 = [28,25,26,24,28]
        self.sequence4 = [40,41,42,41,40]

    def choose_action(self, board):
        print("ca, score", board.score)
        self.blocknum += 1
        if self.blocknum <= 2:
            yield(Direction.Drop)
        #assert False
        skips = self.map[board.falling.shape]
        for i in range (skips):
            yield Direction.Left
            #sleep(1)
        print(board.score)
        assert(False)

weights = {'hdep' : 182.25000000000009, 'holes' : 5400.0, 'bridges' : 246.91358024691365, 'xdiff'
: 0.0, 'xdiff2' : 50, 'hsum' : 0.22222222222222224, 'rowpen' : 55.55555555555556, 'lfholes' : 1, "lf12" : 1}

random = Random(None)

def permut_wights():
    global prevweights, weights
    prevweights = weights.copy()
    ix = random.choice(list(weights.keys()))
    mult = random.choice([0.9, 1/0.9, 0.5, 1/0.5])
    prevweights("changing", ix, "from", weights[ix], "to", weights[ix] * mult)
    weights[ix] = weights[ix] * mult

def print_weights():
    global prevweights, weights
    weights = prevweights
    print("restoring old weights to", weights)

class MyPlayer(Player):
    def __init__(self, seed = 1):
        self.random = Random(seed)
        self.blocknum = 0
        self.discards_remaining = 10
        self. bombs_remaining = 5

    def fix_board(self, board):
        for (x,y) in board.cells:
            board.cellcolor[(x,y)] = "red"
        
    def print_board(self, board):
        print()
        for y in range(24):
            s = ""
            for x in range(10):
                if board.falling is not None and (x,y) in board.falling.cells:
                    s = s + "*"
                elif (x,y) in board.cells:
                    s = s + "#"
                else:
                    s = s + "."
            print(s)
    
    def count_holes(self, board):
        holes = 0
        maxheight = 24
        for x in range(10):
            highest = 24
            for y in range(24):
                if (x,y) in board.cells:
                    if y < highest:
                        highest = y
                        if highest < maxheight:
                            maxheight = highest
                elif y > highest:
                    holes += 1
        #print("Holes: ", holes)
        return holes, maxheight
    
    def count_bridges(self, board):
        bridges = 0
        for x in range(10):
            lowest_holes = 0
            for y in range(23,0,-1):
                if (x,y) in board.cells:
                    if lowest_holes > 0:
                        bridges += 1
                else:
                    if y >lowest_holes:
                        lowest_holes = y
        return bridges

    def lower_four(self, board):
        l4counts = [0,0,0,0,0,0,0,0,0,0]
        totcounts = [0,0,0,0,0,0,0,0,0,0]
        lfholes = [0,0,0,0,0,0,0,0,0,0]
        total = 0
        holes = 0 
        for x in range(10):
            above = False
            for y in range(24):
                if y >= 20:
                    if(x,y) in board.cells:
                        l4counts[x] += 1
                        total += 1
                    else:
                        if l4counts[x] > 0 or totcounts[x] > 0:
                            holes += 1
                            lfholes [x] += 1
                else:
                    if(x,y) in board.cells:
                        totcounts[x] += 1

        zeros = 0
        fours = 0
        lastzero = 0
        for x in range(10):
            if l4counts[x] == 0:
                zeros += 1
                lastzero = x
            elif l4counts[x] == 4:
                fours += 1
            #we don't like filling the lower 4, if it creates a hole
            if lfholes[x] > 0:
                l4counts[x] = 0
        l4counts.sort()
        if zeros == 1 and fours == 9:   
            return True,total, holes, l4counts[1]+l4counts[2]+l4counts[3] +l4counts[4]
        return False, total, holes, l4counts[1]+l4counts[2]+l4counts[3] +l4counts[4]        


    def count_blocks(self,board):
        return len(board.cells)

    def init_score(self, board):
        self.prevholes, prevheight = self.count_holes(board)
        self.bridges = self.count_bridges(board)
        self.blockcount0 = self.count_blocks(board)
        lf, self.lftot, self.lfholes, lf12, = self.lower_four(board)

    def score_position(self, board, pr):
        global weights
        if pr:
            self.print_board(board)
        miny = 24
        for x,y in board.cells:
            if y < miny:
                miny = y

        holes = 0
        holedepth = 0

        prevheight = -1
        hdiffs = 0
        hdiffs2 = 0
        smooth = 0
        heights = [0,0,0,0,0,0,0,0,0,0]
        hsum = 0
        xdiff = 0
        xdiff2 = 0
        for x in range(10):
            highest = 24
            above = 0
            for y in range(24):
                if (x,y) in board.cells:
                    if x < 9 and (x+1,y) not in board.cells:
                        xdiff += 1
                        xdiff2 += 24-y
                    if x > 0 and (x-1,y) not in board.cells:
                        xdiff += 1
                        xdiff2 += 24-y
                    if y >= 0:
                        hsum += y*y
                    if y < highest:
                        highest = y
                        heights[x] = y
                    above += 1
                else:
                    if above > 0:
                        holes += 1
                    holedepth += above
            if prevheight != -1:
                diff = abs(highest - prevheight)
                hdiffs += diff
                d4 = max(diff -4, 0)
                hdiffs2 += d4*d4
                if diff == 0 and smooth == 0:
                    smooth = 1
            prevheight = highest

        onerow = False; tworow = False; threerow = False; fourrow = False
        bdiff1 = self.blockcount0 - self.blockcount1
        bdiff2 = self.blockcount1 - self.blockcount2
        if bdiff1 == 6 or bdiff2 == 6:
            onerow = True
        elif bdiff1 == 16 or bdiff2 == 16:
            tworow = True    
        elif bdiff1 == 26 or bdiff2 == 26:
            threerow = True
        elif bdiff1 == 36 or bdiff2 == 36:
            fourrow = True    

        row_pen = 0
        if onerow:
            if miny > 16:
                row_pen = 20
            elif miny > 13:
                row_pen = 2
        if tworow and miny > 18:
            row_pen = 2
        if threerow and miny > 18:
            row_pen = 1
        plus4 = 0
        if fourrow:
            plus4 = 10000000;

        bridges = self.count_bridges(board)

        rowbonus = 0
        if miny < 12:
            if onerow or tworow or threerow:
                rowbonus = 1

        ypen = max(0, 12-y)

        score = 0
        score -= xdiff * weights['xdiff']
        score -= xdiff2 * weights['xdiff2']
        score -= row_pen * weights['rowpen']
        score += rowbonus * 1000
        score -= holedepth * weights['hdep']
        score -= holes * weights['holes']
        score += plus4
        score -= bridges * weights['bridges']
        score += hsum * weights['hsum']
        lf, lftot, lfholes, lf12 = self.lower_four(board)
        print("here1")
        if self.lftot > lftot:
            print("here")
            #we're removeing blocks from the lower 4
            #don't do this...
            score -= 500
        if self.lftot < lftot:
            score += 10
        score -= lfholes * weights['lfholes']
        score += lf12 * weights['lf12']
        if lf:
            score += 500000
        return score

    def get_rotations(self,block):
        rmin = -1
        rmax = 2
        if block.shape == Shape.O or block.shape == Shape.B:
            rmin = 0
            rmax = 0
        elif block.shape == Shape.I \
            or block.shape == Shape.S \
            or block.shape == Shape.Z: 
            rmin = 0
            rmax = 1
        return rmin, rmax

    def test_rotate(self, board, rot, moves):
        moves.append(rot)
        return board.rotate(rot)

    def test_move(self, board, mv, moves):
        moves.append(mv)
        return board.move(mv)

    def move_to_location(self, board, tr, tx, moves):
        landed = False
        if tr < 0:
            landed = self.test_rotate(board, Rotation.Anticlockwise, moves)
        while not landed and tr > 0:
            landed = self.test_rotate(board, Rotation.Clockwise, moves)
            tr -= 1
        if not landed:
            dist = tx - board.falling.left
        while not landed and dist < 0:
            landed = self.test_move(board, Direction.Left, moves)
            dist += 1
        while not landed and dist > 0:
            landed = self.test_move(board, Direction.Right, moves)
            dist -= 1
        if not landed:
            self.test_move(board, Direction.Drop, moves)

    def choose_action(self, board):
        self.blocknum += 1
        self.blockcount0 = 0
        self.blockcount1 = 0
        self.blockcount2 = 0
        self.prevholes, dummy = self.count_holes(board)
        bsetscore = -1000000000
        bestmoves = []
        bestboard = None

        rmin, rmax = self.get_rotations(board.falling)
        rmin2, rmax2 = self.get_rotations(board.next)
        for r1 in range(rmin, rmax+1):
            for x1 in range(0,10):
                sandbox = board.clone()
                self.fix_board(sandbox)
                moves = []
                self.move_to_location(sandbox, r1, x1, moves)
                self.blockcount1 = self.count_blocks(sandbox)
                for r2 in range(rmin2, rmax2+1):
                    for x2 in range(0,10):
                        sandbox2 = sandbox.clone()
                        self.fix_board(sandbox2)
                        moves2 = moves.copy()
                        self.move_to_location(sandbox, r2, x2, moves)
                        self.blockcount2 = self.count_blocks(sandbox2)
                        score = self.score_position(sandbox2, False)
                        if score > bestscore:
                            bestscore = score
                            bestmoves = moves
                            bestboard = sandbox

        holes, height = self.count_holes(bestboard)
        bridges = self.count_bridges(bestboard)

        if height < 19 and self.discards_remaining > 0:
            self.discard_remaining -= 1
            return Action.Discard
        if bridges > self.bridges:
            if height < 19:
                if self.discards_remaining > 0:
                    if self.bridges > 1 or \
                        (self.bridges > 0 and self.random.random() > 0.75) \
                        or height < 12:
                        self.discards_remaining -= 1 
                        return Action.Discard
                elif self.bomb_remaing > 0 and board.falling.shape != Shape.B \
                    and board.next.shape != Shape.B:
                    sys.stdout.flush()
                    self.bomb_remaing -= 1
                    return Action.Bomb
        return bestmoves


SelectedPlayer = MyPlayer

