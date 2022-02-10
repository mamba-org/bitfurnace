import sys

# import tempfile
import importlib.util
from bitfurnace.util import variables
from pathlib import Path

header = """
import sys
sys.path.append({bitfurnace_dir})
from bitfurnace.util import initialize_globals, run

initialize_globals(globals())
"""

def run_recipe(r):
    r.pre_configure()
    r.configure()
    r.build()

    if variables.target_platform == variables.build_platform:
        r.test()

    r.install()
    r.post_install()



if __name__ == "__main__":
    temp_recipe = "rendered_build.py"
    with open(temp_recipe, "wb") as fo:
        header = header.format(bitfurnace_dir=Path(__file__).parent[0])
        fo.write(header.encode("utf-8"))
        with open(sys.argv[1], "rb") as fi:
            fo.write(fi.read())

    with open(temp_recipe, "r") as fi:
        print("Running full recipe: \n" + fi.read())

    spec = importlib.util.spec_from_file_location("Recipe", temp_recipe)
    recipe_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(recipe_module)
    r = recipe_module.Recipe()

    run_recipe(r)
