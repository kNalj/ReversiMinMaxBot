import tkinter
from tkinter import Frame, Canvas, Label

class GUI(object):
    
    cell_size = 50
    oval_start = 5
    oval_end = 45

    def __init__(self):
        # create GUI
        self.root = tkinter.Tk()
        self.root.protocol('WM_DELETE_WINDOW', self.close)        
        self.root.title('Reversi')
        frame = Frame(self.root)
        frame.pack()
        # add GUI elements
        self.black_label = Label(frame, text='Black: 00')
        self.black_label.pack(side=tkinter.LEFT)
        self.white_label = Label(frame, text='White: 00')
        self.white_label.pack(side=tkinter.RIGHT)        
        self.board_view = Canvas(frame, bg='lightblue', height=8*self.cell_size, width=8*self.cell_size) 
        self.board_view.pack(side=tkinter.TOP)

    def close(self):
        print("Exiting...")
        self.root.destroy()
    
    def show(self, board):
        self.board_view.children.clear()
        bpoints, wpoints = 0, 0
        # grid
        for i in range(8):
            self.board_view.create_line(0, i*self.cell_size, 8*self.cell_size, i*self.cell_size)
            self.board_view.create_line(i*self.cell_size, 0, i*self.cell_size, 8*self.cell_size)
        # pieces
        for i, c in enumerate(board):
            x, y = (i%8)*self.cell_size, (i//8)*self.cell_size
            oval = x+self.oval_start, y+self.oval_start, x+self.oval_end, y+self.oval_end
            if c == 1:
                bpoints += 1
                self.board_view.create_oval(oval, fill='black')
            elif c == 2:
                wpoints += 1
                self.board_view.create_oval(oval, fill='white')
        #points
        self.black_label['text'] = 'Black: {:02d}'.format(bpoints)
        self.white_label['text'] = 'White: {:02d}'.format(wpoints)

