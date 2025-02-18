<h1>python-as3lib</h1>
A partial implementation of ActionScript3 and adobe flash in python. This project aims to have as accurate of an implementation as possible of the stuff that I choose to implement, however, due to my limited knowledge of advanced programming and Adobe's subpar documentation, this might not be completely accurate. Some stuff will be impossible to implement in python because <a href="https://docs.python.org/3/glossary.html#term-global-interpreter-lock">python is a fish</a>. The toplevel stuff is mostly implemented but it is very slow at the moment, everything else is hit or miss.
<h3>Notes</h3>
If you need acuracy, use <a href="https://ruffle.rs">ruffle</a> instead. This is mostly a porting library and is developed by one person.
<br>Versions of this library before 0.0.6 are broken on windows.
<br>There is an init message the first time this library is loaded when using wayland (linux). This is not something that I can fix as I'm currently not using a graphical toolkit that allows for information to be gotten automatically. These values are stored in &lt;library-directory&gt;/wayland.cfg and only need to be accurate if you need to have a graphical interface.
<br>Use of multiple displays has not been tested yet.
<br>interface_tk is a testing library, it does not have anything from actionscript and is only there to work things out. Do not expect consistency between versions and do not expect it to be kept around.
<br>Using "from as3lib import *" currently imports everything from the toplevel module with int renamed to Int so it doesn't conflict with python's int.
<h3>Requirements</h3>
Linux:
<br>&emsp;a posix compatible shell, echo, grep, awk, loginctl, whoami
<br>&emsp;(xorg): xwininfo, xrandr
<br>Windows:
<br>&emsp;PyLaucher
<br>Python built-ins:
<br>&emsp;tkinter, re, math, io, platform, subprocess, random, time, datetime, os, pwd (linux), pathlib, configparser, webbrowser, textwrap, typing
<br>Python external:
<br>&emsp;<a href="https://pypi.org/project/numpy">numpy</a>, <a href="https://pypi.org/project/Pillow">Pillow</a>, <a href="https://pypi.org/project/tkhtmlview">tkhtmlview</a>
<h3>Config Files</h3>
<b>&lt;library-directory&gt;/mm.cfg</b> - this file is the same as it was in actionscript with the same options as defined <a href="https://web.archive.org/web/20180227100916/helpx.adobe.com/flash-player/kb/configure-debugger-version-flash-player.html">here</a> with the exception of "ClearLogsOnStartup" which I added to configure what it says. Its defualt value is 1 to match the behavior in actionscript.
<br><br><b>&lt;library-directory&gt;/wayland.cfg</b> - generated on the first use of this library if you are using wayland. Stores all of the values that can't be fetched automatically (without systemd) so you only have to input them once. They must be changed manually if you want to change them.
