from setuptools import setup, find_packages, Extension
import platform
with open("README.md", "r") as ld:
      long_desc = ld.read()

def _requirements():
      if platform.system() == "Windows":
            return ["setuptools","numpy","tkhtmlview","Pillow","pywin32"]
      return ["setuptools","numpy","tkhtmlview","Pillow"]

setup(name="as3lib",
      version="0.0.9",
      author="ajdelguidice",
      author_email="ajdelguidice@gmail.com",
      url="https://github.com/ajdelguidice/python-as3lib",
      description="Partial implementation of ActionScript3 in Python",
      long_description=long_desc,
      long_description_content_type="text/markdown",
      packages=find_packages(),
      classifiers=[
            "Development Status :: 4 - Beta",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3.10",
            "Topic :: Utilities",
            ],
      python_requires=">=3.10",
      ext_modules=[
        Extension(name="as3lib.cmath",
            sources = ["sourcecode/cmath.c"],
        ),
        Extension(name="as3lib.flash.crypto",
            sources = ["sourcecode/crypto.c"],
        ),
      ],
      install_requires=_requirements(),
      )
