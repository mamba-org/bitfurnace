from bitfurnace.util import run, variables


class RecipeBase:
    workdir = variables.src_dir

    def __init__(self):
        pass

    def pre_configure(self):
        if not self.workdir.exists():
            print(f"Creating workdir at {self.workdir}")
            self.workdir.mkdir(parents=True, exist_ok=False)

    def configure(self):
        args = [
            str(x)
            for x in [self.configure_cmd]
            + self.get_default_configure_args()
            + self.get_configure_args()
        ]

        run(args, cwd=self.workdir, shell=False)

    def build(self):
        args = [
            str(x)
            for x in [self.build_cmd]
            + self.get_default_build_args()
            + self.get_build_args()
        ]
        run(
            args, cwd=self.workdir,
        )

    def install(self):
        args = [
            str(x)
            for x in [self.install_cmd]
            + self.get_default_install_args()
            + self.get_install_args()
        ]
        run(
            args, cwd=self.workdir,
        )

    def test(self):
        args = [
            str(x)
            for x in [self.test_cmd]
            + self.get_default_test_args()
            + self.get_test_args()
        ]
        run(
            args, cwd=self.workdir,
        )

    def post_install(self):
        pass

    default_configure_args = []

    def get_default_configure_args(self):
        return self.default_configure_args

    configure_args = []

    def get_configure_args(self):
        return self.configure_args

    default_build_args = []

    def get_default_build_args(self):
        return self.default_build_args

    build_args = []

    def get_build_args(self):
        return self.build_args

    default_install_args = []

    def get_default_install_args(self):
        return self.default_install_args

    install_args = []

    def get_install_args(self):
        return self.install_args

    default_test_args = []

    def get_default_test_args(self):
        return self.default_test_args

    test_args = []

    def get_test_args(self):
        return self.test_args
