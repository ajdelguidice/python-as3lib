from __future__ import annotations
from as3lib import Error, Object
from as3lib.flash.display import NativeMenu, NativeMenuItem, Stage
from as3lib.flash.events import ContextMenuEvent


class ContextMenu(NativeMenu):
    @property
    def builtInItems(self):
        raise NotImplementedError

    @builtInItems.setter
    def builtInItems(self, value: ContextMenuBuiltInItems):
        raise NotImplementedError

    @property
    def clipboardItems(self):
        raise NotImplementedError

    @clipboardItems.setter
    def clipboardItems(self, value: ContextMenuClipboardItems):
        raise NotImplementedError

    @property
    def clipboardMenu(self):
        raise NotImplementedError

    @clipboardMenu.setter
    def clipboardMenu(self, value):
        raise NotImplementedError

    @property
    def customItems(self):
        raise NotImplementedError

    @customItems.setter
    def customItems(self, value):
        raise NotImplementedError

    @property
    def isSupported(self):
        raise NotImplementedError

    @property
    def items(self):
        raise NotImplementedError

    @items.setter
    def items(self, value):
        raise NotImplementedError

    @property
    def link(self):
        raise NotImplementedError

    @link.setter
    def link(self, value):
        raise NotImplementedError

    @property
    def numItems(self):
        raise NotImplementedError

    def __init__(self):
        # TODO: Restrict number of custom items to 15
        super().__init__()
        self.menuSelect = ContextMenuEvent('menuSelect')
        ...

    def addItemAt(self, item: NativeMenuItem, index):
        raise NotImplementedError

    def clone(self):
        raise NotImplementedError

    def containsItem(self, item: NativeMenuItem):
        raise NotImplementedError

    def display(self, stage: Stage, stageX, stageY):
        raise NotImplementedError

    def getItemAt(self, index):
        raise NotImplementedError

    def getItemIndex(self, item: NativeMenuItem):
        raise NotImplementedError

    def hideBuiltInItems(self):
        raise NotImplementedError

    def removeAllItems(self):
        raise NotImplementedError

    def removeItemsAt(self, index):
        raise NotImplementedError


class ContextMenuBuiltInItems(Object):
    @property
    def forwardAndBack(self):
        return self._forwardAndBack

    @forwardAndBack.setter
    def forwardAndBack(self, value):
        self._forwardAndBack = value

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value):
        self._loop = value

    @property
    def play(self):
        return self._play

    @play.setter
    def play(self, value):
        self._play = value

    @property
    def print(self):
        return self._print

    @print.setter
    def print(self, value):
        self._print = value

    @property
    def quality(self):
        return self._quality

    @quality.setter
    def quality(self, value):
        self._quality = value

    @property
    def rewind(self):
        return self._rewind

    @rewind.setter
    def rewind(self, value):
        self._rewind = value

    @property
    def save(self):
        return self._save

    @save.setter
    def save(self, value):
        self._save = value

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, value):
        self._zoom = value

    def __init__(self):
        self._forwardAndBack = True
        self._loop = True
        self._play = True
        self._print = True
        self._quality = True
        self._rewind = True
        self._save = True
        self._zoom = True


class ContextMenuClipboardItems(Object):
    @property
    def clear(self):
        return self._clear

    @clear.setter
    def clear(self, value):
        self._clear = value

    @property
    def copy(self):
        return self._copy

    @copy.setter
    def copy(self, value):
        self._copy = value

    @property
    def cut(self):
        return self._cut

    @cut.setter
    def cut(self, value):
        self._cutm = value

    @property
    def paste(self):
        return self._paste

    @paste.setter
    def paste(self, value):
        self._paste = value

    @property
    def selectAll(self):
        return self._selectAll

    @selectAll.setter
    def selectAll(self, value):
        self._selectAll = value

    def __init__(self):
        self._clear = True
        self._copy = True
        self._cut = True
        self._paste = True
        self._selectAll = True


class ContextMenuItem(NativeMenuItem):
    @property
    def caption(self):
        return self._caption

    @caption.setter
    def caption(self, value):
        '''
        TODO:
        Each caption must contain at least one visible character.
        Control characters, newlines, and other white space characters are ignored.
        Captions that are identical to any built-in menu item, or to another custom item, are ignored, whether the matching item is visible or not. Menu captions are compared to built-in captions or existing custom captions without regard to case, punctuation, or white space.
        '''
        # Captions can not be more than 100 characters long.
        if len(value) > 100:
            raise Error('Captions can not be more than 100 characters long.')
        # Restricted captions
        if value in {'Save', 'Zoom In', 'Zoom Out', '100%', 'Show All', 'Quality', 'Play', 'Loop', 'Rewind', 'Forward', 'Back', 'Movie not loaded', 'About', 'Print', 'Show Redraw Regions', 'Debugger', 'Undo', 'Cut', 'Copy', 'Paste', 'Delete', 'Select All', 'Open', 'Open in new window', 'Copy link'}:
            raise Error(f'Caption "{value}" is not allowed.')
        # Restricted phrases
        if value.find('Adobe') != -1 or value.find('Macromedia') != -1 or value.find('Flash Player') != -1 or value.find('Settings') != -1:
            raise Error(f'Caption {value} contains a restricted phrase.')
        self._caption = value

    @property
    def separatorBefore(self):
        return self._separatorBefore

    @separatorBefore.setter
    def separatorBefore(self, value):
        self._separatorBefore = value

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value

    def __init__(self, caption, separatorBefore=False, enabled=True, visible=True):
        super().__init__('')
        self.menuItemSelect = ContextMenuEvent('menuItemSelect')
        self._caption = None
        self.caption = caption
        self._separatorBefore = separatorBefore
        self._enabled = enabled
        self._visible = visible

    def clone(self):
        raise NotImplementedError

    @staticmethod
    def systemClearMenuItem():
        raise NotImplementedError

    @staticmethod
    def systemCopyLinkMenuItem():
        raise NotImplementedError

    @staticmethod
    def systemCopyMenuItem():
        raise NotImplementedError

    @staticmethod
    def systemCutMenuItem():
        raise NotImplementedError

    @staticmethod
    def systemOpenLinkMenuItem():
        raise NotImplementedError

    @staticmethod
    def systemPasteMenuItem():
        raise NotImplementedError

    @staticmethod
    def systemSelectAllMenuItem():
        raise NotImplementedError


class GameInput:
    ...


class GameInputControl:
    ...


class GameInputDevice:
    ...


class Keyboard:
    ...


class KeyboardType:
    ...


class KeyLocation:
    ...


class Mouse:
    ...


class MouseCursor(Object):
    ARROW = 'arrow'
    AUTO = 'auto'
    BUTTON = 'button'
    HAND = 'hand'
    IBEAM = 'ibeam'


class MouseCursorData:
    ...


class Multitouch:
    ...


class MultitouchInputMode:
    ...
