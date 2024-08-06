"""
该文件中的字典 `keyboards_info` 保存了各键盘VIA改键存档文件的路径、层索引和按键行分区索引。

其中各按键行分区对应的经典键位如下：

| 分区名 | 经典键位 | 按键数 |
| --- | --- | --- |
| r4 | 234...9 | 8 |
| r3 | {TAB}QWER...P | 11 |
| r2 | {CAPS}ASDF...{QUOT} | 12 |
| r1_2 | ZXCV...{SLSH}{RSFT} | 11 |
| r1_1 | {LCTL}{LGUI}{LALT}{SPC}{SPC}{RALT}{APP}{RCTL} | 8 |
"""

import itertools

keyboards_info = {
    'Neo Ergo': {
        'keymod_json_path': 'neoergo_keymod.json',
        'layer_indices': [0, 1, 2],
        'row_indices': {
            'r4': itertools.chain(range(2, 7), range(8, 11)),
            'r3': range(16, 27),
            'r2': range(31, 43),
            'r1_2': itertools.chain(range(47, 52), range(53, 59)),
            'r1_1': [61, 62, 63, 66, 67, 70, 72, 74],
        },
    },
    'NuPhy Air 75 V2': {
        'keymod_json_path': 'nuphyair75v2_keymod.json',
        'layer_indices': [2, 5, 6],
        'row_indices': {
            'r4': range(19, 27),
            'r3': range(34, 45),
            'r2': range(51, 63),
            'r1_2': itertools.chain(range(70, 80), [81]),
            'r1_1': [85, 86, 87, 91, 91, 94, 95, 65],
        },
    },
}
