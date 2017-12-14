import sys, random
from position import Position

class FlatMCBot(object):
    
    def __init__(self):
        self.pos = Position()
        self.time_for_move = None
        self.sims_per_move = 3
    
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
            move = self.best_move()
            self.output('move ' + str(move) + '\n')
        elif cstr.startswith('quit'):
            quit()
        else:
            self.error('unknown command ' + cstr + '\n')
        return True
    
    def simulate(self, m):
        pos = self.pos.copy()
        pos.move(m)
        while pos.game_over() == 0:
            m = random.choice(pos.legal_moves())
            pos.move(m)
        if pos.game_over() == self.pos.turn:
            return 1.0
        elif pos.game_over() == 3:
            return 0.5
        else:
            return 0.0
        
    def best_move(self):
        moves = self.pos.legal_moves()
        values = [0.0] * len(moves)
        for i, m in enumerate(moves):
            for _ in range(self.sims_per_move):
                values[i] += self.simulate(m)
        move, value = max(zip(moves, values), key=lambda x: x[1])
        self.error(' '.join(str((m,v)) for m,v in zip(moves, values)) + '\n' )
        return move
    
if __name__ == '__main__':
    bot = FlatMCBot()        
    while True:
        cstr = sys.stdin.readline()
        bot.command(cstr)
        
