import tkinter
import tkhtmlview
import re
import PIL
from io import BytesIO as btio
"""
Warning: To acheive the things that I did in this module I had to use both eval and exec.
Notes:
- Canvas is not supported yet even though there is an option for it 
- Scrollbars in the htmlscrolledtext widget don't change size but that is a small price to pay for this working
- Commands aren't implemented yet so you have to set them manually
Todo:
- Optimize refresh for HTMLScrolledText
- Replace the eval and exec statements with dictionaries where possible
- Optimize image resizing
"""

class window:
   def __init__(self, width, height, title="Python",_type="canvas", color="#FFFFFF"):
      self.oldmult = 100
      self.aboutwindowtext = "placeholdertext"
      self.oimagedict = {}
      self.rimagedict = {}
      self.otext = {}
      self.ftext = {}
      self.childlist = []
      self.stfontbold = False
      self.startwidth = width
      self.startheight = height
      self.color = color
      self.root = tkinter.Tk()
      self.root.title(title)
      self.root.geometry(f"{self.startwidth}x{self.startheight}")
      self.root.minsize(262,175)
      if _type == "canvas":
         self.display = tkinter.Canvas(self.root, background=self.color, confine=True)
         self.display.place(anchor="center", width=1176, height=662, x=588, y=331)
      elif _type == "frame":
         self.display = tkinter.Frame(self.root, background=self.color)
         self.display.place(anchor="center", width=1176, height=662, x=588, y=331)
      else:
         raise Exception("_type must be either frame or canvas.")
      self.menubar = tkinter.Menu(self.root, bd=1)
      self.filemenu = tkinter.Menu(self.menubar, tearoff=0)
      self.filemenu.add_command(label="Quit", font=("Terminal",8), command=self.endProcess)
      self.menubar.add_cascade(label="File", font=("Terminal",8), menu=self.filemenu)
      self.viewmenu = tkinter.Menu(self.menubar, tearoff=0)
      self.viewmenu.add_command(label="Full Screen", font=("Terminal",8), command=self.gofullscreen)
      self.menubar.add_cascade(label="View", font=("Terminal",8), menu=self.viewmenu)
      self.controlmenu = tkinter.Menu(self.menubar, tearoff=0)
      self.controlmenu.add_command(label="Controls", font=("Terminal",8))
      self.menubar.add_cascade(label="Control", font=("Terminal",8), menu=self.controlmenu)
      self.helpmenu = tkinter.Menu(self.menubar, tearoff=0)
      #helpmenu.add_command(label="Help")
      self.helpmenu.add_command(label="About", font=("Terminal",8), command=self.aboutwin)
      self.menubar.add_cascade(label="Help", font=("Terminal",8), menu=self.helpmenu)
      self.root.config(menu=self.menubar)
      self.root.bind("<Configure>",self.doResize)
      self.root.bind("<Escape>",self.outfullscreen)
   def round(self, num):
      tempList = str(num).split(".")
      tempList[1] = f".{tempList[1]}"
      if float(tempList[1]) >= 0.5:
         return int(tempList[0]) + 1
      else:
         return int(tempList[0])
   def tupletolist(self, tup):
      templist = []
      for i in tup:
         templist.append(i)
      return templist
   def listtotuple(self, li):
      return tuple(li)
   def resizefont(self, font:tuple, mult):
      tempfont = self.tupletolist(font)
      tempfont[1] = self.round(font[1]*mult/100)
      tempfont = self.listtotuple(tempfont)
      return tempfont
   def mainloop(self):
      self.root.mainloop()
   def enableResizing(self):
      self.root.resizable(True,True)
   def disableResizing():
      self.root.resizable(False,False)
   def endProcess(self):
      self.root.destroy()
   def gofullscreen(self):
      self.root.attributes("-fullscreen", True)
   def outfullscreen(self, useless):
      self.root.attributes("-fullscreen", False)
   def setAboutWindowText(self, text):
      self.aboutwindowtext = text
   def aboutwin(self):
      self.aboutwindow = tkinter.Toplevel(borderwidth=1)
      self.aboutwindow.geometry("350x155")
      self.aboutwindow.resizable(False,False)
      self.aboutwindow.group(self.root)
      self.aboutwindow.configure(background=self.color)
      self.aboutlabel1 = tkinter.Label(self.aboutwindow, font=("TkTextFont",9), justify="left", text=self.aboutwindowtext, background=self.color)
      self.aboutlabel1.place(anchor="nw", x=7, y=9)
      self.aboutokbutton = tkinter.Button(self.aboutwindow, text="OK", command=self.closeabout, background=self.color)
      self.aboutokbutton.place(anchor="nw", width=29, height=29, x=299, y=115)
   def closeabout(self):
      self.aboutwindow.destroy()
   def addButton(self, master:str, name:str, x, y, width, height, font, anchor:str="nw"):
      if master == "root":
         master = "display"
      exec(f"self.{name} = tkinter.Button(self.{master})")
      eval(f"self.{name}").place(x=x,y=y,width=width,height=height,anchor=anchor)
      try:
         self.childlist.append([name,"Button",x,y,width,height,font, anchor])
      except:
         self.childlist = [[name,"Button",x,y,width,height,font, anchor]]
      self.resizeChild(name, self.oldmult)
   def addLabel(self, master:str, name:str, x, y, width, height, font, anchor:str="nw"):
      if master == "root":
         master = "display"
      exec(f"self.{name} = tkinter.Label(self.{master})")
      eval(f"self.{name}").place(x=x,y=y,width=width,height=height,anchor=anchor)
      try:
         self.childlist.append([name,"Label",x,y,width,height,font,anchor])
      except:
         self.childlist = [[name,"Label",x,y,width,height,font,anchor]]
      self.resizeChild(name, self.oldmult)
   def addFrame(self, master:str, name:str, x, y, width, height, anchor:str="nw"):
      if master == "root":
         master = "display"
      exec(f"self.{name} = tkinter.Frame(self.{master})")
      eval(f"self.{name}").place(x=x,y=y,width=width,height=height,anchor=anchor)
      try:
         self.childlist.append([name,"Frame",x,y,width,height,"",anchor])
      except:
         self.childlist = [[name,"Frame",x,y,width,height,"",anchor]]
      self.resizeChild(name, self.oldmult)
   def addHTMLScrolledText(self, master:str, name:str, x, y, width, height, font, anchor:str="nw"):
      if master == "root":
         master = "display"
      exec(f"self.{name} = tkhtmlview.HTMLScrolledText(self.{master})")
      eval(f"self.{name}").place(x=x,y=y,width=width,height=height,anchor=anchor)
      exec(f"self.{name}text = ''")
      exec(f"self.{name}bg = '#FFFFFF'")
      exec(f"self.{name}fg = '#000000'")
      self.otext[f"{name}"] = ""
      self.ftext[f"{name}"] = ""
      try:
         self.childlist.append([name,"HTMLScrolledText",x,y,width,height,font,anchor])
      except:
         self.childlist = [[name,"HTMLScrolledText",x,y,width,height,font,anchor]]
      self.resizeChild(name, self.oldmult)
   def prepareHTMLSTForEval(self, child:str, text:str):
      if self.otext[f"{child}"] == text:
         self.HTMLSTUpdateText(child, True)
      else:
         self.otext[f"{child}"] = text
         self.HTMLSTUpdateText(child)
   def HTMLSTUpdateText(self, child:str, rt=False):
      eval(f"self.{child}")["state"] = "normal"
      for i in self.childlist:
         if i[0] == child:
            font = i[6]
            fontsize = font[1]
            break
      if rt == False:
         self.ftext[f"{child}"] = re.sub("(\t)", "    ", self.otext[f"{child}"])
      text = self.ftext[f"{child}"]
      if self.stfontbold == True:
         text = "<b>" + text + "</b>"
      text = "<pre style=\"color: " + eval(f"self.{child}fg") + "; background-color: " + eval(f"self.{child}bg") + "; font-size: " + f"{int(fontsize*self.oldmult/100)}px; font-family: {font[0]}\">{text}</pre>"
      eval(f"self.{child}").set_html(text)
      eval(f"self.{child}")["state"] = "disabled"
   def addImage(self, image_name:str, image_data):
      self.oimagedict[f"{image_name}"] = image_data
   def addImageLabel(self, master:str, name:str, x, y, width, height, anchor:str="nw", image_name:str=""):
      if master == "root":
         master = "display"
      self.resizeImage((width,height), image_name)
      exec(f"self.{name} = tkinter.Label(self.{master})")
      eval(f"self.{name}").place(x=x,y=y,width=width,height=height,anchor=anchor)
      eval(f"self.{name}")["image"] = self.rimagedict[f'{image_name}']
      try:
         self.childlist.append([name,"ImageLabel",x,y,width,height,"",anchor,image_name])
      except:
         self.childlist = [[name,"ImageLabel",x,y,width,height,"",anchor,image_name]]
      self.resizeChild(name, self.oldmult)
   def resizeImage(self, size:tuple, image_name):
      img = PIL.Image.open(btio(self.oimagedict[f"{image_name}"]))
      img.thumbnail(size)
      self.rimagedict[f"{image_name}"] = PIL.ImageTk.PhotoImage(img)
   def resizeChildren(self, mult):
      for i in self.childlist:
         eval(f"self.{i[0]}").place(x=i[2]*mult/100,y=i[3]*mult/100,width=i[4]*mult/100,height=i[5]*mult/100,anchor=i[7])
         if i[1] == "HTMLScrolledText":
            self.HTMLSTUpdateText(i[0])
         elif i[1] == "ImageLabel":
            self.resizeImage((int(i[4]*mult/100),int(i[5]*mult/100)),i[8])
            eval(f"self.{i[0]}")["image"] = self.rimagedict[f"{i[8]}"]
         elif i[1] != "Frame":
            f = i[6]
            eval(f"self.{i[0]}")["font"] = self.resizefont(f,mult)
   def resizeChild(self, child:str, mult):
      for i in self.childlist:
         if i[0] == child:
            eval(f"self.{i[0]}").place(x=i[2]*mult/100,y=i[3]*mult/100,width=i[4]*mult/100,height=i[5]*mult/100,anchor=i[7])
            if i[1] == "HTMLScrolledText":
               self.HTMLSTUpdateText(i[0])
            elif i[1] == "ImageLabel":
               self.resizeImage((int(i[4]*mult/100),int(i[5]*mult/100)),i[8])
               eval(f"self.{i[0]}")["image"] = self.rimagedict[f"{i[8]}"]
            elif i[1] != "Frame":
               f = i[6]
               eval(f"self.{i[0]}")["font"] = self.resizefont(f,mult)
            break
   def bindChild(self, child:str, tkevent, function):
      eval(f"self.{child}").bind(tkevent, function)
   def configureChild(self, child:str, **args):
      k = []
      v = []
      for i in args.keys():
         k.append(i)
      for i in args.values():
         v.append(i)
      i = 0
      while i < len(k):
         if k[i] == "x" or k[i] == "y" or k[i] == "width" or k[i] == "height" or k[i] == "font" or k[i] == "anchor":
            for j in self.childlist:
               if j[0] == child:
                  newlist = self.childlist[j]
                  if k[i] == "x":
                     newlist[2] = v[i]
                  elif k[i] == "y":
                     newlist[3] = v[i]
                  elif k[i] == "width":
                     newlist[4] = v[i]
                  elif k[i] == "height":
                     newlist[5] = v[i]
                  elif k[i] == "font":
                     newlist[6] = v[i]
                  elif k[i] == "anchor":
                     newlist[7] = v[i]
                  self.childlist[j] = newlist
                  self.resizeChild(child)
                  break
         elif k[i] == "text" or k[i] == "textadd":
            for j in self.childlist:
               if j[0] == child:
                  if j[1] == "HTMLScrolledText":
                     if k[i] == "text":
                        text = v[i]
                     else:
                        text = self.otext[f"{child}"] + v[i]
                     self.prepareHTMLSTForEval(child, text)
                  else:
                     eval(f"self.{child}")[k[i]] = v[i]
                  break
         elif k[i] == "background" or k[i] == "foreground":
            for j in self.childlist:
               if j[0] == child:
                  if j[1] == "HTMLScrolledText":
                     if k[i] == "background":
                        exec(f"self.{j[0]}bg = f'{v[i]}'")
                     else:
                        exec(f"self.{j[0]}fg = f'{v[i]}'")
                     self.prepareHTMLSTForEval(child, self.otext[f"{child}"])
                  else:
                     eval(f"self.{child}")[k[i]] = v[i]
         elif k[i] == "image":
            for j in self.childlist:
               if j[0] == child:
                  j[8] = v[i]
                  break
            self.resizeChild(child, self.oldmult)
         else:
            eval(f"self.{child}")[k[i]] = v[i]
         #for j in self.childlist:
         #   if j[0] == child:
         #      if j[1] == "HTMLScrolledText":
         #         self.prepareHTMLSTForEval(child, otext[f"{child}"])
         #      break
         i += 1
   def destroyChild(self, child:str):
      i = 0
      htmlst = False
      while i < len(self.childlist):
         j = self.childlist[i]
         if j[0] == child:
            if j[1] == "HTMLScrolledText":
               htmlst = True
            self.childlist.pop(i)
            break
         i += 1
      if htmlst == True:
         self.otext.pop(f"{child}")
         self.ftext.pop(f"{child}")
      eval(f"self.{child}").destroy()
   def doResize(self, event):
      if event.widget == self.root:
         mult = self.calculate()
         self.set_size(mult)
         self.resizeChildren(mult)
   def calculate(self):
      newwidth = self.root.winfo_width()
      newheight = self.root.winfo_height()
      xmult = (100*newwidth)/self.startwidth
      ymult = (100*newheight)/self.startheight
      if xmult > ymult:
         mult = ymult
      elif xmult < ymult:
         mult = xmult
      elif xmult == ymult:
         mult = xmult
      if mult < 22.2789:
         mult = 22.2789
      if self.oldmult == mult:
         return self.oldmult
      else:
         self.oldmult = mult
         return mult
   def set_size(self, mult):
      newwidth = self.root.winfo_width()
      newheight = self.root.winfo_height()
      self.display.place(anchor="center", width=self.startwidth*mult/100, height=self.startheight*mult/100, x=newwidth/2, y=newheight/2)

if __name__ == "__main__":
   #Test
   from platform import python_version
   testcolor = 0
   def test_cyclecolor():
      global testcolor
      testcolorlist = ["#FFFFFF","#8F2F9F","#AAAAAA"]
      testcolor += 1
      if testcolor >= 3:
         testcolor = 0
      return testcolorlist[testcolor]
   root = window(1176,662,title="Adobe Flash Projector-like Window Test",_type="canvas")
   placeholderversion = "0.0.1"
   root.setAboutWindowText(f"Adobe Flash Projector-like window test version {placeholderversion}\n\nPython {python_version()}")
   root.addButton("root","testbutton1",0,0,130,30,("Times New Roman",12))
   root.testbutton1["command"] = lambda: root.configureChild("testtext", background=test_cyclecolor())
   root.addLabel("root","testlabel1",0,30,100,20,("Times New Roman",12))
   root.addHTMLScrolledText("root","testtext",0,50,600,400,("Times New Roman",12),anchor="nw")
   root.configureChild("testtext", text="TestText", cursor="arrow", wrap="word")
   root.configureChild("testbutton1", text="TestButton")
   root.configureChild("testlabel1", text="TestLabel")
   root.mainloop()