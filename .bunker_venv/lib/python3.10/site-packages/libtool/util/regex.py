import re


def get_val(val, string):
    sec = """{}(\s|)+=(\s|)+(["'])(.*)(["'])""".format(val)
    return re.findall(sec, string)[0][3]
