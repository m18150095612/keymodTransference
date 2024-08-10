import json
import sys

from keyboards_info import keyboards_info


class KeymodProcessor:
    def __init__(self, keyboard):
        """
        初始化 KeymodProcessor 类的实例。

        参数:
        - keyboard (str): 键盘的名称，用于获取键盘配置信息。
        """
        self.keyboard = keyboard
        self.keyboard_info = keyboards_info[keyboard]
        self.keymod_json_path = self.keyboard_info['keymod_json_path']
        self.layer_indices = self.keyboard_info['layer_indices']
        self.row_indices = self.keyboard_info['row_indices']
        # 将所有行分区的按键索引拼接成一个列表
        self.key_indices = sum(self.row_indices.values(), [])

        # 读取当前键盘的 keymod JSON 文件
        with open(self.keymod_json_path) as json_file:
            self.keymod_dict = json.load(json_file)

        # 读取标准 keymod JSON 文件
        with open('standard_keymod.json') as json_file:
            self.standard_keymod_dict = json.load(json_file)

        self.standard_layer_names = ['base_layer', 'alt_layer1', 'alt_layer2']


class KeymodUpdateProcessor(KeymodProcessor):
    def __init__(self, keyboard, initial_key_setting='KC_TRNS'):
        """
        初始化 KeymodUpdateProcessor 类，设置初始按键配置。
        """
        super().__init__(keyboard)
        self.initial_key_setting = initial_key_setting

    def update_layer(self, standard_layer_name):
        """
        更新指定层中的按键设定。
        """
        # 将标准 keymod 中的指定层所有行分区的按键设定拼接成一个列表
        key_settings = sum(self.standard_keymod_dict[standard_layer_name].values(), [])
        layer_index = self.layer_indices[
            self.standard_layer_names.index(standard_layer_name)]
        if standard_layer_name != 'base_layer':
            self.keymod_dict['layers'][layer_index] = [self.initial_key_setting] * len(
                self.keymod_dict['layers'][layer_index])
        for key_index, key_setting in zip(self.key_indices, key_settings):
            self.keymod_dict['layers'][layer_index][key_index] = key_setting

    def update_layers(self):
        """
        使用标准按键设定更新键盘。
        """
        for standard_layer_name in self.standard_layer_names:
            self.update_layer(standard_layer_name)

    def replace_layer_indices(self):
        """
        替换键盘映射中的层索引。
        """
        keymod_str = json.dumps(self.keymod_dict)
        replaced = keymod_str.replace(
            'LT(1', f'LT({self.layer_indices[1]}'
        ).replace(
            'LT(2', f'LT({self.layer_indices[2]}'
        )
        self.keymod_dict = json.loads(replaced)

    def update_macros(self):
        """
        更新宏设置。
        """
        default = [''] * 16
        self.keymod_dict['macros'] = self.standard_keymod_dict.get('macros', default)

    def save_keymod_json(self):
        """
        将更新后的 keymod 配置保存回 JSON 文件。
        """
        with open(self.keymod_json_path, 'w') as outfile:
            json.dump(self.keymod_dict, outfile, indent=2)

    def process(self):
        """
        执行更新流程，包括层配置和宏配置的更新，并保存到文件。
        """
        self.update_layers()
        self.replace_layer_indices()
        self.update_macros()
        self.save_keymod_json()


if __name__ == '__main__':
    processor = KeymodUpdateProcessor(*sys.argv[1:])
    processor.process()
