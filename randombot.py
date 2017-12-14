import sys, random, time
from position import Position

class RandomBot(object):
    
    def __init__(self):
        self.pos = Position()
        self.time_for_move = None
    
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

    def best_move(self):
        #time.sleep(self.time_for_move/1000)
        return random.choice(self.pos.legal_moves())    
    
if __name__ == '__main__':
    bot = RandomBot()        
    while True:
        cstr = sys.stdin.readline()
        bot.command(cstr)
        
