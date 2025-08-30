"""
Note to self: remove all of the things that could change outside of this library
    Display stuff should not change (as defined by the actionscript documentation)
"""
platform = "" #Windows, Linux, or Darwin
displayserver = "" #linux (x11 or wayland) or darwin (x11 or native) only
librarydirectory = "" #full path to as3lib (this library)
pythonversion = "" #version of python currently running
interfaceType = "" #type of interface (Tkinter, or whatever else I decide to use)

#Global config
_cfg = None #DO NOT EDIT THIS. This is for determining if the config needs to be saved.
hasDependencies = False
addedFeatures = False #Enables features added by this library.
flashVersion = (32,0,0,371) #this currently doesn't do anything [majorVersion,minorVersion,buildNumber,internalBuildNumber]
ErrorReportingEnable = False #State of error reporting
MaxWarnings = 100 #Maximum number of warnings until they are suppressed
TraceOutputFileEnable = False #Determines whether to output "trace" to a file or to the console
TraceOutputFileName = "" #File path where error messages are stored if TraceOutputFileEnable is True
ClearLogsOnStartup = True #If True, clears logs on startup. This is the default behavior in flash
width = "" #maximum width of the display window (not implemented yet)
height = "" #maximum height of the display window (not implemented yet)
refreshrate = "" #refresh rate of the display window (not implemented yet)
colordepth = "" #color depth of the display window (not implemented yet)

#toplevel
as3DebugEnable = False #State of debug mode
CurrentWarnings = 0 #Current number of warnings
MaxWarningsReached = False #If the maximum number of warnings has been reached
defaultTraceFilePath_Flash = "" #Default file path for trace output in flash
appdatadirectory = None #The path to the application specific data directory (must be set by the application, should not be set by other libraries)

#flash.display
windows = {} #dictionary containing all of the defined windows (not implemented yet)

#flash.filesystem
separator = ""
userdirectory = ""
desktopdirectory = ""
documentsdirectory = ""

#initcheck
initdone = False #variable to make sure this module has initialized
initerror = [] #[(errcode:int,errdesc:str),...]
