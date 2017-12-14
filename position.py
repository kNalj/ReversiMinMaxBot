class Position(object):
    
    INIT_BOARD = '0000000000000000000000000001200000021000000000000000000000000000'
    
    def __init__(self, init_str=None, turn=1, skip=False):
        if not skip:
            self.turn = turn
            self.setup(self.INIT_BOARD if init_str is None else self.init_str)
            
    def copy(self):
        c = Position(None, 1, True)
        c.turn = self.turn
        c.board = self.board[:]
        c.count = self.count[:]    
        return c
        
    def setup(self, bstr):
        if len(bstr) != 64:
            print('Board string length {}'.format(len(bstr)))
        else:
            self.board = [ int(c) for c in bstr ]
            self.count = [ 0, 0, 0 ]
            for c in self.board:
                self.count[c] += 1
    
    def change_list(self, m):
        # collect changing piece indexes in list
        cplist = []
        oppturn = 1 if self.turn == 2 else 2
        x, y = m%8, m//8
        for dx, dy in [ (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1) ]:
            d, dlist = 1, []
            while 0 <= (x+d*dx) and (x+d*dx) < 8 and 0 <= (y+d*dy) and (y+d*dy) < 8:
                bi = (y+d*dy)*8 + (x+d*dx)
                if self.board[bi] != oppturn:
                    if self.board[bi] == self.turn:
                        cplist += dlist
                    break
                dlist.append(bi)
                d += 1
        return cplist

    def move(self, m):        
        # play move, change pieces, update counts and change player's turn
        self.board[m] = self.turn
        oppturn = 1 if self.turn == 2 else 2
        for bi in self.change_list(m):
            self.board[bi] = self.turn
            self.count[self.turn] += 1 
            self.count[oppturn] -= 1 
        self.count[0] -= 1 
        self.turn = 1 if self.turn == 2 else 2        

    def legal_moves(self):
        return [ m for m in range(64) if self.board[m] == 0 ]
    
    def is_legal(self, m):
        return self.board[m] == 0

    def tostring(self):
        return str(self.turn), ''.join(str(c) for c in self.board)
    
    def move_count(self):
        return 64 - self.count[0]
        
    def game_over(self):
        # 0 - still playing, 1 or 2 - victory, 3 - draw
        if self.count[0] > 0:
            return 0
        elif self.count[1] > self.count[2]:
            return 1
        elif self.count[2] > self.count[1]:
            return 2
        else:
            return 3            

if __name__ == '__main__':
    pos = Position()
    print(pos.tostring())
    