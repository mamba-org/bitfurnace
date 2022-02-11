import subprocess
import os
from pathlib import Path
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class dotdict(dict):
    """dot.notation access to dictionary attributes"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


variables = dotdict(
    {
        "prefix": Path(os.environ.get("PREFIX")),
        "build_prefix": Path(os.environ.get("BUILD_PREFIX")),
        "recipe_dir": Path(os.environ.get("RECIPE_DIR")),
        "target_platform": os.environ.get("target_platform"),
        "build_platform": os.environ.get("build_platform"),
        "src_dir": Path(os.environ.get("SRC_DIR")),
        "cpu_count": os.environ.get("CPU_COUNT"),
        "host": os.environ.get("HOST"),
        "build": os.environ.get("BUILD"),
        "pkg_version": os.environ.get("PKG_VERSION"),
        "cc": os.environ.get("CC"),
        "cxx": os.environ.get("CXX"),
        "cpp": os.environ.get("CPP"),
        "fortran": os.environ.get("FORTRAN"),
    }
)

if variables.target_platform.startswith("win"):
    variables["library_lib"] = Path(os.environ.get("LIBRARY_LIB"))
    variables["library_bin"] = Path(os.environ.get("LIBRARY_BIN"))

features = dotdict()
for k in os.environ.keys():
    if k.startswith("FEATURE_"):
        feature_name = k[len("FEATURE_") :].lower()
        features[feature_name] = os.environ[k] == "1"
variables["features"] = features


def initialize_globals(g=None):
    if not g:
        g = globals()
    g.update(variables)


initialize_globals()


def shorten_strings(x):
    x = str(x)
    x = x.replace(str(variables.prefix), "$PREFIX")
    x = x.replace(str(variables.src_dir), "$SRC_DIR")
    return x


def fancy_print(args):
    if not isinstance(args, list):
        args = [args]
    short_args = [shorten_strings(x) for x in args]
    print(f"Running {short_args[0]} with arguments:\n")
    if len(short_args) > 2:
        print(f"{short_args[0]} \\")
        for a in short_args[1:]:
            print(f"   {a} \\")
    else:
        print(" ".join(short_args))
    print("\n")


def run(*args, **kwargs):
    fancy_print(args[0])
    subprocess.check_call(*args, **kwargs)
