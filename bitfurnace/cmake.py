from bitfurnace.recipe import RecipeBase
from bitfurnace.util import variables, run


class CMake(RecipeBase):
    configure_cmd = "cmake"
    build_cmd = "ninja"
    cmakelists_dir = variables.src_dir

    # default build folder
    workdir = variables.src_dir / "build"

    default_configure_args = [
        f"-DCMAKE_INSTALL_PREFIX={variables.prefix}",
        f"-DCMAKE_PREFIX_PATH={variables.prefix}",
        "-DCMAKE_INSTALL_LIBDIR=lib",
        "-GNinja",
    ]

    default_args = []

    def get_default_configure_args(self):
        return self.default_configure_args + [self.cmakelists_dir]

    def get_configure_args(self):
        args = []
        if hasattr(self, "cmake_configure_args"):
            if isinstance(self.cmake_configure_args, dict):
                for key, val in self.cmake_configure_args.items():
                    if isinstance(val, bool):
                        val = "ON" if val else "OFF"
                    args.append(f"-D{key}={val}")
            else:
                args = self.cmake_configure_args
        return args

    def build(self):
        run(self.build_cmd, cwd=self.workdir)

    def install(self):
        run([self.build_cmd, "install"], cwd=self.workdir)
