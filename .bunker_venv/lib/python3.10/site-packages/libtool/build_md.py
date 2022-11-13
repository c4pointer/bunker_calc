from .get_imports import get_requires_info


def get_python_modules_name(modules_list):
    b = "\nand " + modules_list[-1]
    a = ",\n".join(modules_list[:-1])
    f = a + b
    if len(modules_list) == 1:
        f = "".join(modules_list)
    return f  # moviepy,mhmovie and nupy


def get_build_with(modules_list):
    final = []
    tav = "* [{name}]({url}) - {description}"
    descriptions, home_urls = get_requires_info(modules_list)
    for name in modules_list:
        url = home_urls[name]
        description = descriptions[name]
        ft = tav.format(name=name, url=url, description=description)
        final.append(ft)
    final = "\n".join(final)
    return final


def _build_md(name, description, python_v, python_code, python_modules_name, built_with, author, pylicense, out, md_in):
    author_title = "Author"
    #python_modules_s = "s" if len(python_modules_name) == 1 else ""
    ###########################
    with open(md_in) as rm_file:
        text = rm_file.read()
    text = text.format(
        name=name,
        description=description,
        python_v=python_v,
        python_code=python_code,
        python_modules_name=python_modules_name,
        built_with=built_with,
        authors=author,
        pylicense=pylicense,
        author_title=author_title,
    )
    with open(out, "w") as rm_file:
        rm_file.write(text)


def build_md(name: str,
             description: str,
             python_v,
             python_code: str,
             install_requires: list,
             author: str,
             pylicense: str,
             out: str = "README_out.md",
             md_in: str = "README.md"
             ):
    python_modules_name = get_python_modules_name(install_requires)
    built_with = get_build_with(install_requires)

    _build_md(name, description, python_v, python_code, python_modules_name, built_with, author, pylicense, out, md_in)


if __name__ == "__main__":
    mo = "moviepy mhmovie numpy".split(" ")
    # print(python_modules_name(mo))
    # print(get_build_with(mo))
