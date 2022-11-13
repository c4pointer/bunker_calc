import shutil
import glob as sys_glob
import re
from .util.regex import get_val


class UpVersion:
    def __init__(self, folder, v=None):
        self.init_name = folder + "\\__init__.py"
        self.setup_name = "setup.py"
        ########################################
        if not v:
            with open(self.setup_name) as setup_bin:
                self.v = get_val("version", setup_bin.read())
        ###########################
        self.up_n()
        ##########################
        print("update __init__.py")
        self.init_replace()
        ##########################
        print("update setup.py")
        self.setup_replace()

    def up_n(self):
        self.v = input(f"enter new version:\n{self.v} ->")
        try:
            if self.v[0] == ".":
                print("invalid version")
                quit(2)
                # raise self.VersionException(self.v)
            if self.v[-1] == ".":
                print("invalid version")
                quit(2)
            if self.v in ["", " "]:
                print("invalid version")
                quit(2)
        except IndexError:
            print("up version canceled by user")
        except KeyboardInterrupt:
            print("up version canceled by user")
            # raise self.VersionException(self.v)

    def file_replace(self, file, sec):
        with open(file, "r")as bin_file:
            contact = bin_file.read()

        contact = (re.sub(*sec, contact))

        with open(file, "w") as setup_file:
            setup_file.write(contact)

    def setup_replace(self):
        setup_sec = ["version=.(.+).\,", f"version=\'{self.v}\',"]
        self.file_replace(self.setup_name, setup_sec)

    def init_replace(self):
        init_sec = [r"__version__.+[\'|\"](.+).", f"__version__ = \'{self.v}\'"]
        self.file_replace(self.init_name, init_sec)

    class VersionException(BaseException):
        def __init__(self, s):
            message = f"Invalid version - \"{s}\""
            super().__init__(message)


class Remove:
    def __init__(self):
        self.rmtree('dist')
        self.rmtree(self.glob0('*.egg-info'))
        self.rmtree(self.glob0('build'))

    def glob0(self, l):
        try:
            return sys_glob.glob(l)[0]
        except IndexError:
            pass

    def rmtree(self, s):
        try:
            if s is None:
                return
            shutil.rmtree(s)
        except FileNotFoundError:
            pass
