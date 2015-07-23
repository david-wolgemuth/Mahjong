ROW = 0
COL = 1
CIRCLE = 'circle'
BAMBOO = 'bamboo'
CHAR = 'character'
ANIMAL = 'animal'
DIRECTIONAL = 'directional'
DRAGON = 'dragon'
SEASON = 'season'
TEXT = 'text'
AVALANCHE = 'avalanche'
TILE_SIZE = 20
TILE_RATIO = (3, 4)
TILE_DEPTH = int(TILE_SIZE * 0.4)
WINDOW_HEIGHT = 700
WINDOW_WIDTH = 1000

COLORS = {
    'R': 'firebrick4',
    'B': 'skyblue4',
    'G': 'olivedrab',
    'highlight': 'steelblue3',
    'face': 'linen',
    'left side': 'steelblue2',
    'bottom side': 'steelblue4',
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
