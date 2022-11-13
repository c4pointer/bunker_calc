import os

from .get_imports import get_imports, get_imports_code, find_main, License
import sys
from os import path
from .tmp_text import _setup_build, _init_bg
from .build_md import build_md
from .util.builtins import Bustr


class Library:
    def __init__(self, test_file, email, description, url, pylicense, author,
                 install_requires: list or tuple, folder="auto", start_version="0.0.1", scripts=None):
        # ###################
        # install_requires += ["libtool"]
        # #########################################################################################################################################################################
        (self.author, self.email, self.description, self.url, self.pylicense,
         self.install_requires, self.folder, self.scripts
         ) = (
            author, email, description, url, pylicense, install_requires, folder, scripts)
        with open(test_file, "r") as r:
            self.test_lines = r.readlines()
        self.imports = get_imports(test_file)
        self.imports_code = get_imports_code(test_file)
        # ### #get folder from test_file
        if folder != "auto":
            self.folder = folder
        else:
            folder = [*self.imports][0]
            if folder.module:
                self.folder = folder.module[0]
            else:
                self.folder = folder.name[0]
        self.abspath = lambda p: self.folder + "\\" + p
        # ######################################################################
        # v_file = path.abspath("version.txt")
        # if not path.exists(v_file):
        #    with open(v_file, "w") as v_file_io:
        #        v_file_io.write(str(start_version))

        # with open(v_file, "r") as version:
        #    version = version.read()
        self.version = start_version
        # ######################################################################
        self.main = find_main(test_file)
        self.test_file = test_file

    def c_init(self):
        init_file = self.abspath("__init__"".py")
        init_text = ['if __name__ == "__main__":'] + self.main
        init_text = "\n".join(init_text)
        import_code = "\n".join(self.imports_code)
        #####################
        author = self.author
        ##############
        init_pre = [self.folder, self.description, self.url, self.version,
                    self.email, author, self.pylicense]
        init_text = import_code + _init_bg(*init_pre) + init_text

        with open(init_file, "w") as init:
            init.write(init_text)

    def c_setup(self):
        if self.install_requires is None:
            self.install_requires = []
        package_name = self.folder

        python_requires = sys.version.split(' ')[0].split(".")[0] + "." + sys.version.split(' ')[0].split(".")[1]
        programming_language = sys.version.split(' ')[0].split(".")[0]
        author = self.author
        ##################################################################
        setup_text = _setup_build(
            package_name=package_name,
            author=author,
            author_email=self.email,
            description=self.description,
            url=self.url,
            License=self.pylicense,
            install_requires=self.install_requires,
            python_requires=python_requires,
            Programming_Language=programming_language,
            version=self.version,
            scripts=self.scripts
        )
        with open(path.abspath("setup.py"), "w") as setup:
            setup.write(setup_text)

    def c_md(self):
        python_v = sys.version.split(' ')[0].split(".")[0]
        ##############################
        tab_dict = {"\t": "", " " * 4: ""}
        funk = lambda s: Bustr(s).replace_all(tab_dict, 1)
        no_tabs_main = list(map(funk, self.main))
        no_tabs_main[-1] = no_tabs_main[-1].rstrip()
        ####
        python_code = "\n".join(self.imports_code) + "\n\n" + "".join(no_tabs_main)
        ###
        md_in = os.path.dirname(__file__) + "\\" + "README_in.md"
        build_md(
            name=self.folder,
            description=self.description,
            python_v=python_v,
            python_code=python_code,
            install_requires=self.install_requires,
            author=self.author,
            pylicense=self.pylicense,
            out=path.abspath("README.md"),
            md_in=md_in
        )

    def c_licence(self):
        license_file = self.abspath("license.txt")
        pylicense = self.pylicense
        license_contact = str(License(pylicense, self.author))
        with open(license_file, "w") as license_bin_file:
            license_bin_file.write(license_contact)

    def edit_md(self):
        md = path.abspath("README.md")
        os.system(f"markdown_edit \"{md}\"")

def __main__():
    import os
    os.chdir("..")
    os.system("py ..\\create.py")
    # u = Library("..\\test_file.py")
    # u.Csetup("matan", "@gmail", "to add @gmail", "matan.wixsite.com",install_requires=("r","rr"))
    # u.Cinit()
    # print(u.folder)
    # print('\n'.join(u.imports_code))
    # u.Csetup("name", "matan", "matanEmaile", "matan description", install_requires=["f", "g"])
