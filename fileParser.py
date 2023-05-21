"""
Кодирование и декодирование файлов с тестами.
По умолчанию файл с тестом является json-файлом,
но для защиты он должен быть закодирован в кастомный
формат .tdata, не позволяющий легко получить данные из файла.
Данный способ кодирования не сказать, что особенно безопасный, но
хомячки не выкупят, ну и для курсача самое то.
"""
import pathlib
import json


KEY = "VERS_WAS_HERE"


def encode_file(filepath: str, key=KEY, outpath=None):
    """Кодирует файл с ключём"""
    input_file = pathlib.Path(filepath)
    if not input_file.suffix == ".json":
        raise FileNotFoundError
    with open(input_file, 'r', encoding="utf-8") as file:
        text = file.read()
    encoded_text = ''
    key_index = 0
    key_length = len(key)
    for char in text:
        encoded_char = chr(ord(char) ^ ord(key[key_index]))
        encoded_text += encoded_char
        key_index = (key_index + 1) % key_length
    output_filepath = str(input_file.parent) + "/" + str(input_file.stem) + ".tdata"
    if outpath:
        output_filepath = outpath + "/" + str(input_file.stem) + ".tdata"
    with open(output_filepath, 'w', encoding="utf-8") as file:
        file.write(encoded_text)


def decode_file(filepath: str, key=KEY):
    """Декодирует файл .tdata с ключём"""
    input_file = pathlib.Path(filepath)
    if not input_file.suffix == ".tdata":
        raise FileNotFoundError
    with open(input_file, 'r', encoding="utf-8") as file:
        encoded_text = file.read()
    decoded_text = ''
    key_index = 0
    key_length = len(key)
    for char in encoded_text:
        decoded_char = chr(ord(char) ^ ord(key[key_index]))
        decoded_text += decoded_char
        key_index = (key_index + 1) % key_length
    return json.loads(decoded_text)


def read_tdata(filepath: str):
    """Декодирует .tdata и возвращает dict"""
    return decode_file(filepath)



