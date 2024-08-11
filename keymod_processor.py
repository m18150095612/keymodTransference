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
    def update_layer(self, standard_layer_name):
        """
        更新指定层中的按键设定。
        """
        # 将标准 keymod 中的指定层所有行分区的按键设定拼接成一个列表
        key_settings = sum(self.standard_keymod_dict[standard_layer_name].values(), [])
        layer_index = self.layer_indices[
            self.standard_layer_names.index(standard_layer_name)]
        if standard_layer_name != 'base_layer':
            self.keymod_dict['layers'][layer_index] = ['KC_TRNS'] * len(
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


class KeymodExtractProcessor(KeymodProcessor):
    def process(self):
        """
        提取并标准化特定键盘的按键设置。

        功能:
        1. 从指定的 JSON 文件中加载键盘设置。
        2. 提取指定层和分区的按键设置，并标准化层索引。
        3. 提取宏设置。
        4. 将标准化后的键盘设置保存到新的 JSON 文件中。
        """
        self.extract_layers()
        self.normalize_layer_indices()
        self.extract_macros()
        self.save_standard_keymod_json()

    def extract_layers(self):
        for standard_layer_name in self.standard_layer_names:
            self.extract_layer_key_settings(standard_layer_name)

    def extract_layer_key_settings(self, standard_layer_name):
        """
        功能:
        - 提取指定标准层的按键设定
        - 行分区索引（row_indices）是一个字典

          键是键盘按键行分区的名称，值是相应分区的按键索引列表。
        """
        # 获取指定层的按键设置
        layer_index = self.layer_indices[
            self.standard_layer_names.index(standard_layer_name)
        ]
        layer = self.keymod_dict['layers'][layer_index]

        # 根据行分区索引提取该层的按键设置，并映射到标准层中
        standard_layer = {row: [layer[i] for i in indices]
                          for (row, indices) in self.row_indices.items()}

        # 将提取的标准层设置保存到标准化字典中
        self.standard_keymod_dict[standard_layer_name] = standard_layer

    def normalize_layer_indices(self):
        """
        将按键设置中的层索引标准化为1和2，以便统一处理不同的层。

        功能:
        - 查找并替换按键设置中引用的层索引，将它们统一为标准化的索引1和2。
        - 该方法修改后的按键设置将保存回 standard_keymod_dict 字典中。
        """
        # 将标准化字典转换为字符串以便进行层索引的替换操作
        standard_keymod_str = json.dumps(self.standard_keymod_dict)

        # 替换层索引，将其标准化为1和2
        normalized = standard_keymod_str.replace(
            f'LT({self.layer_indices[1]}', 'LT(1'
        ).replace(
            f'LT({self.layer_indices[2]}', 'LT(2'
        )

        # 将标准化后的字符串转换回字典并更新
        self.standard_keymod_dict = json.loads(normalized)

    def extract_macros(self):
        """
        提取宏设置，如果没有宏设置，则使用默认值
        """
        default = [''] * 16
        self.standard_keymod_dict['macros'] = self.keymod_dict.get('macros', default)

    def save_standard_keymod_json(self):
        """
        将标准 keymod 保存为 JSON 文件
        """
        with open('standard_keymod.json', 'w') as output_file:
            json.dump(self.standard_keymod_dict, output_file, indent=2)


def main():
    mode = sys.argv[1]
    keyboard = sys.argv[2]
    if mode in ['ex', 'tr']:
        KeymodExtractProcessor(keyboard).process()
    if mode == 'up':
        KeymodUpdateProcessor(keyboard).process()
    if mode == 'tr':
        keyboard2 = sys.argv[3]
        KeymodUpdateProcessor(keyboard2).process()


if __name__ == '__main__':
    main()
