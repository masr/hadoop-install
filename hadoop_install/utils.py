from xml.dom import minidom
import re
import os
import shutil
import yaml


def trans_dict_to_xml(data):
    values = []
    for k in sorted(data.keys()):
        v = data.get(k)
        v = v.replace("&", "&amp;")
        values.append("<property><name>{key}</name><value>{value}</value></property>".format(key=k, value=v))
    content = '<configuration>{}</configuration>'.format(''.join(values))
    return minidom.parseString(content).toprettyxml()


def trans_dict_to_conf(data, seperator="="):
    content = ""
    for k in sorted(data.keys()):
        content += str(k) + seperator + str(data[k]) + "\n"
    return content


def replace_keys_in_dict(_dict, params):
    ## params should not contain any variable string
    result = {}
    for k, v in _dict.items():
        k = replace_params(str(k), params)
        result[k] = v
    return result


def replace_values_in_dict(_dict, _params):
    ## params may also contain varialble string. And variable may also comes from _dict itself.
    result = _dict.copy()
    params = _params.copy()
    params.update(result)
    while True:
        original_variable_count = len([v for k, v in result.items() if has_variable_string(str(v))])
        for k, v in _dict.items():
            v = replace_params(str(v), params)
            result[k] = v
        params.update(result)
        variables = [v for k, v in result.items() if has_variable_string(str(v))]
        if len(variables) != 0 and len(variables) == original_variable_count:
            content = ','.join(variables)
            raise Exception("Cannot finalize variable in obj, please check loop definition: " + content)
        if len(variables) == 0:
            return result


def has_variable_string(content):
    m = re.findall(r'({%\s*(.*?)\s*%})', content)
    return len(m) > 0


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
            brace_key = i[0]
            key = i[1]
            m2 = re.findall(r'({%\s*(.*?)\s*%})', params[key])
            if len(m2) > 0:
                continue
            else:
                content = content.replace(brace_key, str(params[key]))
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
