from constants import *

class Tile:
    def __init__(self, canvas, left, top, x, y, z, tag, size, ratio, depth):
        self.canvas = canvas
        self.size = size
        self.ratio = ratio
        self.x = x
        self.y = y
        self.plane = self.z = z
        self.tag = tag
        self.depth = depth
        self.face_color = COLORS['face']
        self.side_color = COLORS['left side'], COLORS['bottom side']

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
        self.shadow_top_squared = []
        self.shadow_right_bh = []
        self.shadow_right_th = []
        self.shadow_right_squared = []

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
        top = self.bottom - (self.height / 2)
        bottom = self.bottom - length
        right = self.right + length
        self.shadow_right_bh = [
            (left, top), (right, top),
            (right, bottom), (left, self.bottom)
        ]

    def toggle_highlight(self):
        if self.face_color == COLORS['face']:
            self.face_color = COLORS['highlight']
            self.side_color = COLORS['highlight'], COLORS['highlight']
        else:
            self.face_color = COLORS['face']
            self.side_color = COLORS['left side'], COLORS['bottom side']

    def make_tile(self):
        self.canvas.create_rectangle(
            self.rect,
            fill=self.face_color,
            outline='black',
            width=1,
            tag=self.tag
        )
        self.canvas.create_polygon(
            self.shadow_left,
            fill=self.side_color[0],
            outline='black',
            width=1,
            tag=self.tag
        )
        self.canvas.create_polygon(
            self.shadow_bottom,
            fill=self.side_color[1],
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
    def __init__(self, canvas, left, top, x, y, z, shape, value, tag=None,
                 size=TILE_SIZE, ratio=TILE_RATIO, depth=TILE_DEPTH):
        Tile.__init__(self, canvas, left, top, x, y, z, tag, size, ratio, depth)
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


class Button(FacedTile):
    def __init__(self, canvas, left, top, value, x=0, y=0, z=0, shape=TEXT, click=True,
                 xy=(0.5, 0.5), font=(None, 24), **kwargs):
        FacedTile.__init__(self, canvas, left, top, x, y, z, shape, value, **kwargs)
        self.text_x, self.text_y = xy
        self._font = font
        self.click = click
        self.highlight_partner = []

    def draw(self):
        if self.shape == TEXT:
            self.draw_text()
        elif self.shape == AVALANCHE:
            self.draw_avalanche()

    def draw_text(self):
        self.canvas.create_text(
            self._x(self.text_x), self._y(self.text_y),
            text=self.value,
            font=self._font,
            tag=self.tag,
        )

    def draw_avalanche(self):
        pass
