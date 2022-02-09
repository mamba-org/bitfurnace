from bitfurnace.util import variables
from bitfurnace.recipe import RecipeBase

import os

default_meson_args = os.environ.get("MESON_ARGS") or ""
default_meson_args = default_meson_args.split()


class Meson(RecipeBase):
    configure_cmd = "meson"
    configure_args = [
        "setup",
        "builddir",
        f"--prefix={variables.prefix}",
        "--buildtype=release",
        "-Dlibdir=lib",
    ] + default_meson_args

    build_cmd = "ninja"
    build_args = ["-C", "builddir"]

    install_cmd = "ninja"
    install_args = ["-C", "builddir", "install"]

    test_cmd = "ninja"
    test_args = ["-C", "builddir", "test"]
