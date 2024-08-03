import itertools


row_indices_dict = {
    'Neo Ergo': {
        'r4': itertools.chain(range(2, 7), range(8, 11)),  # 234...9，共8个键
        'r3': range(16, 27),  # {TAB}QWER...P，共11个键
        'r2': range(31, 43),  # {CAPS}ASDF...{QUOT}，共12个键
        'r1_2': itertools.chain(range(47, 52), range(53, 59)),  # ZXCV...{SLSH}{RSFT}，共11个键
        # {LCTL}{LGUI}{LALT}{SPC}{SPC}{RALT}{APP}{RCTL}，共8个键
        'r1_1': [61, 62, 63, 66, 67, 70, 72, 74],
    }
}
