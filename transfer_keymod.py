import itertools
import json


with open('nuphyair75v2_keymod.json') as json_file:
    air75 = json.load(json_file)

# 录入Nuphy Air 75 V2`keymod_json`文件对应标准分区的键位索引
air75_row_indices = {
    "r4": range(17, 27),    # {GRV}1234...9，共10个
    "r3": range(34, 45),    # {TAB}QWER...P，共11个键
    "r2": range(51, 63),    # {CAPS}ASDF...{QUOT}，共12个键
    "r1_2": range(70, 80),  # ZXCV...{SLSH}，共10个键
    # {LCTL}{LGUI}{LALT}{SPC}{SPC}{RALT}{APP}{RCTL}，共8个键
    "r1_1": [85, 86, 87, 91, 91, 94, 95, 65],
}

# 初始化标准的基础层
standard_baselayer = {}

# 获取Nuphy Air 75 V2的基础层
air75_baselayer = air75['layers'][2]

for row, indices in air75_row_indices.items():
    standard_baselayer[row] = [air75_baselayer[i] for i in indices]

# 保存标准的基础层为JSON文件
with open('standard_baselayer.json', 'w') as outfile:
    json.dump(standard_baselayer, outfile, indent=4)
