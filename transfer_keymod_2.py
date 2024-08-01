import json
import itertools


def load_standard_layers(row_indices, standard_layers, output_keymod_json):
    for layer_index, standard_layer in enumerate(standard_layers.values()):
        for row, indices in row_indices.items():
            for i, value in zip(indices, standard_layer[row]):
                output_keymod_json['layers'][layer_index][i] = value
    return output_keymod_json


if __name__ == '__main__':
    with open('standard_layers.json') as json_file:
        standard_layers = json.load(json_file)

    with open('neoergo_keymod.json') as json_file:
        neoergo = json.load(json_file)

    neoergo_row_indices = {
        "r4": itertools.chain(range(0, 7), range(8, 11)),    # {GRV}1234...9，共10个键
        "r3": range(16, 27),    # {TAB}QWER...P，共11个键
        "r2": range(31, 43),    # {CAPS}ASDF...{QUOT}，共12个键
        "r1_2": itertools.chain(range(47, 52), range(53, 58)),  # ZXCV...{SLSH}，共10个键
        # {LCTL}{LGUI}{LALT}{SPC}{SPC}{RALT}{APP}{RCTL}，共8个键
        "r1_1": [61, 62, 63, 66, 67, 70, 72, 74],
    }

    neoergo = load_standard_layers(
        row_indices=neoergo_row_indices, standard_layers=standard_layers, output_keymod_json=neoergo
    )

    # 保存
    with open('neoergo_keymod.json', 'w') as outfile:
        json.dump(neoergo, outfile)
