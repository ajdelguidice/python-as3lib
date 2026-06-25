from as3lib import Array, Boolean, false, null, Object


class XMLNode(Object):
    @property
    def attributes(self):
        raise NotImplementedError

    @attributes.setter
    def attributes(self, value):
        raise NotImplementedError

    @property
    def childNodes(self):
        return self._cNodes

    @property
    def firstChild(self):
        raise NotImplementedError

    @firstChild.setter
    def firstChild(self, value):
        raise NotImplementedError

    @property
    def lastChild(self):
        raise NotImplementedError

    @lastChild.setter
    def lastChild(self, value):
        raise NotImplementedError

    @property
    def localName(self):
        raise NotImplementedError

    @property
    def namespaceURI(self):
        raise NotImplementedError

    @property
    def nextSibling(self):
        raise NotImplementedError

    @nextSibling.setter
    def nextSibling(self, value):
        raise NotImplementedError

    @property
    def nodeName(self):
        raise NotImplementedError

    @nodeName.setter
    def nodeName(self, value):
        raise NotImplementedError

    @property
    def nodeType(self):
        raise NotImplementedError

    @nodeType.setter
    def nodeType(self, value):
        raise NotImplementedError

    @property
    def nodeValue(self):
        raise NotImplementedError

    @nodeValue.setter
    def nodeValue(self, value):
        raise NotImplementedError

    @property
    def parentNode(self):
        raise NotImplementedError

    @parentNode.setter
    def parentNode(self, value):
        raise NotImplementedError

    @property
    def prefix(self):
        raise NotImplementedError

    @property
    def previousSibling(self):
        raise NotImplementedError

    @previousSibling.setter
    def previousSibling(self, value):
        raise NotImplementedError

    def __init__(self, type, value):
        self._cNodes = Array()
        raise NotImplementedError

    def appendChild(self, node):
        raise NotImplementedError

    def cloneNode(self, deep):
        raise NotImplementedError

    def getNamespaceForPrefix(self, prefix):
        raise NotImplementedError

    def getPrefixForNamespace(self, ns):
        raise NotImplementedError

    def hasChildNodes(self):
        return Boolean(self._cNodes.length)

    def insertBefore(self, node, before):
        raise NotImplementedError

    def removeNode(self):
        raise NotImplementedError

    def toString(self):
        raise NotImplementedError


class XMLDocument(XMLNode):
    @property
    def docTypeDecl(self):
        raise NotImplementedError

    @docTypeDecl.setter
    def docTypeDecl(self, value):
        raise NotImplementedError

    @property
    def idMap(self):
        raise NotImplementedError

    @idMap.setter
    def idMap(self, value):
        raise NotImplementedError

    @property
    def ignoreWhite(self):
        return self._ignoreWhite

    @ignoreWhite.setter
    def ignoreWhite(self, value):
        raise NotImplementedError

    @property
    def xmlDecl(self):
        raise NotImplementedError

    @xmlDecl.setter
    def xmlDecl(self, value):
        raise NotImplementedError

    def __init__(self, source=null):
        self._ignoreWhite = false
        raise NotImplementedError

    def createElement(self, name):
        raise NotImplementedError

    def createTextNode(self, text):
        raise NotImplementedError

    def parseXML(self, source):
        raise NotImplementedError

    def toString(self):
        raise NotImplementedError


class XMLNodeType(Object):
    ELEMENT_NODE = 1
    TEXT_NODE = 3
