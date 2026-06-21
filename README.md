# python-as3lib

A partial implementation of ActionScript 3 and the adobe flash api in python. This project is developed for the purpose of making game porting easier and is currently developed by one person.

## Notes

- If you want to run an swf files, use <a href="https://ruffle.rs">ruffle</a> instead.
- Some stuff will be impossible to implement in python because <a href="https://docs.python.org/3/glossary.html#term-global-interpreter-lock">python is a fish</a>.
- Undocumented things can not be implemented unless I am informed about them.
- Versions of this library before 6 are broken on windows.
- Use of multiple displays has not been tested yet.
- interface_tk is a testing module, it does not function like actionscript and is only there to work things out. Do not expect consistency between versions and do not expect it to be kept around.
- The toplevel module is now deprecated and only remains for backwards compatibility. Import the library instead.

## Requirements

> <a href="https://pypi.org/project/numpy">numpy</a>
> <br><a href="https://pypi.org/project/Pillow">Pillow</a>
> <br><a href="https://pypi.org/project/tkhtmlview">tkhtmlview</a>
> <br><a href="https://pypi.org/project/tomli/">tomli</a> (python < 3.11)
> <br><a href="https://pypi.org/project/as3lib-miniAMF/">as3lib-miniAMF</a>

Windows specific<br>
> PyLaucher
> <br> <a href="https://pypi.org/project/pywin32/">pywin32</a>

## Config Files

<b>&lt;library-directory&gt;/as3lib.toml</b> - This library's config file. This includes mm.cfg. Old config files will only be migrated if this file does not exist or if "migrateOldConfig" is set to true. Setting "migrateOldConfig" to true will overwrite the values in this config file with the ones found in the old config files.

<b>&lt;library-directory&gt;/mm.cfg</b> - Migration path for adobe flash player <a href="https://web.archive.org/web/20180227100916/helpx.adobe.com/flash-player/kb/configure-debugger-version-flash-player.html">mm.cfg</a>. Only used on first run or if "migrateOldConfig" is true in as3lib.toml.

<b><u>DEPRECATED</u> &lt;library-directory&gt;/as3lib.cfg</b> - The config file used by version 11.

<b><u>DEPRECATED</u> &lt;library-directory&gt;/wayland.cfg</b> - Generated on versions before 11 to hold the values that can not be fetched automatically on wayland (linux).

## License

as3lib is licensed under the <a href="https://opensource.org/license/MIT">MIT License</a>, however some parts are under a different license. These are:
- as3lib/tests. Most of these tests are based on tests from <a href="https://github.com/ruffle-rs/ruffle">ruffle</a> and are only modified to make them run in python. They are under their original license (Apache 2.0 or MIT) which is located in [otherlicenses/LICENSE-ruffle.md](otherlicenses/LICENSE-ruffle.md)
