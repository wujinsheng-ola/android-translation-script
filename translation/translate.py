import os
import json
import re


def escape_special_characters(value):
    if value is None:
        return ""
    escaped_value = value.replace('\n', r'\n')
    # escaped_value = value.replace('&', '&amp;')
    escaped_value = escaped_value.replace('@', r'\@')
    # escaped_value = escaped_value.replace('\n', r'\n')
    escaped_value = escaped_value.replace('\n', r'&It')
    escaped_value = escaped_value.replace("'", r'\'')
    # escaped_value = escaped_value.replace("'", '&#39;')  # 转义单引号为 &#39;

    return escaped_value


def escape_special_characters_for_key(value):
    if value is None:
        return ""
    if value == "anti_recording/screenshoot_setting_entrance":
        value = "anti_recording_and_screenshoot_setting_entrance"

    escaped_value = re.sub(r'[:\s-]', '', value)
    escaped_value = escaped_value.replace('/', '_')
    escaped_value = escaped_value.replace('&', '_')
    escaped_value = escaped_value.replace('&', '&amp;')
    escaped_value = escaped_value.replace('@', r'\@')
    escaped_value = escaped_value.replace('\n', r'\n')
    escaped_value = escaped_value.replace("'", '&#39;')
    escaped_value = escaped_value.replace("%1.", '')
    escaped_value = escaped_value.replace("%1", '')
    escaped_value = escaped_value.replace("+1", '')
    return escaped_value


def generate_android_values(json_file, output_folder):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    base_name = os.path.splitext(os.path.basename(json_file))[0]
    language_code = base_name.split('string_')[1].replace('_', '-')  # 将下划线替换为连字符
    if language_code == "en":
        output_folder_path = os.path.join(output_folder, f'values')
    else:
        output_folder_path = os.path.join(output_folder, f'values-{language_code}')

    os.makedirs(output_folder_path, exist_ok=True)

    output_file = os.path.join(output_folder_path, 'strings.xml')

    existing_keys = set()  # 用于存储已存在的键

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        f.write('<resources>\n')

        for key, value in data.items():
            # 处理键中的特定字符
            key = escape_special_characters_for_key(key)
            # 如果键为空字符串，则跳过当前键的处理
            if not key.strip():
                continue

            # 如果键已存在，则跳过当前键的处理
            if key in existing_keys:
                continue

            existing_keys.add(key)  # 将当前键添加到已存在的键集合中

            # 处理值中的特定字符并进行转义
            formatted_value = escape_special_characters(value)
            if formatted_value != "":
                f.write('    <string name="{0}"><![CDATA[{1}]]></string>\n'.format(key, formatted_value))

        f.write('</resources>')


if __name__ == '__main__':
    current_directory = os.getcwd()  # 获取当前目录

    for file_name in os.listdir(current_directory):
        file_path = os.path.join(current_directory, file_name)  # 拼接文件路径

        if file_name.endswith('.json') and file_name.startswith('string_'):  # 判断文件是否为以 "string_" 开头的 JSON 文件
            generate_android_values(file_path, current_directory)
