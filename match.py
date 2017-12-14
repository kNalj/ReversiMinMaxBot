import subprocess, threading
from subprocess import PIPE, STDOUT
from position import Position
from gui import GUI

# settings
time_per_move = 100
bot1cmd = 'python flatmcbot.py'
bot2cmd = 'python MinMax.py'

# globals
gui = None
thread_stop = False

def start_bots():
    print('starting bots')
    bot1 = subprocess.Popen(bot1cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    bot2 = subprocess.Popen(bot2cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    print('bots started')
    return bot1, bot2

def bot_command(bot, cstr):
    bot.stdin.write(cstr.encode())
    bot.stdin.flush()

def get_bot_move(turnbot, pos, verbose=False):
    turn, board = pos.tostring()
    bot_command(turnbot, 'update turn ' + turn + '\n')
    bot_command(turnbot, 'update position ' + board + '\n')
    bot_command(turnbot, 'action ' + str(time_per_move) + '\n')
    # read reply until move
    while True:
        rstr = turnbot.stdout.readline().decode()
        if verbose and len(rstr) > 0:
            print('(from bot) >>', rstr)
        if rstr.startswith('move'):
            move = int(rstr[5:])
            return move
    
def gui_play():
    # single game with GUI
    try:
        bot1, bot2 = start_bots()
        pos = Position()
        if gui is not None:
            gui.show(pos.board)
        while pos.game_over() == 0 and not thread_stop:
            turnbot = bot1 if pos.turn == 1 else bot2
            move = get_bot_move(turnbot, pos, verbose=True)
            pos.move(move)
            if gui is not None:
                gui.show(pos.board)
    except Exception as e:
        print(e)
    finally:
        print('Terminating bots')
        bot1.terminate()
        bot2.terminate()

def play_game(bot1, bot2):    
    pos = Position()
    while pos.game_over() == 0 and not thread_stop:
        turnbot = bot1 if pos.turn == 1 else bot2
        move = get_bot_move(turnbot, pos, verbose=False)
        pos.move(move)
    if pos.game_over() == 1:
        return (1.0, 0.0)
    elif pos.game_over() == 2:
        return (0.0, 1.0)
    else:        
        return (0.5, 0.5)
        
def test_play(ngames):
    # multiple games without GUI
    try:
        bot1, bot2 = start_bots()
        b1points, b2points = 0.0, 0.0
        for i in range(ngames//2):
            r1, r2 = play_game(bot1, bot2)
            b1points += r1  
            b2points += r2
            r2, r1 = play_game(bot2, bot1)
            b1points += r1  
            b2points += r2
            print(2*(i+1), b1points, b2points, int(100 * b1points / (b1points + b2points)), '%')
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as e:
        print(e)
    finally:
        print('Terminating bots')
        bot1.terminate()
        bot2.terminate()

show_game = False
if show_game:    
    # start GUI and additional thread for communication with bots
    gui = GUI()
    t = threading.Thread(target=gui_play)
    t.start()
    gui.root.mainloop()
    # stop additional thread when GUI closes
    gui = None
    thread_stop = True
    t.join()
else:
    test_play(100)

    