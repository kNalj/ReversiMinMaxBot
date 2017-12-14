import sys
from position import Position
 
class MinMaxBot(object):
     
    def __init__ (self):
        self.pos = Position()
        self.time_for_move = None
        self.depth_per_move = 3
        self.board_values = [10 , 3 , 2 , 1 , 1 , 2 , 3 , 10 , 
                             3 , 2 , 1 , 1 , 1 , 1 , 2 , 3 ,
                             2 , 0.45 , 0.03 , 0.01 , 0.01 , 0.03 , 0.45 , 2 ,
                             1 , 0.5 , 0.01 , 0.05 , 0.05 , 0.01 , 0.5 , 1 ,
                             1 , 0.5 , 0.01 , 0.05 , 0.05 , 0.01 , 0.5 , 1 , 
                             2 , 0.45 , 0.03 , 0.01 , 0.01 , 0.03 , 0.45 , 2 ,
                             3 , 2 , 1 , 1 , 1 , 1 , 2 , 3 , 
                             10 , 3 , 2 , 1 , 1 , 2 , 3 , 10]
        self.prioritize_position = 40
         
    def output(self, cstr):
        sys.stdout.write(cstr)
        sys.stdout.flush()
         
    def error(self, cstr):
        sys.stderr.write(cstr)
        sys.stderr.flush()
         
    def command(self, cstr):
        if cstr.startswith('update position'):
            self.pos.setup(cstr[16:-1])
        elif cstr.startswith('update turn'):
            self.pos.turn = int(cstr[12])
        elif cstr.startswith('action'):
            self.time_for_move = int(cstr[7:])
            move = self.alphabeta(0, self.pos)
            #move = self.minmax()
            self.output('move ' + str(move) + '\n')
        elif cstr.startswith('quit'):
            quit()
        else:
            self.error('unknown command ' + cstr + '\n')
        return True
     
    #needs rework
    def evaluate(self, position):
 
        token_ratio = 100*((position.count[self.pos.turn]-position.count[3-self.pos.turn]) / (position.count[self.pos.turn]+position.count[3-self.pos.turn]))
        board_ratio = 100*((self.board_value(position,self.pos.turn)-self.board_value(position, 3-self.pos.turn)) / (1+(self.board_value(position,self.pos.turn)+self.board_value(position, 3-self.pos.turn))))
         
        return token_ratio + (self.prioritize_position/position.move_count())*board_ratio
                      
    def minmax(self):
        moves = self.pos.legal_moves()
        best_move = moves[0]
        depth = 0
        best_score = float('-inf')
        for move in moves:
            posi = self.pos.copy()
            posi.move(move)
            score = self.min_play(posi, depth+1)
            if score > best_score:
                best_move = move
                best_score = score
        return best_move
 
    def min_play(self, position, depth):
        if (position.game_over() != 0) or (depth==self.depth_per_move):
            return self.evaluate(position)
        moves = position.legal_moves()
        best_score = float('inf')
        for move in moves:
            posi = position.copy()
            posi.move(move)
            score = self.max_play(posi, depth+1)
            if score < best_score:
                best_score = score
        return best_score
             
    def max_play(self, position,depth):
        if (position.game_over() != 0) or (depth==self.depth_per_move):
            return self.evaluate(position)
        moves = position.legal_moves()
        best_score = float('-inf')
        for move in moves:
            posi = position.copy()
            posi.move(move)
            score = self.min_play(posi, depth+1)
            if score > best_score:
                best_score = score
        return best_score
        
    def board_value(self, position, turn):
        bv = 0
        tokens = [i for i in range(64) if position.board[i] == turn]
        for i in tokens:
            bv+=self.board_values[i]
             
        return bv
     
    def alphabeta(self,depth, position=Position(),alpha=float('-inf'),beta=float('inf')):
        if (position.game_over() != 0) or (depth==self.depth_per_move):
            return self.evaluate(position)
         
        if self.pos.turn == position.turn:
            best_score = float('-inf')
            moves = position.legal_moves()
            best_move = moves[0]
            for move in moves:
                posi = position.copy()
                posi.move(move)
                score = self.alphabeta(depth + 1, posi, alpha, beta)
                if score > best_score:
                    best_move = move
                    best_score = score
                #best_score = max(best_score, self.alphabeta(depth + 1, posi, alpha, beta))
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            if depth == 0:
                return best_move
            return best_score
        else:
            best_score = float('inf')
            moves = position.legal_moves()
            for move in moves:
                posi = position.copy()
                posi.move(move)
                score = self.alphabeta(depth + 1, posi, alpha, beta)
                if score < best_score:
                    best_move = move
                    best_score = score
                #best_score = min(best_score, self.alphabeta(depth + 1, posi, alpha, beta))
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            if depth == 0:
                return best_move
            return best_score
         
        return best_move
         
 
if __name__ == '__main__':
    bot = MinMaxBot()   
    while True:
        cstr = sys.stdin.readline()
        bot.command(cstr)
