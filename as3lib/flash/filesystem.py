from as3lib import Array, as3state, metaclasses
from subprocess import CalledProcessError, check_output


class File:
   # applicationDirectory
   # applicationStorageDirectory
   # cacheDirectory
   # desktopDirectory
   # documentsDirectory
   # downloaded
   # exists
   # icon
   # isDirectory
   # isHidden
   # isPackage
   # isSymbolicLink
   # lineEnding
   # nativePath
   # parent
   # permissionStatus
   # separator
   # spaceAvailable
   # systemCharset
   # url
   # userDirectory
   def __init__(self, path: str):
      # TODO: detect url path
      # TODO: convert path to native path and url
      # TODO: Throw exception ArguementError if path is invalid
      self._filepath = path

   def __str__(self):
      return self.toString()

   def browseForDirectory():
      raise NotImplementedError

   def browseForOpen():
      raise NotImplementedError

   def browseForOpenMultiple():
      raise NotImplementedError

   def browseForSave():
      raise NotImplementedError

   def cancel():
      raise NotImplementedError

   def canonicalize():
      raise NotImplementedError

   def clone():
      raise NotImplementedError

   def copyTo():
      raise NotImplementedError

   def copyToAsync():
      raise NotImplementedError

   def createDirectory():
      raise NotImplementedError

   def createTempDirectory():
      raise NotImplementedError

   def createTempFile():
      raise NotImplementedError

   def deleteDirectory():
      raise NotImplementedError

   def deleteDirectoryAsync():
      raise NotImplementedError

   def deleteFile():
      raise NotImplementedError

   def deleteFileAsync():
      raise NotImplementedError

   def getDirectoryListing():
      raise NotImplementedError

   def getDirectoryListingAsync():
      raise NotImplementedError

   def getRelativePath():
      raise NotImplementedError

   @staticmethod
   def getRootDirectories():
      # TODO: Make windows function better
      if as3state.platform == 'Windows':
         tempDrives = Array()
         for i in check_output(('fsutil', 'fsinfo', 'drives')).decode('utf-8').strip('\r\n').split(' ')[1:]:
            i = i.strip('\\')
            if i == '':
               continue
            try:
               check_output(('fsutil', 'fsinfo', 'volumeinfo', i))  # This requires admin permissions on the main drive
               tempDrives.push(File(i))
            except CalledProcessError as e:
               if 'not ready' in e.output.decode('utf-8'):
                  continue
               tempDrives.push(File(i))
         return tempDrives
      elif as3state.platform in {'Linux', 'Darwin'}:
         return Array(File('/'))

   def moveTo():
      raise NotImplementedError

   def moveToAsync():
      raise NotImplementedError

   def moveToTrash():
      raise NotImplementedError

   def moveToTrashAsync():
      raise NotImplementedError

   def openWithDefaultApplication():
      raise NotImplementedError

   def requestPermission():
      raise NotImplementedError

   def resolvePath():
      raise NotImplementedError

   def toString():
      raise NotImplementedError


class FileMode(metaclass=metaclasses._AS3_CONSTANTSOBJECT):
   APPEND = "append"
   READ = "read"
   UPDATE = "update"
   WRITE = "write"


class FileStream:...


class StorageVolume:...


class StorageVolumeInfo:...
