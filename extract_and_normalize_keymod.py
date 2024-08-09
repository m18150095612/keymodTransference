import json
import sys

from keyboards_info import keyboards_info


class KeymodProcessor:
    def __init__(self, keyboard):
        """
        初始化 KeymodProcessor 类的实例。

        参数:
        - keyboard (str): 键盘的名称，用于获取键盘配置信息。

        功能:
        - 导入并加载与指定键盘相关的配置文件（JSON 文件）。
        - 设置相关的层索引、行分区索引，并初始化用于存储标准化按键设置的字典。
        """
        # 获取指定键盘的配置信息
        keyboard_info = keyboards_info[keyboard]

        # 获取键盘按键设置的 JSON 文件路径
        keymod_json_path = keyboard_info['keymod_json_path']

        # 读取并加载 JSON 文件内容到 keymod_dict 字典
        with open(keymod_json_path) as json_file:
            self.keymod_dict = json.load(json_file)

        # 初始化层索引和行分区索引
        self.layer_indices = keyboard_info['layer_indices']
        self.row_indices = keyboard_info['row_indices']

        # 定义标准层名称
        self.standard_layer_names = ['base_layer', 'alt_layer1', 'alt_layer2']

        # 初始化存储标准化按键设置的字典
        self.standard_keymod_dict = {}

    def extract_and_normalize_keymod(self):
        """
        提取并标准化特定键盘的按键设置。

        功能:
        1. 从指定的 JSON 文件中加载键盘设置。
        2. 提取指定层和分区的按键设置，并标准化层索引。
        3. 提取宏设置。
        4. 将标准化后的键盘设置保存到新的 JSON 文件中。

        返回:
        - dict: 标准化后的键盘设置，包括层按键设置和宏设置。
        """
        # 依次处理每个指定的层
        for (layer_index, standard_layer_name) in zip(self.layer_indices, self.standard_layer_names):
            # 提取每一层的按键设置
            self.extract_layer_key_settings(layer_index, standard_layer_name)

        # 标准化层索引，将按键设置中的层索引统一为1和2
        self.normalize_layer_indices()

        # 提取宏设置，如果没有宏设置，则使用默认值
        default = [''] * 16
        self.standard_keymod_dict['macros'] = self.keymod_dict.get('macros', default)

        # 将标准化后的键盘设置保存到标准化 JSON 文件中
        with open('standard_keymod.json', 'w') as output_file:
            json.dump(self.standard_keymod_dict, output_file, indent=4)

        # 返回标准化后的键盘设置
        return self.standard_keymod_dict

    def extract_layer_key_settings(self, layer_index, standard_layer_name):
        """
        提取特定层的按键设置并将其映射到标准层中。

        参数:
        - layer_index (int): 要提取的层的索引。
        - standard_layer_name (str): 对应标准层的名称。

        返回:
        - dict: 标准层的按键设置。

        功能:
        - 将指定层（layer_index）中各行的按键设置提取到相应名称的标准层（standard_layer_name）中。
        - 行分区索引（row_indices）是一个键值对的集合，键是键盘按键行分区的名称，值是相应分区的按键索引列表。
        """
        # 获取指定层的按键设置
        layer = self.keymod_dict['layers'][layer_index]

        # 根据行分区索引提取该层的按键设置，并映射到标准层中
        standard_layer = {row: [layer[i] for i in indices]
                          for (row, indices) in self.row_indices.items()}

        # 将提取的标准层设置保存到标准化字典中
        self.standard_keymod_dict[standard_layer_name] = standard_layer

        # 返回标准层的按键设置
        return standard_layer

    def normalize_layer_indices(self):
        """
        将按键设置中的层索引标准化为1和2，以便统一处理不同的层。

        功能:
        - 查找并替换按键设置中引用的层索引，将它们统一为标准化的索引1和2。
        - 该方法修改后的按键设置将保存回 standard_keymod_dict 字典中。

        返回:
        - dict: 标准化后的键盘设置字典。
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

        # 返回标准化后的字典
        return self.standard_keymod_dict


if __name__ == '__main__':
    """
    入口点，当模块作为脚本执行时运行。

    功能:
    - 使用命令行参数中提供的键盘名称实例化 KeymodProcessor。
    - 调用 extract_and_normalize_keymod 方法提取和标准化按键设置。
    """
    processor = KeymodProcessor(sys.argv[1])
    processor.extract_and_normalize_keymod()
