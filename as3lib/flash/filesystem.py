from as3lib import Array, Boolean, as3state, Object, String
from as3lib.flash.events import EventDispatcher
from as3lib.flash.net import FileReference
from subprocess import CalledProcessError, check_output


class File(FileReference):
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
        super().__init__()
        self._filepath = path

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
