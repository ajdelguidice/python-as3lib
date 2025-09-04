import as3lib.toplevel as as3
from typing import Union
from as3lib.flash.events import Event, EventDispatcher #, HTTPStatusEvent, IOErrorEvent, PermissionEvent, ProgressEvent, SecurityErrorEvent, DataEvent
from as3lib import metaclasses, as3state
from tkinter import filedialog
import as3lib.flash.utils as utils
from miniamf import sol
import miniamf

def getClassByAlias(aliasName:str):
   try:
      return miniamf.get_class_alias(aliasName)
   except miniamf.UnknownClassAlias:
      as3.ReferenceError(f'Alias {aliasName} was not registered.')
def navigateToURL(request,window:str=None):...
def registerClassAlias(aliasName:str,classObject):
   if aliasName == None or classObject == None:
      as3.TypeError('Arguements to registerClassAlias can not be null.')
      pass
   miniamf.register_class(classObject,aliasName)
def sendToURL(request):...

class DatagramSocket:...
class FileFilter:
   def __init__(self,description:Union[str,as3.String],extension:Union[str,as3.String],macType:Union[str,as3.String]=None):
      self.description = description
      self.extension = extension
      self.macType = macType
   def extensionsToArray(self):
      return as3.Array(*self.extension.split(";"))
   def macTypeToArray(self):
      if self.macType != None:
         return as3.Array(*self.macType.split(";"))
   def toTkTuple(self):
      return (self.description,self.extension.split(";"))
class FileReference(EventDispatcher):
   @staticmethod
   def _getPerStat():
      return True
   permissionStatus = property(fget=_getPerStat)
   def __init__(self):
      super().__init__()
      #self.creationDate
      #self.creator
      #self.data
      #self.extension
      #self.modificationDate
      #self.name
      #self.size
      #self.type
      self._location = None
      #!Most of these events need extra information
      self.cancel = Event("cancel",False,False,self)
      self.complete = Event("complete",False,False,self)
      #self.httpResponseStatus = HTTPStatusEvent("httpResponseStatus",False,False,self)
      #self.httpStatus = HTTPStatusEvent("httpStatus",False,False,self)
      #self.ioError = IOErrorEvent("ioError",False,False,self)
      self.open = Event("open",False,False,self)
      #self.permissionStatus = PermissionEvent("permissionStatus",False,False,self)
      #self.progress = ProgressEvent("progress",False,False,self)
      #self.securityError = SecurityErrorEvent("securityError",False,False,self)
      self.select = Event("select",False,False,self)
      #self.uploadCompleteData = DataEvent("uploadCompleteEvent",False,False,self)
   def _setFile(self,file):
      #Sets the file and all of its details
      ...
   def browse(self,typeFilter:Union[as3.Array,list,tuple]=None):
      #typeFilter is an Array/list/tuple of FileFilter objects
      if typeFilter != None:
         filename = filedialog.askopenfilename(title="Select a file to upload",filetypes=tuple(i.toTkTuple() for i in typeFilter))
      else:
         filename = filedialog.askopenfilename(title="Select a file to upload")
      try:
         return True
      except:
         print("You somhow messed it up")
      finally:
         if filename in (None,()):
            self.dispatchEvent(self.cancel)
         else:
            self.dispatchEvent(self.select)
   def cancel(self):...
   def dowload(self,request,defaultFileName=None):...
   def load(self):...
   def requestPermission(self):...
   def save(self,data,defaultFileName=None):
      #!add check for blacklisted characters  / \ : * ? " < > | %
      file = defaultFileName.split(".")
      savetype = 0 # 1=UTF-8 2=XML 3=ByteArray
      if data == None:
         as3.ArguementError("Invalid Data")
         return False
      elif isinstance(data,str):
         #write a UTF-8 text file
         savetype = 1
      #elif type(data) == #XML:
         #Write as xml format text file with format preserved
         #savetype = 2
      elif isinstance(data,utils.ByteArray):
         #write data to file as is (in byte form)
         savetype = 3
      else:
         #convert to string and save as text file. If it fails throw ArguementError
         try:
            data = str(data)
         except:
            as3.ArguementError("Invalid Data")
            return False
      if len(file) == 1:
         #no extension
         filename = filedialog.asksaveasfilename(title="Select location for download")
      else:
         #extension
         #!doesn't seen to work
         ext = f".{file[-1]}"
         filename = filedialog.asksaveasfilename(title="Select location for download",defaultextension=ext)
      try:
         return True
      except:
         print("You somhow messed it up")
      finally:
         if filename in (None,()):
            self.dispatchEvent(self.cancel)
         else:
            self.dispatchEvent(self.select)
            self._location = filename
            self.dispatchEvent(self.complete)
   def upload(self,request,uploadDataFieldName,testUpload=False):...
   def uploadUnencoded(self,request):...
class FileReferenceList:...
class GroupSpecifier:...
class InterfaceAddress:
   #address = classmethod()
   #broadcast = classmethod()
   def __getAddrType():...
   #ipVersion = classmethod(fget=__AddrType)
   #prefixLength = classmethod()
class IPVersion(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   IPV4 = "IPv4"
   IPV6 = "IPv6"
class LocalConnection:...
class NetGroup:...
class NetGroupInfo:...
class NetGroupReceiveMode:...
class NetGroupReplicationStrategy:...
class NetGroupSendMode:...
class NetGroupSendResult:...
class NetMonitor:...
class NetStream:...
class NetStreamAppendBytesAction:...
class NetStreamInfo:...
class NetStreamMulticastInfo:...
class NetStreamPlayOptions:...
class NetStreamPlayTransitions:...
class NetworkInfo:...
class NetworkInterface:...
class ObjectEncoding(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   AMF0 = 0
   AMF3 = 3
   DEFAULT = 3
class Responder:...
class SecureSocket:...

class SharedObject(dict):
   #! Make this a child of EventDispatcher
   #! Implement remote shared objects
   defaultObjectEncoding = 3 #This can be set globally
   def __getSize(self):
      return len(sol.encode(self._name,self['data'],encoding=self.objectEncoding))
   size=property(fget=__getSize)
   def __getData(self):
      return self['data']
   data=property(fget=__getData)
   def __init__(self):
      self.objectEncoding = SharedObject.defaultObjectEncoding
      super().__init__()
      self._name = None
      self._path = None
      self['data'] = {}
   def clear(self):
      self._path.unlink(missing_ok=True)
      self['data'].clear()
   def close(self):...
   def connect(self):...
   def flush(self,minDiskSpace=0):
      with self._path.open('wb+') as f:
         f.write(sol.encode(self._name,self['data'],encoding=self.objectEncoding).getvalue())
      ...
      return SharedObjectFlushStatus.FLUSHED
   @staticmethod
   def getLocal(name,localPath=None,secure=False):
      #gets local shared object; if object exists, set path and load it. if not, just set path
      #localPath is relative to as3state.appdatadirectory
      if as3state.appdatadirectory == None:
         as3.Error('Application specific data directory was not set. Can not safely determine location.')
         pass
      obj = SharedObject()
      if localPath == None:
         path = as3state.appdatadirectory
      else:
         path = as3state.appdatadirectory / localPath
      obj._name = name
      obj._path = path / f'{name}.sol'
      if obj._path.is_file():
         with obj._path.open('rb') as f:
            obj['data'] = dict(sol.load(f))
      return obj
   @staticmethod
   def getRemote(self,name,remotePath=None,persistance=False,secure=False):...
   def send(self,*arguments):...
   def setDirty(self,propertyName):...
   def setProperty(self,propertyName,value=None):...
class SharedObjectFlushStatus(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   FLUSHED = "flushed"
   PENDING = "pending"
class Socket:...
class URLLoader:...
class URLLoaderDataFormat:...
class URLRequest:...
class URLRequestDefaults:...
class URLRequestHeader:...
class URLRequestMethod:...
class URLStream:...
class URLVariables:...
class XMLSocket:...

if __name__ == "__main__":
   def eventCancel(event=None):
      print("cancel")
   def eventSelect(event=None):
      print("select")
   def eventComplete(event=None):
      print("complete")
   filter1 = FileFilter("Text File","*.txt")
   filter2 = FileFilter("Shell Script","*.sh")
   filter3 = FileFilter("Files","*.xml;*.exe;*.py")
   fr = FileReference()
   fr.addEventListener(Event.CANCEL,eventCancel)
   fr.addEventListener(Event.SELECT,eventSelect)
   fr.addEventListener(Event.COMPLETE,eventComplete)
   fr.browse([filter1,filter2,filter3])
   fr.save("test","test.txt")
