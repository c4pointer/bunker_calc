def _setup_build(package_name, version, License, description, author, author_email, url, install_requires,
                 Programming_Language,
                 python_requires, scripts):
    package_data = """package_data = {
        '{}': ['LICENSE'],
    },""".format(package_name)

    if scripts is not None:
        scripts = f"scripts={scripts},"
    else:
        scripts = ""
    a = f"""\n
import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='{package_name}',
    version='{version}',
    license='{License}',
    description='{description}',
    author='{author}',
    author_email='{author_email}',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = '{url}',
    packages=['{package_name}'],
    {scripts}
    install_requires = {str(install_requires)},
    {package_data}
    classifiers=[
        "Programming Language :: Python :: {Programming_Language}",
        "License :: OSI Approved :: {License}",
        "Operating System :: OS Independent",
    ],
    python_requires='>={python_requires}',
)"""
    return a


#####################################
def _init_bg(title, description, url, version, email, author, pylicense):
    a = f"""
__title__ = '{title}'
__description__ = '{description}.'
__url__ = '{url}'
__version__ = '{version}'
__author__ = '{author}'
__author_email__ = '{email}'
__license__ = '{pylicense}'
"""
    return a
