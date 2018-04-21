from tkinter import *
from PIL import Image, ImageTk


class MainMenu(Frame):
    def __init__(self, master):  # main menu
        Frame.__init__(self, master)
        self.grid()

        video_frame = Frame(root, width=600, height=600)
        video_frame.grid(row=0, column=0, padx=20, pady=10)

        image7 = Image.open("video-generic.png")
        photo7 = ImageTk.PhotoImage(image7)
        video1 = Label(video_frame, width=600, height=350, image=photo7,bg="black")
        video1.grid(row=0, column=0, padx=20, pady=10)
        video1.image = photo7

        video2 = Label(video_frame, width=600, height=350, image=photo7,bg="black")
        video2.grid(row=1, column=0, padx=20, pady=10)
        video2.image = photo7

        rightFrame = Frame(root, width=100, height=50)
        rightFrame.grid(row=0, column=1, padx=50, pady=10)
        listbox = Listbox(rightFrame, width=100, height=45)
        listbox.grid()
        listbox.insert(END, "DATE                           START FRAME                        END FRAME")
        for i in range(0, 1000):
            listbox.insert(END,"21.04.2018                           0                                1000")
            listbox.insert(i)
        scrollbar = Scrollbar(rightFrame)
        scrollbar.grid(sticky="NSW",row=0, column=2,rowspan=2)

        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

root = Tk()  # Makes the window
root.geometry("1500x1200")
app = MainMenu(root)
root.mainloop()  # loop to update GUI
