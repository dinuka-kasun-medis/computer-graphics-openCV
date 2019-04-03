import sys 
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from tkinter import filedialog as fd
from tkinter import messagebox
import cv2 
import numpy as np
#from tkinter import *

import graphic_support

parentImage=None
templateImage=None

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root,top
    root = tk.Tk()
    top = Toplevel1 (root)
    graphic_support.init(root, top)
    root.mainloop()

w = None
def create_Toplevel1(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = tk.Toplevel (root)
    top = Toplevel1 (w)
    graphic_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Toplevel1():
    global w
    w.destroy()
    w = None

def close_window (): 
    root.destroy()
    
def addImage():
    global parentImage
    parentImage=None
    filepath = fd.askopenfilename()
    parentImage=filepath
    if(parentImage):
        load = Image.open(filepath)
        load = load.resize((480,405), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(top.Canvas3,image=render)
        img.image = render
        img.place(relx=0.012, rely=0.012, height=405, width=480,anchor="nw")
    

def setTemplate():
    global templateImage
    templateImage=None
    filepath = fd.askopenfilename()
    templateImage=filepath
    if(templateImage):
        load = Image.open(filepath)
        load = load.resize((300,213), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(top.Template,image=render)
        img.image = render
        img.place(relx=0.012, rely=0.012, height=213, width=300,anchor="nw")

def proceed():
    if(parentImage and templateImage):
        #import parent image and template image
        parent_image=parentImage
        template_image=templateImage

        # Read the parent image 
        mask = cv2.imread(parent_image)
        img_parent = cv2.imread(parent_image)
        img = cv2.imread(parent_image,0)

        # Convert parent image to grayscale 
        img_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY) 

        # Read the template image
        template = cv2.imread(template_image,0) 

        # Store width and heigth of template in w and h 
        w, h = template.shape[::-1]

        # Store width and heigth of parent image in W and H 
        W, H = img.shape[::-1]

        # Perform match operations. 
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED) 

        # Specify a threshold (to maintain accuracy level)
        threshold = (top.slider.get())/100

        # Store the coordinates of matched area in a numpy array 
        cordinates = np.where( res >= threshold)

        # filled mask with black color 
        cv2.rectangle(mask, (0,0), (W, H), (0,0,0),-1)

        # Draw detected areas on mask as white boxes. 
        for pt in zip(*cordinates[::-1]):
            cv2.rectangle(mask, pt, (pt[0] + w, pt[1] + h), (255,255,255),-1) 

        # Merge parent image with mask to provide the output.
        img_parent = cv2.bitwise_and(img_parent, mask)

        # Show the final image with the matched area.
        cv2.imshow('Detected',img_parent)
    else:
        messagebox.showerror("Error", "Please Select Images to Proceed")
        

class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        font11 = "-family {Arial} -size 12 -weight bold"
        font12 = "-family {Arial} -size 11 -weight bold"
        font9 = "-family {Showcard Gothic} -size 18"

        top.geometry("847x578+253+99")
        top.title("New Toplevel")
        top.configure(background="#d9d9d9")

        self.Canvas1 = tk.Canvas(top)
        self.Canvas1.place(relx=-0.012, rely=-0.017, relheight=1.026
                , relwidth=1.019)
        self.Canvas1.configure(background="#ceb477")
        self.Canvas1.configure(borderwidth="2")
        self.Canvas1.configure(insertbackground="black")
        self.Canvas1.configure(relief='ridge')
        self.Canvas1.configure(selectbackground="#c4c4c4")
        self.Canvas1.configure(selectforeground="black")
        self.Canvas1.configure(width=863)

        self.Header = tk.Canvas(self.Canvas1)
        self.Header.place(relx=0.0, rely=0.017, relheight=0.106, relwidth=1.0)
        self.Header.configure(background="#77714b")
        self.Header.configure(insertbackground="black")
        self.Header.configure(relief='ridge')
        self.Header.configure(selectbackground="#c4c4c4")
        self.Header.configure(selectforeground="black")
        self.Header.configure(width=863)

        self.Label1 = tk.Label(self.Header)
        self.Label1.place(relx=0.342, rely=0.159, height=36, width=268)
        self.Label1.configure(background="#77714b")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(font=font9)
        self.Label1.configure(foreground="#ffffff")
        self.Label1.configure(text='''Template Finder V1.0''')

        self.Button1 = tk.Button(self.Canvas1)
        self.Button1.place(relx=0.023, rely=0.877, height=44, width=119)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#77714b")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(font=font11)
        self.Button1.configure(foreground="#ffffff")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Add Image''',command=addImage)
        self.Button1.configure(width=119)

        self.Button2 = tk.Button(self.Canvas1)
        self.Button2.place(relx=0.788, rely=0.885, height=44, width=160)
        self.Button2.configure(activebackground="#ececec")
        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(background="#026b10")
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(font=font11)
        self.Button2.configure(foreground="#ffffff")
        self.Button2.configure(highlightbackground="#d9d9d9")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(text='''Proceed''',command=proceed)
        self.Button2.configure(width=160)

        self.Canvas3 = tk.Canvas(self.Canvas1)
        self.Canvas3.place(relx=0.023, rely=0.169, relheight=0.68
                , relwidth=0.571)
        self.Canvas3.configure(background="#d8c78f")
        self.Canvas3.configure(borderwidth="1")
        self.Canvas3.configure(highlightthickness="0")
        self.Canvas3.configure(insertbackground="black")
        self.Canvas3.configure(relief='ridge')
        self.Canvas3.configure(selectbackground="#c4c4c4")
        self.Canvas3.configure(selectforeground="black")
        self.Canvas3.configure(width=493)

        self.Canvas4 = tk.Canvas(self.Canvas1)
        self.Canvas4.place(relx=0.603, rely=0.169, relheight=0.68
                , relwidth=0.374)
        self.Canvas4.configure(background="#d8c78f")
        self.Canvas4.configure(borderwidth="1")
        self.Canvas4.configure(highlightthickness="0")
        self.Canvas4.configure(insertbackground="black")
        self.Canvas4.configure(relief='ridge')
        self.Canvas4.configure(selectbackground="#c4c4c4")
        self.Canvas4.configure(selectforeground="black")
        self.Canvas4.configure(width=323)

        self.Button3 = tk.Button(self.Canvas4)
        self.Button3.place(relx=0.604, rely=0.571, height=34, width=117)
        self.Button3.configure(activebackground="#ececec")
        self.Button3.configure(activeforeground="#000000")
        self.Button3.configure(background="#77714b")
        self.Button3.configure(disabledforeground="#a3a3a3")
        self.Button3.configure(font=font12)
        self.Button3.configure(foreground="#ffffff")
        self.Button3.configure(highlightbackground="#d9d9d9")
        self.Button3.configure(highlightcolor="black")
        self.Button3.configure(pady="0")
        self.Button3.configure(text='''Set Template''',command=setTemplate)
        self.Button3.configure(width=117)

        self.Template = tk.Canvas(self.Canvas4)
        self.Template.place(relx=0.031, rely=0.025, relheight=0.529
                , relwidth=0.938)
        self.Template.configure(background="#d8c78f")
        self.Template.configure(highlightthickness="1")
        self.Template.configure(insertbackground="black")
        self.Template.configure(relief='ridge')
        self.Template.configure(selectbackground="#c4c4c4")
        self.Template.configure(selectforeground="black")
        self.Template.configure(width=303)

        self.slider = tk.Scale(self.Canvas4, from_=0.0, to=100.0)
        self.slider.place(relx=0.031, rely=0.794, relwidth=0.935, relheight=0.0
                , height=42, bordermode='ignore')
        self.slider.configure(activebackground="#ececec")
        self.slider.configure(background="#bcad7c")
        self.slider.configure(font="TkTextFont")
        self.slider.configure(foreground="#000000")
        self.slider.configure(highlightbackground="#d9d9d9")
        self.slider.configure(highlightcolor="black")
        self.slider.configure(highlightthickness="0")
        self.slider.configure(length="296")
        self.slider.configure(orient="horizontal")
        self.slider.configure(troughcolor="#d9d9d9")

        self.Label2 = tk.Label(self.Canvas4)
        self.Label2.place(relx=0.031, rely=0.72, height=25, width=150)
        self.Label2.configure(background="#d8c78f")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(font=font11)
        self.Label2.configure(foreground="#4f4f4f")
        self.Label2.configure(text='''Set Treshold Value''')

        self.Button4 = tk.Button(self.Canvas1)
        self.Button4.place(relx=0.603, rely=0.885, height=44, width=157)
        self.Button4.configure(activebackground="#ececec")
        self.Button4.configure(activeforeground="#000000")
        self.Button4.configure(background="#a80000")
        self.Button4.configure(disabledforeground="#a3a3a3")
        self.Button4.configure(font=font11)
        self.Button4.configure(foreground="#ffffff")
        self.Button4.configure(highlightbackground="#d9d9d9")
        self.Button4.configure(highlightcolor="black")
        self.Button4.configure(pady="0")
        self.Button4.configure(text='''Exit''',command=close_window)
        self.Button4.configure(width=157)

        self.menubar = tk.Menu(top,font="TkMenuFont",bg=_bgcolor,fg='#8c8c8c')
        top.configure(menu = self.menubar)

if __name__ == '__main__':
    vp_start_gui()





