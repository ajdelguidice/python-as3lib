from as3lib import Array, as3state, Boolean, false, null, Object, String
from as3lib.flash.events import EventDispatcher
from as3lib.flash.net import FileReference
from as3lib.helpers import staticproperty
import os
from subprocess import CalledProcessError, check_output


class File(FileReference):
    @staticproperty
    def applicationDirectory(cls):
        raise NotImplementedError

    @staticproperty
    def applicationStorageDirectory(cls):
        raise NotImplementedError

    @staticproperty
    def cacheDirectory(cls):
        raise NotImplementedError

    @staticproperty
    def desktopDirectory(cls):
        return File(as3state.desktopdirectory)

    @staticproperty
    def documentsDirectory(cls):
        return File(as3state.documentsdirectory)

    @property
    def download(self):
        raise NotImplementedError

    @download.setter
    def download(self, value):
        raise NotImplementedError

    @property
    def exists(self):
        return Boolean(os.path.exists(self._path))

    @property
    def icon(self):
        raise NotImplementedError

    @property
    def isDirectory(self):
        return Boolean(os.path.isdir(self._path))

    @property
    def isHidden(self):
        raise NotImplementedError

    @property
    def isPackage(self):
        # MacOS specific feature
        if as3state.platform == 'Darwin':
            raise NotImplementedError
        return false

    @property
    def isSymbolicLink(self):
        return Boolean(os.path.isjunction(self._path) or os.path.islink(self._path))

    @staticproperty
    def lineEnding(cls):
        if as3state.platform == 'Windows':
            return String('\r\n')
        return String('\n')

    @property
    def nativePath(self):
        raise NotImplementedError

    @nativePath.setter
    def nativePath(self, value):
        raise NotImplementedError

    # parent
    @property
    def parent(self):
        return File(os.path.dirname(self._path))

    @staticproperty
    def permissionStatus(cls):
        raise NotImplementedError

    @property
    def preventBackup(self):
        raise NotImplementedError

    @preventBackup.setter
    def preventBackup(self, value):
        raise NotImplementedError

    @staticproperty
    def separator(cls):
        if as3state.platform == 'Windows':
            return String('\\')
        return String('/')

    @property
    def spaceAvailable(self):
        raise NotImplementedError

    @staticproperty
    def systemCharset(cls):
        raise NotImplementedError

    @property
    def url(self):
        raise NotImplementedError

    @url.setter
    def url(self, value):
        raise NotImplementedError

    @staticproperty
    def userDirectory(cls):
        return File(as3state.userdirectory)

    def __init__(self, path: String = null):
        # TODO: detect url path
        # TODO: convert path to native path and url
        # TODO: Throw exception ArguementError if path is invalid
        super().__init__()
        self._path = os.path.abspath(path)

    def __repr__(self):
        return f'File("{self._path}")'

    def browseForDirectory(self, title: String):
        raise NotImplementedError

    def browseForOpen(self, title: String, typeFilter: Array = null):
        raise NotImplementedError

    def browseForOpenMultiple(self, title: String, typeFilter: Array = null):
        raise NotImplementedError

    def browseForSave(self, title: String):
        raise NotImplementedError

    def cancel(self):
        raise NotImplementedError

    def canonicalize(self):
        raise NotImplementedError

    def clone(self):
        raise NotImplementedError

    def copyTo(self, newLocation: FileReference, overwrite: Boolean = false):
        raise NotImplementedError

    def copyToAsync(self, newLocation: FileReference,
                    overwrite: Boolean = false):
        raise NotImplementedError

    def createDirectory(self):
        raise NotImplementedError

    def createTempDirectory(self):
        raise NotImplementedError

    def createTempFile(self):
        raise NotImplementedError

    def deleteDirectory(self, deleteDirectoryContents: Boolean = false):
        raise NotImplementedError

    def deleteDirectoryAsync(self, deleteDirectoryContents: Boolean = false):
        raise NotImplementedError

    def deleteFile(self):
        raise NotImplementedError

    def deleteFileAsync(self):
        raise NotImplementedError

    def getDirectoryListing(self):
        raise NotImplementedError

    def getDirectoryListingAsync(self):
        raise NotImplementedError

    def getRelativePath(self, ref: FileReference, useDotDot: Boolean = false):
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

    def moveTo(self, newLocation: FileReference, overwrite: Boolean = false):
        raise NotImplementedError

    def moveToAsync(self, newLocation: FileReference,
                    overwrite: Boolean = false):
        raise NotImplementedError

    def moveToTrash(self):
        raise NotImplementedError

    def moveToTrashAsync(self):
        raise NotImplementedError

    def openWithDefaultApplication(self):
        raise NotImplementedError

    def requestPermission(self):
        raise NotImplementedError

    def resolvePath(self, path: String):
        raise NotImplementedError


class FileMode(Object):
    APPEND = "append"
    READ = "read"
    UPDATE = "update"
    WRITE = "write"


class FileStream(EventDispatcher):
    @property
    def bytesAvailable(self):
        raise NotImplementedError

    @property
    def endian(self):
        raise NotImplementedError

    @endian.setter
    def endian(self, value):
        raise NotImplementedError

    @property
    def objectEncoding(self):
        raise NotImplementedError

    @objectEncoding.setter
    def objectEncoding(self, value):
        raise NotImplementedError

    @property
    def position(self):
        raise NotImplementedError

    @position.setter
    def position(self, value):
        raise NotImplementedError

    @property
    def readAhead(self):
        raise NotImplementedError

    @readAhead.setter
    def readAhead(self, value):
        raise NotImplementedError

    def __init__(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def open(self, file, fileMode):
        raise NotImplementedError

    def openAsync(self, file, fileMode):
        raise NotImplementedError

    def readBoolean(self):
        raise NotImplementedError

    def readByte(self):
        raise NotImplementedError

    def readBytes(self, bytes, offset=0, length=0):
        raise NotImplementedError

    def readDouble(self):
        raise NotImplementedError

    def readFloat(self):
        raise NotImplementedError

    def readInt(self):
        raise NotImplementedError

    def readMultiByte(self, length, charSet):
        raise NotImplementedError

    def readObject(self):
        raise NotImplementedError

    def readShort(self):
        raise NotImplementedError

    def readUnsignedByte(self):
        raise NotImplementedError

    def readUnsignedInt(self):
        raise NotImplementedError

    def readUnsignedShort(self):
        raise NotImplementedError

    def readUTF(self):
        raise NotImplementedError

    def readUTFBytes(self, length):
        raise NotImplementedError

    def truncate(self):
        raise NotImplementedError

    def writeBoolean(self, value):
        raise NotImplementedError

    def writeByte(self, value):
        raise NotImplementedError

    def writeBytes(self, bytes, offset=0, length=0):
        raise NotImplementedError

    def writeDouble(self, value):
        raise NotImplementedError

    def writeFloat(self, value):
        raise NotImplementedError

    def writeInt(self, value):
        raise NotImplementedError

    def writeMultiByte(self, value, charSet):
        raise NotImplementedError

    def writeObject(self, object):
        raise NotImplementedError

    def writeShort(self, value):
        raise NotImplementedError

    def writeUnsignedInt(self, value):
        raise NotImplementedError

    def writeUTF(self, value):
        raise NotImplementedError

    def writeUTFBytes(self, value):
        raise NotImplementedError


class StorageVolume(Object):
    @property
    def drive(self):
        raise NotImplementedError

    @property
    def fileSystemType(self):
        raise NotImplementedError

    @property
    def isRemoveable(self):
        raise NotImplementedError

    @property
    def isWritable(self):
        raise NotImplementedError

    @property
    def name(self):
        raise NotImplementedError

    @property
    def rootDirectory(self):
        raise NotImplementedError

    def __init__(self, rootDirPath: File, name: String, writable: Boolean,
                 removeable: Boolean, fileSysType: String, drive: String):
        raise NotImplementedError


class StorageVolumeInfo(EventDispatcher):
    # isSupported
    # storageVolumeInfo
    def getStorageVolumes(self):
        raise NotImplementedError
