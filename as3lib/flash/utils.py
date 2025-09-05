import as3lib as as3
import as3lib.flash.net as fn
from as3lib.flash.events import EventDispatcher, TimerEvent
from as3lib.flash import errors
from as3lib import metaclasses
from threading import Timer as timedExec
from miniamf.amf3 import ByteArray as _ByteArray
from as3lib import as3state
from datetime import datetime
from miniamf import util

#dummy classes
class ByteArray:...


def clearInterval():...
def clearTimeout():...
def describeType():...
def escapeMultiByte():...
def getDefinitionByName():...
def getQualifiedClassName():...
def getQualifiedSuperclassName():...
def getTimer():
   return int(util.get_timestamp(datetime.now()) * 1000) - as3state.startTime
def setInterval():...
def setTimeout():...
def unescapeMultiByte():...

class IDataInput:...
class IDataOutput:...

class ByteArray(_ByteArray):
   def __getBytesAvailable(self):
      return self.remaining()
   bytesAvailable=property(fget=__getBytesAvailable)
   defaultObjectEncoding = 3 # This can be set globally
   def __getEndian(self):
      return super().endian
   def __setEndian(self,endian):
      super().endian = endian
   endian=property(fget=__getEndian,fset=__setEndian)
   def __getLength(self):
      return len(self)
   def __setLength(self,value:int):...
   length=property(fget=__getLength,fset=__setLength)
   def __getPosition(self):
      return self.tell()
   def __setPosition(self,value):
      self.seek(value)
   position=property(fget=__getPosition,fset=__setPosition)
   def __getSharable(self):
      return self.__sharable
   def __setSharable(self,value:bool):
      self.__sharable = value
   shareable=property(fget=__getSharable,fset=__setSharable)
   def __init__(self,data=None):
      super().__init__(data)
      self.objectEncoding = ByteArray.defaultObjectEncoding # This currently does nothing
   def __repr__(self):
      return f"ByteArray({self.getvalue()})"
   def atomicCompareAndSwapIntAt(self,byteIndex:int,expectedValue:int,newValue:int):
      if byteIndex % 4 != 0 or byteIndex < 0:
         as3.ArguementError('ByteArray.atomicCompareAndSwapIntAt; byteIndex must be a multiple of 4 and can not be negative.')
      ...
   def atomicCompareAndSwapLength(self,expectedLength:int,newLength:int):
      """
      In a single atomic operation, compares this byte array's length with a provided value and, if they match, changes the length of this byte array.

      This method is intended to be used with a byte array whose underlying memory is shared between multiple workers (the ByteArray instance's shareable property is true). It does the following:

         1) Reads the integer length property of the ByteArray instance
         2) Compares the length to the value passed in the expectedLength argument
         3) If the two values are equal, it changes the byte array's length to the value passed as the newLength parameter, either growing or shrinking the size of the byte array
         4) Otherwise, the byte array is not changed

      All these steps are performed in one atomic hardware transaction. This guarantees that no operations from other workers make changes to the contents of the byte array during the compare-and-resize operation.

      Parameters
         expectedLength:int — the expected value of the ByteArray's length property. If the specified value and the actual value match, the byte array's length is changed.      
         newLength:int — the new length value for the byte array if the comparison succeeds
      Returns
         int — the previous length value of the ByteArray, regardless of whether or not it changed 
      """
      oldlen = self.length
      if self.length == expectedLength:
         self.length = newLength
      return oldlen
   def clear(self):
      "Clears the contents of the byte array and resets the length and position properties to 0. Calling this method explicitly frees up the memory used by the ByteArray instance."
      self.truncate(0)
   def compress(self,algorithm:str):
      if algorithm != "zlib":
         raise NotImplemented('The underlying stream currently only supports zlib compression.')
      self.compressed = True
   def deflate():...
   def inflate():...
   def readBytes(self,bytes:ByteArray,offset=0,length=0):
      bytes.seek(offset)
      bytes.write(self.read(length))
   def toJSON(self,k:str):
      """
      Provides an overridable method for customizing the JSON encoding of values in an ByteArray object.

      The JSON.stringify() method looks for a toJSON() method on each object that it traverses. If the toJSON() method is found, JSON.stringify() calls it for each value it encounters, passing in the key that is paired with the value.

      ByteArray provides a default implementation of toJSON() that simply returns the name of the class. Because the content of any ByteArray requires interpretation, clients that wish to export ByteArray objects to JSON must provide their own implementation. You can do so by redefining the toJSON() method on the class prototype.

      The toJSON() method can return a value of any type. If it returns an object, stringify() recurses into that object. If toJSON() returns a string, stringify() does not recurse and continues its traversal.

      Parameters
         k:String — The key of a key/value pair that JSON.stringify() has encountered in its traversal of this object

      Returns
         * — The class name string. 
      """
      return "ByteArray"
   def toString(self):...
   def uncompress(self,algorithm:str):
      if algorithm != "zlib":
         raise NotImplemented('The underlying stream currently only supports zlib compression.')
      self.compressed = False
   def writeBytes(self,bytes:ByteArray,offset=0,length=0):
      startpos = bytes.tell()
      bytes.seek(offset)
      self.write(bytes.read(length))
      bytes.seek(startpos) #!I don't know if it is supposed to do this

class CompressionAlgorithm(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   DEFLATE = "deflate"
   LZMA = "lzma"
   ZLIB = "zlib"
class Dictionary(dict):
   def __init__(self,weakKeys:as3.allBoolean=False):
      return super().__init__()
   def __getitem__(self,item):
      return self.get(item) #I think this is how actionscript does it but I'm not sure
   def toJSON(self,k:str):
      return "Dictionary"
class Endian(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   BIG_ENDIAN = "bigEndian"
   LITTLE_ENDIAN = "littleEndian"
class Timer(EventDispatcher):
   def __getCCount(self):
      return self.__currentCount
   currentCount=property(fget=__getCCount)
   def __getDelay(self):
      return self.__delay
   def __setDelay(self,number_ms:as3.allNumber):
      if self.running:
         self.stop()
         self.__delay = number_ms
         self.start()
      else:
         self.__delay = number_ms
   delay=property(fget=__getDelay,fset=__setDelay)
   def __getRCount(self):
      return self.__repeatCount
   def __setRCount(self,number:as3.allInt):
      self.__repeatCount = number
   repeatCount=property(fget=__getRCount,fset=__setRCount)
   def __getRunning(self):
      return self.__running
   running=property(fget=__getRunning)
   def __TimerTick(self):
      self.__currentCount += 1
      self.dispatchEvent(self.timer)
      if self.currentCount >= self.repeatCount:
         self.dispatchEvent(self.timerComplete)
      else:
         self.__timer = timedExec(self.delay/1000,self.__TimerTick)
         self.__timer.start()
   def __init__(self,delay:as3.allNumber,repeatCount:as3.allInt=0):
      super().__init__()
      self.__currentCount = 0
      self.__delay = delay
      self.repeatCount = repeatCount
      self.__running = False
      self.timer = TimerEvent("timer",False,False,self)
      self.timerComplete = TimerEvent("timerComplete",False,False,self)
   def reset(self):
      self.stop()
      self.__currentCount = 0
   def start(self):
      if not self.running:
         self.__timer = timedExec(self.delay/1000,self.__TimerTick)
         self.__running = True
         self.__timer.start()
   def stop(self):
      if self.running:
         self.__timer.cancel()
         self.__running = False
