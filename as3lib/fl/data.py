from as3lib import null, Object, uint
from as3lib.flash.events import EventDispatcher


class DataProvider(EventDispatcher):
   @property
   def length(self):
      raise NotImplementedError

   def __init__(self, value: Object = null):
      ...

   def addItem(self, item: Object):
      raise NotImplementedError

   def addItemAt(self, item: Object, index: uint):
      raise NotImplementedError

   def addItems(self, items: Object):
      raise NotImplementedError

   def addItemsAt(self, items: Object, index: uint):
      raise NotImplementedError

   def clone(self):
      raise NotImplementedError

   def concat(self, items: Object):
      raise NotImplementedError

   def getItemAt(self, index: uint):
      raise NotImplementedError

   def getItemIndex(self, item: Object):
      raise NotImplementedError

   def invalidate(self):
      raise NotImplementedError

   def invalidateItem(self, item: Object):
      raise NotImplementedError

   def invalidateItemAt(self, index: uint):
      raise NotImplementedError

   def merge(self, newData: Object):
      raise NotImplementedError

   def removeAll(self):
      raise NotImplementedError

   def removeItem(self, item: Object):
      raise NotImplementedError

   def removeItemAt(self, index: uint):
      raise NotImplementedError

   def replaceItem(self, newItem: Object, oldItem: Object):
      raise NotImplementedError

   def replaceItemAt(self, newItem: Object, index: uint):
      raise NotImplementedError

   def sort(self, *sortArgs):
      raise NotImplementedError

   def sortOn(self, fieldName: Object, options: Object = null):
      raise NotImplementedError

   def toArray(self):
      raise NotImplementedError

   def toString(self):
      raise NotImplementedError


class SimpleCollectionItem(Object):
   @property
   def data(self):
      return self._data

   @data.setter
   def data(self, value):
      self._data = String(value)

   @property
   def label(self):
      return self._label

   @label.setter
   def label(self, value):
      self._label = String(value)

   def __init__(self):
      self._data = String()
      self._label = String()


class TileListCollectionItem(Object):
   @property
   def label(self):
      return self._label

   @label.setter
   def label(self, value):
      self._label = String(value)

   @property
   def source(self):
      return self._source

   @source.setter
   def source(self, value):
      self._source = String(value)

   def __init__(self):
      self._label = String()
      self._source = String()
