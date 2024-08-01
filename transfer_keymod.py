import itertools
import json


def get_standard_layer(layer_index, row_indices, keymod_json):
    input_layer = keymod_json['layers'][layer_index]
    standard_layer = {}
    for row, indices in row_indices.items():
        standard_layer[row] = [input_layer[i] for i in indices]
    return standard_layer


def get_standard_layers(layer_indices, row_indices, keymod_json):
    layer_names = ['baselayer', 'altlayer1', 'altlayer2']
    standard_layers = {
        name: get_standard_layer(layer_index, row_indices, keymod_json)
        for (name, layer_index) in zip(layer_names, layer_indices)
    }
    return standard_layers


def replace_layer_indices(layer_indices, standard_layers):
    standard_layers_str = json.dumps(standard_layers)
    replaced = standard_layers_str.replace(
        f'LT({layer_indices[1]}', 'LT(1'
    ).replace(
        f'LT({layer_indices[2]}', 'LT(2'
    )
    return json.loads(replaced)


if __name__ == '__main__':
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
    air75_layer_indices = [2, 5, 6]

    standard_layers = get_standard_layers(
        layer_indices=air75_layer_indices,
        row_indices=air75_row_indices,
        keymod_json=air75
    )
    standard_layers = replace_layer_indices(
        standard_layers=standard_layers,
        layer_indices=air75_layer_indices
    )
    # 保存标准化的改键结果
    with open('standard_layers.json', 'w') as outfile:
        json.dump(standard_layers, outfile, indent=4)
