from __future__ import annotations
from as3lib._toplevel.Array import Array
from as3lib._toplevel.Constants import undefined, null
from as3lib._toplevel.Errors import ArgumentError
from as3lib._toplevel.Functions import isXMLName
from as3lib._toplevel.Object import Object
from as3lib._toplevel.String import String
from multipledispatch import dispatch


class Namespace(Object):
   _mdspns = {}

   @property
   def prefix(self):
      return self._prefix

   @prefix.setter
   def prefix(self, value):
      self._prefix = value

   @property
   def uri(self):
      return self._uri

   @uri.setter
   def uri(self, value):
      self._uri = value

   @dispatch(object, object, namespace=_mdspns)
   def __init__(self, prefixValue, uriValue):
      if prefixValue is None or isinstance(prefixValue, undefined):
         self._prefix = undefined()
      elif isXMLName(prefixValue):
         self._prefix = str(prefixValue)
      else:
         self._prefix = undefined()
      if isinstance(uriValue, QName):
         self._uri = uriValue.uri
      else:
         self._uri = str(uriValue)

   @dispatch(object, namespace=_mdspns)
   def __init__(self, uriValue):
      if isinstance(uriValue, Namespace):
         self._prefix = uriValue.prefix
         self._uri = uriValue.uri
      elif isinstance(uriValue, QName):
         self._prefix = None
         self._uri = uriValue.uri

   @dispatch(namespace=_mdspns)
   def __init__(self):
      self._prefix = String()
      self._uri = String()

   def toString(self):
      return self.uri

   def valueOf(self):...


class QName(Object):
   _mdspns = {}

   @property
   def localName(self):
      return self._localName

   @property
   def uri(self):
      return self._uri

   @dispatch(object, namespace=_mdspns)
   def __init__(self, qname):
      if isinstance(qname, QName):
         self._localName = qname.localName
         self._uri = qname.uri
      elif isinstance(qname, undefined):
         self._localName = ''
         self._uri = None
      else:
         self._localName = str(qname)
         self._uri = None

   @dispatch(object, object, namespace=_mdspns)
   def __init__(self, uri, localName):
      if isinstance(uri, Namespace):
         self._uri = uri.uri
      elif isinstance(uri, null):
         self._uri = null
      else:
         self._uri = str(uri)
      if isinstance(localName, QName):
         self._localName = localName.localName
      else:
         self._localName = str(localName)

   @dispatch(namespace=_mdspns)
   def __init__(self):
      self._localName = ''
      self._uri = None

   def toString(self):
      if self.uri == '':
         return self.localName
      elif isinstance(self.uri, null):
         return f'*::{self.localName}'
      else:
         return f'{self.uri}::{self.localName}'

   def valueOf(self):...


class XMLList(Object):
   # TODO: Check to see if any of these functions should return a flattened list
   def __init__(self, value):
      self._value = Array()
      ...

   def attribute(self, attributeName):
      res = Array()
      for i in self._value:
         j = i.attributes(attributeName)
         if j.length() > 0:
            res.append(j)
      return XMLList(res)

   def attributes(self):
      return XMLList([i.attributes() for i in self._value])

   def child(self, propertyName):
      return XMLList([i.child(propertyName) for i in self._value])

   def children(self):
      return XMLList([i.children() for i in self._value])

   def comments(self):...
   def contains(self, value):...
   def copy(self):...
   def decendants(self, name):...
   def elements(self, name):...
   def hasComplexContext(self):...
   def hasOwnProperty(self, p):...
   def hasSimpleContext(self):...

   def length(self):
      return self._value.length

   def normalize(self):...
   def parent(self):...
   def processingInstructions(self, name):...
   def propertyIsEnumerable(self, p):...

   def text(self):
      return XMLList([i.text() for i in self._value])

   def toString(self):...
   def toXMLString(self):...

   def valueOf(self):
      return self


class XML(Object):
   # Prerequisite: Object attribute access
   # TODO: Implement accessing children. This should be done by using <xmlobj>.<child>. Doing this appears to return all children with the name <child>
   ignoreComments = True
   ignoreProcessingInstructions = True
   ignoreWhitespace = True
   prettyIndent = 2
   prettyPrinting = True

   def __init__(self, value):
      self._name: QName = None
      self._type = None  # INTERNAL: Node type (text, comment, processing-instruction, attribute, or element)
      self._namespace = None
      self._namespaces = Array()
      ...

   def addNamespace(self, ns):...
   def appendChild(self, child):...
   def attribute(self, attributeName):...
   def attributes(self):...
   def child(self, propertyName):...
   def childIndex(self):...
   def children(self):...
   def comments(self):...
   def contains(self, value):...
   def copy(self):...

   @staticmethod
   def defaultSettings():
      # TODO: Make this return an Object once that is properly implemented
      return {
         'ignoreComments': True,
         'ignoreProcessingInstructions': True,
         'ignoreWhitespace': True,
         'prettyIndent': 2,
         'prettyPrinting': True
      }

   def decendants(self, name):...
   def elements(self, name):...
   def hasComplexContext(self):...
   def hasOwnProperty(self, p):...
   def hasSimpleContext(self):...
   def inScopeNamespace(self):...
   def inserChildAfter(self, child1, child2):...
   def insertChildBefore(self, child1, child2):...

   def length(self):
      return 1

   def localName(self):
      return self._name.localName

   def name(self):
      return self._name

   def namespace(prefix):...
   def namespaceDeclarations(self):...

   def nodeKind(self):
      return self._type

   def normalize(self):...
   def parent(self):...
   def prependChild(self):...
   def processingInstructions(self, name):...
   def propertyIsEnumerable(self, p):...
   def removeNamespace(self, ns):...
   def replace(self, propertyName, value):...
   def setChildren(self, value):...

   def setLocalName(self, name):
      self._name._localName = name

   def setName(self, name):...

   def setNamespace(self, ns:Namespace):
      self._namespace = ns

   @staticmethod
   def setSettings(*rest):...

   def settings(self):
      # TODO: Make this return an Object once that is properly implemented
      return {
         'ignoreComments': self.ignoreComments,
         'ignoreProcessingInstructions': self.ignoreProcessingInstructions,
         'ignoreWhitespace': self.ignoreWhitespace,
         'prettyIndent': self.prettyIndent,
         'prettyPrinting': self.prettyPrinting
      }

   def text(self):...
   def toString(self):...
   def toXMLString(self):...

   def valueOf(self):
      return self
