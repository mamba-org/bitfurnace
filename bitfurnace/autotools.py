from bitfurnace.util import variables, run
from bitfurnace.recipe import RecipeBase

import logging
log = logging.getLogger(__file__)

import shutil


class Autotools(RecipeBase):
    workdir = variables.src_dir
    configure_cmd = workdir / "configure"

    configure_args = [
        f"--prefix={variables.prefix}",
        f"--host={variables.host}",
        f"--build={variables.build}",
    ]

    # Builds are usually done with `make`
    install_cmd = build_cmd = "make"

    build_args = [f"-j{variables.cpu_count}"]

    install_args = ["install"]

    run_autoreconf = True
    update_config_guess = True

    def pre_configure(self):
        if self.update_config_guess:
            # Do this from Python
            # cp $BUILD_PREFIX/share/gnuconfig/config.* .
            loc = list(variables.src_dir.rglob("config.guess"))
            if len(loc):
                config_guess_loc = loc[0].parents[0]
                for f in (variables.build_prefix / "share" / "gnuconfig").glob(
                    "config.*"
                ):
                    print(f"Copying new file: {f} to {config_guess_loc}")
                    shutil.copy(f, config_guess_loc)

        if self.run_autoreconf:
            autoreconf_path = variables.build_prefix / "bin" / "autoreconf"
            if not autoreconf_path.exists():
                log.warning("Autoreconf not installed in build prefix. Add `autoconf` package to build.")
            else:
                run(
                    [variables.build_prefix / "bin" / "autoreconf", "-v", "-f", "-i"],
                    cwd=self.workdir,
                )

        super().pre_configure()
