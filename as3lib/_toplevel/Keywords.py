# This file defines the actionscript keywords as python decorators/functions
from dataclasses import dataclass
from miniamf import register_package


@dataclass
class amfMetaData:
    # The variable names for this are defined by miniamf's __amf__ property
    static_attrs: list
    exclude_attrs: list
    readonly_attrs: list
    proxy_attrs: list
    amf3: bool
    dynamic: bool
    alias: bool  # TODO: Placeholder data type
    external: bool
    synonym_attrs: list


@dataclass
class as3PackageMetaData:
    namespace: str
    ...


class extends:
    def __init__(self, parent):
        self._p = parent

    def __call__(self, cls):
        cls.prototype = self._p
        return cls


class package:
    ...


class implements:
    def __init__(self, *interfaces):
        self._i = interfaces

    def __call__(self, cls):
        cls._as3_implements = self._i


class namespace:
    # Currently only works on packages
    def __init__(self, ns):
        self.ns = ns

    def __call__(self, cls):
        register_package(cls, self.ns)
        return cls
