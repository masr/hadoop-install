import xml.dom.minidom
import re
import os
import shutil
import yaml


def trans_dict_to_xml(data):
    values = []
    for k in sorted(data.keys()):
        v = data.get(k)
        values.append("<property><name>{key}</name><value>{value}</value></property>".format(key=k, value=v))
    content = '<configuration>{}</configuration>'.format(''.join(values))
    return xml.dom.minidom.parseString(content).toprettyxml()


def trans_dict_to_conf(data, seperator="="):
    content = ""
    for k in sorted(data.keys()):
        content += str(k) + seperator + str(data[k]) + "\n"
    return content


def replace_keys_in_dict(obj, params):
    result = {}
    for k, v in obj.items():
        k = replace_params(str(k), params)
        result[k] = v
    return result


def replace_values_in_dict(obj, params):
    result = {}
    for k, v in obj.items():
        v = replace_params(str(v), params)
        result[k] = v
    return result


def delete_keys_by_prefix(obj, prefix):
    result = {}
    for k, v in obj.items():
        if not k.startswith(prefix):
            result[k] = v
    return result


def replace_params(content, params):
    m = re.findall(r'({%\s*(.*?)\s*%})', content)
    if len(m) > 0:
        for i in m:
            content = content.replace(i[0], str(params[i[1]]))
    return content


def check_and_create_dir(dir_path):
    if os.path.exists(dir_path) and not os.path.isdir(dir_path):
        raise Exception(dir_path + " should be a directory")
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


def clean_and_create_dir(dir_path):
    if os.path.exists(dir_path) and not os.path.isdir(dir_path):
        raise Exception(dir_path + " should be a directory")
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
        os.mkdir(dir_path)
    else:
        os.mkdir(dir_path)


def get_configuration(config_file_path):
    result = {}
    if os.path.exists(config_file_path):
        with open(config_file_path) as config_file:
            result = yaml.load(config_file.read(), Loader=yaml.Loader)
            if result is None:
                result = {}
    return result
