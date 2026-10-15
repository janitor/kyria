from pathlib import Path
from subprocess import check_output
import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph


OUT = Path(__file__).with_name('CHEATSHEET.pdf')

FONT_DIR = Path(os.environ['KYRIA_FONT_DIR']) if 'KYRIA_FONT_DIR' in os.environ else None


def font_file(pattern, preferred):
    if FONT_DIR is not None:
        path = FONT_DIR / preferred
        if not path.is_file():
            raise FileNotFoundError(path)
        return str(path)
    return check_output(['fc-match', '-f', '%{file}', pattern], text=True).strip()


pdfmetrics.registerFont(TTFont('Noto', font_file('sans:style=Regular', 'NotoSans-Regular.ttf')))
pdfmetrics.registerFont(TTFont('NotoBold', font_file('sans:style=Bold', 'NotoSans-Bold.ttf')))
pdfmetrics.registerFont(TTFont('Key', font_file('sans:style=Bold', 'DejaVuSans-Bold.ttf')))

W, H = landscape(A4)
INK = colors.HexColor('#17233B')
MUTED = colors.HexColor('#617086')
BLUE = colors.HexColor('#2368B6')
PALE = colors.HexColor('#EDF4FC')
TEAL = colors.HexColor('#187B75')
TEAL_PALE = colors.HexColor('#EBF8F5')
AMBER = colors.HexColor('#9A5C0A')
AMBER_PALE = colors.HexColor('#FFF7E9')
LINE = colors.HexColor('#D8E1EC')
PAPER = colors.white

c = Canvas(str(OUT), pagesize=(W, H))
c.setTitle('Kyria Wireless — current keymap cheat sheet')
c.setAuthor('')


def txt(x, y, s, size=10, color=INK, bold=False):
    c.setFillColor(color)
    c.setFont('NotoBold' if bold else 'Noto', size)
    c.drawString(x, y, s)


def para(x, top, width, s, size=9, leading=12, color=INK, bold=False):
    style = ParagraphStyle(
        'p', fontName='NotoBold' if bold else 'Noto', fontSize=size,
        leading=leading, textColor=color, alignment=TA_LEFT,
        spaceBefore=0, spaceAfter=0,
    )
    p = Paragraph(s, style)
    _, h = p.wrap(width, 1000)
    p.drawOn(c, x, top - h)
    return top - h


def card(x, y, w, h, fill=PAPER, stroke=LINE):
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.setLineWidth(0.8)
    c.roundRect(x, y, w, h, 9, fill=1, stroke=1)


def header(num, title, subtitle):
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.rect(0, H - 9, W, 9, fill=1, stroke=0)
    txt(32, 557, title, 19, INK, True)
    txt(32, 538, subtitle, 9.2, MUTED)
    c.setStrokeColor(LINE)
    c.line(32, 27, W - 32, 27)
    txt(32, 13, 'Halcyon Kyria rev4 • Wellum 36 QWERTY • current base keymap', 7.5, MUTED)
    c.setFont('NotoBold', 8)
    c.setFillColor(MUTED)
    c.drawRightString(W - 32, 13, str(num) + ' / 3')


def key(x, y, w, h, value, label=None, fill=PALE, border=LINE,
        value_size=10, value_color=INK):
    c.setFillColor(fill)
    c.setStrokeColor(border)
    c.roundRect(x, y, w, h, 5, fill=1, stroke=1)
    if label:
        txt(x + 5, y + h - 11, label, 7.2, MUTED, True)
    c.setFont('Key', value_size)
    c.setFillColor(value_color)
    tw = pdfmetrics.stringWidth(value, 'Key', value_size)
    c.drawString(x + (w - tw) / 2, y + (h - value_size) / 2 + (0 if label else 2), value)


def base_row(y, left, right):
    x1, x2, kw, gap = 48, 462, 52, 4
    for i, item in enumerate(left):
        label, val = item if isinstance(item, tuple) else (None, item)
        fill = PAPER if val == '·' else PALE
        if val == 'NAV': fill = TEAL_PALE
        key(x1 + i * (kw + gap), y, kw, 34, val, label=label, fill=fill,
            value_color=MUTED if val == '·' else INK, value_size=10 if label else 9.5)
    for i, item in enumerate(right):
        label, val = item if isinstance(item, tuple) else (None, item)
        fill = PAPER if val == '·' else PALE
        if val == 'Bksp': fill = TEAL_PALE
        key(x2 + i * (kw + gap), y, kw, 34, val, label=label, fill=fill,
            value_color=MUTED if val == '·' else INK, value_size=10 if label else 9.1)


def action(x, y, w, name, combo, note=None):
    c.setStrokeColor(LINE)
    c.line(x, y - 7, x + w, y - 7)
    txt(x, y + 6, name, 9.1, INK, True)
    c.setFont('NotoBold', 9)
    c.setFillColor(BLUE)
    c.drawRightString(x + w, y + 6, combo)
    if note:
        txt(x, y - 5, note, 7.5, MUTED)


def layer_map(y, name, description, left_rows, right_rows, note):
    x, w, h = 32, W - 64, 157
    card(x, y, w, h)
    txt(x + 14, y + 136, name, 12.5, BLUE, True)
    txt(x + 75, y + 137, description, 8.2, MUTED)
    label_left = [['Q','W','E','R','T'], ['A','S','D','F','G'], ['Z','X','C','V','B']]
    label_right = [['Y','U','I','O','P'], ['H','J','K','L',';'], ['N','M',',','.','/']]
    for r in range(3):
        yy = y + 92 - r * 34
        for i in range(5):
            kw, gap = 60, 4
            v1, v2 = left_rows[r][i], right_rows[r][i]
            key(47 + i * (kw + gap), yy, kw, 29, v1, label_left[r][i],
                value_size=7.9 if len(v1) > 7 else 8.8,
                fill=TEAL_PALE if ('1×' in v1 or v1 == 'GAME') else PALE)
            key(468 + i * (kw + gap), yy, kw, 29, v2, label_right[r][i],
                value_size=7.9 if len(v2) > 7 else 8.8,
                fill=TEAL_PALE if '1×' in v2 else PALE)
    txt(x + 14, y + 8, note, 7.7, MUTED)


# Page 1: physical BASE and daily actions.
header(1, 'Kyria × Universal Layout Ortho',
       'Large: EN / RU output on Mac. Small: key sent by Kyria firmware.')
card(32, 307, W - 64, 225)
txt(47, 510, 'BASE · English / Russian', 12, BLUE, True)
txt(47, 491, 'Left half', 8.5, MUTED)
txt(462, 491, 'Right half', 8.5, MUTED)
base_row(448,
    ['Tab', ('Q','q / й'), ('W','w / ц'), ('E','e / у'), ('R','r / к'), ('T','t / е')],
    [('Y','y / н'), ('U','u / г'), ('I','i / ш'), ('O','o / з'), ('P','p / х'), 'Bksp'])
base_row(409,
    ['Esc', ('A','a / ф'), ('S','s / ы'), ('D','d / в'), ('F','f / а'), ('G','g / п')],
    [('H','h / р'), ('J','j / о'), ('K','k / л'), ('L','l / д'), (';','~ / ж'), '·'])
base_row(370,
    ['·', ('Z','z / я'), ('X','x / ч'), ('C','c / с'), ('V','v / м'), ('B','b / и')],
    [('N','n / т'), ('M','m / ь'), (',','& / б'), ('.','[ / ю'), ('/','] / э'), '·'])
txt(364, 360, 'next to B: F13 → Universal', 7.1, TEAL, True)
for x, vals, kw, gap in [(48, ['LCmd','Caps','Space','NAV','ALT'], 58, 3),
                         (511, ['Caps','SYM','Shift','ALT','RCmd'], 54, 3)]:
    for i, v in enumerate(vals):
        key(x + i * (kw + gap), 320, kw, 33, v,
            fill=TEAL_PALE if v in ['NAV','SYM','ALT'] else PALE,
            value_size=8.8)

txt(32, 281, 'COMMON ACTIONS', 10, BLUE, True)
left_actions = [
    ('Backspace', 'right of P / NAV+O'),
    ('Forward delete', 'NAV+P'),
    ('Enter', 'NAV+G / NAV+H'),
    ('Escape', 'NAV+T / NAV+Y'),
    ('Arrows ← ↓ ↑ →', 'NAV+J / K / L / ;'),
    ('Home / End', 'NAV+U / I'),
]
right_actions = [
    ('Page Up / Down', 'NAV+M / ,'),
    ('Digits 1-5', 'NUM+Q / W / E / R / T'),
    ('Digits 6-0', 'NUM+Y / U / I / O / P'),
    ('SYM: top row', '! @ # $ % / ^ ? * ( )'),
    ('F1-F10', 'SYM+NAV + lower row'),
    ('English / Russian', 'Caps: second left'),
]
for i, (name, combo) in enumerate(left_actions):
    action(32, 254 - i * 35, 372, name, combo)
for i, (name, combo) in enumerate(right_actions):
    action(438, 254 - i * 35, 372, name, combo)
txt(32, 36, 'NUM = NAV + SYM. F13 next to B selects Universal via Karabiner; NAV+W switches app windows.', 8, MUTED)
c.showPage()


# Page 2: full working-layer maps.
header(2, 'NAV, SYM and NUM',
       'Small: BASE position. SYM shows Universal Layout Ortho output; NUM sends keypad digits.')
layer_map(376, 'NAV', 'Hold inner left thumb key',
    [['C+Tab','Cmd+`','C+S+Tab','C+Tab','Esc'],
     ['1× Cmd','1× Opt','1× Ctrl','1× Shift','Enter'],
     ['C+M+←','C+M+→','GAME','Print','Tab']],
    [['Esc','Home','End','Bksp','Del'],
     ['Enter','←','↓','↑','→'],
     ['Tab','PgUp','PgDn',"'",'NumLock']],
    'NAV + Caps position = CMD. NAV+C activates GAME.')
layer_map(207, 'SYM', 'Hold second left key of right thumb cluster',
    [['!','@','#','$','%'],
     ['~ / ж','`',"'",'"','-'],
     ['\\','¦',';',',','_']],
    [['^','?','*','(',')'],
     ['+','1× Shift','1× Ctrl','1× Opt','1× Cmd'],
     ['=','.',':','|','/']],
    'SYM+Q..P sends symbols. Right of P is Backspace. ~ / ж depends on Caps.')
layer_map(38, 'NUM', 'Hold NAV and SYM together',
    [['KP1','KP2','KP3','KP4','KP5'],
     ['1× Cmd','1× Opt','1× Ctrl','1× Shift','F11'],
     ['F1','F2','F3','F4','F5']],
    [['KP6','KP7','KP8','KP9','KP0'],
     ['F12','1× Shift','1× Ctrl','1× Opt','1× Cmd'],
     ['F6','F7','F8','F9','F10']],
    'Hold NAV+SYM for digits 1-0. Right of P is Backspace; 1× modifies the next key.')
c.showPage()


# Page 3: Mac behavior and remaining layers.
header(3, 'Mac, other layers and Studio',
       'Universal Layout Ortho is selected in macOS; Kyria sends firmware keys and saved Studio changes.')

card(32, 174, 379, 359)
txt(46, 511, 'MAC: LANGUAGE, WINDOWS AND TABS', 10.5, BLUE, True)
top = 491
sections = [
    ('English / Russian',
     'With <b>Universal Layout Ortho</b> selected, press the second left thumb key, <b>Caps</b>, to switch EN/RU within the layout. The macOS input source stays the same. Select Polish separately.'),
    ('Digits and symbols',
     '<b>NAV+SYM</b> activates NUM: the top row sends digits 1-0. On SYM it sends <b>! @ # $ % ^ ? * ( )</b>. The ; , . / keys also change in Universal; see BASE.'),
    ('macOS windows and apps',
     '<b>NAV+W</b> sends Command+Grave for the next window. To switch apps: <b>NAV+A</b>, release, then <b>NAV+B</b> or <b>NAV+N</b> sends Command+Tab. The app sequence is not yet verified.'),
    ('Tabs',
     '<b>NAV+Q</b> or <b>NAV+R</b> sends Control+Tab; <b>NAV+E</b> sends Control+Shift+Tab. These work in apps that support them.'),
    ('Restore Universal',
     'F13 next to B selects Universal Layout Ortho via Karabiner. The outer LCmd and RCmd thumb keys may select U.S. or Russian.'),
]
for title, body in sections:
    txt(47, top, title, 9.2, TEAL, True)
    top = para(47, top - 5, 349, body, 8.5, 11.7) - 13

card(32, 43, 379, 116, fill=TEAL_PALE)
txt(46, 137, 'ZMK STUDIO', 10.5, TEAL, True)
para(46, 127, 350,
     'Connect to the USB-C dongle through <b>zmk.studio</b> and press <b>Save</b> after editing. '
     'Ordinary Backspace is <b>Key Press → Keyboard Delete</b>. '
     '<b>Keypad Backspace</b> is a different code; <b>Keyboard Delete Forward</b> deletes to the right.',
     8.3, 11.3)
para(46, 70, 350,
     'Verified Studio edits are in the source keymap. Later Studio edits take precedence.',
     7.7, 10.2, MUTED)

card(427, 333, 383, 200)
txt(441, 511, 'GAME', 10.5, BLUE, True)
txt(496, 511, 'NAV+C activates • second left right-thumb key returns to BASE', 7.6, MUTED)
game_left = [['Tab','Q','W','E','R'],['Shift','A','S','D','F'],['Ctrl','Z','X','C','V']]
game_right = [['·','·','↑','·','Tab'],['·','←','↓','→','Shift'],['·','·','·','·','Ctrl']]
for r in range(3):
    yy = 459 - r * 39
    for i in range(5):
        key(441 + i * 36, yy, 32, 32, game_left[r][i],
            ['Q','W','E','R','T'][i] if r == 0 else (['A','S','D','F','G'][i] if r == 1 else ['Z','X','C','V','B'][i]),
            value_size=7.3)
        key(633 + i * 33, yy, 29, 32, game_right[r][i],
            ['Y','U','I','O','P'][i] if r == 0 else (['H','J','K','L',';'][i] if r == 1 else ['N','M',',','.','/'][i]),
            value_size=7.1, fill=PAPER if game_right[r][i] == '·' else PALE)
txt(441, 346, 'Thumbs: Option / Space / GFN     |     BASE / Space / Print Screen', 8.0, TEAL, True)

card(427, 43, 383, 275)
txt(441, 296, 'OTHER LAYERS', 10.5, BLUE, True)
txt(441, 270, 'GFN', 9.5, TEAL, True)
para(441, 265, 353,
     'On GAME, hold the NAV position. The first two left thumb keys send Esc and Enter. '
     'GFN also has Reset and Bootloader; check their positions in firmware before use.',
     8.5, 11.7)
txt(441, 204, 'ALT', 9.5, TEAL, True)
para(441, 199, 353,
     'Hold the rightmost left thumb key or the second rightmost right thumb key: '
     '<b>ALT+T = ё, ALT+I = щ, ALT+M = ъ</b>. ALT+L = « and ALT+; = ». '
     'These are Universal characters; Space sends a nonbreaking space.',
     8.5, 11.7)
txt(441, 138, 'CMD', 9.5, TEAL, True)
para(441, 133, 353,
     'Hold NAV and the Caps-position thumb key. U / I / O: volume down / '
     'mute / up. J / K / L: previous track / play-pause / next track. '
     'The extra key left of Q unlocks Studio. '
     'The second left right-thumb key sends left Command.',
     8.5, 11.7)

c.showPage()
c.save()
print(OUT)
