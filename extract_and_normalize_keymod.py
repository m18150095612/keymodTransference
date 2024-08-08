import json
import sys

from keyboards_info import keyboards_info


def extract_layer_key_settings(layer_index, keyboard):
    keyboard_info = keyboards_info[keyboard]
    keymod_json_path = keyboard_info['keymod_json_path']
    row_indices = keyboard_info['row_indices']

    with open(keymod_json_path) as json_file:
        keymod_dict = json.load(json_file)
    layer = keymod_dict['layers'][layer_index]

    standard_layer = {row: [layer[i] for i in indices]
                      for (row, indices) in row_indices.items()}
    return standard_layer


def normalize_layer_indices(standard_keymod_dict, input_layer_indices):
    standard_keymod_str = json.dumps(standard_keymod_dict)
    normalized = standard_keymod_str.replace(
        f'LT({input_layer_indices[1]}', 'LT(1'
    ).replace(
        f'LT({input_layer_indices[2]}', 'LT(2'
    )
    return json.loads(normalized)


def extract_macros(keyboard):
    keymod_json_path = keyboards_info[keyboard]['keymod_json_path']
    with open(keymod_json_path) as json_file:
        keymod_dict = json.load(json_file)
    return keymod_dict['macros']


def extract_and_normalize_keymod(keyboard):
    """
    提取特定键盘via改键存档（json文件）中的指定层指定分区的按键设置，标准化层索引，并提取宏设置。

    参数:
        keyboard (str): 指定所提取文件对应的键盘名。

    返回:
        dict: 标准化的键盘设置，包括层按键设置和宏设置。

    功能:
        1. 从指定的json文件中加载键盘设置。
        2. 提取指定层和分区的按键设置，并标准化层索引。
        3. 提取宏设置。
        4. 将标准化后的键盘设置保存到新的json文件中。
    """
    # 使用`input_`前缀的变量名，以和函数`normalize_layer_indices`的参数名统一
    input_layer_indices = keyboards_info[keyboard]['layer_indices']

    standard_layer_names = ['base_layer', 'alt_layer1', 'alt_layer2']
    standard_keymod_dict = {
        name: extract_layer_key_settings(layer_index, keyboard)
        for (name, layer_index) in zip(standard_layer_names, input_layer_indices)
    }
    standard_keymod_dict = normalize_layer_indices(standard_keymod_dict,
                                                   input_layer_indices)
    standard_keymod_dict['macros'] = extract_macros(keyboard)

    with open('standard_keymod.json', 'w') as output_file:
        json.dump(standard_keymod_dict, output_file, indent=4)
    return standard_keymod_dict


if __name__ == '__main__':
    extract_and_normalize_keymod(sys.argv[1])
