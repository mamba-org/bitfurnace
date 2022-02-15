import os
import pathlib

from bitfurnace.util import run, variables

class RecipeBase:
    workdir = variables.src_dir

    cflags = os.environ.get("CFLAGS", "").split()
    cxxflags = os.environ.get("CXXFLAGS", "").split()
    ldflags = os.environ.get("LDFLAGS", "").split()

    env = os.environ.copy()

    def get_env(self):
        env = self.env.copy()
        env["CFLAGS"] = " ".join(self.cflags)
        env["CXXFLAGS"] = " ".join(self.cxxflags)
        env["LDFLAGS"] = " ".join(self.ldflags)
        return env

    def run_cmd(self, args):
        run(args, cwd=self.workdir, env=self.get_env(), shell=False)

    def run_stage(self, stage_name):
        """
        run a default stage by name

        this collects cmd, default args and args.
        For example, for the configure stage it will look at

        configure_cmd, get_configure_default_args or configure_default_args and
        get_configure_args or configure_args and then concatenate all of them
        and run
        """

        cmd = getattr(self, f"{stage_name}_cmd", None)
        if not cmd:
            return False

        if isinstance(cmd, str) or isinstance(cmd, pathlib.PurePath):
            cmd = [str(cmd)]

        if hasattr(self, f"get_default_{stage_name}_args"):
            default_args = getattr(self, f"get_default_{stage_name}_args")()
        else:
            default_args = getattr(self, f"default_{stage_name}_args", [])

        if hasattr(self, f"get_{stage_name}_args"):
            args = getattr(self, f"get_{stage_name}_args")()
        else:
            args = getattr(self, f"{stage_name}_args", [])

        cmd = [str(c) for c in (cmd + default_args + args)]

        self.run_cmd(cmd)

    def run_all_stages(self):
        # execute all stages
        for stage in self.stages:
            getattr(self, stage)()

    def __init__(self):
        pass

    stages = ["pre_configure", "configure", "build", "test", "install", "post_install"]

    def pre_configure(self):
        if not self.workdir.exists():
            print(f"Creating workdir at {self.workdir}")
            self.workdir.mkdir(parents=True, exist_ok=False)

    def configure(self):
        self.run_stage("configure")

    def build(self):
        self.run_stage("build")

    def install(self):
        self.run_stage("install")

    def test(self):
        if variables.target_platform != variables.build_platform:
            return False
        self.run_stage("test")

    def post_install(self):
        self.run_stage("post_install")
