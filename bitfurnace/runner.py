import sys

# import tempfile
import importlib.util
from bitfurnace.util import variables

header = """
from bitfurnace.util import initialize_globals, run

initialize_globals(globals())
"""


def run_recipe(r):
    r.pre_configure()
    r.configure()
    r.build()

    r.install()
    r.post_install()

    if variables.target_platform == variables.build_platform:
        r.test()


if __name__ == "__main__":
    # temp_recipe = tempfile.NamedTemporaryFile()
    temp_recipe = "xx.py"
    with open(temp_recipe, "wb") as fo:
        fo.write(header.encode("utf-8"))
        with open(sys.argv[1], "rb") as fi:
            fo.write(fi.read())

    with open(temp_recipe, "r") as fi:
        print(fi.read())

    spec = importlib.util.spec_from_file_location("Recipe", temp_recipe)
    recipe_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(recipe_module)
    r = recipe_module.Recipe()

    run_recipe(r)
