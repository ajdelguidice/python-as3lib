from __future__ import annotations
from as3lib._toplevel.Array import Array
from as3lib._toplevel.Boolean import false, true
from as3lib._toplevel.Constants import undefined, null
from as3lib._toplevel.Errors import ArgumentError, TypeError
from as3lib._toplevel.Functions import isXMLName
from as3lib._toplevel.Keywords import each
from as3lib._toplevel.int import int
from as3lib._toplevel.Object import Object
from as3lib._toplevel.String import String


class Namespace(Object):
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

   def __init__(self, *args):
      # Fix enumeration order
      self._uri = undefined
      self._prefix = undefined

      if len(args) >= 2:
         val1 = args[0]
         val2 = args[1]
         if val1 is null:
            val1 = undefined
         if isXMLName(val1):
            self._prefix = String(val1)
         else:
            self._prefix = undefined
         if isinstance(val2, QName):
            self._uri = val2.uri
         elif self.prefix != '' and isinstance(val2, str) and not len(val2):
            raise TypeError('Illegal prefix %s for no namespace.' % self.prefix, 1098)
         else:
            self._uri = String(val2)
      elif len(args):
         val = args[0]
         if isinstance(val, Namespace):
            self._prefix = val.prefix
            self._uri = val.uri
         elif isinstance(val, QName):
            self._prefix = undefined
            self._uri = val.uri
         elif isinstance(val, str) and val == '':
            self._prefix = String()
            self._uri = String()
         else:
            self._prefix = undefined
            self._uri = String(val)
      else:
         self._prefix = String()
         self._uri = String()

   def toString(self):
      return self.uri

   def valueOf(self):
      return self.uri


class QName(Object):
   @property
   def localName(self):
      return self._localName

   @property
   def uri(self):
      return self._uri

   def __init__(self, *args):
      self._uri = null
      if len(args) >= 2:
         uri = args[0]
         localName = args[1]
         if isinstance(uri, Namespace):
            self._uri = uri.uri
         elif uri is not null:
            self._uri = String(uri)
         if isinstance(localName, QName):
            self._localName = localName.localName
         else:
            self._localName = String(localName)
      elif len(args):
         qname = args[0]
         if isinstance(qname, QName):
            self._localName = qname.localName
            self._uri = qname.uri
         elif qname is undefined or qname is null:
            self._localName = String()
         else:
            self._localName = String(qname)
      else:
         self._localName = String()

   def toString(self):
      if self.uri == '':
         return self.localName
      elif self.uri is null:
         return '*::%s' % self.localName
      return '%s::%s' % (self.uri, self.localName)

   def valueOf(self):
      return self


class XMLList(Object):
   # TODO: Check to see if any of these functions should return a flattened list
   def __init__(self, value):
      self._value = Array()
      ...

   def attribute(self, attributeName):
      res = Array()
      for i in each(self._value):
         j = i.attributes(attributeName)
         if j.length() > 0:
            res.append(j)
      return XMLList(res)

   def attributes(self):
      return XMLList([i.attributes() for i in each(self._value)])

   def child(self, propertyName):
      return XMLList([i.child(propertyName) for i in each(self._value)])

   def children(self):
      return XMLList([i.children() for i in each(self._value)])

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
      obj = Object()
      obj.ignoreComments = true
      obj.ignoreProcessingInstructions = true
      obj.ignoreWhitespace = true
      obj.prettyIndent = int(2)
      obj.prettyPrinting = true
      return obj

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
   def setSettings(rest = null):
      if rest is null:
         rest = XML.defaultSettings()
      if 'ignoreComments' in rest:
         XML.ignoreComments = rest.ignoreComments
      if 'ignoreProcessingInstructions' in rest:
         XML.ignoreProcessingInstructions = rest.ignoreProcessingInstructions
      if 'ignoreWhitespace' in rest:
         XML.ignoreWhitespace = rest.ignoreWhitespace
      if 'prettyIndent' in rest:
         XML.prettyIndent = rest.prettyIndent
      if 'prettyPrinting' in rest:
         XML.prettyPrinting = rest.prettyPrinting

   @staticmethod
   def settings():
      obj = Object()
      obj.ignoreComments = XML.ignoreComments
      obj.ignoreProcessingInstructions = XML.ignoreProcessingInstructions
      obj.ignoreWhitespace = XML.ignoreWhitespace
      obj.prettyIndent = XML.prettyIndent
      obj.prettyPrinting = XML.prettyPrinting
      return obj

   def text(self):...
   def toString(self):...
   def toXMLString(self):...

   def valueOf(self):
      return self
