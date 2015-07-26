#! /usr/bin/env python

from board import *
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
import os


class Game(GameBoard):
    def __init__(self, canvas):
        GameBoard.__init__(self, canvas)

    def welcome_screen(self):
        self.update()
        size = 60
        ratio = (2, 1)
        left = (WINDOW_WIDTH / 2) - (3 * size * ratio[0])
        top = (WINDOW_HEIGHT / 2) + (2 * size * ratio[1])
        text = 'Play Game'
        play = Button(self.canvas, left, top, value=text,
                      tag=text, size=size, ratio=ratio, y=4)

        left += play.width * 3
        mahjong = Button(self.canvas, left, top, value='Mahjong',
                         font=('Apple Chancery', 48), size=size*2,
                         ratio=ratio, y=6)
        left -= play.width * 3
        # top -= play.height * 3
        # tag = DIFFICULTY
        # diff = Button(self.canvas, left, top, value=tag, y=2,
        #               size=size, ratio=ratio, click=False)
        # left += diff.width
        # text = 'Easy', 'Regular'
        # ratio = (1, 1)
        # easy = Button(self.canvas, left, top, tag=tag,
        #               value=text[0], size=size, ratio=ratio, x=1, y=2)
        # left += easy.width
        # reg = Button(self.canvas, left, top, font=(None, 16),
        #              tag=tag, value=text[1], size=size, ratio=ratio, x=2, y=2)
        # reg.highlight_partner.append(easy)
        # reg.toggle_highlight()
        # easy.highlight_partner.append(reg)

        top -= play.height * 3
        # left -= (diff.width + easy.width)
        tag = CHEAT
        cheats = Button(self.canvas, left, top, value=tag, tag=tag,
                        ratio=(2, 1), size=size, click=False)
        left += cheats.width
        on = Button(self.canvas, left, top, value='On', tag=tag,
                                ratio=ratio, size=size, x=1)
        left += on.width
        off = Button(self.canvas, left, top, value='Off', tag=tag, ratio=ratio,
                     size=size, x=2)
        off.highlight_partner.append(on)
        on.highlight_partner.append(off)
        off.toggle_highlight()

        left -= cheats.width * 2
        top -= play.height * 4

        created_by = Button(self.canvas, left, top, value=' Created \n   By:',
                            y=-2, size=size/2)
        left += created_by.width * 1.5
        david = Button(self.canvas, left, top, value='David Wolgemuth',
                       ratio=(2, 0.5), size=size*1.7, y=-2, x=2)

        self.board.extend([play,
                           mahjong,
                           # diff, easy, reg,
                           cheats, on, off,
                           created_by, david
                           ])
        self.update()

    def select_tile(self, tile):
        if tile.tag == 'Play Game':
            self.board = []
            self.make()
            self.update()
        elif tile.value == 'Undo':
            self.undo(tile)
        else:
            self.highlight_tile(tile)


class MainApp(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.height = WINDOW_HEIGHT
        self.width = WINDOW_WIDTH
        self.canvas = None
        self.game = None
        self.master.geometry('+%d+%d' % (300, 0))
        self.main()

    def main(self):
        self.make_main_canvas()
        self.game = Game(self.canvas)
        self.game.welcome_screen()

    def make_main_canvas(self):
        self.canvas = tk.Canvas(
            self.master,
            height=self.height,
            width=self.width,
            bg='azure2'
        )
        self.canvas.grid()


if __name__ == '__main__':
    root = tk.Tk()
    app = MainApp(root)
    os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
    root.mainloop()
