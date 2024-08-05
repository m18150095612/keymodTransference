import json

from row_indices_dict import row_indices_dict


def update_layer_with_row(layer, standard_layer, keyboard):
    row_indices = row_indices_dict.get(keyboard)
    for row, indices in row_indices.items():
        for i, key_setting in zip(indices, standard_layer[row]):
            layer[i] = key_setting
    return layer


def update_keymod_dict(keymod_dict, keyboard, standard_keymod,
                       initial_key_setting='KC_TRNS'):
    # 更新按键设置

    # 引入局部变量layers，避免多次书写`keymod_dict['layers']`
    layers = keymod_dict['layers']
    standard_layer_names = ['base_layer', 'alt_layer1', 'alt_layer2']
    standard_layers = [v for (k, v) in standard_keymod.items()
                       if k in standard_layer_names]
    for layer_index, standard_layer in enumerate(standard_layers):
        layer = layers[layer_index]
        # 初始化基础层外的按键设置
        if layer_index != 0:
            layer = [initial_key_setting] * len(layer)
        layers[layer_index] = update_layer_with_row(
            layer, standard_layer, keyboard)

    # 更新宏设置
    default = [''] * 16
    keymod_dict['macros'] = standard_keymod.get('macros', default)
    return keymod_dict


def update_keymod_json(keymod_json_path, keyboard):
    # 读取保存按键设置的JSON文件
    with open(keymod_json_path) as json_file:
        keymod_dict = json.load(json_file)

    with open('standard_keymod.json') as json_file:
        standard_keymod = json.load(json_file)

    keymod_dict = update_keymod_dict(keymod_dict, keyboard, standard_keymod)

    # 保存
    with open(keymod_json_path, 'w') as outfile:
        json.dump(keymod_dict, outfile)


if __name__ == '__main__':
    update_keymod_json('neoergo_keymod.json', 'Neo Ergo')
