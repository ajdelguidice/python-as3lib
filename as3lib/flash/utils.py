from as3lib import toplevel as as3
from as3lib.flash import net as fn
from typing import Union
import binascii

#dummy classes
class ByteArray:...


def clearInterval():
   pass
def clearTimeout():
   pass
def describeType():
   pass
def escapeMultiByte():
   pass
def getDefinitionByName():
   pass
def getQualifiedClassName():
   pass
def getQualifiedSuperclassName():
   pass
def getTimer():
   pass
def setInterval():
   pass
def setTimeout():
   pass
def unescapeMultiByte():
   pass

class IDataInput:
   pass
class IDataOutput:
   pass

class ByteArray:
   #!Does position advance on read/write?
   __slots__ = ("__defObjEncode","__ObjEncode","__value")
   def __getBytesAvailable(self):
      return self.length - self.position
   bytesAvailable=property(fget=__getBytesAvailable)
   def __getDefObjectEncoding(self):
      return self.__defObjEncode
   def __setDefObjectEncoding(self,value):
      if value in (fn.ObjectEncoding.AMF0,fn.ObjectEncoding.AMF3):
         self.__defObjEncode = value
   defaultObjectEncoding=property(fget=__getDefObjectEncoding,fset=__setDefObjectEncoding)
   def __getEndian(self):
      return Endian.BIG_ENDIAN #!placeholder
   def __setEndian(self):...
   endian=property(fget=__getEndian,fset=__setEndian)
   def __getLength(self):
      return len(self.__value)
   def __setLength(self,value:int):
      if value > self.length:
         for i in range(value-self.length):
            self.__value += b"\x00"
      elif value < self.length:
         self.__value = self.__value[:-(self.length-value)]
   length=property(fget=__getLength,fset=__setLength)
   def __getObjectEncoding(self):
      return self.__ObjEncode
   def __setObjectEncoding(self,value):
      if value in (fn.ObjectEncoding.AMF0,fn.ObjectEncoding.AMF3):
         self.__ObjEncode = value
   objectEncoding=property(fget=__getObjectEncoding,fset=__setObjectEncoding)
   def __getPosition(self):
      return self.__position
   def __setPosition(self,value):
      #!Add error when out of range
      if value >= 0 and value <= self.length:
         self.__position = value
   position=property(fget=__getPosition,fset=__setPosition)
   def __getSharable(self):
      return self.__sharable
   def __setSharable(self,value:bool):
      self.__sharable = value
   shareable=property(fget=__getSharable,fset=__setSharable)
   def __init__(self):
      self.__value = bytearray()
      self.defaultObjectEncoding = fn.ObjectEncoding.AMF3
      self.objectEncoding = self.defaultObjectEncoding
   def __len__(self):
      return self.length
   def __getitem__(self,item):
      #!Possibly do str(binascii.hexlify(self.__value[item]))[2:-1]
      return hex(self.__value[item])[2:]
   def __setitem__(self,item,value):
      #Must be a hex value as a string
      if type(value) in (bytearray,bytes,ByteArray) and len(value) == 1:
         self.__value[item] = int(binascii.hexlify(value),16)
      else:
         self.__value[item] = int(value,16)
   def __str__(self):
      return str(binascii.hexlify(self.__value))[2:-1]
   def __repr__(self):
      return f"ByteArray({str(binascii.hexlify(self.__value))[2:-1]})"
   def atomicCompareAndSwapIntAt():
      pass
   def atomicCompareAndSwapLengthAt():
      pass
   def clear(self):
      self.position = 0
      self.__value = bytearray()
   def compress():
      pass
   def deflate():
      pass
   def inflate():
      pass
   def readBoolean(self):
      if self.__value[self.position] == "\x00":
         return False
      return True
   def readByte(self):
      return int(self.__value[self.position],16)-128
   def readBytes():
      pass
   def readDouble():
      pass
   def readInt():
      pass
   def readMultiByte():
      pass
   def readObject():
      pass
   def readShort():
      pass
   def readUnsignedByte():
      pass
   def readUnsignedInt():
      pass
   def readUnsignedShort():
      pass
   def readUTF():
      pass
   def readUTFBytes():
      pass
   def toJSON():
      pass
   def toString(self):
      """
      Converts the byte array to a string. If the data in the array begins with a Unicode byte order mark, the application will honor that mark when converting to a string. If System.useCodePage is set to true, the application will treat the data in the array as being in the current system code page when converting
      """
      return str(binascii.hexlify(self.__value))[2:-1]
   def uncompress():
      pass
   def __ConvBoolToByte(self,value:bool):
      if value != None:
         if value:
            return "01"
         return "00"
   def writeBoolean(self,value:bool):
      self[self.position] = __ConvBoolToByte(value)
   def writeByte():
      pass
   def writeBytes():
      pass
   def writeDouble():
      pass
   def writeFloat():
      pass
   def writeInt():
      pass
   def writeMultiByte():
      pass
   def writeObject():
      pass
   def writeShort():
      pass
   def writeUnsignedInt():
      pass
   def writeUTF():
      pass
   def writeUTFBytes():
      pass
class CompressionAlgorithm:
   DEFLATE = "deflate"
   LZMA = "lzma"
   ZLIB = "zlib"
class Dictionary:
   pass
class Endian:
   BIG_ENDIAN = "bigEndian"
   LITTLE_ENDIAN = "littleEndian"
class Timer:
   pass
