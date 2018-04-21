from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import cv2
import tkinter as tk, threading
listbox_date=None
listbox_startFrame=None
listbox_endFrame=None
selection=0
previousValue=0
class MainMenu(Frame):
    def __init__(self, master):  # main menu
        Frame.__init__(self, master)
        self.grid()
        global listbox_date,listbox_endFrame,listbox_startFrame
        video_frame = Frame(root, width=600, height=600)
        video_frame.grid(row=0, column=0, padx=20, pady=0)

        image7 = Image.open("video-generic.png")
        photo7 = ImageTk.PhotoImage(image7)

        video1 = Label(video_frame, width=600, height=350, bg="black")
        video1.grid(row=0, column=0, padx=20, pady=0)

        thread = threading.Thread(target=self.stream, args=(video1,))
        thread.daemon = 1
        thread.start()

        video2 = Label(video_frame, width=600, height=350, image=photo7, bg="black")
        video2.grid(row=1, column=0, padx=20, pady=10)
        video2.image = photo7

        video_bottom = Frame(video_frame, width=600, height=100)
        video_bottom.grid(row=2, column=0)
        image = Image.open("mor_play.png")
        photo = ImageTk.PhotoImage(image)
        play = Button(video_bottom, image=photo, border=0)
        play.image = photo
        play.grid(row=0, column=0)

        image2 = Image.open("mor_stop.png")
        photo2 = ImageTk.PhotoImage(image2)
        pause = Button(video_bottom, image=photo2, text="Pause", border=0)
        pause.image = photo2
        pause.grid(row=0, column=1)

        slider = Scale(video_bottom, from_=0, to=100, orient=HORIZONTAL, length=500, fg='black')
        slider.grid(row=0, column=2)

        right_frame = Frame(root, width=100, height=50)
        right_frame.grid(row=0, column=1, padx=50, pady=10)

        date = Label(right_frame, text="DATE", width=25, height=1, bg="white")
        date.grid(row=0, column=0, padx=5, pady=5,sticky="NW")

        start_frame = Label(right_frame, text="START FRAME", width=25, height=1, bg="white")
        start_frame.grid(row=0, column=1, padx=5, pady=5)

        end_frame = Label(right_frame, text="END FRAME", width=25, height=1, bg="white")
        end_frame.grid(row=0, column=2, padx=5, pady=5)

        listbox_date = Listbox(right_frame, width=33, height=45,)
        listbox_date.bind("<<ListboxSelect>>", self.OnSelect)
        listbox_date.grid(row=1,column=0)

        for i in range(100):
            listbox_date.insert(END,"21.04.2018")
            listbox_date.insert(END, i)

        listbox_startFrame = Listbox(right_frame, width=33, height=45)
        listbox_startFrame.bind("<<ListboxSelect>>", self.OnSelect)
        listbox_startFrame.grid(row=1,column=1)

        for i in range(100):
            listbox_startFrame.insert(END,"255")
            listbox_startFrame.insert(END, i)

        listbox_endFrame = Listbox(right_frame, width=33, height=45,selectbackground="blue")
        listbox_endFrame.bind("<<ListboxSelect>>", self.OnSelect)
        listbox_endFrame.grid(row=1,column=2)

        for i in range(100):
            listbox_endFrame.insert(END,"1628")
            listbox_endFrame.insert(END, i)

        scrollbar = Scrollbar(right_frame,command=self.scrollBoth)
        scrollbar.grid(sticky="NSW", row=1, column=3, rowspan=2)

        listbox_date.configure(yscrollcommand=scrollbar.set,selectbackground="purple4")
        listbox_startFrame.configure(selectbackground="purple4")
        listbox_endFrame.configure(selectbackground="purple4")

    def OnSelect(self, event):
        global selection,previousValue
        widget = event.widget
        previousValue=selection
        selection = widget.curselection()
        if previousValue is not selection:
            listbox_date.itemconfig(previousValue, background="white", foreground="black")
            listbox_startFrame.itemconfig(previousValue, background="white", foreground="black")
            listbox_endFrame.itemconfig(previousValue, background="white", foreground="black")

            listbox_date.itemconfig(selection, background="purple4", foreground="white")
            listbox_startFrame.itemconfig(selection,background="purple4",foreground="white")
            listbox_endFrame.itemconfig(selection, background="purple4", foreground="white")
        else:
            listbox_date.itemconfig(selection, background="purple4", foreground="white")
            listbox_startFrame.itemconfig(selection, background="purple4", foreground="white")
            listbox_endFrame.itemconfig(selection, background="purple4", foreground="white")




    def scrollBoth(self, *args):
        global listbox_date,listbox_startFrame,listbox_endFrame
        listbox_date.yview(*args)
        listbox_startFrame.yview(*args)
        listbox_endFrame.yview(*args)
        return None
    def stream(self, label):
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()

            img = cv2.resize(frame, (600, 350))
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            frame_image = ImageTk.PhotoImage(Image.fromarray(rgb))

            label.config(image=frame_image)
            label.image = frame_image

root = Tk()  # Makes the window
root.geometry("1500x1200")
app = MainMenu(root)
root.mainloop()  # loop to update GUI
