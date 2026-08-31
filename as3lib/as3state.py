'''
Note to self: remove all of the things that could change outside of this library
    Display stuff should not change (as defined by the actionscript documentation)
'''
__version__ = 13

platform = None  # Windows, Linux, or Darwin
displayserver = None  # x11 or wayland (linux), x11 or native (darwin)
librarydirectory = None  # full path to as3lib (this library)
startTime = None  # logs start time for flash.utils.getTimer
nativeApplication = None  # The native application instance for the running application
audioDeviceManager = None  # The singleton for flash.media.AudioDeviceManager

# Main file header information (Default values are placeholders)
swfVersion = 44
frameRate = 30
viewportWidth = 200
viewportHeight = 200

# Global config
_cfg = None  # DO NOT EDIT THIS. This is for determining if the config needs to be saved.
hasDependencies = False
addedFeatures = False  # Enables features added by this library.
flashVersion = (32, 0, 0, 371)  # This currently doesn't do anything [majorVersion,minorVersion,buildNumber,internalBuildNumber]
ErrorReportingEnable = False  # Enables logging of errors (console output seems to always be active in the debugger)
MaxWarnings = 100  # Number of warnings to log before stopping.
TraceOutputFileEnable = False  # Enables trace logging (console output is always be active in the debugger)
TraceOutputFileName = None  # Path to the log

# toplevel
as3DebugEnable = False  # State of debug mode
CurrentWarnings = 0  # Current number of warnings
MaxWarningsReached = False  # If the maximum number of warnings has been reached
appdatadirectory = None  # The path to the application specific data directory
prototypes = {}  # Each class needs a global default instance of itself. Store it here

# flash.filesystem
separator = None
_user = None  # Name of the currect user.
userdirectory = None
desktopdirectory = None
documentsdirectory = None

# flash.utils
intervals = {}  # Storage for timers set by setInterval and setTimeout

# initcheck
initdone = False  # Variable to make sure this module has initialised
initerror = []  # List of errors that happened during initialisation
