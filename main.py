from board import *
import tkinter as tk
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

        top -= play.height * 3
        tag = 'Difficulty'
        diff = Button(self.canvas, left, top, value=tag, y=2,
                      size=size, ratio=ratio, click=False)
        left += diff.width
        text = 'Easy', 'Regular'
        ratio = (1, 1)
        easy = Button(self.canvas, left, top, tag=tag,
                      value=text[0], size=size, ratio=ratio, x=1, y=2)
        left += easy.width
        reg = Button(self.canvas, left, top, font=(None, 16),
                     tag=tag, value=text[1], size=size, ratio=ratio, x=2, y=2)
        reg.highlight_partner.append(easy)
        reg.toggle_highlight()
        easy.highlight_partner.append(reg)

        top -= play.height * 3
        left -= (diff.width + easy.width)
        tag = 'cheats'
        cheats = Button(self.canvas, left, top, value=tag, tag=tag,
                        ratio=(2, 1), size=size, click=False)
        left += cheats.width
        on = Button(self.canvas, left, top, value='On', tag=tag, ratio=ratio,
                    size=size, x=1)
        left += on.width
        off = Button(self.canvas, left, top, value='Off', tag=tag, ratio=ratio,
                     size=size, x=2)
        off.highlight_partner.append(on)
        on.highlight_partner.append(off)
        off.toggle_highlight()
        self.board.extend([play, diff, easy, reg, cheats, on, off])
        self.update()

    def select_tile(self, tile):
        if tile.tag == 'Play Game':
            self.board = []
            self.make()
            self.update()
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
