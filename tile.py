import tkinter as tk
from random import shuffle
import os

ROW = 0
COL = 1
CIRCLE = 'circle'
BAMBOO = 'bamboo'
CHAR = 'character'
ANIMAL = 'animal'
DIRECTIONAL = 'directional'
DRAGON = 'dragon'
SEASON = 'season'
TILE_SIZE = 20
TILE_RATIO = (3, 4)
TILE_DEPTH = int(TILE_SIZE * 0.4)
WINDOW_HEIGHT = 700
WINDOW_WIDTH = 1000

COLORS = {
    'R': 'firebrick4',
    'B': 'skyblue4',
    'G': 'olivedrab'
}

TILE_PLANES = [
    [0, 2, 1, 0],
    [None, 3, 3, 3],
    [None, None, 4, 4],
    [None, None, None, 5]
]

for p in TILE_PLANES:
    p += reversed(p)

BAMBOOS = list(range(1, 10))
CIRCLES = list(range(1, 10))
CHARACTERS = {
    1: [u'壹', u'一'],
    2: [u'貳', u'二'],
    3: [u'參', u'三'],
    4: [u'肆', u'四'],
    5: [u'伍', u'五'],
    6: [u'陸', u'六'],
    7: [u'柒', u'七'],
    8: [u'捌', u'八'],
    9: [u'玖', u'九']
}
DIRECTIONALS = {
    'North': u'北',
    'East': u'東部',
    'South': u'南',
    'West': u'西'
}
DRAGONS = {
    'Red': [u'中', COLORS['R']],
    'Green': [u'發', COLORS['G']],
    'White': [u'⟦⟧', COLORS['B']],
}
ANIMALS = {
    'tiger': [
        ['n', ('Superclarendon', 'L'), (0.7, 0.7)],
        [u'ر', (None, 'L'), (0.45, 0.4)],
        ['F', ('Brush Script MT', 'XS'), (0.53, 0.4)],
        ['ـد', (None, 'XS'), (0.35, 0.55)]
    ],
    'rat': [
        ['Q', ('Apple Chancery', 'L'), (0.45, 0.6)],
        ['c', ('Apple Chancery', 'M'), (0.4, 0.34)],
        ['o', ('Brush Script MT', 'M'), (0.5, 0.25)]
    ],
    'dragon': [
        [u'ى', (None, 'XL'), (0.45, 0.4)],
        [u'۵', (None, 'L'), (0.83, 0.5)]
    ],
    'rooster': [
        [u'C', ('Apple Chancery', 'L'), (0.45, 0.6)],
        [u'ا', (None, 'S'), (0.5, 0.82)],
        [u'ا', (None, 'S'), (0.45, 0.83)],
        [u'ر', (None, 'M'), (0.5, 0.5)],
        [u'ج', (None, 'M'), (0.5, 0.25)],
    ]
}
SEASONS = {
    'spring': [
        u'春', 1,
        [u'۳', 'L', 'G', (0.5, 0.7)],
        [u'۰۵', 'M', 'R', (0.5, 0.5)]
    ],
    'summer': [
        u'夏', 2,
        [u'༗', 'L', 'G', (0.5, 0.6)],
        [u'۰ᔊᠠ', 'M', 'R', (0.55, 0.5)]
    ],
    'autumn': [
        u'秋', 3,
        [u'ٱ', 'L', 'G', (0.5, 0.7)],
        [u'ھ', 'L', 'R', (0.5, 0.45)]
    ],
    'winter': [
        u'冬', 4,
        [u'۷', 'L', 'G', (0.5, 0.7)],
        [u'۰', 'L', 'R', (0.6, 0.5)],
        [u'ݸ', 'M', 'R', (0.3, 0.45)]
    ],
}

ALL_TILES = {
    CHAR: [CHARACTERS.keys(), 4],
    BAMBOO: [BAMBOOS, 4],
    CIRCLE: [CIRCLES, 4],
    DIRECTIONAL: [DIRECTIONALS.keys(), 4],
    SEASON: [SEASONS.keys(), 1],
    ANIMAL: [ANIMALS.keys(), 1],
    DRAGON: [DRAGONS.keys(), 4]
}

class Tile:
    def __init__(self, canvas, left, top, x, y, z, tag):
        self.canvas = canvas
        self.size = TILE_SIZE
        self.ratio = TILE_RATIO
        self.x = x
        self.y = y
        self.plane = self.z = z
        self.tag = tag
        self.depth = TILE_DEPTH

        self.height = 0
        self.width = 0
        self.left = left + (self.plane * self.depth)
        self.top = top - (self.plane * self.depth)
        self.bottom = 0
        self.right = 0
        self.rect = []

        self.shadow_left = []
        self.shadow_bottom = []
        self.shadow_right = []
        self.shadow_top = []
        self.shadow_right_bh = []
        self.shadow_right_th = []

        self.set_sides()
        self.set_shadow()

    def set_sides(self):
        self.height = int(self.size * self.ratio[1])
        self.width = int(self.size * self.ratio[0])
        self.bottom = self.top + self.height
        self.right = self.left + self.width
        self.rect = self.left, self.top, self.right, self.bottom

    def set_shadow(self):
        length = self.depth

        # Bottom Shadow
        top = self.bottom
        bottom = top + length
        left = self.left - length
        right = self.right - length
        self.shadow_bottom = [
            (self.left, top), (self.right, top),
            (right, bottom), (left, bottom)
        ]

        # Left Shadow
        top = self.top + length
        bottom = self.bottom + length
        right = self.left
        left = right - length
        self.shadow_left = [
            (left, top), (right, self.top),
            (right, self.bottom), (left, bottom)
        ]

        # Top Shadow
        top = self.top - length
        bottom = self.top
        left = self.left + length
        right = self.right + length
        self.shadow_top = [
            (self.left, bottom), (left, top),
            (right, top), (self.right, bottom)
        ]

        # Squared Top Shadow
        self.shadow_top_squared = [
            (self.left, bottom), (left, top),
            (self.right, top), (self.right, bottom)
        ]

        # Right Shadow
        top = self.top - length
        bottom = self.bottom - length
        left = self.right
        right = self.right + length
        self.shadow_right = [
            (left, self.top), (right, top),
            (right, bottom), (left, self.bottom)
        ]

        # Squared Right Shadow
        self.shadow_right_squared = [
            (left, self.top), (right, self.top),
            (right, bottom), (left, self.bottom)
        ]

        # Right Top Half Shadow
        left = self.right
        top = self.top - length
        bottom = self.bottom - (self.height / 2)
        right = self.right + length
        self.shadow_right_th = [
            (left, self.top), (right, top),
            (right, bottom), (left, bottom)
        ]

        # Right Bottom Half Shadow
        left = self.right
        top = self.bottom - ((self.height) / 2)
        bottom = self.bottom - length
        right = self.right + length
        self.shadow_right_bh = [
            (left, top), (right, top),
            (right, bottom), (left, self.bottom)
        ]

    def make_tile(self):
        self.canvas.create_rectangle(
            self.rect,
            fill='linen',
            outline='black',
            width=1,
            tag=self.tag
        )
        self.canvas.create_polygon(
            self.shadow_bottom,
            fill='steelblue4',#tan4',
            outline='black',
            width=1,
            tag=self.tag
        )
        self.canvas.create_polygon(
            self.shadow_left,
            fill='steelblue2',#bisque2',
            outline='black',
            width=1,
            tag=self.tag
        )

    def make_shadow(self, *sides):
        for side in sides:
            self.canvas.create_polygon(
                side,
                fill='gray30',
                outline='gray30',
                width=1,
                tag=self.tag
            )


class FacedTile(Tile):
    def __init__(self, canvas, left, top, x, y, z, shape, value, tag):
        Tile.__init__(self, canvas, left, top, x, y, z, tag)
        self.shape = shape
        self.value = value
        self.pattern = []
        self.coordinates = []
        self.fontsize = {
            'XS': int(self.size / 2),
            'S': int(self.size / 1.5),
            'M': self.size,
            'L': int(self.size * 1.5),
            'XL': int(self.size * 2.5),
        }
        if isinstance(self.value, int):
            self.choose_pattern()
            self.set_pattern()

    def _x(self, x):
        return self.left + (self.width * x)

    def _y(self, y):
        return self.top + (self.height * y)

    def choose_pattern(self):
        empty = [False] * 9
        patterns = [
            [5],
            [2, 8],
            [1, 5, 9],
            [1, 3, 7, 9],
            [1, 3, 5, 7, 9],
            [1, 3, 4, 6, 7, 9],
            [1, 2, 3, 5, 7, 8, 9],
            [1, 2, 3, 4, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9]
        ]
        pattern = patterns[self.value-1]
        for shape in pattern:
            empty[shape-1] = True
        self.pattern = [
            empty[0:3],
            empty[3:6],
            empty[6:]
        ]

    def set_pattern(self):
        rows = [
            int(self.height * 1/5) + self.top,
            int(self.height * 1/2) + self.top,
            int(self.height * 4/5) + self.top
        ]
        columns = [
            int(self.width * 1/5) + self.left,
            int(self.width * 1/2) + self.left,
            int(self.width * 4/5) + self.left
        ]
        for row in range(len(self.pattern)):
            for column in range(len(self.pattern[row])):
                if self.pattern[row][column]:
                    self.coordinates.append(
                        [rows[row], columns[column]]
                    )

    def draw(self):
        if self.shape == CIRCLE:
            self.draw_circles()
        elif self.shape == BAMBOO:
            self.draw_bamboo()
        elif self.shape == CHAR:
            self.draw_character()
        elif self.shape == ANIMAL:
            self.draw_animal()
        elif self.shape == DIRECTIONAL:
            self.draw_directional()
        elif self.shape == DRAGON:
            self.draw_dragon()
        elif self.shape == SEASON:
            self.draw_season()

    def draw_circles(self):
        radius = self.width * 0.13 if self.value != 1 else self.width * 0.35
        for circle in self.coordinates:
            for i in range(1, 3):
                left = circle[COL] - int(radius/i)
                top = circle[ROW] - int(radius/i)
                right = circle[COL] + int(radius/i)
                bottom = circle[ROW] + int(radius/i)
                self.canvas.create_oval(
                    left, top, right, bottom,
                    outline='black',
                    fill='SkyBlue4' if i == 2 else None,
                    width=1,
                    tag=self.tag
                )

    def draw_bamboo(self):
        rat = 0.12 if self.value != 1 else 0.2
        width = self.width * rat
        height = self.height * rat
        for bamboo in self.coordinates:
            left = bamboo[COL] - width
            top = bamboo[ROW] - height
            right = bamboo[COL] + width
            bottom = bamboo[ROW] + height
            midx = int((right + left) / 2)
            midy = int((bottom + top) / 2)
            offset = int((right - left) * 0.2)
            corners = [
                (left, top), (right, top),
                (midx - offset, midy), (right, bottom),
                (left, bottom), (midx + offset, midy)
            ]
            self.canvas.create_polygon(
                corners,
                outline='black',
                fill='olive drab',
                width=1,
                tag=self.tag
            )

    def draw_character(self):
        self.canvas.create_text(
            self._x(0.9), self._y(0.1),
            text=self.value,
            font=(None, self.fontsize['S']),
            tag=self.tag

        )
        self.canvas.create_text(
            self._x(0.5), self._y(0.25),
            text=CHARACTERS[self.value][1],
            font=(None, self.fontsize['M']),
            tag=self.tag

        )
        self.canvas.create_text(
            self._x(0.5), self._y(0.7),
            text=CHARACTERS[self.value][0],
            font=(None, self.fontsize['L']),
            fill='firebrick4',
            tag=self.tag
        )

    def draw_animal(self):
        animal = ANIMALS[self.value]
        for part in animal:
            text = part[0]
            font = part[1][0]
            size = part[1][1]
            x = part[2][0]
            y = part[2][1]
            self.canvas.create_text(
                self._x(x), self._y(y),
                text=text,
                font=(font, self.fontsize[size]),
                fill='black',
                tag=self.tag
            )

    def draw_directional(self):
        fs = 'XL' if self.value != 'East' else 'L'
        self.canvas.create_text(
            self._x(0.5), self._y(0.5),
            text=DIRECTIONALS[self.value],
            font=(None, self.fontsize[fs]),
            fill='black',
            tag=self.tag
        )
        self.canvas.create_text(
            self._x(0.72), self._y(0.1),
            text=self.value,
            font=(None, self.fontsize['XS']),
            fill='firebrick4',
            tag=self.tag
        )

    def draw_dragon(self):
        text = DRAGONS[self.value][0]
        color = DRAGONS[self.value][1]
        self.canvas.create_text(
            self._x(0.5), self._y(0.5),
            text=text,
            font=(None, self.fontsize['XL']),
            fill=color,
            tag=self.tag
        )

    def draw_season(self):
        char = SEASONS[self.value][0]
        num = SEASONS[self.value][1]
        flower = SEASONS[self.value][2:]
        self.canvas.create_text(
            self._x(0.27), self._y(0.17),
            text=char,
            font=(None, self.fontsize['M']),
            fill=COLORS['R'],
            tag=self.tag
        )
        self.canvas.create_text(
            self._x(0.83), self._y(0.17),
            text=num,
            font=(None, self.fontsize['S']),
            fill=COLORS['B'],
            tag=self.tag
        )
        for aspect in flower:
            text = aspect[0]
            size = aspect[1]
            color = COLORS[aspect[2]]
            x = aspect[3][0]
            y = aspect[3][1]
            self.canvas.create_text(
                self._x(x), self._y(y),
                text=text,
                font=(None, self.fontsize[size]),
                fill=color,
                tag=self.tag
            )

    def make(self):
        self.make_tile()
        self.draw()


class Board:
    def __init__(self, canvas):
        self.canvas = canvas
        self.border_x = int
        self.border_y = int
        self.temp_board = []
        self.temp_board_specials = {}
        self.board = []
        self.unplaced_tiles = []
        self.set_border()

    def make(self):
        self.randomize_tiles()
        self.make_planes()
        self.fill_spaces()
        if self.canvas:
            self.place_tiles()
            self.make_tiles()

    def set_border(self):
        x = WINDOW_WIDTH - 15 * TILE_SIZE * TILE_RATIO[0]
        y = WINDOW_HEIGHT - 8 * TILE_SIZE * TILE_RATIO[1]
        self.border_x = int(x / 2)
        self.border_y = int(y / 2)

    def randomize_tiles(self):
        for tile_type in ALL_TILES:
            for value in ALL_TILES[tile_type][0]:
                for i in range(ALL_TILES[tile_type][1]):
                    self.unplaced_tiles.append((tile_type, value))
        shuffle(self.unplaced_tiles)

    def make_planes(self):
        for z in range(4):
            plane = []
            for y in range(8):
                row = []
                for x in range(12):
                    row.append([])
                plane.append(row)
            self.temp_board.append(plane)
        self.temp_board_specials = {
            'apex': [4, 6.5],
            'left': [0, 0],
            'r1': [0, 13],
            'r2': [0, 14]
        }

    def fill_spaces(self):
        for z, plane in enumerate(self.temp_board):
            for y, row in enumerate(plane):
                for x, space in enumerate(row):
                    border = TILE_PLANES[z][y]
                    if isinstance(border, int) and border <= x < 12 - border:
                        space.extend(self.unplaced_tiles.pop())
                    else:
                        space.append(None)
        for space in self.temp_board_specials:
            self.temp_board_specials[space].extend(self.unplaced_tiles.pop())

    def place_tiles(self):
        self.place_special('r2', 'r1')
        for z, plane in enumerate(self.temp_board):
            for y, row in enumerate(plane):
                for x, tile in enumerate(reversed(row)):
                    if tile[0]:
                        self.place_tile(tile, 12-x, y, z)
        self.place_special('left', 'apex')

    def place_special(self, *spaces):
        for space in spaces:
            z, x, shape, value = self.temp_board_specials[space]
            self.place_tile([shape, value], x, 3.5, z)

    def place_tile(self, tile, x, y, z):
        tile_width = TILE_SIZE * TILE_RATIO[0]
        tile_height = TILE_SIZE * TILE_RATIO[1]
        x_ = x + self.border_x + tile_width * x
        y_ = y + self.border_y + tile_height * y
        shape = tile[0]
        value = tile[1]
        tag = '%s::%s' % (shape, value)
        tile = FacedTile(self.canvas, x_, y_, x, y, z, shape, value, tag)
        self.board.append(tile)

    def make_tiles(self):
        for z in range(-10, 10):
            plane = []
            for tile in self.board:
                if tile.z == z:
                    plane.append(tile)
            plane.sort(key=lambda t: t.x, reverse=True)
            for tile in plane:
                tile.make()
                self.make_shadow(tile)

    def make_shadow(self, tile):
        bordering_x = False
        bordering_y = False
        up_over = False
        only_th = False
        only_bh = False
        sq_top = False

        for tile_2 in self.board:
            if tile_2.z == tile.z:
                if tile_2.x == tile.x + 1:
                    if tile_2.y == tile.y:
                        bordering_x = True
                    elif tile_2.y == tile.y + 0.5:
                        only_th = True
                    elif tile_2.y == tile.y - 0.5:
                        only_bh = True
                        sq_top = True
                if tile_2.y == tile.y - 1:
                    if tile_2.x == tile.x:
                        bordering_y = True
                    elif tile_2.x == tile.x + 1:
                        up_over = True

        if not bordering_x:
            if only_bh and only_th:
                pass
            elif only_th:
                tile.make_shadow(tile.shadow_right_th)
            elif only_bh:
                tile.make_shadow(tile.shadow_right_bh)
            elif up_over:
                tile.make_shadow(tile.shadow_right_squared)
            else:
                tile.make_shadow(tile.shadow_right)

        if not bordering_y:
            if up_over:
                tile.make_shadow(tile.shadow_top_squared)
            elif sq_top:
                tile.make_shadow(tile.shadow_top_squared)
            else:
                tile.make_shadow(tile.shadow_top)


class GameBoard(Board):
    def __init__(self, canvas):
        Board.__init__(self, canvas)
        self.canvas.bind('<Button 1>', self.get_mouse_click)
        self.highlighted_tile = None

    def get_mouse_click(self, event):
        x = event.x
        y = event.y
        eligible_tiles = []
        for tile in self.board:
            d = tile.depth
            if (
                        (tile.left < x < tile.right and
                         tile.top < y < tile.bottom)
                    or (tile.left < x + d < tile.right and
                        tile.top < y - d < tile.bottom)
            ):
                eligible_tiles.append(tile)

        highest = None
        for tile in eligible_tiles:
            if (
                    not highest or
                    tile.plane > highest.plane or
                    (tile.plane == highest.plane and tile.x < highest.x)
            ):
                highest = tile

        if highest:
            self.process_tile_click(tile)

    def process_tile_click(self, tile):
        blocking_left = False
        blocking_right = False
        blocking_top = False
        x1 = tile.x
        y1 = tile.y
        z1 = tile.z
        for tile_2 in self.board:
            if tile is tile_2:
                continue
            x2 = tile_2.x
            y2 = tile_2.y
            z2 = tile_2.z
            if y2 - 0.5 <= y1 <= y2 + 0.5 and z1 <= z2:
                if x2 - 0.5 <= x1 <= x2 + 0.5:
                    blocking_top = True
                    break
                if x1 == x2 + 1:
                    blocking_left = True
                if x1 == x2 - 1:
                    blocking_right = True
        if not (blocking_left and blocking_right) and not blocking_top:
            self.highlight_tile(tile)

    def highlight_tile(self, tile):
        if self.highlighted_tile is tile:
            self.canvas.delete('highlight')
            self.highlighted_tile = None
        elif (
                (self.highlighted_tile and
                 self.highlighted_tile.shape == tile.shape) and
                (tile.value == self.highlighted_tile.value or
                 tile.shape == ANIMAL or
                 tile.shape == SEASON)
            ):
            self.remove_tile(tile)
            self.remove_tile(self.highlighted_tile)
        else:
            self.highlighted_tile = tile
            self.canvas.delete('highlight')
            self.canvas.create_rectangle(
                tile.rect,
                fill=None,
                outline='springgreen2',
                width=4,
                tag='highlight'
            )

    def remove_tile(self, tile):
        self.board.remove(tile)
        self.canvas.delete('all')
        self.make_tiles()


class MainApp(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.height = WINDOW_HEIGHT
        self.width = WINDOW_WIDTH
        self.canvas = None
        self.board = None
        self.master.geometry('+%d+%d' % (300, 0))
        self.main()

    def main(self):
        self.make_main_canvas()
        self.board = GameBoard(self.canvas)
        self.board.make()

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
