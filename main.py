from tkinter import *
from PIL import Image, ImageTk


class MainMenu(Frame):
    def __init__(self, master):  # main menu
        Frame.__init__(self, master)
        self.grid()

        video_frame = Frame(root, width=600, height=600)
        video_frame.grid(row=0, column=0, padx=20, pady=10)

        photo = ImageTk.PhotoImage(Image.open("default1.png"))
        video1 = Label(video_frame, width=600, height=350, image=photo)
        video1.grid(row=0, column=0, padx=20, pady=10)
        video1.image = photo

        video2 = Label(video_frame, width=600, height=350, image=photo)
        video2.grid(row=1, column=0, padx=20, pady=10)
        video2.image = photo

        rightFrame = Frame(root, width=100, height=50)
        rightFrame.grid(row=0, column=1, padx=150, pady=10)
        listbox = Listbox(rightFrame, width=100, height=45)
        listbox.grid()
        listbox.insert(END, "a list entry")
        for item in ["one", "two", "three", "four"]:
            listbox.insert(END, item)


root = Tk()  # Makes the window
root.geometry("1500x1200")
app = MainMenu(root)
root.mainloop()  # loop to update GUI
