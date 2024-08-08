"""
该文件中的字典 `keyboards_info` 保存了各键盘VIA改键存档文件的路径、层索引和按键行分区索引。

其中各按键行分区对应的经典键位如下：

| 分区名 | 经典键位 | 按键数 |
| --- | --- | --- |
| r4 | 234...9 | 8 |
| r3 | {TAB}QWER...P | 11 |
| r2 | {CAPS}ASDF...{QUOT} | 12 |
| r1_2 | ZXCV...{SLSH}{RSFT} | 11 |
| r1_1 | {LCTL}{LGUI}{LALT}{SPC}{SPC}{RALT}{APP}{APP}{RCTL} | 9 |
"""
keyboards_info = {
    'Neo Ergo': {
        'keymod_json_path': 'neoergo_keymod.json',
        'layer_indices': range(3),
        'row_indices': {
            'r4': list(range(2, 7)) + list(range(8, 11)),
            'r3': range(16, 27),
            'r2': range(31, 43),
            'r1_2': list(range(47, 52)) + list(range(53, 59)),
            'r1_1': list(range(61, 64)) + [66, 67, 70] + [72] * 2 + [74],
        },
    },
    'NuPhy Air 75 V2': {
        'keymod_json_path': 'nuphyair75v2_keymod.json',
        'layer_indices': [2, 5, 6],
        'row_indices': {
            'r4': range(19, 27),
            'r3': range(34, 45),
            'r2': range(51, 63),
            'r1_2': list(range(70, 80)) + [81],
            'r1_1': list(range(85, 88)) + [91] * 2 + [94] + [95] * 2 + [65],
        },
    },
    'Keychron Q3': {
        'keymod_json_path': 'keychronq3_keymod.json',
        'layer_indices': range(3),
        'row_indices': {
            'r4': range(18, 26),
            'r3': range(32, 43),
            'r2': range(48, 60),
            'r1_2': list(range(66, 76)) + [77],
            'r1_1': list(range(80, 83)) + [86] * 2 + list(range(90, 94)),
        },
    },
}
