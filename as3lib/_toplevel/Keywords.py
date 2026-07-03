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


class property:
    # Adds a property type with write-only support
    def __init__(self, **kwargs):
        if 'fset' in kwargs:
            self.fset = kwargs['fset']
        if 'fget' in kwargs:
            self.fget = kwargs['fget']

    def getter(self, fget):
        self.fget = fget
        return self

    def __get__(self, instance, owner):
        if not hasattr(self, 'fget'):
            raise AttributeError("can't get attribute")
        cls = instance if instance is not None else self
        return self.fget(cls, owner)

    def setter(self, fset):
        self.fset = fset
        return self

    def __set__(self, instance, value):
        if not hasattr(self, 'fset'):
            raise AttributeError("can't set attribute")
        cls = instance if instance is not None else self
        self.fset(cls, value)


class property_get(property):
    '''
    Decorator replacement for "property get"

    Use like this:

    @property_get
    def prop(self):
        ...

    Using this property type means that property setter must be set like this:

    @prop.setter
    def prop(self, value):
        ...

    '''
    def __init__(self, fget):
        self.fget = fget


class property_set(property):
    '''
    Decorator replacement for "property set"

    Use like this:

    @property_set
    def prop(self, value):
        ...

    Using this property type means that property getter must be set like this:

    @prop.getter
    def prop(self):
        ...

    '''
    def __init__(self, fset):
        self.fset = fset


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
