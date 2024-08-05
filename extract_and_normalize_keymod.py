import json

from row_indices_dict import row_indices_dict


def extract_layer_key_settings(input_keymod_dict, layer_index, keyboard):
    input_layer = input_keymod_dict['layers'][layer_index]
    row_indices = row_indices_dict.get(keyboard)
    standard_layer = {}
    for row, indices in row_indices.items():
        standard_layer[row] = [input_layer[i] for i in indices]
    return standard_layer


def extract_macro(input_keymod_dict):
    extracted = input_keymod_dict['macro']
    return extracted


def normalize_layer_indices(standard_keymod_dict, input_layer_indices):
    standard_keymod_str = json.dumps(standard_keymod_dict)
    normalized = standard_keymod_str.replace(
        f'LT({input_layer_indices[1]}', 'LT(1'
    ).replace(
        f'LT({input_layer_indices[2]}', 'LT(2'
    )
    return json.loads(normalized)


def extract_and_normalize_keymod(input_path, input_layer_indices, keyboard):
    """
    提取特定键盘via改键存档（json文件）中的指定层指定分区的按键设置，标准化层索引，并提取宏设置。

    参数:
        input_path (str): 输入的json文件路径。
        input_layer_indices (list): 指定要提取的层索引列表。
        keyboard (str): 指定所提取文件对应的键盘名。

    返回:
        dict: 标准化的键盘设置，包括层按键设置和宏设置。

    功能:
        1. 从指定的json文件中加载键盘设置。
        2. 提取指定层和分区的按键设置，并标准化层索引。
        3. 提取宏设置。
        4. 将标准化后的键盘设置保存到新的json文件中。
    """
    with open(input_path) as json_file:
        input_keymod_dict = json.load(json_file)
    layer_names = ['baselayer', 'altlayer1', 'altlayer2']
    standard_keymod_dict = {
        name: extract_layer_key_settings(
            input_keymod_dict, layer_index, keyboard)
        for (name, layer_index) in zip(layer_names, input_layer_indices)
    }
    standard_keymod_dict = normalize_layer_indices(standard_keymod_dict,
                                                   input_layer_indices)
    standard_keymod_dict['macros'] = input_keymod_dict.get('macros')
    with open('standard_keymod.json', 'w') as output_file:
        json.dump(standard_keymod_dict, output_file, indent=4)
    return standard_keymod_dict


if __name__ == '__main__':
    extract_and_normalize_keymod(input_path='nuphyair75v2_keymod.json',
                                 input_layer_indices=[2, 5, 6],
                                 keyboard='NuPhy Air 75 V2')
