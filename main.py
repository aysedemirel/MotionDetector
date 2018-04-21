from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import cv2
import tkinter as tk, threading


class MainMenu(Frame):
    def __init__(self, master):  # main menu
        Frame.__init__(self, master)
        self.grid()

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

        date = Label(right_frame, text="DATE", width=15, height=1, bg="white")
        date.grid(row=0, column=0, padx=5, pady=5, sticky="NW")

        start_frame = Label(right_frame, text="START FRAME", width=15, height=1, bg="white")
        start_frame.grid(row=0, column=0, padx=5, pady=5, sticky="N")

        end_frame = Label(right_frame, text="END FRAME", width=15, height=1, bg="white")
        end_frame.grid(row=0, column=0, padx=5, pady=5, sticky="NE")

        listbox = Listbox(right_frame, width=100, height=45)
        listbox.grid()

        for i in range(0, 1000):
            listbox.insert(END, "21.04.2018 "
                               "                                                                  255     "
                               "                                                                    1000")
        scrollbar = Scrollbar(right_frame)
        scrollbar.grid(sticky="NSW", row=0, column=2, rowspan=2)

        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

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
