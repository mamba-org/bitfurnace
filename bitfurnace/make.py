from bitfurnace.recipe import RecipeBase

class Make(RecipeBase):
    def configure(self):
        return 0

    # Builds are done with `make`
    install_cmd = build_cmd = "make"

    default_build_args = [f"PREFIX='${prefix}'", f"-j{variables.cpu_count}"]

    default_install_args = ["install"]