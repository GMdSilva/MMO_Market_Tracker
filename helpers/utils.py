import json
from typing import Union, Tuple
import os


def spell_out_string(to_be_spelled: Union[str, Tuple[str, ...]]) -> Tuple[str, ...]:
    """ Gets a string or tuple of strings and converts it to a dict containing
    each string name as a key and each spelled out string as a value,
    e.g. {'item': ('i', 't', 'e', 'm')

    Args:
        to_be_spelled: string(s) we want to save and spell out
    Returns:
        item_dict: dict containing each string as a key and their spelled out
            lists as a value

    """

    string = to_be_spelled.strip()
    letters = []
    for letter in string:
        letters.append(letter)
    return tuple(letters)


def create_output_folder(folder_name):
    """
    Create a folder named with the current date to store results.
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Folder '{folder_name}' created.")
    else:
        print(f"Folder '{folder_name}' already exists.")


def read_coin_price(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data['average_coin_price']


def write_coin_price(average_coin_price, file_path):
    with open(file_path, 'w') as file:
        json.dump({"average_coin_price": average_coin_price}, file)
