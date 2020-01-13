"""
generate ObjectiveC code for:
  getKeyDataForOya(keycode, gOya)
"""
from string import ascii_lowercase, ascii_uppercase

"""
static NSString* keymap[0x80] = {
    @"a", @"s", @"d", @"f", @"h", @"g", @"z", @"x",
    @"c", @"v", @"[Section]", @"b", @"q", @"w", @"e", @"r",
    @"y", @"t", @"1", @"2", @"3", @"4", @"6", @"5",
    @"^"/* = */, @"9", @"7", @"-", @"8", @"0", @"["/* ] */, @"o",
    @"u", @"@"/* [ */, @"i", @"p", @"↩", @"l", @"j", @":"/* ' */,
    @"k", @";", @"]"/* \ */, @",", @"/", @"n", @"m", @".",
    @"⇥", @"␣", @"`", @"⌫", @"⌤"/* no def */, @"⎋", @"[R⌘]", @"⌘",
    @"⇧", @"⇪", @"⌥", @"⌃", @"[R⇧]", @"[R⌥]", @"[R⌃]", @"[fn]",
    @"[F17]", @"[K.]", @"<42>", @"[K*]", @"<44>", @"[K+]", @"<46>", @"⌧"/* Keypad */,
    @"[VolumeUp]", @"[VolumeDown]", @"[Mute]", @"[K/]", @"[K⌤]", @"<4d>", @"[K-]", @"[F18]",
    @"[F19]", @"[K=]", @"[K0]", @"[K1]", @"[K2]", @"[K3]", @"[K4]", @"[K5]",
    @"[K6]", @"[K7]", @"[F20]", @"[K8]", @"[K9]", @"¥", @"_", @"[K,]",
    @"[F5]", @"[F6]", @"[F7]", @"[F3]", @"[F8]", @"[F9]", @"[Eisu]", @"[F11]",
    @"[Kana]", @"[F13]", @"[F16]", @"[F14]", @"<6c>", @"[F10]", @"<6e>", @"[F12]",
    @"<70>", @"[F15]", @"[Help]", @"↖", @"⇞", @"⌦", @"[F4]", @"↘",
    @"[F2]", @"⇟", @"[F1]", @"←", @"→", @"↓", @"↑", @"<7f>",
};
"""

KEYMAP = [
    "a", "s", "d", "f", "h", "g", "z", "x",
    "c", "v", "[Section]", "b", "q", "w", "e", "r",
    "y", "t", "1", "2", "3", "4", "6", "5",
    "^", "9", "7", "-", "8", "0", "[", "o",
    "u", "@", "i", "p", "↩", "l", "j", ":",
    "k", ";", "]", ",", "/", "n", "m", ".",
    "⇥", "␣", "`", "⌫", "⌤", "⎋", "[R⌘]", "⌘",
    "⇧", "⇪", "⌥", "⌃", "[R⇧]", "[R⌥]", "[R⌃]", "[fn]",
    "[F17]", "[K.]", "<42>", "[K*]", "<44>", "[K+]", "<46>", "⌧",
    "[VolumeUp]", "[VolumeDown]", "[Mute]", "[K/]", "[K⌤]", "<4d>", "[K-]", "[F18]",
    "[F19]", "[K=]", "[K0]", "[K1]", "[K2]", "[K3]", "[K4]", "[K5]",
    "[K6]", "[K7]", "[F20]", "[K8]", "[K9]", "¥", "_", "[K,]",
    "[F5]", "[F6]", "[F7]", "[F3]", "[F8]", "[F9]", "[Eisu]", "[F11]",
    "[Kana]", "[F13]", "[F16]", "[F14]", "<6c>", "[F10]", "<6e>", "[F12]",
    "<70>", "[F15]", "[Help]", "↖", "⇞", "⌦", "[F4]", "↘",
    "[F2]", "⇟", "[F1]", "←", "→", "↓", "↑", "<7f>",
]
KEYCODE_SHIFT = KEYMAP.index("⇧")
assert KEYCODE_SHIFT == 0x38

"""
static CGKeyCode viewTable[] = {
    6, 7, 8, 9, 11, 45, 46, 43, 47, 44, LAYOUT_KEY_COUNT - 1,   // 94
    0, 1, 2, 3, 5, 4, 38, 40, 37, 41, 39, 42,
    12, 13, 14, 15, 17, 16, 32, 34, 31, 35, 33, 30,
    18, 19, 20, 21, 23, 22, 26, 28, 25, 29, 27, 24, LAYOUT_KEY_COUNT - 2   // 93
};
"""
kVK_JIS_Yen = 93
kVK_JIS_Underscore = 94
JIS_KEY_LAYOUT = [
    [18, 19, 20, 21, 23, 22, 26, 28, 25, 29, 27, 24, kVK_JIS_Yen],
    [12, 13, 14, 15, 17, 16, 32, 34, 31, 35, 33, 30],
    [0, 1, 2, 3, 5, 4, 38, 40, 37, 41, 39, 42],
    [6, 7, 8, 9, 11, 45, 46, 43, 47, 44, kVK_JIS_Underscore],
]
FLAT_JIS_KEY_LAYOUT = sum(JIS_KEY_LAYOUT, [])
# MEMO: in Lacaille's ObjC code,
# `LAYOUT_KEY_COUNT = 50`,
# so `LAYOUT_KEY_COUNT - 1` is not 94, it is 49.
# Those differences is absorbed in *getKeyDataForOya
# ```
# (keycode < LAYOUT_KEY_COUNT - 2) ? [(ViewDataModel *)prefLayout[keycode] getKeyData:oya] :
# (keycode == kVK_JIS_Yen) ? [(ViewDataModel * )prefLayout[(LAYOUT_KEY_COUNT - 2)] getKeyData:oya] :
# (keycode == kVK_JIS_Underscore) ? [(ViewDataModel * )prefLayout[(LAYOUT_KEY_COUNT - 1)] getKeyData:oya] :
# [[NSData alloc] initWithBytes:(unsigned char[]){keycode} length: 1]);
# ```


def test_JIS_KEY_LAYOUT():
    """
    >>> test_JIS_KEY_LAYOUT()
    1234567890-^¥
    qwertyuiop@[
    asdfghjkl;:]
    zxcvbnm,./_
    """
    for row in JIS_KEY_LAYOUT:
        print("".join(KEYMAP[x] for x in row))


SHIFTED_KEYS, BASE_KEYS = (
    "!#$%&'()=~`{}*+?<>|" + "\"" + ascii_uppercase,
    "13456789-^@[]:;/<>¥" + "2" + ascii_lowercase
)
SHIFT_MAP = dict(zip(BASE_KEYS, SHIFTED_KEYS))
REVERSE_SHIFT_MAP = dict(zip(SHIFTED_KEYS, BASE_KEYS))


def test_REVERSE_SHIFT_MAP(x):
    """
    >>> test_REVERSE_SHIFT_MAP("!")
    '1'
    """
    return REVERSE_SHIFT_MAP[x]


def strToKeyData(s):
    """
    >>> strToKeyData("u").hex()
    '20ffff'
    >>> strToKeyData("wo").hex()
    '0d1fff'
    >>> strToKeyData("[").hex()
    '1effff'
    >>> strToKeyData("{").hex()
    '381eff'
    """
    buf = bytearray([0xFF, 0xFF, 0xFF])
    i = 0
    for c in s:
        if c in REVERSE_SHIFT_MAP:
            c = REVERSE_SHIFT_MAP[c]
            buf[i] = KEYCODE_SHIFT
            buf[i + 1] = KEYMAP.index(c)
            i += 2
        else:
            buf[i] = KEYMAP.index(c)
            i += 1
    return buf


# Sample
original_keymap = [
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '^', '¥',
    'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '@', '[',
    'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', ':', ']',
    'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', '_']
assert len(original_keymap) == 48
assert FLAT_JIS_KEY_LAYOUT == [KEYMAP.index(c) for c in original_keymap]
shifted_keymap = [SHIFT_MAP.get(c, c) for c in original_keymap]
assert (shifted_keymap == [
    '!', '"', '#', '$', '%', '&', "'", '(', ')', '0', '=', '~', '|',
    'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '`', '{',
    'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', '+', '*', '}',
    'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '?', '_'])

# My keymap definition
keymap_for_BASE = [
    '1', '2', '3', '4', '5', '', '6', '7', '8', '9', '0', '-', '^',
    'q', 'w', 'e', 'r', 't', '!', 'y', 'u', 'i', 'o', 'p', '@',
    'a', 's', 'd', 'f', 'g', '-', 'h', 'j', 'k', 'l', ';', ':',
    'z', 'x', 'c', 'v', 'b', '@', 'n', 'm', ',', '.', '/']
keymap_for_LSHIFT = [
    '', '', '', '', '', '', '', '', '', '', '', '', '',
    '1', '2', '3', '4', '5', '|', '6', '7', '8', '9', '0', '',
    '¥', '/', '=', '{', '}', '', '(', ')', '␣', '"', '', '',
    '?', '+', '-', '[', ']', '^', '*', '_', '', '', '#']
keymap_for_RSHIFT = [
    '!', '"', '#', '$', '%', '', '&', "'", '(', ')', '0', '=', '~',
    'Q', 'W', 'E', 'R', 'T', '&', 'Y', 'U', 'I', 'O', 'P', '`',
    'A', 'S', 'D', 'F', 'G', '_', 'H', 'J', 'K', 'L', '+', '*',
    'Z', 'X', 'C', 'V', 'B', '$', 'N', 'M', ',', '.', '?']

assert (sorted(FLAT_JIS_KEY_LAYOUT) ==
        [0,  1,  2,  3,  4,  5,  6,  7,  8,  9,
         11, 12, 13, 14, 15, 16, 17, 18, 19,
         20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
         30, 31, 32, 33, 34, 35,     37, 38, 39,
         40, 41, 42, 43, 44, 45, 46, 47, 93, 94])

LAYOUT_KEY_COUNT = 50

output = ["0xFF, 0xFF, 0xFF"] * LAYOUT_KEY_COUNT


def generate_objc(keymap):
    if "\\" in keymap:
        raise RuntimeError("use `¥` instead of `\\`")
    if " " in keymap:
        raise RuntimeError("use `␣` instead of ` `")

    for keycode in sorted(FLAT_JIS_KEY_LAYOUT):
        position = original_keymap.index(KEYMAP[keycode])
        newkey = keymap[position]
        newkey = strToKeyData(newkey)
        newkey = ", ".join(f"0x{x:02X}" for x in newkey)
        if keycode == kVK_JIS_Yen:
            index = LAYOUT_KEY_COUNT - 2
        elif keycode == kVK_JIS_Underscore:
            index = LAYOUT_KEY_COUNT - 1
        else:
            index = keycode

        output[index] = newkey

    print(", ".join(output))


generate_objc(keymap_for_LSHIFT)

generate_objc(keymap_for_RSHIFT)


def test():
    import doctest
    doctest.testmod()


if __name__ == "__main__":
    test()
