"""
该文件中的字典 `keyboards_info` 保存了各键盘VIA改键存档文件的路径、层索引和按键行分区索引。

其中各按键行分区对应的经典键位如下：

| 分区名 | 经典键位 | 按键数 |
| --- | --- | --- |
| r4 | 234...9 | 8 |
| r3 | {TAB}QWER...P | 11 |
| r2 | {CAPS}ASDF...{QUOT} | 12 |
| r1_2 | ZXCV...{SLSH}{RSFT} | 11 |
| r1_1 | {LCTL}{LGUI}{LALT}{SPC}{RALT}{APP} | 6 |
"""
keyboards_info = {
    'Neo Ergo': {
        'keymod_json_path': 'neoergo_keymod.json',
        'layer_indices': range(3),
        'row_indices': {
            'r4': list(range(2, 7)) + list(range(8, 11)),
            'r3': list(range(16, 27)),
            'r2': list(range(31, 43)),
            'r1_2': list(range(47, 52)) + list(range(53, 59)),
            'r1_1': list(range(61, 64)) + [66, 70, 72],
        },
    },
    'NuPhy Air 75 V2': {
        'keymod_json_path': 'nuphyair75v2_keymod.json',
        'layer_indices': [2, 5, 6],
        'row_indices': {
            'r4': list(range(19, 27)),
            'r3': list(range(34, 45)),
            'r2': list(range(51, 63)),
            'r1_2': list(range(70, 80)) + [81],
            'r1_1': list(range(85, 88)) + [91, 94, 95],
        },
    },
    'Keychron Q3': {
        'keymod_json_path': 'keychronq3_keymod.json',
        'layer_indices': range(3),
        'row_indices': {
            'r4': list(range(18, 26)),
            'r3': list(range(32, 43)),
            'r2': list(range(48, 60)),
            'r1_2': list(range(66, 76)) + [77],
            'r1_1': list(range(80, 83)) + [86, 90, 91],
        },
    },
}
