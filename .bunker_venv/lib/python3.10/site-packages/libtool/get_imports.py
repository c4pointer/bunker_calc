import json

import requests
from collections import namedtuple

Import = namedtuple("Import", ["module", "name", "alias"])


def get_imports_code(file):
    imports_sys = ("import ", "from ", "#")
    imports = []
    with open(file) as file_io:
        contact = file_io.read().split("\n")
    ############################
    for i in contact:
        i_ls = i.lstrip()
        startswith = i_ls.startswith
        if startswith(imports_sys) or i_ls == "":
            imports.append(i)
        else:
            break
    return imports


def get_imports(path):
    import ast

    with open(path) as fh:

        root = ast.parse(fh.read(), path)

    for node in ast.iter_child_nodes(root):
        if isinstance(node, ast.Import):
            module = []
        elif isinstance(node, ast.ImportFrom):
            module = node.module.split('.')
        else:
            continue

        for n in node.names:
            yield Import(module, n.name.split('.'), n.asname)


def find_main(path):
    main = []
    main_code = []
    with open(path, "r") as r:
        for line in r.readlines():
            if ('if __name__' in line and '__main__' in line and '==' in line) or (main == True):
                if 'if __name__' in line and '__main__' in line and '==' in line:
                    main = True
                elif main == True:
                    main_code.append(line)
    return main_code


def get_requires_info(install_requires):
    descriptions = {}
    home_urls = {}
    for install_r in install_requires:
        r = requests.get('https://pypi.python.org/pypi/{}/json'.format(install_r))
        try:
            description = r.json()["info"]["summary"]
        except json.decoder.JSONDecodeError:
            home_urls.update({install_r:""})
            descriptions.update({install_r:"libtool cant find this library"})
            continue
        descriptions.update({install_r: description})
        ###############################################
        home_url = (r.json()["info"]["home_page"])
        home_urls.update({install_r: home_url})
    return [descriptions, home_urls]


class License:
    def __init__(self, pylicense, name):
        self.pylicense = pylicense
        self.name = name

    def __str__(self):
        f = self.get_json()
        year = self.getyear()
        name = self.name
        f = f.replace("[year]", str(year), 1)
        f = f.replace("[fullname]", name , 1)
        return f

    def get_json(self) -> str:
        import requests
        pylicense = self.pylicense
        url = f"https://api.github.com/licenses/{pylicense}"
        r = requests.get(url)
        r = r.json()
        try:
            url = r["body"]
        except KeyError:
            raise self.LicenseNotFound(pylicense)
        return url

    def getyear(self):
        from datetime import datetime
        return datetime.today().year

    class LicenseNotFound(BaseException):
        def __init__(self, l):
            messege = f"""
license \"{l}\" not Found
you can write -e in cmd license. or not write .c_license() in python. and write your license.txt"""
            super().__init__(messege)


if __name__ == "__main__":
    mo = "moviepy mhmovie numpy".split(" ")
    g = get_requires_info(mo)
    print(g)
