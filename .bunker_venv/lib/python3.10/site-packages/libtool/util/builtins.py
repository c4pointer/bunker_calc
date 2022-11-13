from os import path


class Bustr(str):
    def __init__(self, s=""):
        str.__init__(s)

    def replace_all(self, dic, count=...):
        text = self
        for i, j in dic.items():
            text = text.replace(i, j, count)
        return text



class BuDict(dict):
    def __init__(self, s=None):
        super().__init__(s)

    def rename_key(self, old_key, new_key):
        self[new_key] = self.pop(old_key)
        return self


class BuList(list):
    def __init__(self, s=()):
        super().__init__(s)

    def pops(self, i, default=None, funk=None):
        try:
            return self.pop(i)
        except IndexError:
            if funk:
                funk()
            return default

    def get(self, index, default=None, funk=None):
        try:
            return self.__getitem__(index)
        except IndexError:
            if funk:
                funk()
            return default

    def replace(self, a, b, i=None):
        return list(map(lambda x: x.replace(a, b, i), self))


def buinput(text_before, text_to_need: list, text_after: str, funk=None) -> str:
    """
    :param text_before: start  input text
    :param text_to_need: list to while
    :param text_after: after  input text
    :param funk:funk fi=or text
    :return: str
    """
    name = input(text_before)
    if funk:
        funk(name)
    while name not in text_to_need:
        text_after = text_after.format(name, " or ".join(text_to_need))
        name = input(text_after)
        if funk:
            funk(name)
    return name


def r_ex(ex):  # raise ex
    """

    :param ex: error
    :return: None
    """
    print(ex)
    quit(2)


def file_exists(file):
    if not path.exists(file):
        raise FileNotFoundError(f"the {file} file is not found")
    else:
        return True
