import xml.dom.minidom
import re
import os
import shutil


def trans_dict_to_xml(data, params):
    values = []
    for k in sorted(data.keys()):
        v = data.get(k)
        if isinstance(v, str):
            v = replace_params(v, params)
        values.append("<property><name>{key}</name><value>{value}</value></property>".format(key=k, value=v))
    content = '<configuration>{}</configuration>'.format(''.join(values))
    return xml.dom.minidom.parseString(content).toprettyxml()


def replace_params(content, params):
    m = re.findall(r'{%\s*(.*?)\s*%}', content)
    if len(m) > 0:
        for i in m:
            content = content.replace("{%" + str(i) + "%}", str(params[i]))
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
