import tkinter
from tkinter import filedialog
from tkinter.ttk import Combobox, Notebook
import tkhtmlview
import PIL
from io import BytesIO
import as3lib as as3
try:
   from as3lib import cmath
except:
   from as3lib.cfail import cmath
from as3lib import helpers, as3state
from as3lib._toplevel.Errors import *
"""
Temporary interface to get things working. A bit slow when too many things are defined. Even after this module is no longer needed, it will probably stay for compatibility purposes.
Notes:
- Canvas is not supported yet even though there is an option for it
- When setting commands, they must be accessible from the scope of where they are called
- When grouping windows together, the object that should be used is <windowobject>.children["root"]
- If using wayland, windows made using tkinter.Tk() will not group with windows made using tkinter.Toplevel(). This will hopefully be fixed if the ext-zones protocol is merged (tcl/tk would have to support it as well).
"""

as3state.interfaceType = "Tkinter"

def help():
   print("If you are confused about how to use this module, please run this module by itself and look at the test code at the bottom. This is more of a test module so don't expect it to make any sense.")

class ComboEntryBox:
   __slots__ = ("_properties","labels","entries","frame","button")
   def __init__(self,master,x,y,width,height,anchor,font,textwidth,buttonwidth,text:list|tuple|str|as3.String|as3.Array,buttontext="Ok",rows=1,textalign="w"):
      self._properties = {"x":x,"y":y,"width":width,"height":height,"anchor":anchor,"font":font,"textwidth":textwidth,"buttonwidth":buttonwidth,"text":text,"buttontext":buttontext,"rows":rows,"textalign":textalign}
      self.labels = []
      self.entries = []
      self.frame = tkinter.Frame(master)
      if rows < 1:
         raise Exception(f"ComboEntryBox; rows must be greater than or equal to 1, got {rows}")
      if rows == 1:
         self.frame.place(x=x,y=y,width=width,height=height,anchor=anchor)
         self.frame.configure(borderwidth=0,highlightthickness=0)
         if isinstance(text,str):
            self.labels.append(tkinter.Label(self.frame,text=text,font=font,anchor=textalign))
         else:
            self.labels.append(tkinter.Label(self.frame,text=text[0],font=font,anchor=textalign))
         self.labels[0].place(x=0-2,y=0,width=textwidth+2,height=height,anchor="nw")
         self.entries.append(tkinter.Entry(self.frame,font=font))
         self.entries[0].place(x=textwidth,y=0,width=width-(textwidth+buttonwidth),height=height,anchor="nw")
         self.button = tkinter.Button(self.frame,text=buttontext,font=font)
         self.button.place(x=textwidth+(width-(textwidth+buttonwidth)),y=0,width=buttonwidth,height=height,anchor="nw")
      else:
         self.frame.place(x=x,y=y,width=width,height=(height*rows),anchor=anchor)
         self.frame.configure(borderwidth=0,highlightthickness=0)
         if isinstance(text,str):
            for i in range(rows):
               self.labels.append(tkinter.Label(self.frame,text=text,font=font,anchor=textalign))
               self.labels[i].place(x=0-2,y=i*height,width=textwidth+2,height=height,anchor="nw")
         else:
            for i in range(rows):
               self.labels.append(tkinter.Label(self.frame,text=text[i],font=font,anchor=textalign))
               self.labels[i].place(x=0-2,y=i*height,width=textwidth+2,height=height,anchor="nw")
         for i in range(rows):
            self.entries.append(tkinter.Entry(self.frame,font=font))
            self.entries[i].place(x=textwidth,y=i*height,width=width-(textwidth+buttonwidth),height=height,anchor="nw")
         self.button = tkinter.Button(self.frame,text=buttontext,font=font)
         self.button.place(x=textwidth+(width-(textwidth+buttonwidth)),y=(rows-1)*height,width=buttonwidth,height=height,anchor="nw")
   def __resizeandplace(self):
      w = self._properties["width"]
      h = self._properties["height"]
      tw = self._properties["textwidth"]
      bw = self._properties["buttonwidth"]
      r = self._properties["rows"]
      self.frame.place(x=self._properties["x"],y=self._properties["y"],width=w,height=(h*r),anchor=self._properties["anchor"])
      for i in range(r):
         self.labels[i].place(x=0-2,y=i*h,width=tw+2,height=h,anchor="nw")
         self.entries[i].place(x=tw,y=i*h,width=w-(tw+bw),height=h,anchor="nw")
      self.button.place(x=tw+(w-(tw+bw)),y=(r-1)*h,width=bw,height=h,anchor="nw")
   def configure(self,**kwargs):
      for attr,value in kwargs.items():
         if attr in {"x","y","anchor"}:
            self._properties[attr] = value
            self.frame.place(x=self._properties["x"],y=self._properties["y"],width=self._properties["width"],height=self._properties["height"],anchor=self._properties["anchor"])
         elif attr in {"width","height","textwidth","buttonwidth"}:
            self._properties[attr] = value
            self.__resizeandplace()
         elif attr == "font":
            self._properties["font"] = value
            for j in range(self._properties["rows"]):
               self.labels[j].configure(font=value)
               self.entrys[j].configure(font=value)
            self.button.configure(font=value)
         elif attr == "text":
            if isinstance(value,(str,list,tuple)):
               self._properties["text"] = value
               if isinstance(value,str):
                  for j in range(self._properties["rows"]):
                     self.labels[j].configure(text=value)
               else:
                  for j in range(self._properties["rows"]):
                     self.labels[j].configure(text=value[j])
         elif attr == "buttontext":
            self._properties["buttontext"] = value
            self.button.configure(text=value)
         elif attr == "command":
            self.button.configure(command=value)
         elif attr == "rows":
            print("Changing number of rows not implemented yet.")
         elif attr == "textalign":
            print("Changing text alignment not implemented yet.")
         else:
            for i in {self.frame,self.label,self.entry,self.button}:
               i[attr] = value
   def configurePlace(self,**kwargs):
      for i in (set(kwargs.keys()) & {"x","y","width","height","anchor","textwidth","buttonwidth"}):
         self._properties[i] = kwargs[i]
      self.__resizeandplace()
   def getEntry(self,number,*args):
      return self.entries[number].get()
   def getEntries(self,*args):
      return [i.get() for i in self.entries]
   def destroy(self):
      self.frame.destroy()
   def _getBackground(self):
      return self['background']
   def _setBackground(self, color):
      self['background'] = color
   background = property(fset=_setBackground,fget=_getBackground)
   def _getForeground(self):
      return self['foreground']
   def _setForeground(self, color):
      self['foreground'] = color
   foreground = property(fset=_setForeground,fget=_getForeground)

def _nullProp(*args):...

class itkBaseWidget:
   _intName = None  # This is to replace the class name from childproperties
   def __init__(self, klass, master, **kwargs):
      self._x = kwargs.pop('x',None)
      self._y = kwargs.pop('y',None)
      self._width = kwargs.pop('width',None)
      self._height = kwargs.pop('height',None)
      self._anchor = kwargs.pop('anchor','nw')
      tempfont = kwargs.pop('font',('TkTextFont',12,''))
      self._font = tempfont[0]
      self._fontSize = tempfont[1]
      self._fontStyle = tempfont[2] if len(tempfont) == 3 else ''
      self._window = kwargs.pop('itkWindow',None)
      klass.__init__(self, master, **kwargs)
   def update(self):
      nm = self._window.properties['nm']
      self.place(x=self._x*nm,y=self._y*nm,width=self._width*nm,height=self._height*nm,anchor=self._anchor)
   def updateText(self):
      self['font'] = (self._font,cmath.resizefont(self._fontSize,self._window.properties['mult']),self._fontStyle)
   def resize(self):
      self.update()
      self.updateText()
   background = property(fset=_nullProp,fget=_nullProp)
   foreground = property(fset=_nullProp,fget=_nullProp)
   text = property(fset=_nullProp,fget=_nullProp)
   bold = property(fset=_nullProp,fget=_nullProp)
   border = property(fset=_nullProp,fget=_nullProp)
   def _getFont(self):
      return (self._font,self._fontSize,self._fontStyle)
   def _setFont(self, font):
      self._font = tempfont[0]
      self._fontSize = tempfont[1]
      self._fontStyle = tempfont[2] if len(tempfont) == 3 else None
      self.updateText()
   font = property(fset=_setFont,fget=_getFont)
   def _getX(self):
      return self._x
   def _setX(self, x):
      self._x = x
      self.update()
   x = property(fset=_setX,fget=_getX)
   def _getY(self):
      return self._y
   def _setY(self, y):
      self._y = y
      self.update()
   y = property(fset=_setY,fget=_getY)
   def _getWidth(self):
      return self._width
   def _setWidth(self, w):
      self._width = w
      self.update()
   width = property(fset=_setWidth,fget=_getWidth)
   def _getHeight(self):
      return self._height
   def _setHeight(self, h):
      self._height = h
      self.update()
   height = property(fset=_setHeight,fget=_getHeight)
   def _getAnchor(self):
      return self._anchor
   def _setAnchor(self, a):
      self._anchor = a
      self.update()
   anchor = property(fset=_setAnchor,fget=_getAnchor)
   mult = property(fset=_nullProp,fget=_nullProp)

class itkFrame(itkBaseWidget, tkinter.Frame):
   _intName = 'Frame'
   def __init__(self, master=None, **kwargs):
      itkBaseWidget.__init__(self, tkinter.Frame, master, **kwargs)
   def updateText(self):...
   def _getBackground(self):
      return self['bg']
   def _setBackground(self, color):
      self['bg'] = color
   background = property(fset=_setBackground,fget=_getBackground)
   font = property(fset=_nullProp,fget=_nullProp)
   
class itkLabel(itkBaseWidget, tkinter.Label):
   _intName = 'Label'
   def __init__(self, master=None, **kwargs):
      itkBaseWidget.__init__(self, tkinter.Label, master, **kwargs)
   def _getBackground(self):
      return self['background']
   def _setBackground(self, color):
      self['background'] = color
   background = property(fset=_setBackground,fget=_getBackground)
   def _getForeground(self):
      return self['foreground']
   def _setForeground(self, color):
      self['foreground'] = color
   foreground = property(fset=_setForeground,fget=_getForeground)
   def _getText(self):
      return self['text']
   def _setText(self, text):
      self['text'] = text
   text = property(fset=_setText,fget=_getText)

class itknwhLabel(itkLabel):
   _intName = 'nwhLabel'
   def update(self):
      nm = self._window.properties['nm']
      self.place(x=self._x*nm,y=self._y*nm,anchor=self._anchor)
   width = property(fset=_nullProp,fget=_nullProp)
   height = property(fset=_nullProp,fget=_nullProp)

class itkButton(itkBaseWidget, tkinter.Button):
   _intName = 'Button'
   def __init__(self, master=None, **kwargs):
      itkBaseWidget.__init__(self, tkinter.Button, master, **kwargs)
   def _getBackground(self):
      return self['background']
   def _setBackground(self, color):
      self['background'] = color
   background = property(fset=_setBackground,fget=_getBackground)
   def _getForeground(self):
      return self['foreground']
   def _setForeground(self, color):
      self['foreground'] = color
   foreground = property(fset=_setForeground,fget=_getForeground)
   def _getText(self):
      return self['text']
   def _setText(self, text):
      self['text'] = text
   text = property(fset=_setText,fget=_getText)

class itkHTMLScrolledText(itkBaseWidget, tkhtmlview.HTMLScrolledText):
   _intName = 'HTMLScrolledText'
   def __init__(self, master=None, **kwargs):
      self._sbscaling = kwargs.pop('sbscaling',True)
      self._sbwidth = kwargs.pop('sbwidth',12)
      self._text = kwargs.pop('text','')
      itkBaseWidget.__init__(self, tkhtmlview.HTMLScrolledText, master, **kwargs)
      self._bold = False
      self._textCache = ''
      self._border = False
   def update(self):
      nm = self._window.properties['nm']
      if self._sbscaling:
         self.vbar["width"] = self._sbwidth*nm
      self.place(x=self._x*nm,y=self._y*nm,width=self._width*nm,height=self._height*nm,anchor=self._anchor)
   def updateText(self):
      self['state'] = 'normal'
      temp = ('<b>','</b>') if self.bold else ('','')
      self.set_html(f'{temp[0]}<pre style="color: {self.foreground}; background-color: {self.background}; font-size: {cmath.resizefont(self._fontSize,self._window.properties["mult"])}px; font-family: {self._font}">{self._textCache}</pre>{temp[1]}')
      self["state"] = "disabled"
   def _getBackground(self):
      return self['background']
   def _setBackground(self, color):
      self['background'] = color
      self.updateText()
   background = property(fset=_setBackground,fget=_getBackground)
   def _getForeground(self):
      return self['foreground']
   def _setForeground(self, color):
      self['foreground'] = color
      self.updateText()
   foreground = property(fset=_setForeground,fget=_getForeground)
   def _getText(self):
      return self._text
   def _setText(self, text):
      if self._text != text:
         self._text = text
         self._textCache = text.replace("\t","    ")
      self.updateText()
   text = property(fset=_setText,fget=_getText)
   def _getBold(self):
      return self._bold
   def _setBold(self, value):
      self._bold = value
      self.updateText()
   bold = property(fset=_setBold,fget=_getBold)
   def _getBorder(self):
      return self._border
   def _setBorder(self, value:bool):
      self._border = value
      if value:
         self.configure(borderwidth=1,highlightthickness=1)
      else:
         self.configure(borderwidth=0,highlightthickness=0)
   border = property(fset=_setBorder,fget=_getBorder)
   def _getFont(self):
      return (self._font,self._fontSize)
   def _setFont(self, font):
      self._font, self._fontSize = font
      self.updateText()
   font = property(fset=_setFont,fget=_getFont)
   def _getSBScaling(self):
      return self._sbscaling
   def _setSBScaling(self, value):
      self._sbscaling = value
      self.update()
   sbscaling = property(fset=_setSBScaling,fget=_getSBScaling)
   def _getSBWidth(self):
      return self._sbwidth
   def _setSBWidth(self, value):
      self._sbwidth = value
      self.update()
   sbwidth = property(fset=_setSBWidth,fget=_getSBWidth)
   def destroy(self):
      super().destroy()
      self.frame.destroy()

class itkEntry(itkBaseWidget, tkinter.Entry):
   _intName = 'Entry'
   def __init__(self, master=None, **kwargs):
      if 'textvariable' in kwargs:
         self._text = kwargs.pop('textvariable')
      else:
         self._text = tkinter.StringVar()
      itkBaseWidget.__init__(self, tkinter.Entry, master, textvariable=self._text, **kwargs)
   def _getBackground(self):
      return self['background']
   def _setBackground(self, color):
      self['insertbackground'] = color
      self['background'] = color
   background = property(fset=_setBackground,fget=_getBackground)
   def _getForeground(self):
      return self['foreground']
   def _setForeground(self, color):
      self['foreground'] = color
   foreground = property(fset=_setForeground,fget=_getForeground)
   def _getText(self):
      return self._text.get()
   def _setText(self, text):
      self._text.set(text)
   text = property(fset=_setText,fget=_getText)

class itkNotebook(itkBaseWidget, Notebook):
   _intName = 'Notebook'
   def __init__(self, master=None, **kwargs):
      itkBaseWidget.__init__(self, Notebook, master, **kwargs)
   def update(self):
      if self._x != None and self._y != None and self._width != None and self._height != None:
         nm = self._window.properties['nm']
         self.place(x=self._x*nm,y=self._y*nm,width=self._width*nm,height=self._height*nm,anchor=self._anchor)
      else:
         self.pack(expand=True)
   def updateText(self):...
   def _getBackground(self):
      return self['background']
   def _setBackground(self, color):
      self['background'] = color
   background = property(fset=_setBackground,fget=_getBackground)
   def _getForeground(self):
      return self['foreground']
   def _setForeground(self, color):
      self['foreground'] = color
   foreground = property(fset=_setForeground,fget=_getForeground)

class itkNBFrame(itkFrame):
   _intName = 'NBFrame'
   def update(self):
      nm = self._window.properties['nm']
      self["width"] = self._width*nm
      self["height"] = self._height*nm
   x = property(fset=_nullProp,fget=_nullProp)
   y = property(fset=_nullProp,fget=_nullProp)
   anchor = property(fset=_nullProp,fget=_nullProp)

class itkImageLabel(itkLabel):
   _intName = 'ImageLabel'
   def __init__(self, master, **kwargs):
      temp = kwargs.pop('image_name','')
      itkLabel.__init__(self, master, **kwargs)
      self._imgname = ''
      self.image_name = temp
   def updateText(self):
      self["image"] = self._window.images[self._imgname].img
   def _getImgName(self):
      return self._imgname
   def _setImgName(self, name):
      if name in self._window.images:
         if self._imgname != '':
            self._window.images[self._imgname].references -= 1
         self._imgname = name
         self["image"] = self._window.images[name].img
         self._window.images[name].references += 1
   image_name = property(fset=_setImgName,fget=_getImgName)

#----------------------------------------------------
#This section contains code that is a modification of code from tkhtmlview
class ScrolledListbox(tkinter.Listbox):
   # Uses HTMLScrolledText as a reference but uses a listbox instead of HTMLText
   def __init__(self, master=None, **kwargs):
      self.frame = tkinter.Frame(master)
      self.vbar = tkinter.Scrollbar(self.frame)

      kwargs["yscrollcommand"] = self.vbar.set
      self.vbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
      self.vbar["command"] = self.yview

      tkinter.Listbox.__init__(self, self.frame, **kwargs)
      self.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

      text_meths = vars(tkinter.Text).keys()
      methods = vars(tkinter.Pack).keys() | vars(tkinter.Grid).keys() | vars(tkinter.Place).keys()
      methods = methods.difference(text_meths)

      for m in methods:
         if m[0] != "_" and m != "config" and m != "configure":
            setattr(self, m, getattr(self.frame, m))
   def __str__(self):
      return str(self.frame)
   def destroy(self):
      super().destroy()
      self.frame.destroy()
   def _getBackground(self):
      return self['background']
   def _setBackground(self, color):
      self['background'] = color
   background = property(fset=_setBackground,fget=_getBackground)
   def _getForeground(self):
      return self['foreground']
   def _setForeground(self, color):
      self['foreground'] = color
   foreground = property(fset=_setForeground,fget=_getForeground)
class HTMLText(itkHTMLScrolledText):
   #Modified to have no borders by default
   def __init__(self, *args, html=None, **kwargs):
      super().__init__(*args, html=None, **kwargs)
      self.configure(borderwidth=0,highlightthickness=0)
   def _w_init(self, kwargs):
      super()._w_init(kwargs)
      self.vbar.pack_forget()
   def fit_height(self):
      super().fit_height()
      self.vbar.pack_forget()
#----------------------------------------------------

class itkScrolledListBox(itkBaseWidget, ScrolledListbox):
   _intName = "ScrolledListBox"
   def __init__(self, master=None, **kwargs):
      self._sbscaling = kwargs.pop('sbscaling',True)
      self._sbwidth = kwargs.pop('sbwidth',12)
      itkBaseWidget.__init__(self, ScrolledListbox, master, **kwargs)
   def update(self):
      nm = self._window.properties['nm']
      if self._sbscaling:
         self.vbar["width"] = self._sbwidth*nm
      self.place(x=self._x*nm,y=self._y*nm,width=self._width*nm,height=self._height*nm,anchor=self._anchor)
   def _getBackground(self):
      return self['background']
   def _setBackground(self, color):
      self['background'] = color
   background = property(fset=_setBackground,fget=_getBackground)
   def _getForeground(self):
      return self['foreground']
   def _setForeground(self, color):
      self['foreground'] = color
   foreground = property(fset=_setForeground,fget=_getForeground)
   def _getFont(self):
      return (self._font,self._fontSize)
   def _setFont(self, font):
      self._font, self._fontSize = font
      self.updateText()
   font = property(fset=_setFont,fget=_getFont)
   def _getSBScaling(self):
      return self._sbscaling
   def _setSBScaling(self, value):
      self._sbscaling = value
      self.update()
   sbscaling = property(fset=_setSBScaling,fget=_getSBScaling)
   def _getSBWidth(self):
      return self._sbwidth
   def _setSBWidth(self, value):
      self._sbwidth = value
      self.update()
   sbwidth = property(fset=_setSBWidth,fget=_getSBWidth)

class _ComboLabelWithRadioButtons(tkinter.Label):
   def __init__(self, master=None, **kwargs):
      numOptions = kwargs.pop('numOptions',2)
      self.frame = tkinter.Frame(master)
      self.radiobuttons = []
      self.rbvar = tkinter.IntVar()
      tkinter.Label.__init__(self,self.frame,anchor="nw",**kwargs)
      self.pack(side="top", fill="both")
      for i in range(numOptions):
         self.radiobuttons.append(tkinter.Radiobutton(self.frame,variable=self.rbvar,anchor="nw",value=i))
         self.radiobuttons[i].pack(side="top", fill="both")
      text_meths = vars(tkinter.Label).keys()
      methods = vars(tkinter.Pack).keys() | vars(tkinter.Grid).keys() | vars(tkinter.Place).keys()
      methods = methods.difference(text_meths)
      for m in methods:
         if m[0] != "_" and m != "config" and m != "configure":
            setattr(self, m, getattr(self.frame, m))

class ComboLabelWithRadioButtons(itkBaseWidget, tkinter.Label):
   _intName = 'ComboLabelWithRadioButtons'
   def __init__(self, master=None, **kwargs):
      #! Add a Label widget for every radiobutton because radiobutton.foreground also changes the button colour
      bg = kwargs.pop('background','')
      fg = kwargs.pop('foreground','')
      itkBaseWidget.__init__(self, _ComboLabelWithRadioButtons, master, **kwargs)
      self.background = bg
      self.foreground = fg
   def updateText(self):
      temp = (self._font,cmath.resizefont(self._fontSize,self._window.properties['mult']),self._fontStyle)
      self['font'] = temp
      for i in self.radiobuttons:
         i['font'] = temp
   def _setSelected(self,value:int):
      self.rbvar.set(value)
   def _getSelected(self):
      return self.rbvar.get()
   selected = property(fget=_getSelected,fset=_setSelected)
   def _setBackground(self, color):
      self.frame["bg"] = color
      self["background"] = color
      for i in self.radiobuttons:
         i.configure(background=color,highlightbackground=color)
   def _getBackground(self):
      return self["background"]
   background = property(fset=_setBackground,fget=_getBackground)
   def _setForeground(self, color):
      self["foreground"] = color
      for i in self.radiobuttons:
         i.configure(foreground=color)
   def _getForeground(self):
      return self["background"]
   foreground = property(fset=_setForeground,fget=_getForeground)
   def _setText(self, text):
      if isinstance(text,(list,tuple)) and len(text) == 2:
         self.radiobuttons[text[0]]["text"] = text[1]
      else:
         self['text'] = text
   text = property(fset=_setText) # This can not have a get method because get does not accept arguements
class CheckboxWithLabel(itkBaseWidget, tkinter.Label):
   _intName = 'CheckboxWithLabel'
   def __init__(self, master=None, **kwargs):
      self.frame = tkinter.Frame(master)
      self._cbvar = tkinter.BooleanVar()
      bg = kwargs.pop('background')
      fg = kwargs.pop('foreground')
      self.cb = tkinter.Checkbutton(self.frame,variable=self._cbvar)
      itkBaseWidget.__init__(self, tkinter.Label, self.frame, **kwargs)
      self['anchor'] = 'w'  # Right align text
      if bg != None:
         self._setBackground(bg)
      if fg != None:
         self._setForeground(fg)
      self.update()
   def update(self):
      nm = self._window.properties['nm']
      self.frame.place(x=self._x*nm,y=self._y*nm,width=self._width*nm,height=self._height*nm,anchor=self._anchor)
      self.cb.place(x=0,y=0,width=self._height*nm,height=self._height*nm,anchor='nw')
      self.place(x=self._height*nm,y=0,width=(self._width-self._height)*nm,height=self._height*nm,anchor='nw')
   def updateText(self):
      self['font'] = (self._font,cmath.resizefont(self._fontSize,self._window.properties['mult']),self._fontStyle)
   def select(self):
      self.cb.select()
   def deselect(self):
      self.cb.deselect()
   def getcb(self):
      return self._cbvar.get()
   def _getBackground(self):
      return self['background']
   def _setBackground(self, color):
      self.frame['bg'] = color
      self['background'] = color
      self.cb['background'] = color
      self.cb['highlightbackground'] = color
   background = property(fset=_setBackground,fget=_getBackground)
   def _getForeground(self):
      return self['foreground']
   def _setForeground(self, color):
      self['foreground'] = color
   foreground = property(fset=_setForeground,fget=_getForeground)

class CheckboxWithEntry(itkBaseWidget, tkinter.Entry):
   _intName = 'CheckboxWithEntry'
   def __init__(self, master=None, **kwargs):
      self._indent = kwargs.pop('indent',0)
      self._cbvar = tkinter.BooleanVar()
      self._entryvar = tkinter.StringVar()
      self.frame = tkinter.Frame(master)
      self.cb = tkinter.Checkbutton(self.frame,variable=self._cbvar,command=self.checkCB)
      self.l1 = tkinter.Label(self.frame,text=kwargs.pop('text',''),anchor="w")
      self.l2 = tkinter.Label(self.frame,anchor="w")
      self._entrytextwidth, self.l2['text'] = kwargs.pop('entrytext',(0,''))
      bg = kwargs.pop('background','')
      fg = kwargs.pop('foreground','')
      itkBaseWidget.__init__(self, tkinter.Entry, self.frame, textvariable=self._entryvar, **kwargs)
      self.background = bg
      self.foreground = fg
      self["state"] = "disabled"
      self.update()
      self.updateText()
   def update(self):
      nm = self._window.properties['nm']
      self.frame.place(x=self._x*nm,y=self._y*nm,width=self._width*nm,height=self._height*nm*2,anchor=self._anchor)
      self.cb.place(x=0,y=0,width=self._height*nm,height=self._height*nm,anchor="nw")
      self.l1.place(x=self._height*nm,y=0,width=(self._width-self._height)*nm,height=self._height*nm,anchor="nw")
      self.l2.place(x=self._indent*nm,y=self._height*nm,width=self._entrytextwidth*nm,height=self._height*nm,anchor="nw")
      self.place(x=(self._indent+self._entrytextwidth)*nm,y=self._height*nm,width=(self._width-self._indent-self._entrytextwidth)*nm,height=self._height*nm,anchor="nw")
   def updateText(self):
      temp = (self._font,cmath.resizefont(self._fontSize,self._window.properties['mult']),self._fontStyle)
      self['font'] = temp
      self.l1['font'] = temp
      self.l2['font'] = temp
   def checkCB(self):
      if self._cbvar.get():
         self._enable()
      else:
         self._disable()
   def _enable(self):
      self['state'] = 'normal'
   def _disable(self):
      self['state'] = 'disabled'
   def select(self):
      self.cb.select()
      self._enable()
   def deselect(self):
      self.cb.deselect()
      self._disable()
   def get(self):
      return self._entryvar.get()
   def set(self,value):
      self._entryvar.set(value)
   def getcb(self):
      return self._cbvar.get()
   def _getBackground(self):
      return self.l1['background']
   def _setBackground(self, color):
      self.frame["bg"] = color
      self.cb["background"] = color
      self.cb["highlightbackground"] = color
      self.l1["background"] = color
      self.l2["background"] = color
   background = property(fset=_setBackground,fget=_getBackground)
   def _getForeground(self):
      return self.l1['foreground']
   def _setForeground(self, color):
      self.l1["foreground"] = color
      self.l2["foreground"] = color
   foreground = property(fset=_setForeground,fget=_getForeground)

class CheckboxWithCombobox(itkBaseWidget, Combobox):
   _intName = 'CheckboxWithCombobox'
   def __init__(self, master=None, **kwargs):
      self._indent = kwargs.pop('indent',0)
      self._cbvar = tkinter.BooleanVar()
      self.frame = tkinter.Frame(master)
      self.cb = tkinter.Checkbutton(self.frame,variable=self._cbvar,command=self.checkCB)
      self.l1 = tkinter.Label(self.frame,text=kwargs.pop('text',''),anchor="w")
      self.l2 = tkinter.Label(self.frame,anchor="w")
      self._entrytextwidth, self.l2['text'] = kwargs.pop('entrytext',(0,''))
      bg = kwargs.pop('background','')
      fg = kwargs.pop('foreground','')
      itkBaseWidget.__init__(self, Combobox, self.frame, **kwargs)
      self.background = bg
      self.foreground = fg
      self.checkCB()
   def update(self):
      nm = self._window.properties['nm']
      h = self._height*nm
      self.frame.place(x=self._x*nm,y=self._y*nm,width=self._width*nm,height=h*2,anchor=self._anchor)
      self.cb.place(x=0,y=0,width=h,height=h,anchor="nw")
      self.l1.place(x=h,y=0,width=(self._width-self._height)*nm,height=h,anchor="nw")
      self.l2.place(x=self._indent*nm,y=h,width=self._entrytextwidth*nm,height=h,anchor="nw")
      self.place(x=(self._indent+self._entrytextwidth)*nm,y=h,width=(self._width-self._indent-self._entrytextwidth)*nm,height=h,anchor="nw")
   def updateText(self):
      temp = (self._font,cmath.resizefont(self._fontSize,self._window.properties['mult']),self._fontStyle)
      self.l1['font'] = temp
      self.l2['font'] = temp
      self['font'] = temp
   def checkCB(self):
      if self._cbvar.get():
         self._enable()
      else:
         self._disable()
   def _enable(self):
      self['state'] = 'normal'
   def _disable(self):
      self['state'] = 'disabled'
   def select(self):
      self.cb.select()
      self._enable()
   def deselect(self):
      self.cb.deselect()
      self._disable()
   def getcb(self):
      return self._cbvar.get()
   def _getBackground(self):
      return self.l1['background']
   def _setBackground(self, color):
      self.frame["bg"] = color
      self.l1["background"] = color
      self.l2["background"] = color
      self.cb["background"] = color
      self.cb["highlightbackground"] = color
   background = property(fset=_setBackground,fget=_getBackground)
   def _getForeground(self):
      return self.l1['foreground']
   def _setForeground(self, color):
      self.l1["foreground"] = color
      self.l2["foreground"] = color
      self.filebutton["foreground"] = color
   foreground = property(fset=_setForeground,fget=_getForeground)

class FileEntryBox(itkBaseWidget, tkinter.Entry):
   _intName = 'FileEntryBox'
   def __init__(self, master=None, **kwargs):
      self.filetype = kwargs.pop('filetype','dir')
      self.fileaction = kwargs.pop('fileaction','open')
      self.initdir = kwargs.pop('initdir',None)
      self.initfile = kwargs.pop('initfile',None)
      self._indent = kwargs.pop('indent',0)
      self._entryvar = tkinter.StringVar()
      self.frame = tkinter.Frame(master)
      self.l1 = tkinter.Label(self.frame,text=kwargs.pop('text',''),anchor="w")
      self.l2 = tkinter.Label(self.frame,anchor="w")
      self._entrytextwidth, self.l2['text'] = kwargs.pop('entrytext',(0,''))
      bg = kwargs.pop('background','')
      fg = kwargs.pop('foreground','')
      itkBaseWidget.__init__(self, tkinter.Entry, self.frame, textvariable=self._entryvar, **kwargs)
      self.filebutton = tkinter.Button(self.frame,command=self.selectfile)
      self.background = bg
      self.foreground = fg
   def update(self):
      nm = self._window.properties['nm']
      self.frame.place(x=self._x*nm,y=self._y*nm,width=self._width*nm,height=self._height*nm*2,anchor=self._anchor)
      self.l1.place(x=0,y=0,width=(self._width-self._height)*nm,height=self._height*nm,anchor="nw")
      self.l2.place(x=self._indent*nm,y=self._height*nm,width=self._entrytextwidth*nm,height=self._height*nm,anchor="nw")
      self.place(x=(self._indent+self._entrytextwidth)*nm,y=self._height*nm,width=(self._width-self._indent-self._entrytextwidth-self._height)*nm,height=self._height*nm,anchor="nw")
      self.filebutton.place(x=(self._width-self._height)*nm,y=self._height*nm,width=self._height*nm,height=self._height*nm,anchor="nw")
   def updateText(self):
      temp = (self._font,cmath.resizefont(self._fontSize,self._window.properties['mult']),self._fontStyle)
      self.l1['font'] = temp
      self.l2['font'] = temp
      self['font'] = temp
   def selectfile(self):
      if self.filetype == 'dir':
         file = filedialog.askdirectory(initialdir=self.initdir)
      elif self.filetype == 'file':
         if self.fileaction == 'open':
            file = filedialog.askopenfilename(initialdir=self.initdir,initialfile=self.initfile)
         elif self.fileaction == 'save':
            file = filedialog.asksaveasfilename(initialdir=self.initdir,initialfile=self.initfile)
      if not (isinstance(file,tuple) or file == ''):
         self._entryvar.set(file)
   def get(self):
      return self._entryvar.get()
   def set(self, value):
      self._entryvar.set(value)
   def _getBackground(self):
      return self.l1['background']
   def _setBackground(self, color):
      self.frame["bg"] = color
      self.l1["background"] = color
      self.l2["background"] = color
      self.filebutton["background"] = color
   background = property(fset=_setBackground,fget=_getBackground)
   def _getForeground(self):
      return self.l1['foreground']
   def _setForeground(self, color):
      self.l1["foreground"] = color
      self.l2["foreground"] = color
   foreground = property(fset=_setForeground,fget=_getForeground)

class itkDisplay(itkFrame):
   _intName = 'display'
   def update(self):
      nm = self._window.properties['nm']
      self.place(x=self._window.properties['width']//2, y=self._window.properties['height']//2, width=self._window.properties["startwidth"]*nm, height=self._window.properties["startheight"]*nm, anchor="center")

class itkImage:
   _intName = 'Image'
   def __init__(self, window, data='', size=(0,0)):
      self._window = window
      self._data = data
      self.img = ''
      self.references = 0
      if size == None:
         size = PIL.Image.open(BytesIO(image_data)).size
      self._size = [size[0],size[1]]
   def resize(self):
      nm = self._window.properties['nm']
      img = PIL.Image.open(BytesIO(self._data))
      img.thumbnail((self._size[0]*nm,self._size[1]*nm))
      self.img = PIL.ImageTk.PhotoImage(img)
class itkBlankImage(itkImage):
   def resize(self):...
   
class itkRootTk(tkinter.Tk):
   _intName = 'Window'
   def update(self):...
   def updateText(self):...
   def resize(self):...

class itkRootToplevel(tkinter.Toplevel):
   _intName = 'Window'
   def update(self):...
   def updateText(self):...
   def resize(self):...

class DefaultIcon:
   FLASH = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00d\x00\x00\x00d\x08\x06\x00\x00\x00p\xe2\x95T\x00\x00\x01\x84iCCPICC profile\x00\x00(\x91}\x91=H\xc3@\x1c\xc5_[\xa5R*\n\x16\x11q\xc8P\x9d\xecbE\x1ck\x15\x8aP!\xd4\n\xad:\x98\\\xfa\x05M\x1a\x92\x14\x17G\xc1\xb5\xe0\xe0\xc7b\xd5\xc1\xc5YW\x07WA\x10\xfc\x00qvpRt\x91\x12\xff\x97\x14Z\xc4xp\xdc\x8fw\xf7\x1ew\xef\x00\x7f\xb3\xcaT\xb3\'\x01\xa8\x9aedRI!\x97_\x15\x82\xaf\x08a\x10\xc3\x88#&1S\x9f\x13\xc54<\xc7\xd7=||\xbd\x8b\xf1,\xefs\x7f\x8e~\xa5`2\xc0\'\x10\'\x98nX\xc4\x1b\xc43\x9b\x96\xcey\x9f8\xc2\xca\x92B|N<i\xd0\x05\x89\x1f\xb9.\xbb\xfc\xc6\xb9\xe4\xb0\x9fgF\x8clf\x9e8B,\x94\xbaX\xeebV6T\xe2i\xe2\xa8\xa2j\x94\xef\xcf\xb9\xacp\xde\xe2\xacV\xeb\xac}O\xfe\xc2pA[Y\xe6:\xcd1\xa4\xb0\x88%\x88\x10 \xa3\x8e\n\xaa\xb0\x10\xa3U#\xc5D\x86\xf6\x93\x1e\xfeQ\xc7/\x92K&W\x05\x8c\x1c\x0b\xa8A\x85\xe4\xf8\xc1\xff\xe0w\xb7f1>\xe5&\x85\x93@\xef\x8bm\x7f\x8c\x03\xc1]\xa0\xd5\xb0\xed\xefc\xdbn\x9d\x00\x81g\xe0J\xeb\xf8kM`\xf6\x93\xf4FG\x8b\x1e\x01\x03\xdb\xc0\xc5uG\x93\xf7\x80\xcb\x1d`\xe4I\x97\x0c\xc9\x91\x024\xfd\xc5"\xf0~F\xdf\x94\x07\x86n\x81\xd0\x9a\xdb[{\x1f\xa7\x0f@\x96\xbaJ\xdf\x00\x07\x87\xc0D\x89\xb2\xd7=\xde\xdd\xd7\xdd\xdb\xbfg\xda\xfd\xfd\x00\x05xr\xe1\xf0a\xe0\x07\x00\x00\x00\x06bKGD\x00\xff\x00\xff\x00\xff\xa0\xbd\xa7\x93\x00\x00\x00\tpHYs\x00\x00\x0fa\x00\x00\x0fa\x01\xa8?\xa7i\x00\x00\x00\x07tIME\x07\xe8\n\x10\x164\x05\xff\x81\xa4\xcb\x00\x00\x07nIDATx\xda\xed\xddkP\x94U\x18\x07\xf0\xff^`wA\x04aq\x11\xc6\x15\r\xb1`0\xc7\x0b:\xa2\x94\x95]Dq\xfcP*\xe3P\xe9\x989YF^\xc6\x19\xbb\xd9\xe8\xe8\x98a\xa3ejcN\x9a\xd0\xa81~\xc84\t\x99Ra\x08\xc4\xcb\x98\xa6\x90\x86\x88\x97PP\x89\xe5\xba\x9c>,\x97].\xc9\xbb\xbb\xe7\xbc\xe7=\xbc\xe7\xd3\xb2\x03\xbb\xcf\xf2\x9bs\x9es_MN\xcc(\x82>P\x08\x00B\x00\x02\xe2x\xdc\xfa\xa4\xe3q\xc7s\x84\xb4\xfd>q\xfa\x9b\xd6\xdf\xef\xe69\xd2\xfa"\x1d?\x03\x84\x10\x10\xe7\xf7\xed\xee\xb9N\xef\xdd\xf6\x1aZ\x15\x83\x1f\x8c>\x01\xa2$\x0c\x02"6\x88\xd20\x84\xae!J\xc4 DP\x10\xa5b@\xc4\x1a\xa2d\x0c\xe1\x9a,\xa5c\x08\x95\xd4E\xc0\x10&\x87\x88\x82!D\x93%\x12\x86\xe2AD\xc3Pt/KD\x0cB\x14\x9a\xd4E\xc5Pd\x93%2\x86\xe2@D\xc7P\x14H_\xc0 \x00\xf4*FW\x0c\xe8t\xe8?\xc4\x8a~\x91V\x18\x82\x83a2\x9b\xe1\x13\xd0\x0f\xa77\xa6S\xc5\x00!\xfc\x83\xb0\xc2\x08\x8a\x8dA\xf8\x94DX&\x8c\x87\xf9\xc98\xe8\x8c\xc6.\xb1\x14mL\xa7\x8a\xc1}\r\xa1\x8da\x08\t\xc6\xb0\xb9\xb3\x119s:\x02"\x87<:\x1e\xca\x18\\\x83\xd0\xc4\xf0\x8f\x88@\xcc[obHr\x12\xb4\xbe\xbe\xd2b\xa2\x88\xc1-\x08-\x0c\x9d\x9f\t#\x16\xbc\x86\xc7\xdfX\x00\x9d\xc1\xe0F\\t1\x08\xe1\x10\x84\x16\x86%1\x01\xf1\xeb\xd7\xc2\x18j\xf6(6\x9a\x18\x04\x9c%u\x1a\x18Z\x83\x01q+\xd30|^\n\xa0\xd1x\x1c M\x0c\xf0\xd4d\xd1\xc0\xf0\t\x0cD\xc2\xf6-0\x8f\x19\xed\xbd\x18)bp\x93Ch`\xf8E\x84c\xf2\xae\xed\x08\x186\xd4\xbbqR\xc4\xe0"\x87\xd0\xc0\xf0\xb7\x0e\xc6\x94\xccoa\x0c\r\xf5r\xact1d\x9f:\xa1\x81\xe1;`\x00&}\xbd\xcd\xeb\x18\xe8\x12\x8b\xf71d]S\xa7\x92\xc0\x8d\x06L\xfcj\x0b\x02\x86F\xd2\x89\x992\x86l9\x84V\xd7v\xec\xba50\x8f\x1e\xe5\xf5x\x9b\xeb\xea\x1ds\\\x941d\xe9e\xd1\xc2\xb0&\'\xc1:#\xc9\xe3\xf8\xea\xab\xabq\xed\xc81\xdc)>\x8b\xca\x0b\x7f\xa0\xba\xf4/\xd8\x9b\xedL0\x98\'uZ\x18\xa6\xf00\x8c\xfep\xb5G\xb1U\x97\x94\xe2\xec\x97;p\xf5\xf0Q\xd8\x9b\x9b\x99$\xf0\xce\x18L\x9b,\x9asS\xf1\x1b\xd6\xc1\xa7\x7f\x80[q5\xd5\xd6\xa2h\xd3\xe7\xb8\xb8\'\x03---L\xba\xb6=a0\x03\xa1\x89\x111\xf5Y\x0c\x9c\x10\xefV\\U\x97\xfeD\xf6\xa2%\xa8)\xaf`2\xe8{\x14\x06\x93\xa9\x13\x9a\x18\x1a\xad\x0e#\x97\xa7\xb9\x15WYv\x0er\xd3V\xa0\xb9\xb6\x8e\x1b\x0c\xea9\x84\xf6z\xc6\xb09/\xbb\xd5\xc5\xbd\xf1\xdbI\x1c\x7f\xfb=\xd8\x1b\x1a\xb9\xc2\x00\xcd\x81!m\x0c\xad\xd1\x80\xd8%\x8b%\xc7u\xbb\xa0\x10\xd9\x8b\x96p\x89Am\xa4\xceb\xd9\xd5:#\tFs\x88\xa4\xb8\xea\xee\xde\xc3\xf1\xa5\xcb`\xafo\xe0\x12\x83\n\x08\xab5\xf0\xa8\xb9\xb3\xa5\xc5e\xb7\xe3\xf8\xd2e\xb0\xdd\xa9\xe4\x16\xc3\xebS\'\xac0\x82G\xc6!8.VRl\x972\xf7\xe3V^\x01\xd7\x18^=\x8e\xc0r\xabNT\x8a\xb4\xda\xd1p\xff\x01\x8a\xd3\xb7r\x8f\xe1\xb5&\x8b%\x86\xceh\x80u\xda\x8b\x92\xe2+\xfct3\xea\xaa\xab\xb9\xc7\xf0J/\x8b\xf5&6K\xc2D\xe8M\xc6^\xc7W{\xfb6.\x1f\xc8R\x04\x86\xc7#u9\xb6wF<\xf3\x94\xb4\x01\xe0/\xb9\x08\x8b\x1f\xeb\xf2\xa1\xe1\xfc\xde\x9d0\xda\xfe\xf1e\'\xf3\x98c\x10B\xa0q\xf7\xae\x13Y\xf6\xdaj4\x98u2\x07~\x16\x0b\xf5\xe9\x9etk4s\x0c\xb7s\x88\\\x1b\x9f\x07\xc4\xc60\xc1\x80\x0c5\xc3\xedq\x88\x9c\xbb\xd0\xa56W\x9e.\x0f\xb2\xc6\x90\x9c\xd4\xe5>\x12\x10\x918\x99\xed\xda\rc\x0cI\xe3\x10\xb91|\x03\xfb#D\xe2`\xd0+ \x0c1z=R\xe7\xe1\xb0\xcc\xa0I\t\xd0\xe8t\xb2\xacn\xb2\xc2\xe8U\x0e\xe1\xe5\xe4Rxb\x02\xdb\xb5\x7f\x190\x1e\t\xc2\x0b\x86F\xa7c\x9a?:\xa2f\x8b\xf1\xbf <\x9d\xe9\xb3\x8c\x1f\x07\x93\x07\xbb\xd6=o\xb6\xd8`\xa0\xa7\xa4\xce\xdb\x01\xcb\xa1\xd3\xa7\xf5\t\x8cn\x93:o\x18\x1a\xbd\x0f\x86\xbc0\x95=\x88\x0c\x18]\x9a,\x1e\x8f\x1e\x0f~\xe6i\x18\x82\x02\xe5\xa9!\x8c1\\&\x17y=\x07\xfeDj\x8a\xa4\x7f\xe4\xe9m;q\xfdT~\xb7\xa3m\xe7t\xdd\xf93\xa2\x87\xcf\xcc\x12\xa3}\xd7\t\xaf\x18A\xd1Q\x18$e\xcf\x15!8\xbb{\x0fj\xff\xa9\x94u\n\xdd]\x0c\x02@\xcb\xf3\r\t\xb1\xaf\xa7J:\x86v\xaf\xa4T\xd1\x18\x00\x81\x96W\x0c\xff\x88pD\xcdJ\x96\xd4\\\x95\xfe\xf4\xb3\xa21Zk\x08\x9fw\x87\x8cI{\x07:\tg\xc8A\x08.\xfdpH\xd1\x18\x84\xb45Y\x9ca\x04GG#j\xe6tI\xb5\xe3fQ1\xee\x97]W4F{\x0e\xe1\tC\xa3\xd1"a\xedG\x92\'\x12/\x1e\xccR<\x86c\x1c\xc2\xd9\x15G\xb1\xf3Sa\x19+\xed\x18s\xe3\xbf\xb5\xb8\xf2\xe3Q\xc5c\x10\x90\xb6&\x8b\x0f\x0c\xf3\xc88\x8c[\xfe\xae\xe4A\xdc\xb9\xbd\xfbP_S\xa3x\x0ctN\xearb\x98\x06\x86b\xea\x8e\xad\x92\xef i\xb2\xd5\xa1h\xe77B`\xb8$u91\x8c\xe6\x10\xbc\xb4w\x17\xfc\xc3,n\xd4\x8e\x0c\xd8\xeeU\t\x81\xe120\x94\x0b#h\xf8cH>\x98\x81\xe0\xe8\xe1\x921\x1ajjP\xb8c\x970\x18\x04\x80^.\x0c\xadV\x87\x11)\xaf`\xfc\xaa\x15\xd0\xfb\x99\xdc\x9a\x00<\xb1\xe13\xd8*+\x85\xc1h\x9f\\d\x89\xe1\x17\x16\x86\xc8\xe7\x9fCLj\n\x02=\xb8\x87\xa4\xa2\xa8\x18\xe7\xbf\xcb\x14\n\x83\x10\x02=\x0b\x8c9\xbf\x9f@\xb3\xcd\x06\xbd\xbf\x1fL!!\xf0\xb4\xd8\x1b\x1b\x91\xbdr\xb5\xd3\xa9Y10\x00@\xcf\xa2f\x98\xcc!\x00<\x87h+9\xef\xaf\xc1\xdd\x92R\xe10\x1cI\x9dA3\xe5\xcdrf\xf7\x1e\x9c\xcf\xdc/$\x06\xe0<\x97E\xb37\xe5\xa5Rv"\x0f\xb9\x9f\xac\x17\x16\xa3\x1d\x84v\xd7\xd6\x1b\xe5FA!\x0e-\\\xdcz\xed\x85\x98\x18p\xac\xa9\xd3\xbf~\xdb\xf3\x9aq\n\x07\xe7\xcdGc\xadMh\x0c\xb8\xae\x18\xd2\xbb\x0b\xdd\x93r~\xdf\xf7\xc8zu!\x9a\xea\xeb\x85\xc7@\xdb\xc0\x90\xf6\xc5\xf4\xee\x94\xa6\xba:\xe4\xac\xfe\x18\x17\x0ed\t\x9d3\xba\x82P\xc6p\x87\xa3<\xbf\x00\xd9\xab>@\xd5\xd5k}\n\xc3\t\x84\xfeW6\xf4\xa6\xdc\xbd|\x05\xf9\x9b\xbf\xc0\x95\xc3G\x84\x1b\x81\xf7\xb6\x7f\xa3\x97\x1b\x83\xb4\xb4\xa0<\xbf\x00\xe7\xf6f\xa0\xe4h6\x88\xdd\xdeg1\x00@\xcf\xe2\xcbL\xba[\xc3\xb8U|\x06\x7f\xe7\xfe\x8a\x92#\xc7\xf0\xe0F\x850\xeb\x19\x9e`t\xca!\xf4\xbeY&o\xc3&4\xd9\xea\xf0\xb0\xe2&\x1e\x96\x97\xa3\xaa\xf5\x1eC\x11\xd6\xc0\xbd\x89\x01\x00\x9a\xcc\xa8X"\xf7\xd7\xfc\xa8\x18]\xc6!*\x06\x0f\x18\x0e\x10\x15\x83\x1b\x0c\xa7\xb9,\x15\x83\x07\x8c\xd6\xb9,\x15\x83\x17\x0c\x97\xe9w\x15C~\x8c\x9e\x93\xba\x8a!\x0bF\xf7I]\xc5\x90\r\xa3kRW1d\xc5pM\xea*\x86\xec\x18\xdd,P\xa9\x18rb\xc0u\xd7\x89\x8a!7\x86S\xb7W\xc5\xe0\x01\xa3\x15D\xc5\xe0\x05\xa3\xa3\x97\xa5bp\x81\xe1\xe8e\xa9\x18\xdc`\xb8N\x9d\xa8\x18\xb2c\x00\xc0\x7f\xe7\x06\xe8\xb1iL\xc9O\x00\x00\x00\x00IEND\xaeB`\x82'
   FLASH_PY = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00d\x00\x00\x00d\x08\x06\x00\x00\x00p\xe2\x95T\x00\x00\x01\x84iCCPICC profile\x00\x00(\x91}\x91=H\xc3@\x1c\xc5_S\xa5R*\n\x16\x11q\xc8P\x9d\xecRE\x1ck\x15\x8aP!\xd4\n\xad:\x98\\\xfa\x05M\x1a\x92\x14\x17G\xc1\xb5\xe0\xe0\xc7b\xd5\xc1\xc5YW\x07WA\x10\xfc\x00qvpRt\x91\x12\xff\xd7\x14Z\xc4xp\xdc\x8fw\xf7\x1ew\xef\x00\xa1Qa\x9a\xd5\x13\x074\xdd6\xd3\xc9\x84\x98\xcd\xad\x8a\x81W\x041\x88a\xc4 \xc8\xcc2\xe6$)\x05\xcf\xf1u\x0f\x1f_\xef\xa2<\xcb\xfb\xdc\x9f\xa3_\xcd[\x0c\xf0\x89\xc4qf\x986\xf1\x06\xf1\xcc\xa6mp\xde\'\x0e\xb3\x92\xac\x12\x9f\x13O\x9atA\xe2G\xae+.\xbfq.\xb6X\xe0\x99a3\x93\x9e\'\x0e\x13\x8b\xc5.V\xba\x98\x95L\x8dx\x9a8\xa2j:\xe5\x0bY\x97U\xce[\x9c\xb5J\x8d\xb5\xef\xc9_\x18\xca\xeb+\xcb\\\xa79\x86$\x16\xb1\x04\t"\x14\xd4PF\x056\xa2\xb4\xea\xa4XH\xd3~\xc2\xc3?\xda\xf2K\xe4R\xc8U\x06#\xc7\x02\xaa\xd0 \xb7\xfc\xe0\x7f\xf0\xbb[\xab0\x15s\x93B\t\xa0\xf7\xc5q>\xc6\x81\xc0.\xd0\xac;\xce\xf7\xb1\xe34O\x00\xff3p\xa5w\xfc\xd5\x060\xfbIz\xbd\xa3E\x8e\x80\x81m\xe0\xe2\xba\xa3){\xc0\xe5\x0e0\xf2d\xc8\xa6\xdc\x92\xfc4\x85B\x01x?\xa3o\xca\x01C\xb7@p\xcd\xed\xad\xbd\x8f\xd3\x07 C]\xa5n\x80\x83C`\xa2H\xd9\xeb\x1e\xef\xee\xeb\xee\xed\xdf3\xed\xfe~\x00\x97\xebr\xb5\x8e\x92\xb6\xfb\x00\x00\x00\x06bKGD\x00\xff\x00\xff\x00\xff\xa0\xbd\xa7\x93\x00\x00\x00\tpHYs\x00\x00\x0fa\x00\x00\x0fa\x01\xa8?\xa7i\x00\x00\x00\x07tIME\x07\xe8\n\x10\x1623fa\x96\xd4\x00\x00\x08\xdbIDATx\xda\xed\xdd{pT\xd5\x1d\x07\xf0\xef\xdd\xbb\xc9\xeef\xf3"\xd9dCRB\x92\x86\x04\xb2\x13tx\xaa\x01\x8a\xda\xf4!\x88\xa33\xad\x9aa\xd2\xaac-\x95\xd6R\x1f\xe3\x0c}\xd9\xd1\x91Z\x05G\xac\x15,u\n\x958\x8a\x0c\xce\x88Pc\xa0-\xaf\t\x8912V\x02IU\x08\xaf\x907\xc9\xee&\xd9\xc7\xe9\x1fy\x90\xddd\xc9\xde\xbd\xf7\x9c{\xee\xe5\x9e\xbf\xb2\x97%\xfb\xdb\xfd\xe4\x9c\xdf=\xcf\x15jJn$\xb8\x0e\n\x01@\x08@@\x86\x7f\x1e\xb98\xfc\xf3\xd5k\x84\x8c>\x9f\x8c\xfb?#\xcf\x9f\xe4\x1a\x19\xf9%W\x1f\x03\x84\x10\x90\xf1\xaf;\xd9\xb5\xb0\xd7\x1e\xfd\x1d&\x03\x83\x1f\x8c\xeb\x02DK\x18\x04D\xdf Z\xc3\xd0u\r\xd1"\x06!:\x05\xd1*\x06\xf4XC\xb4\x8c\xa1\xbb&K\xeb\x18\xbaJ\xeaz\xc0\xd0M\x0e\xd1\x0b\x86.\x9a,=ah\x1eDo\x18\x9a\xbe\xcb\xd2#\x06!\x1aM\xeaz\xc5\xd0d\x93\xa5g\x0c\xcd\x81\xe8\x1dCS \xd7\x03\x06\x01`60&b@\x14\x91<3\x17\x89y\xb9\xb0\xa4\xa5\xc1\xe6p .)\x11\x9f\xbc\xb0\x91*\x06\x08\xe1\x1f\x84\x15F\xaa\xab\x04\xd9\xb7.\x83\xf3\xa6\xc5p\xdcP\n\xd1j\x9d\x10K\xfd\x0b\x1b\xa9bp_ChcX\xd2\xd3Pp\xff\xbd\xc8\xbbk%\x92\xf2fN\x1d\x0fe\x0c\xaeAhb\xd8srP\xf2\xe8O1s\xd5\n\x98\xe2\xe3\xa5\xc5D\x11\x83[\x10Z\x18b\x82\r\xc5\x0f\xfd\x18\xb3\x7f\xf2\x10D\x8b%\x86\xb8\xe8b\x10\xc2!\x08-\x0c\xe7\xb22,z\xfeYX3\x1c\xb2b\xa3\x89A\xc0YR\xa7\x81a\xb2XP\xfa\xd4:\xccZ]\x01\x08\x82\xec\x00ib\x80\xa7&\x8b\x06F\\J\n\xca^\x7f\x05\x8e\xf9\xf3\x94\x8b\x91"\x0679\x84\x06FBN6\x96n{\x1dI\x05\xf9\xca\xc6I\x11\x83\x8b\x1cB\x03\xc3\x9e;\x03\xb7V\xfd\x1d\xd6\x8c\x0c\x85c\xa5\x8b\xa1\xfa\xd0\t\r\x8c\xf8i\xd3\xb0\xe4\x8d\xd7\x14\xc7\xc0\x84X\x94\xc7PuN\x9dJ\x02\xb7Zp\xcb_^AR~\x1e\x9d\x98)c\xa8\x96Ch\xdd\xda.x\xee\x198\xe6\xdd\xa8x\xbc~\xef\xc0\xf0\x18\x17e\x0cU\xee\xb2ha\xe4\xaeZ\x81\xdc;W\xc8\x8eo\xa0\xbb\x1b_\xed\xfb\x08m\r\x8dh\xff\xfc\xbf\xe8n\xf9\x1f\x02\xfe\x00\x13\x0c\xe6I\x9d\x16\x86-;\x0b\xf3~\xbb^Vl\xdd\xcd-h\xfc\xf3\x16|\xb9w?\x02~?\x93\x04\x1e\x8e\xc1\xb4\xc9\xa296\xb5h\xc3s\x88KN\x8a).\x9f\xdb\x8d\xfa\x17_\xc6\x17\xdbw"\x18\x0c2\xb9\xb5\x8d\x84\xc1\x0c\x84&FN\xf9\xed\xc8\xbciQLqu\x9dlB\xf5#k\xd1\xd7z\x9eI\xa7o*\x0c&C\'41\x04\x93\x88\xb9O\xac\x8b)\xae3\xd558\xb8\xeeI\xf8\xdd^n0\xa8\xe7\x10\xda\xf3\x19\x05\xf7\xfd \xa6[\xdcs\xff9\x8c\x03?\xff\x15\x02\x83C\\a\x80f\xc7\x906\x86\xc9j\x81k\xed\x1a\xc9q]\xaa\xadC\xf5#k\xb9\xc4\xa0\xd6Sg1\xed\x9a{\xe7\nX\x1d\xe9\x92\xe2\xf2vt\xe2\xc0c\x8f#00\xc8%\x06\x15\x10Vs\xe0\x85\xf7\xdf+-\xae@\x00\x07\x1e{\x1c\x9e\xb6vn1\x14\x1f:a\x85\x916\xb7\x14i\xa5.I\xb1\x9d\xacz\x07\x17\x8f\xd6r\x8d\xa1\xe8v\x04\x96Ku\n+\xa4\xd5\x8e\xc1\x9e^4l\xdc\xcc=\x86bM\x16K\x0c\xd1jA\xee\x1d\xdf\x93\x14_\xdd\x9f6\xc1\xdb\xdd\xcd=\x86"wY\xac\x17\xb19\xcbn\x81\xd9f\x8d:>\xf7\xa5K8\xf5\xeenM`\xc8\xee\xa9\xab\xb1\xbc3\xe7\xb6oI\xeb\x00~|\x10Y\x8b\x16\x84\xbci\x8c\x7f\xed0\x8c\xd1\x0f\xfe\xcc\xe1\xa3\xcc1\x08!\x10b=\xebD\x95\xb5\xb6\x82\x80\xbb\x0f\xd7 \xc1\xe9\xa4>\xdc\xb31\xb7\x889F\xcc9D\xad\x85\xcf\xd3\\%L0\xa0B\xcd\x88\xb9\x1f\xa2\xe6*t\xa9\xcd\x95\xdc\xe9A\xd6\x18\x92\x93\xba\xda[\x02r\x96-e;w\xc3\x18CR?Dm\x8c\xf8\x94d\xa4K\xec\x0c*\x02\xc2\x10#\xea\x9e:\x0f\x9be\xa6/)\x83 \x8a\xaa\xccn\xb2\xc2\x88*\x87\xf0\xb2s){Y\x19\xdb\xb9\x7f\x150\xa6\x04\xe1\x05C\x10E\xa6\xf9\xe3j\xd4l1\xae\t\xc2\xd3\x9e>\xe7\xe2\x85\xb0\xc9X\xb5.\xbf\xd9b\x83\x81HI\x9d\xb7\r\x96\xf9+\xef\xb8.0&M\xea\xbca\x08\xe68\xcc\xfcn9{\x10\x150&4Y<n=\x9eq\xdbrXRS\xd4\xa9!\x8c1B\x06\x17y\xdd\x07>\xa7\xb2B\xd2\x07\xf9\xc9k[q\xf6\xc8\xb1I{\xdb\xe3\xd3u\xf8{D\x84\xf7\xcc\x12cl\xd5\t\xaf\x18\xa9E\x85\x98.e\xcd\x15!h|s;\xdc\x97\xdbU\x1dB\x8f\x15\x83\x000\xf1|B\x82\xeb\x81JI\xdb\xd0:\x9b[4\x8d\x01\x10\x98x\xc5\xb0\xe7d\xa3\xf0\xeeU\x92\x9a\xab\x96\x0f\xff\xa9i\x8c\x91\x1a\xc2\xe7\xd9!\xf3\xd7\xfd\x02\xa2\x84=\xe4 \x04\'\xdf\xdb\xa3i\x0cBF\x9b,\xce0\xd2\x8a\x8aPx\xd7JI\xb5\xe3B}\x03z\xce\x9c\xd54\xc6X\x0e\xe1\tC\x10L({\xf6w\x92\x07\x12\xbf\xd8\xb5[\xf3\x18\xc3\xfd\x10\xce\x8e8r=X\t\xe7\x02i\xdb\x98\x87\xfa\xdd8\xfd\xc1~\xcdc\x10\x90\xd1&\x8b\x0f\x0c\xc7\xdcR,|\xe2\x97\x92;q\x9f\xedx\x0b\x03}}\x9a\xc7@xRW\x13\xc3\x96\x99\x81\xf2-\x9b%\x9fA\xe2\xf3xQ\xbf\xf5o\xba\xc0\x08I\xeajbX\x1d\xe9\xf8\xfe\x8em\xb0g9c\xa8\x1d;\xe1\xe9\xec\xd2\x05FH\xc7P-\x8c\xd4Y\xdf\xc4\xaa];\x91V4K2\xc6`_\x1f\xea\xb6l\xd3\r\x06\x01`V\x0b\xc3d\x12Q\\\xf1C,~\xfaI\x98\x13l1\r\x00\x1e\xda\xf0\x12<\xed\xed\xba\xc1\x18\x1b\\d\x89\x91\x90\x95\x85\xbc\xef|\x1b%\x95\x15H\x91q\x0e\xc9\xf9\xfa\x06\x9c\xf8G\x95\xae0\x08!0\xb3\xc0\xb8\xef\xf8!\xf8=\x1e\x98\xed\t\xb0\xa5\xa7Cn\t\x0c\r\xa1\xfa\xa9\xf5\xe3v\xcd\xea\x03\x03\x00\xcc,j\x86\xcd\x91\x0e@>\xc4h\xa9\xf9\xf53\xe8hn\xd1\x1d\xc6pRg\xd0L)Y>}s;NT\xbd\xa3K\x0c`\xfcX\x16\xcd\xbb)\x85\xca\x99CGq\xf0\x0f\xcf\xeb\x16c\x0c\x84\xf6\xad\xad\x12\xe5\\m\x1d\xf6<\xbcf\xe4\xd8\x0b}b`xN\x9d\xfe\xf1\xdb\xf2k\xc6\x11\xecZ\xfd \x86\xdc\x1e]c t\xc6\x90\xdeY\xe8r\xca\x89\xb7\xde\xc6\xee\x1f=\x0c\xdf\xc0\x80\xee10\xda1\xa4}0},\xc5\xe7\xf5\xa2f\xfd\xef\xf1\xf9\xbb\xbbu\x9d3&\x82P\xc6\x88\x85\xa3\xf5X-\xaa\x9f\xfe\r\xba\xbe\xfcJ3\x18\xbe\xc4T\xb4-\xb9\x07A\x8b5d)\xd1\xf8\x07\x82o\x10\t-\x8d\xb0\x9f\xaa\x9b\n\x84\xfeW6DS:N\x9d\xc6\xb1M\xaf\xe2\xf4\xde}\x9a\xeb\x81\xf7\x16-\x84\x7f\xce|,\x99=\x1d\x1f\x9fh\x8d\xf8\x1e=\x05s\x01B`?]\x1f\tD]\x0c\x12\x0c\xa2\xf5X->\xdb\xb1\x13\xcd\xfb\xabA\x02\x01M\x0e\x87\x04\xcd"\xec\x163n\xc8\xcf\xb8&\x08\x00\xb8\x8b\xe6E\x06a\xf1e&\x93\xcda\\l\xf8\x14_\x1f\xfc7\x9a\xf7}\x84\xdes\xe7u1\x9f\xd1\xd97\x80\x97\xdeo\x98\xfa\x8f0\xde\x16M\x0e\xa1\xf7\xcd2G7\xbc\x08\x9f\xc7\x8b+\xe7/\xe0Jk+\xbaF\xce1\xd4\xc3\x1c\xf8X4\n\xf5\xb7\x84\xaaB\x17Q\xfbk~\xb4\x86\x11\x14\xcd\xe8\x99s3\x82#\xcb\x94\x08\x01:\x12S\xe1IN\x9b\xf0\x01\x8b\xd6\x04X\xb3\nBkAg\x0b6-?>\xf68\x18$\xf8\xf0\xaf-h\xaa\xef\x18\x1d\\40\xa4\xd4\x8c\x1eW\x19./\xbd\'\xf4/\x1b\x80=\xdaj \np\xdd\x1cz\xd0\xb3 \x00M\xf5\x1d0\x19\x18\xd2\x9b)\xbf\xd5\x06\xa5\x8b9N\x1c?\x96e`H\xce\x192J\xf17"\xff\x9b\xc9\xc0`\x9b\xc0\xcd\xa6\x00\x1e-\xef\x88\xe2.\xcb\xc0\x904\x1c\x12^,\xbd_#=\xfe\xc251\\\xf9q\xa8\\>\x88\x9cd\xef\x14 \x06\x86,\x0c\x00(L\xbc\x88\xcdk\xdc\xb2\x9b3\x93\x81\x11\xdb@!\xadb20\xf8\xc1\x08M\xea\x06F\xf4C\xe8~\xbf\xe2\x10\xfd=\x83\x93\xad:10\xa2\x99\xcfH<u\x1cC\x993\x10\xb4\\\xed\x8f\xa4L\xbf\x82\xf0m\xffm\x97\xbdh\xbb<1\xaf\xb8{}\xe8j\xea\x1f{<\xe4\t\xe0\xd0\x9e\xb3\xe1\x13T\x06F\xb4\x93Kb\x7f\x0f2\xf6m\x0b\xf9\x90\x17\xfc\xac\x18@q\xc85g\xa6\r\xce\xcc\x89\x9d\xc8\xa6\xbaNl}\xf9d\xe4\x1cb`\xc8\x9f\xe9S0\xa9\x1b\x18J`\x0c\xf4\xfb\xa6\xfe\xb4\x13o\x07,\xc5Q\xdce\x19\x18\xb2kF\xe3\xbf\xda04\x18\x98b\xa1\xc09 \xd0\x05\xbf/\xf2\xf3\xcc\x06\x862\xcdT\xdbY7\xfe\xf8\xc0\x11\x94\xaf.@\xd2\xb4H\x9b\x8e\xda\x11\x0c\x12\xec}\xa39\xf2|\xc8\xd6\xbc\xd9\xc4\xc0P/g\x84\x97\xff\x03\x83\xd6\xf0\xae\xa5\x99d\xba\x00\x00\x00\x00IEND\xaeB`\x82'

class window: #! Make this a toplevel and get rid of children['root']
   __slots__ = ("properties","children","childproperties","images","aboutwindow","menubar")
   def __init__(self,width,height,title="Python",color="#FFFFFF",mainwindow:bool=True,defaultmenu:bool=True,nomenu:bool=False,dwidth=None,dheight=None,flashIcon=False):
      self.properties = {"mult":100,"fullscreen":False,"startwidth":width,"startheight":height,"dwidth":dwidth,"dheight":dheight,"mainwindow":mainwindow,"color":color,"nm":1,'width':width,'height':height}
      self.children = {}
      self.menubar = {}
      self.images = {'':itkBlankImage(self,'',(0,0))}
      if mainwindow == True:
         self.aboutwindow = [False,"placeholdertext",{}]
         self.children["root"] = itkRootTk()
      else:
         self.aboutwindow = None
         self.children["root"] = itkRootToplevel()
      if flashIcon == False:
         self.setIcon(fileBytes=DefaultIcon.FLASH_PY)
      else:
         self.setIcon(fileBytes=DefaultIcon.FLASH)
      if nomenu == False:
         if defaultmenu == True:
            self.menubar["root"] = tkinter.Menu(self.children["root"], bd=1)
            self.menubar["filemenu"] = tkinter.Menu(self.menubar["root"], tearoff=0)
            self.menubar["filemenu"].add_command(label="Quit", font=("Terminal",8), command=self.endProcess)
            self.menubar["root"].add_cascade(label="File", font=("Terminal",8), menu=self.menubar["filemenu"])
            self.menubar["viewmenu"] = tkinter.Menu(self.menubar["root"], tearoff=0)
            self.menubar["viewmenu"].add_command(label="Full Screen", font=("Terminal",8), command=self.togglefullscreen)
            self.menubar["viewmenu"].add_command(label="Reset Size", font=("Terminal",8), command=self.resetSize)
            self.menubar["root"].add_cascade(label="View", font=("Terminal",8), menu=self.menubar["viewmenu"])
            self.menubar["controlmenu"] = tkinter.Menu(self.menubar["root"], tearoff=0)
            self.menubar["controlmenu"].add_command(label="Controls", font=("Terminal",8))
            self.menubar["root"].add_cascade(label="Control", font=("Terminal",8), menu=self.menubar["controlmenu"])
            if mainwindow == True:
               self.menubar["helpmenu"] = tkinter.Menu(self.menubar["root"], tearoff=0)
               self.menubar["helpmenu"].add_command(label="About", font=("Terminal",8), command=self.aboutwin)
               self.menubar["root"].add_cascade(label="Help", font=("Terminal",8), menu=self.menubar["helpmenu"])
            self.children["root"].config(menu=self.menubar["root"])
         else:
            self.menubar["root"] = tkinter.Menu(self.children["root"], bd=1)
            self.children["root"].config(menu=self.menubar["root"])
      self.children["root"].title(title)
      self.properties["dwidth"] = self.properties["startwidth"] if dwidth == None else dwidth
      self.properties["dheight"] = self.properties["startheight"] if dheight == None else dheight
      if as3state.width not in {-1,None} and as3state.height not in {-1,None}:
         self.children["root"].maxsize(as3state.width,as3state.height)
      self.children["display"] = itkDisplay(self.children["root"],itkWindow=self,background=self.properties["color"])
      self.children["display"].update()
      self.children["root"].bind("<Configure>",self.doResize)
      self.children["root"].geometry(f"{self.properties['dwidth']}x{self.properties['dheight']}")
      self.children["root"].bind("<Escape>",self.outfullscreen)
   def __getattr__(self, key):
      return self.children[key]
   def resetSize(self):
      self.children["root"].geometry(f"{self.properties['dwidth']}x{self.properties['dheight']}")
   def group(self, object_:object):
      self.children["root"].group(object_)
   def toTop(self):
      self.children["root"].lift()
   def forceFocus(self, child:str):
      self.children[child].focus_force()
   def minimumSize(self,type_:str="b",**kwargs):
      """
      type_ must be either 'w','h',or 'b' (meaning width, height, or both). If nothing is passed, assumed to be 'b' (both)
      kwargs must include width, height, or both depending on what you chose for type_
      if 'w' or 'height' is chosen, the other will be assumed based on the ration of the original size
      """
      if type_ == "w":
         if self.properties["mainwindow"] == True:
            self.children["root"].minsize(kwargs["width"],int((kwargs["width"]*self.properties["startheight"])/self.properties["startwidth"]) + 28)
         else:
            self.children["root"].minsize(kwargs["width"],int((kwargs["width"]*self.properties["startheight"])/self.properties["startwidth"]))
      elif type_ == "h":
         if self.properties["mainwindow"] == True:
            self.children["root"].minsize(int((self.properties["startwidth"]*kwargs["height"])/self.properties["startheight"]) - 52,kwargs["height"])
         else:
            self.children["root"].minsize(int((self.properties["startwidth"]*kwargs["height"])/self.properties["startheight"]),kwargs["height"])
      elif type_ == "b":
         self.children["root"].minsize(kwargs["width"],kwargs["height"])
      else:
         as3.trace("Invalid type")
   def minimumSizeReset(self):
      if self.properties["mainwindow"] == True:
         self.children["root"].minsize(262,int((262*self.properties["startheight"])/self.properties["startwidth"]) + 28)
      else:
         self.children["root"].minsize(262,int((262*self.properties["startheight"])/self.properties["startwidth"]))
   def resizefont(self, font:tuple, mult):
      return (font[0],cmath.resizefont(font[1],mult))
   def setIcon(self, file=None, fileBytes=None):
      if file != None:
         img = file
      elif fileBytes != None:
         img = BytesIO(fileBytes)
      else:
         as3.trace("interface_tk.window.setIcon: Error: called but no icon specified")
         pass
      self.children["root"].iconphoto(True,PIL.ImageTk.PhotoImage(PIL.Image.open(img)))
   def mainloop(self):
      if self.properties["mainwindow"] == False:
         as3.trace("Can not run mainloop on a child window.")
      else:
         self.resizeChildren()
         self.children["root"].mainloop()
   def enableResizing(self):
      self.children["root"].resizable(True,True)
   def disableResizing(self):
      self.children["root"].resizable(False,False)
   def endProcess(self):
      with helpers.recursionDepth(100000): #workaround for python sefaulting while doing this
         self.children["root"].destroy()
   def closeWindow(self):
      self.children["root"].destroy()
   def togglefullscreen(self):
      if self.properties["fullscreen"] == True:
         self.outfullscreen()
      else:
         self.gofullscreen()
   def gofullscreen(self):
      self.properties["fullscreen"] = True
      self.children["root"].attributes("-fullscreen", True)
   def outfullscreen(self, useless=""):
      self.properties["fullscreen"] = False
      self.children["root"].attributes("-fullscreen", False)
   def setAboutWindowText(self, text):
      if self.aboutwindow:
         self.aboutwindow[1] = text
         if "label" in self.aboutwindow[2]:
            self.aboutwindow[2]["label"].configure(text=text)
   def aboutwin(self):
      if self.aboutwindow:
         if self.aboutwindow[0]:
            self.aboutwindow[2]["window"].lift()
         else:
            self.aboutwindow[2]["window"] = tkinter.Toplevel()
            self.aboutwindow[2]["window"].geometry("350x155")
            self.aboutwindow[2]["window"].resizable(False,False)
            self.aboutwindow[2]["window"].transient(self.children["root"])
            self.aboutwindow[2]["window"].configure(background=self.properties["color"])
            self.aboutwindow[2]["window"].bind("<Destroy>",self.closeabout)
            self.aboutwindow[2]["label"] = tkinter.Label(self.aboutwindow[2]["window"], font=("TkTextFont",9), justify="left", text=self.aboutwindow[1], background=self.properties["color"])
            self.aboutwindow[2]["label"].place(anchor="nw", x=7, y=9)
            self.aboutwindow[2]["okbutton"] = tkinter.Button(self.aboutwindow[2]["window"], text="OK", command=self.closeabout, background=self.properties["color"])
            self.aboutwindow[2]["okbutton"].place(anchor="nw", width=29, height=29, x=299, y=115)
            self.aboutwindow[0] = True
   def closeabout(self,*e):
      if self.aboutwindow:
         self.aboutwindow[2]["window"].destroy()
         self.aboutwindow[2].clear()
         self.aboutwindow[0] = False
   def addWidget(self, widget, master:str, name:str, **kwargs):
      if master == "root":
         master = "display"
      if not as3.isXMLName(master):
         as3.trace("Invalid Master")
      elif not as3.isXMLName(name):
         as3.trace("Invalid Name")
      else:
         self.children[name] = widget(self.children[master],itkWindow=self,**kwargs)
         self.children[name].resize()
   def addButton(self, master:str, name:str, **kwargs):
      self.addWidget(itkButton, master, name, **kwargs)
   def addLabel(self, master:str, name:str, **kwargs):
      self.addWidget(itkLabel, master, name, **kwargs)
   def addnwhLabel(self, master:str, name:str, **kwargs):
      self.addWidget(itknwhLabel, master, name, **kwargs)
   def addFrame(self, master:str, name:str, **kwargs):
      self.addWidget(itkFrame, master, name, **kwargs)
   def addHTMLScrolledText(self, master:str, name:str, **kwargs):
      self.addWidget(itkHTMLScrolledText, master, name, **kwargs)
   def addHTMLText(self, master:str, name:str, **kwargs):
      self.addWidget(HTMLText, master, name, **kwargs)
   def addImage(self, image_name:str, image_data, size:tuple=None):
      """
      size - the target (display) size of the image before resizing
      if size is not defined it is assumed to be the actual image size
      """
      if image_name == '':
         raise Error('interface_tk.window.addImage; image_name can not be empty string')
      self.images[image_name] = itkImage(self,image_data,size)
      self.images[image_name].resize()
   def addImageLabel(self, master:str, name:str, **kwargs):
      self.addWidget(itkImageLabel, master, name, **kwargs)
   def addScrolledListbox(self, master:str, name:str, **kwargs):
      self.addWidget(itkScrolledListBox, master, name, **kwargs)
   def slb_Insert(self, child:str, position, item):
      self.children[child].insert(position,item)
   def slb_Delete(self, child:str, start, end):
      self.children[child].delete(start, end)
   def addEntry(self, master:str, name:str, **kwargs):
      self.addWidget(itkEntry, master, name, **kwargs)
   def addCheckboxWithLabel(self, master:str, name:str, **kwargs):
      self.addWidget(CheckboxWithLabel, master, name, **kwargs)
   def addCheckboxWithEntry(self, master:str, name:str, **kwargs):
      self.addWidget(CheckboxWithEntry, master, name, **kwargs)
   def addCheckboxWithCombobox(self, master:str, name:str, **kwargs):
      self.addWidget(CheckboxWithCombobox, master, name, **kwargs)
   def addFileEntryBox(self, master:str, name:str, **kwargs):
      self.addWidget(FileEntryBox, master, name, **kwargs)
   def addNotebook(self, master:str, name:str, **kwargs):
      self.addWidget(itkNotebook, master, name, **kwargs)
   def addNBFrame(self, master:str, name:str, **kwargs):
      text = kwargs.pop('text','')
      self.addWidget(itkNBFrame, master, name, **kwargs)
      self.children[master].add(self.children[name],text=text)
   def addLabelWithRadioButtons(self, master:str, name:str, **kwargs):
      self.addWidget(ComboLabelWithRadioButtons, master, name, **kwargs)
   def resizeChildren(self):
      for i in self.images.values():
         i.resize()
      for i in self.children.values():
         i.resize()
   def bindChild(self, child:str, tkevent, function):
      self.children[child].bind(tkevent, function)
   def configureChildren(self, children:list|tuple, **kwargs):
      for attr,value in kwargs.items():
         if attr == "background":
            for child in children:
               self.children[child].background = value
         elif attr in {"x","y","width","height","font","anchor"}:
            for child in children:
               setattr(self.children[child], attr, value)
               self.children[child].resize()
         elif attr == "text":
            for child in children:
               self.children[child].text = value
         elif attr == "textadd":
            for child in children:
               self.children[child].text = self.children[child].text + value
         elif attr in {"text1","text2"}:...
         elif attr == "indent":...
         elif attr == "foreground":
            for child in children:
               self.children[child].foreground = value
         elif attr == "image":
            for child in children:
               self.children[child].image_name = value
         elif attr == "htmlfontbold":
            for child in children:
               self.children[child].bold = value
         elif attr == "sbwidth":
            for child in children:
               self.children[child].sbwidth = int(value)
         elif attr == "addTab":
            for child in children:
               if self.children[child]._intNanem == "Notebook":
                  self.children[child].add(self.children[value[0]],text=value[1])
         else:
            for child in children:
               self.children[child][attr] = value
   def configureChild(self, child:str, **args):
      if child == "root":
         return
      for attr,value in args.items():
         if attr == "background":
            self.children[child].background = value
         elif attr in {"x","y","width","height","font","anchor"}:
            setattr(self.children[child], attr, value)
            self.children[child].resize()
         elif attr == "text":
            self.children[child].text = value
         elif attr == "textadd":
            self.children[child].text = self.children[child].text + value
         elif attr in {"text1","text2"}:...
         elif attr == "indent":...
         elif attr == "foreground":
            self.children[child].foreground = value
         elif attr == "image":
            self.children[child].image_name = value
         elif attr == "htmlfontbold":
            self.children[child].bold = value
         elif attr == "sbwidth":
            self.children[child].sbwidth = int(value)
         elif attr == "addTab" and self.children[child]._intName == "Notebook":
            self.children[child].add(self.children[value[0]],text=value[1])
         else:
            self.children[child][attr] = value
   def destroyChild(self, child:str):
      if child in {"display","root"}:
         return
      if self.children[child]._intName == "ImageLabel":
         self.images[self.children[child].image_name].references -= 1
      self.children[child].destroy()
      self.children.pop(child)
   def getChildAttribute(self, child:str, attribute:str):
      if child in self.children and self.children[child]._intName == "Entry" and attribute == "text":
         return self.children[child].text
      return self.children[child].cget(attribute)
   def getChildAttributes(self, child:str, *args:str):
      return {i:self.getChildAttribute(child,i) for i in args}
   def doResize(self, event):
      if event.widget == self.children["root"]:
         self.properties['width'], self.properties['height'] = self.children["root"].winfo_width(), self.children["root"].winfo_height()
         mult = cmath.calculate(self.properties['width'],self.properties['height'],self.properties["startwidth"],self.properties["startheight"])
         if mult != self.properties["mult"]:
            self.properties["mult"] = mult
            self.properties["nm"] = mult/100
            self.resizeChildren()

if __name__ == "__main__": #! Update this
   #Test
   from platform import python_version
   testcolor = 0
   fontBold = False
   def test_changebold():
      global fontBold
      if fontBold == True:
         fontBold = False
         return False
      elif fontBold == False:
         fontBold = True
         return True
   def test_cyclecolor():
      global testcolor
      testcolorlist = ("#FFFFFF","#8F2F9F","#AAAAAA")
      testcolor += 1
      if testcolor >= 3:
         testcolor = 0
      return testcolorlist[testcolor]
   root = window(1176,662,title="Adobe Flash Projector-like Window Demo")
   root.setAboutWindowText(f"Adobe Flash Projector-like window demo.\n\nPython {python_version()}")
   root.addButton("root","testbutton1",130,0,130,30,("Times New Roman",12))
   root.configureChild("testbutton1",command=lambda: root.configureChild("testtext", background=test_cyclecolor()))
   root.addLabel("root","testlabel1",0,30,100,20,("Times New Roman",12))
   root.addHTMLScrolledText("root","testtext",0,50,600,400,("Times New Roman",12),anchor="nw")
   root.addHTMLText("root","testtext2",601,50,400,400,("Times New Roman",12),anchor="nw")
   root.configureChild("testtext", text="TestTextpt1\n\nTestTextpt2", cursor="arrow", wrap="word")
   root.configureChild("testtext2", text="HTMLTextTest\n\ntext", cursor="arrow", wrap="word")
   root.configureChild("testbutton1", text="st_colourtest")
   root.configureChild("testlabel1", text="TestLabel")
   secondwindow = window(400,400,title="Second Window",mainwindow=False,nomenu=True)
   secondwindow.group(root.children["root"])
   root.addButton("root","testbutton2",0,0,130,30,("Times New Roman",12))
   root.configureChild("testbutton2",command=lambda: secondwindow.toTop()) 
   root.configureChild("testbutton2", text="liftsecondwindow")
   root.addButton("root","testbutton3",260,0,130,30,("Times New Roman",12))
   root.configureChild("testbutton3",command=lambda: root.configureChild("testtext",htmlfontbold=test_changebold()))
   root.configureChild("testbutton3", text="st_boldtest")
   root.addScrolledListbox("root","testslb",0,450,150,150,("Times New Roman",12))
   for i in range(1,21):
      root.slb_Insert("testslb", "end", i)
   root.mainloop()
