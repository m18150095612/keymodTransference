import json

from row_indices_dict import row_indices_dict


def update_layer_with_row(layer, standard_layer, row_indices):
    for row, indices in row_indices.items():
        for i, key_setting in zip(indices, standard_layer[row]):
            layer[i] = key_setting
    return layer


def update_keymod_dict(keymod_dict, row_indices, standard_layers,
                       initial_key_setting='KC_TRNS'):
    # 引入局部变量layers，减少了多次书写`keymod_dict['layers']`
    layers = keymod_dict['layers']
    for layer_index, standard_layer in enumerate(standard_layers.values()):
        layer = layers[layer_index]
        if layer_index != 0:
            layer = [initial_key_setting] * len(layer)
        layers[layer_index] = update_layer_with_row(
            layer, standard_layer, row_indices)
    return keymod_dict


def update_keymod_json(keymod_json_path, keyboard):
    # 读取保存按键设置的JSON文件
    with open(keymod_json_path) as json_file:
        keymod_dict = json.load(json_file)

    row_indices = row_indices_dict.get(keyboard)

    with open('standard_layers.json') as json_file:
        standard_layers = json.load(json_file)

    keymod_dict = update_keymod_dict(
        keymod_dict, row_indices, standard_layers)

    # 保存
    with open(keymod_json_path, 'w') as outfile:
        json.dump(keymod_dict, outfile)


if __name__ == '__main__':
    update_keymod_json('neoergo_keymod.json', 'Neo Ergo')
