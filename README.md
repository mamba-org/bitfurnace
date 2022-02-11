# bitfurnace

Write cross platform build scripts with the power of Python! 
To be used in the `boa` project.

Currently supports `CMake`, `Autotools`, `Meson` and `Make`.

## Examples

More coming soon!

### CMake

```py
from cmake import CMake

class Recipe(CMake):
    cmake_configure_args = {
        'BUILD_SHARED_LIBS': not features.static,
        'REPROC++': True
    }

    def pre_configure(self):
        if (self.workdir / "CMakeCache.txt").exists():
            (self.workdir / "CMakeCache.txt").unlink()
```

### Autotools

If `autoconf` and `gnuconfig` is added, automatically calls `autoreconf` and copies new `config.guess` files

```py
from autotools import Autotools

class Recipe(Autotools):

	def get_configure_args(self):
		configure_args = []

		if features.static:
			configure_args += ['--enable-static', '--disable-shared']
		else:
			configure_args += ['--disable-static', '--enable-shared']

		if target_platform.startswith('osx'):
			configure_args += ['--with-iconv']
		else:
			configure_args += ['--without-iconv']
			if features.zstd:
				self.ldflags += ['-pthread']


		configure_args += [
			'--without-cng',
			'--without-nettle',
			'--without-expat',
		]

		return configure_args
```