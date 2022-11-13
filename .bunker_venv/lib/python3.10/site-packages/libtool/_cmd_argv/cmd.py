import sys
import configparser
################################
from libtool.libtool_class import Library
from libtool.up_version import *
from libtool.pypi import up_pypi
#######################################
from libtool.util.builtins import *
from libtool.util.regex import get_val


######################################
def get_folder():
    with open("setup.py") as setup_py:
        setup_py_read = setup_py.read()
    ###################################
    folder = get_val("name", setup_py_read)
    return folder


def version(argv, es):
    folder = get_folder()
    Remove()
    UpVersion(folder)
    print("done")


def create(argv, es):
    file = argv.pops(0, funk=lambda: r_ex("you need ini file with info tag and param"))
    file_exists(file)  # if not file exists raise error

    config = configparser.ConfigParser()

    config.read(file)
    info = config["info"]
    info_dict = dict(info)
    ######################
    if "install_requires" in info_dict.keys():
        info_dict["install_requires"] = info_dict["install_requires"].split(",")
    if "scripts" in info_dict.keys():
        info_dict["scripts"] = info_dict["scripts"].split(",")
    if "license" in info_dict.keys():
        info_dict = BuDict(info_dict).rename_key("license", "pylicense")

    l = Library(**info_dict)

    if "init" not in es:
        print("create __init__.py")
        l.c_init()

    if "setup" not in es:
        print("create setup.py")
        l.c_setup()
    if "licence" not in es:
        print("create Licence.txt")
        l.c_licence()
    if "readme" not in es:
        print("create README.md")
        l.c_md()

    ############
    choose = ["n", "y"]

    if "edit" not in es:
        f = buinput("you want to open editor for README.md? (y\\n)>", choose, "'{}' is not {}\n", str.lower)
        f = choose.index(f)  # n:False,y:True
    else:
        f = False  # not edit
    if f:  # buinput == y
        l.edit_md()

    print("done")
    ####################


def upload(argv, es):
    # up_pypi.creat_dist()
    opp = " ".join(argv)
    folder = get_folder()
    up_pypi.up(folder, opp)


def help(argv=None, es=None):
    print("""
version----remove build folders and up version to your choose version
create-----create auto library from simple ini file with -e for disable files
upload-----upload library to pypi
help-------show this messege
 
you can use shortcuts:
v----------version
c----------create
u----------upload
?----------help
for more help see https://github.com/matan-h/libtool
    """)
    quit(0)


def get_e(argv):
    final = []
    if "-e" in argv:
        i = argv.index("-e")
        final = argv[i:]
        final.pop(0)
    return final


def _parse(f, argv, es):
    if f == "version":
        version(argv, es)
    if f == "create":
        create(argv, es)
    if f == "upload":
        upload(argv, es)
    if f == "help":
        help(argv, es)


def parse(argv=None):
    # quit(5555)
    #####################################################
    if argv is None:
        argv = sys.argv
        argv.pop(0)  # pop __file__

    argv1_tree = [
        "version",  # remove build folders and up version
        "create",  # create Library from ini
        "upload",  # upload to pypi
        "help",  # help
    ]
    argv1_tree_s = {
        "v": "version",
        "c": "create",
        "u": "upload",
        "?": "help",
    }
    ################################
    argv = BuList(argv.copy())
    # print("argv=",argv)
    ###################



    first = argv.pops(0, funk=help)

    final = None
    if first in argv1_tree:
        final = first

    elif first in argv1_tree_s.keys():
        final = argv1_tree_s[first]

    else:
        print(f"the command '{first}' not found")
        quit(2)

    if final is None:
        quit(2)
    #######################
    es = get_e(argv)
    _parse(final, argv, es)


if __name__ == "__main__":
    parse()
