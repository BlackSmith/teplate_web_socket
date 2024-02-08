import yaml


def get_yaml(filename):
    with open(filename, 'r+') as fd:
        return yaml.safe_load(fd)

def dict_bytes2str(dd):
    res = {}
    for k in dd.keys():
        key = k.decode() if isinstance(k, bytes) else k
        if isinstance(dd[k], bytes):
            res[key] = dd[k].decode()
        else:
            res[key] = dd[k]
    return res
