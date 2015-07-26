from tile import *
import random

class Board:
    def __init__(self, canvas):
        self.canvas = canvas
        self.border_x = int
        self.border_y = int
        self.temp_board = []
        self.temp_board_specials = {}
        self.board = []
        self.cheat_tiles = []
        self.removed_tiles = []
        self.unplaced_tiles = []
        self.set_border()
        self.cheats = False
        self.easy = False

    def make(self):
        self.randomize_tiles()
        self.make_planes()
        if self.easy:
            self.fill_spaces_easy()
        else:
            self.fill_spaces()
        if self.canvas:
            self.place_tiles()
            if self.cheats:
                self.place_cheats()
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
        random.shuffle(self.unplaced_tiles)

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
                        self.place_tile(tile, 12 - x, y, z)
        self.place_special('left', 'apex')

    def place_special(self, *spaces):
        for space in spaces:
            z, x, shape, value = self.temp_board_specials[space]
            self.place_tile([shape, value], x, 3.5, z)

    def place_cheats(self):
        for i in range(6):
            x = 14
            y = 6
            z = i
            self.place_tile([CHEAT, 'Undo'], x, y, z)

    def place_tile(self, tile, x, y, z):
        tile_width = TILE_SIZE * TILE_RATIO[0]
        tile_height = TILE_SIZE * TILE_RATIO[1]
        x_ = self.border_x + tile_width * x
        y_ = self.border_y + tile_height * y
        shape = tile[0]
        value = tile[1]
        tag = '%s::%s' % (shape, value)
        if CHEAT in tag:
            tile = Button(self.canvas, x_, y_, value, x, y, z, TEXT,
                          depth=(TILE_DEPTH/2))
            self.cheat_tiles.append(tile)
        else:
            tile = FacedTile(self.canvas, x_, y_, x, y, z, shape, value, tag)
            self.board.append(tile)

    def make_tiles(self):
        for z in range(-10, 10):
            plane = []
            for board in self.board, self.cheat_tiles:
                for tile in board:
                    if tile.z == z:
                        plane.append(tile)
            plane.sort(key=lambda t: t.y)
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

    def update(self):
        self.canvas.delete('all')
        self.make_tiles()

    def get_mouse_click(self, event):
        x = event.x
        y = event.y
        eligible_tiles = []
        board = self.board + self.cheat_tiles
        for tile in board:
            d = tile.depth
            if (
                (tile.left < x < tile.right and
                 tile.top < y < tile.bottom) or
                (tile.left < x + d < tile.right and
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
            self.process_tile_click(highest)

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
        if hasattr(tile, 'click'):
            if tile.click:
                self.select_tile(tile)
        elif (not (blocking_left and blocking_right) and
              not blocking_top):
            self.select_tile(tile)

    def select_tile(self, tile):
        self.highlight_tile(tile)

    def highlight_tile(self, tile):
        if hasattr(tile, 'highlight_partner') and tile.highlight_partner:
            for i in tile.highlight_partner:
                tile.highlight_partner[0].toggle_highlight()
            tile.toggle_highlight()
            self.setup_preferences(tile)
        elif self.highlighted_tile is tile:
            self.highlighted_tile = None
            tile.toggle_highlight()
        elif (
            (self.highlighted_tile and
             self.highlighted_tile.shape == tile.shape) and
            (tile.value == self.highlighted_tile.value or
             tile.shape == ANIMAL or tile.shape == SEASON)
        ):
            self.remove_tile(tile)
            self.remove_tile(self.highlighted_tile)
        else:
            if self.highlighted_tile:
                self.highlighted_tile.toggle_highlight()
            self.highlighted_tile = tile
            tile.toggle_highlight()
        self.update()

    def remove_tile(self, tile, group=None):
        if group:
            group.remove(tile)
        else:
            self.board.remove(tile)
            self.removed_tiles.append(tile)
        self.update()

    def setup_preferences(self, tile):
        if tile.tag == CHEAT:
            if tile.value == 'On':
                self.cheats = True
            elif tile.value == 'Off':
                self.cheats = False
        elif tile.tag == DIFFICULTY:
            if tile.value == 'Easy':
                self.easy = True
            elif tile.value == 'Regular':
                self.easy = False

    def undo(self, undo_tile):
        if self.removed_tiles:
            self.board.append(self.removed_tiles.pop())
            self.board.append(self.removed_tiles.pop())
            self.cheat_tiles.remove(undo_tile)
            self.update()
