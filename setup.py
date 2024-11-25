from setuptools import setup, Extension

setup(ext_modules=[
        Extension(name="as3lib.cmath",
            sources = ["sourcecode/cmath.c"],
        ),
        Extension(name="as3lib.flash._crypto",
            sources = ["sourcecode/crypto.c"],
        ),
      ]
      )
