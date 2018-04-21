from tkinter import *
from PIL import Image, ImageTk


class MainMenu(Frame):
    def __init__(self, master):  # main menu
        Frame.__init__(self, master)
        self.grid()

        video_frame = Frame(root, width=600, height=600)
        video_frame.grid(row=0, column=0, padx=20, pady=0)

        image7 = Image.open("video-generic.png")
        photo7 = ImageTk.PhotoImage(image7)
        video1 = Label(video_frame, width=600, height=350, image=photo7,bg="black")
        video1.grid(row=0, column=0, padx=20, pady=0)
        video1.image = photo7

        video2 = Label(video_frame, width=600, height=350, image=photo7,bg="black")
        video2.grid(row=1, column=0, padx=20, pady=10)
        video2.image = photo7

        image = Image.open("mor_play.png")
        photo = ImageTk.PhotoImage(image)
        play = Button(video_frame, image=photo,border=0)
        play.image = photo
       # play.place(relx=0.4, rely=0.87, relheight=0.15, relwidth=0.1)
        play.grid(row=2, column=0, padx=10, pady=0,sticky="W")

        image2 = Image.open("mor_stop.png")
        photo2 = ImageTk.PhotoImage(image2)
        pause = Button(video_frame, image=photo2, text="Pause", border=0)
        pause.image = photo2
        pause.place(relx=0.09, rely=0.9225, relheight=0.1, relwidth=0.1)
        #pause.grid(row=2, column=0, padx=10, pady=0,sticky="NW")


        slider = Scale(video_frame, from_=0, to=100, orient=HORIZONTAL, length=500, fg='black')
       # slider.grid(row=2, column=0, padx=20, pady=0,sticky="E")
        slider.place(relx=0.2, rely=0.9225, relheight=0.1, relwidth=0.77)

        rightFrame = Frame(root, width=100, height=50)
        rightFrame.grid(row=0, column=1, padx=50, pady=10)

        date = Label(rightFrame, text ="DATE",width=15, height=1, bg="white")
        date.grid(row=0, column=0, padx=5, pady=5, sticky="NW")

        start_frame = Label(rightFrame, text="START FRAME", width=15, height=1, bg="white")
        start_frame.grid(row=0, column=0, padx=5, pady=5, sticky="N")

        end_frame = Label(rightFrame, text="END FRAME", width=15, height=1, bg="white")
        end_frame.grid(row=0, column=0, padx=5, pady=5, sticky="NE")

        listbox = Listbox(rightFrame, width=100, height=45)
        listbox.grid()



        for i in range(0, 1000):
            listbox.insert(END,"21.04.2018 "
                               "                                                                  255     "
                               "                                                                    1000")
        scrollbar = Scrollbar(rightFrame)
        scrollbar.grid(sticky="NSW",row=0, column=2,rowspan=2)

        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

root = Tk()  # Makes the window
root.geometry("1500x1200")
app = MainMenu(root)
root.mainloop()  # loop to update GUI
