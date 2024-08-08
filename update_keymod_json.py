import json
import sys

from keyboards_info import keyboards_info


def update_layer_with_row(layer, standard_layer, keyboard):
    """
    Update the given layer with the standard key settings.
    """
    row_indices = keyboards_info.get(keyboard).get('row_indices')
    for row, indices in row_indices.items():
        for i, key_setting in zip(indices, standard_layer[row]):
            layer[i] = key_setting
    return layer


def update_keymod_json(keyboard, initial_key_setting='KC_TRNS'):
    """
    Update the keymod JSON configuration for the given keyboard.
    """
    # Read keyboard information
    keyboard_info = keyboards_info[keyboard]
    keymod_json_path = keyboard_info['keymod_json_path']
    layer_indices = keyboard_info['layer_indices']

    # Read the current keymod JSON file
    with open(keymod_json_path) as json_file:
        keymod_dict = json.load(json_file)

    # Introduce local variable layers to avoid multiple accesses to `keymod_dict['layers']`
    layers = keymod_dict['layers']

    # Read the standard keymod JSON file
    with open('standard_keymod.json') as json_file:
        standard_keymod = json.load(json_file)

    standard_layer_names = ['base_layer', 'alt_layer1', 'alt_layer2']
    standard_layers = [v for (k, v) in standard_keymod.items() if k in standard_layer_names]

    # Update layers with the standard settings
    for layer_index, standard_layer, name in zip(layer_indices, standard_layers, standard_layer_names):
        layer = layers[layer_index]
        # Initialize key settings for non-base layers
        if name != 'base_layer':
            layer = [initial_key_setting] * len(layer)
        layers[layer_index] = update_layer_with_row(layer, standard_layer, keyboard)

    # Update macros
    default = [''] * 16
    keymod_dict['macros'] = standard_keymod.get('macros', default)

    # Save the updated keymod configuration back to the JSON file
    with open(keymod_json_path, 'w') as outfile:
        json.dump(keymod_dict, outfile)

    return keymod_dict


if __name__ == '__main__':
    update_keymod_json(*sys.argv[1:])
