<h1>python-as3lib</h1>
A partial implementation of ActionScript3 and adobe flash in python. This project aims to have as accurate of an implementation as possible of the stuff that I choose to implement, however, due to my limited knowledge of advanced programming and Adobe's subpar documentation, this might not be completely accurate. Some stuff will be impossible to implement in python because <a href="https://docs.python.org/3/glossary.html#term-global-interpreter-lock">python is a fish</a>.
<br><br><b>Warning:</b> Some early versions of this library that contain the config module are very broken on Windows and can cause major issues. This was fixed in version 0.0.6.
<br><br><b>If you are using wayland, this library will have a first time init message because wayland does not currently support easily fetching some values automatically (without systemd, I do not want to depend on that). You must either launch this library, or the program that uses it, from the terminal to input these values, or fill out the blank config file that I provide on github (it will lock up otherwise).</b> These values are stored in &lt;library-directory&gt;/wayland.cfg. They only need to be accurate if you are using the graphical elements of this library. I will not be able to fix the window grouping jank on wayland until tcl/tk natively supports wayland.
<h3>Requirements</h3>
System:
<br>&emsp;Linux:
<br>&emsp;&emsp;bash (or a bash compatible shell)
<br>&emsp;&emsp;echo
<br>&emsp;&emsp;grep
<br>&emsp;&emsp;xwininfo (xorg)
<br>&emsp;&emsp;xrandr (xorg)
<br>&emsp;&emsp;awk
<br>&emsp;&emsp;loginctl (This requirement will probably be removed later, this was just the easiest way to do things)
<br>&emsp;&emsp;whoami
<br>&emsp;Windows:
<br>&emsp;&emsp;PyLaucher (should be included in the python installer)
<br>Python:
<br>&emsp;Built-in:
<br>&emsp;&emsp;tkinter, re, math, io, platform, subprocess, random, time, datetime, os, pwd (linux), pathlib, configparser, webbrowser, textwrap, typing
<br>&emsp;External:
<br>&emsp;&emsp;<a href="https://pypi.org/project/numpy">numpy</a>, <a href="https://pypi.org/project/Pillow">Pillow</a>, <a href="https://pypi.org/project/tkhtmlview">tkhtmlview</a>
<h3>Modules</h3>
There are currently 16 modules plus a parser (doesn't work yet. If you actually need something like that, you should probably be using <a href="https://ruffle.rs">ruffle</a> instead) in this library, toplevel, interface_tk, keyConversions, configmodule, initconfig, com.adobe, flash.ui, flash.display, flash.filesystem, flash.utils, flash.events, flash.display3D, flash.net, flash.crypto, flash.system, and flash.errors.
<br>Using "from as3lib import *" currently imports everything from the toplevel module with int renamed to Int so it doesn't conflict with python's int.
<h4>directory: cfail<h4>
This directory contains all of the backup modules for when the c modules fail to compile. These are used instead of them.
<h4>toplevel</h4>
Most of this is implemented, however there are probably a lot of inconsistencies with how things work due to terrible documentation. Please open an issue on the github if you find something that you know is wrong. For functions which have multiple interpretations from the documentation, I added an arguement called "interpretation" which is an integer that specifies which one you want.
<h4>interface_tk</h4>
Interface library for testing purposes written in tkinter. I will likely keep this around once the real interface stuff is implemented but no promises.
<br><b>Warning:</b> This is a testing library, do not expect consistancy between versions.
<h4>keyConversions</h4>
This module includes cross-platform key conversion functions for tkinter events, javascript (actionscript) keycodes, and mouse buttons (currently only supports united states standard keyboard on linux and windows). <b>This will be moved later since flash has a place for it.</b>
<h4>configmodule</h4>
The module that holds all of the things that this library needs globally or that need to be used many times so I only have to fetch them once while it is running. This module includes information like;
<br>the current platform
<br>the library directory
<br>library debug status
<br>the config for the trace function loaded from mm.cfg
<br>details about the screen (width, hight, refresh rate, and color depth) for the display module.
<br>information about the filesystem (path separator, user directory, desktop directory, and documents directory) for the flash.filesystem module
<br>library initialization status and errors
<h4>initconfig</h4>
The module that is called when this library initializes with the sole purpose of setting the variables in configmodule.
<br>Note: use of multiple displays has not been tested yet.
<h4>flash.cryto</h4>
This module only has one function in it, generateRandomBytes. It uses a c module on unix but python code on windows because windows cryptography is extremely complicated and painful. On anything but windows, this requires /dev/urandom and C99's dynamic array length assignment (creating as array with the length specified by a variable), however, if they aren't present, python code will be used instead.
<h4>com.adobe, flash.ui, flash.display, flash.filesystem, flash.utils, flash.events, flash.display3D, flash.net, flash.cryto, flash.system, and flash.errors</h4>
These modules contain things from their respective actionscript modules. None of them are complete yet since many actionscript modules rely on each other to function. I have to go back and forth between modules coding things here and there so these are taking much longer than the other modules.
<h3>Config Files</h3>
<b>&lt;library-directory&gt;/mm.cfg</b> - this file is the same as it was in actionscript with the same options as defined <a href="https://web.archive.org/web/20180227100916/helpx.adobe.com/flash-player/kb/configure-debugger-version-flash-player.html">here</a> with the exception of "ClearLogsOnStartup" which I added to configure what it says. Its defualt value is 1 to match the behavior in actionscript.
<br><br><b>&lt;library-directory&gt;/wayland.cfg</b> - generated on the first use of this library if you are using wayland. Stores all of the values that can't be fetched automatically (without systemd) so you only have to input them once. They must be changed manually if you want to change them.
