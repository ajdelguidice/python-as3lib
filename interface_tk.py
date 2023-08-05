import tkinter
import tkhtmlview
import re

"""
Warning: To acheive the things that I did in this module I had to use both eval and exec.
"""

class window:
   def __init__(self, width, height, title="Python",_type="canvas", color="#FFFFFF"):
      self.oldmult = 100
      self.aboutwindowtext = "placeholdertext"
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
      self.helpmenu.add_command(label="About Game", font=("Terminal",8), command=self.aboutwin)
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
      try:
         self.childlist.append([name,"HTMLScrolledText",x,y,width,height,font,anchor])
      except:
         self.childlist = [[name,"HTMLScrolledText",x,y,width,height,font,anchor]]
      self.resizeChild(name, self.oldmult)
   def HTMLSTUpdateText(self, child:str):
      eval(f"self.{child}")["state"] = "normal"
      for i in self.childlist:
         if i[0] == child:
            font = i[6]
            fontsize = font[1]
            break
      text = re.sub("retfunc", "\n", eval(f"self.{child}text"))
      text = re.sub("doublequotefunc", "\"", text)
      text = re.sub("quotefunc", "'", text)
      if self.stfontbold == True:
         text = "<b>" + text + "</b>"
      text = "<pre style=\"color: " + eval(f"self.{child}fg") + "; background-color: " + eval(f"self.{child}bg") + f"; font-size: {fontsize}px; font-family: {font[0]}\">{text}</pre>"
      eval(f"self.{child}").set_html(text)
      eval(f"self.{child}")["state"] = "disabled"
   def resizeChildren(self, mult):
      for i in self.childlist:
         eval(f"self.{i[0]}").place(x=i[2]*mult/100,y=i[3]*mult/100,width=i[4]*mult/100,height=i[5]*mult/100,anchor=i[7])
         if i[1] != "Frame":
            f = i[6]
            eval(f"self.{i[0]}")["font"] = (f[0],self.round(f[1]*mult/100))
   def resizeChild(self, child:str, mult):
      for i in self.childlist:
         if i[0] == child:
            eval(f"self.{i[0]}").place(x=i[2]*mult/100,y=i[3]*mult/100,width=i[4]*mult/100,height=i[5]*mult/100,anchor=i[7])
            if i[1] != "Frame":
               f = i[6]
               eval(f"self.{i[0]}")["font"] = (f[0],self.round(f[1]*mult/100))
            break
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
                  text = re.sub("(\t)", "    ", v[i])
                  text = re.sub("(\n)", "retfunc", text)
                  text = re.sub("'", "quotefunc", text)
                  text = re.sub("doublequotefunc", "\"", text)
                  if j[1] == "HTMLScrolledText":
                     if k[i] == "text":
                        exec(f"self.{j[0]}text = f'{text}'")
                     else:
                        exec(f"self.{j[0]}text += f'{text}'")
                     self.HTMLSTUpdateText(j[0])
                  else:
                     eval(f"self.{child}")[k[i]] = text
                  break
         elif k[i] == "background" or k[i] == "foreground":
            for j in self.childlist:
               if j[0] == child:
                  if j[1] == "HTMLScrolledText":
                     if k[i] == "background":
                        exec(f"self.{j[0]}bg = f'{v[i]}'")
                     else:
                        exec(f"self.{j[0]}fg = f'{v[i]}'")
                     self.HTMLSTUpdateText(j[0])
                  else:
                     eval(f"self.{child}")[k[i]] = v[i]
         else:
            eval(f"self.{child}")[k[i]] = v[i]
         for j in self.childlist:
            if j[0] == child:
               if j[1] == "HTMLScrolledText":
                  self.HTMLSTUpdateText(j[0])
               break
         i += 1
   def destroyChild(self, child:str):
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
         #print(mult)
         return mult
   def set_size(self, mult):
      newwidth = self.root.winfo_width()
      newheight = self.root.winfo_height()
      self.display.place(anchor="center", width=self.startwidth*mult/100, height=self.startheight*mult/100, x=newwidth/2, y=newheight/2)

if __name__ == "__main__":
   #Test
   from platform import python_version
   root = window(1176,662,title="Adobe Flash Projector-like Window Test",_type="canvas")
   placeholderversion = "0.0.1"
   root.setAboutWindowText(f"Adobe Flash Projector-like window test version {placeholderversion}\n\nPython {python_version()}")
   root.addButton("root","testbutton1",0,0,130,30,("Times New Roman",12))
   root.testbutton1["command"] = lambda: print("test")
   root.addLabel("root","testlabel1",0,30,100,20,("Times New Roman",12))
   root.addHTMLScrolledText("root","testtext",0,50,600,400,("Times New Roman",12),anchor="nw")
   root.configureChild("testtext", text="TestText", cursor="arrow", wrap="word")
   root.configureChild("testbutton1", text="TestButton")
   root.configureChild("testlabel1", text="TestLabel")
   root.mainloop()