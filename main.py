from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import cv2
import tkinter as tk, threading
import time
selection = 0
previousValue = 0


class MainMenu(Frame):
    videoFirst = 0
    videoPlay = False
    sliderLenght = 100
    def __init__(self, master):  # main menu
        Frame.__init__(self, master)
        self.grid()

        """self.quit_button = Button(root, width=10, height=10, text="quit", command=self.quit)
        self.quit_button.grid(row=0, column=2)"""

        self.video_frame = Frame(root, width=600, height=600)
        self.video_frame.grid(row=0, column=0, padx=20, pady=0)

        self.image7 = Image.open("video-generic.png")
        self.photo7 = ImageTk.PhotoImage(self.image7)

        self.video1 = Label(self.video_frame, width=600, height=350, bg="black")
        self.video1.grid(row=0, column=0, padx=20, pady=0)

        # self.camera_on = True
        self.thread = threading.Thread(target=self.stream, args=(self.video1,))
        self.thread.daemon = 1
        self.thread.start()

        self.video2 = Label(self.video_frame, width=600, height=350, image=self.photo7, bg="black")
        self.video2.grid(row=1, column=0, padx=20, pady=10)
        self.video2.image = self.photo7

        self.video_bottom = Frame(self.video_frame, width=600, height=100)
        self.video_bottom.grid(row=2, column=0)
        self.image = Image.open("mor_play.png")
        self.photo = ImageTk.PhotoImage(self.image)
        self.play = Button(self.video_bottom, image=self.photo, border=0, command=self.contn)
        self.play.image = self.photo
        self.play.grid(row=0, column=0)

        self.image2 = Image.open("mor_stop.png")
        self.photo2 = ImageTk.PhotoImage(self.image2)
        self.pause = Button(self.video_bottom, image=self.photo2, text="Pause", border=0, command=self.stop)
        self.pause.image = self.photo2
        self.pause.grid(row=0, column=1)

        self.draw_slider()

        self.right_frame = Frame(root, width=100, height=50)
        self.right_frame.grid(row=0, column=1, padx=50, pady=10)

        self.date = Label(self.right_frame, text="DATE", width=25, height=1, bg="white")
        self.date.grid(row=0, column=0, padx=5, pady=5, sticky="NW")

        self.start_frame = Label(self.right_frame, text="START FRAME", width=25, height=1, bg="white")
        self.start_frame.grid(row=0, column=1, padx=5, pady=5)

        self.end_frame = Label(self.right_frame, text="END FRAME", width=25, height=1, bg="white")
        self.end_frame.grid(row=0, column=2, padx=5, pady=5)

        self.listbox_date = Listbox(self.right_frame, width=33, height=45,)
        self.listbox_date.bind("<<ListboxSelect>>", self.OnSelect)
        self.listbox_date.bind("<Double-Button-1>", self.OnDouble)
        self.listbox_date.grid(row=1, column=0)

        self.listbox_startFrame = Listbox(self.right_frame, width=33, height=45)
        self.listbox_startFrame.bind("<<ListboxSelect>>", self.OnSelect)
        self.listbox_startFrame.bind("<Double-Button-1>", self.OnDouble)
        self.listbox_startFrame.grid(row=1, column=1)

        self.listbox_endFrame = Listbox(self.right_frame, width=33, height=45, selectbackground="blue")
        self.listbox_endFrame.bind("<<ListboxSelect>>", self.OnSelect)
        self.listbox_endFrame.bind("<Double-Button-1>", self.OnDouble)
        self.listbox_endFrame.grid(row=1, column=2)

        for i in range(1000):
            current_date = time.strftime("%d/%m/%Y")+"      "+time.strftime("%H:%M:%S")
            self.listbox_date.insert(END, current_date)
            self.listbox_startFrame.insert(END, str(20))
            self.listbox_endFrame.insert(END, str(400))

        self.scrollbar = Scrollbar(self.right_frame, command=self.scrollBoth)
        self.scrollbar.grid(sticky="NSW", row=1, column=3, rowspan=2)

        self.listbox_date.configure(yscrollcommand=self.scrollbar.set, selectbackground="purple4")
        self.listbox_startFrame.configure(selectbackground="purple4")
        self.listbox_endFrame.configure(selectbackground="purple4")

    def draw_slider(self):
        self.slider = Scale(self.video_bottom, from_=0, to=self.sliderLenght, orient=HORIZONTAL, length=500, fg='black')
        self.slider.grid(row=0, column=2)

    def contn(self):
        self.videoPlay = True

    def stop(self):
        self.videoPlay = False

    def OnSelect(self, event):
        global selection, previousValue
        widget = event.widget
        previousValue = selection
        selection = widget.curselection()

        if previousValue is not selection:
            self.listbox_date.itemconfig(previousValue, background="white", foreground="black")
            self.listbox_startFrame.itemconfig(previousValue, background="white", foreground="black")
            self.listbox_endFrame.itemconfig(previousValue, background="white", foreground="black")

            self.listbox_date.itemconfig(selection, background="purple4", foreground="white")
            self.listbox_startFrame.itemconfig(selection, background="purple4", foreground="white")
            self.listbox_endFrame.itemconfig(selection, background="purple4", foreground="white")

        else:
            self.listbox_date.itemconfig(selection, background="purple4", foreground="white")
            self.listbox_startFrame.itemconfig(selection, background="purple4", foreground="white")
            self.listbox_endFrame.itemconfig(selection, background="purple4", foreground="white")

    def OnDouble(self, event):
        self.videoFirst += 1
        widget = event.widget
        selection = widget.curselection()
        self.videostart = self.listbox_startFrame.get(selection)
        self.videoend = self.listbox_endFrame.get(selection)
        self.contn()
        if self.videoFirst == 1:
            thread2 = threading.Thread(target=self.video_open, args=(self.video2,))
            thread2.daemon = 1
            thread2.start()

    def video_open(self, label):
        cap = cv2.VideoCapture('video1.MKV')
        self.sliderLenght = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.draw_slider()
        previous = self.videoFirst
        count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if self.videoPlay is True:
                if int(self.videostart) <= count <= int(self.videoend):
                    time.sleep(0.01)
                    img = cv2.resize(frame, (600, 350))
                    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    frame_image = ImageTk.PhotoImage(Image.fromarray(rgb))
                    label.config(image=frame_image)
                    label.image = frame_image
                    self.slider.set(count)
                count += 1
            else:
                while True:
                    if self.videoPlay is True:
                        break
            if cv2.waitKey(1) & self.videoFirst != previous:
                break
        cap.release()
        cv2.destroyAllWindows()
        self.video_open(label)

    def scrollBoth(self, *args):
        self.listbox_date.yview(*args)
        self.listbox_startFrame.yview(*args)
        self.listbox_endFrame.yview(*args)
        return None

    def stream(self, label):
        cap = cv2.VideoCapture(0)
        while cap.isOpened():  # and self.camera_on:
            ret, frame = cap.read()
            img = cv2.resize(frame, (600, 350))
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            frame_image = ImageTk.PhotoImage(Image.fromarray(rgb))
            label.config(image=frame_image)
            label.image = frame_image
        cap.release()
        cv2.destroyAllWindows()

    def saveInListbox(self, start_frame, end_frame):
        if self.motion is True:
            current_date = time.strftime("%d/%m/%Y")
            self.listbox_date.insert(END, current_date)
            self.listbox_startFrame.insert(END, self.current_start_frame)
            self.listbox_endFrame.insert(END, self.current_end_frame)

    """def quit(self):
        self.camera_on = False
        root.destroy()"""

root = Tk()
root.geometry("1500x1200")
app = MainMenu(root)
root.mainloop()
