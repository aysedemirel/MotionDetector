from tkinter import *
from PIL import Image, ImageTk
import cv2
import threading
import time

selection = 0
previousValue = 0


class MainMenu(Frame):
    img = ...  # type: None
    videoFirst = 0
    videoPlay = False
    scrll = False
    clk = 0
    last = 0
    videostart = 0
    videoend = 0

    def __init__(self, master):  # main menu
        Frame.__init__(self, master)
        self.grid()

        """self.image_quit = Image.open("quit.png")
        self.photo_quit = ImageTk.PhotoImage(self.image_quit)
        self.quit_button = Button(root, image=self.photo_quit, border=0, command=self.quit)
        self.quit_button.image = self.photo_quit
        self.quit_button.grid(row=0, column=0, sticky="NW")"""

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

        self.right_frame = Frame(root, width=600, height=600)
        self.right_frame.grid(row=0, column=1, padx=50, pady=0)

        self.right_buttom_frame = Frame(self.right_frame, width=600, height=600)
        self.right_buttom_frame.grid(row=0, column=0, padx=50, pady=0)

        self.date = Label(self.right_buttom_frame, text="DATE", width=25, height=1, bg="white")
        self.date.grid(row=0, column=0, padx=5, pady=0, sticky="NW")

        self.start_frame = Label(self.right_buttom_frame, text="START FRAME", width=25, height=1, bg="white")
        self.start_frame.grid(row=0, column=1, padx=5, pady=0)

        self.end_frame = Label(self.right_buttom_frame, text="END FRAME", width=25, height=1, bg="white")
        self.end_frame.grid(row=0, column=2, padx=5, pady=0)

        self.listbox_date = Listbox(self.right_buttom_frame, width=33, height=20, )
        self.listbox_date.bind("<<ListboxSelect>>", self.OnSelect)
        self.listbox_date.bind("<Double-Button-1>", self.OnDouble)
        self.listbox_date.grid(row=1, column=0)

        self.listbox_startFrame = Listbox(self.right_buttom_frame, width=33, height=20)
        self.listbox_startFrame.bind("<<ListboxSelect>>", self.OnSelect)
        self.listbox_startFrame.bind("<Double-Button-1>", self.OnDouble)
        self.listbox_startFrame.grid(row=1, column=1)

        self.listbox_endFrame = Listbox(self.right_buttom_frame, width=33, height=20, selectbackground="blue")
        self.listbox_endFrame.bind("<<ListboxSelect>>", self.OnSelect)
        self.listbox_endFrame.bind("<Double-Button-1>", self.OnDouble)
        self.listbox_endFrame.grid(row=1, column=2)

        self.scrollbar = Scrollbar(self.right_buttom_frame, command=self.scrollBoth)
        self.scrollbar.grid(sticky="NSW", row=1, column=3, rowspan=2)

        self.listbox_date.configure(yscrollcommand=self.scrollbar.set, selectbackground="purple4")
        self.listbox_startFrame.configure(selectbackground="purple4")
        self.listbox_endFrame.configure(selectbackground="purple4")

        self.video3 = Label(self.right_frame, width=600, height=380, image=self.photo7, bg="black")
        self.video3.grid(row=1, column=0, padx=20, pady=10)
        self.video3.image = self.photo7


    def draw_slider(self):
        self.slider = Scale(self.video_bottom, from_=self.videostart, to=self.videoend, orient=HORIZONTAL,
                            length=500, command=self.slider_func)
        self.slider.grid(row=0, column=2)

    def slider_func(self, label):
        if not self.videoPlay:
            self.scrll = True

    def contn(self):
        self.videoPlay = True
        self.scrll = False
        self.slider.set(self.last)

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
        selectionLine = widget.curselection()
        self.videostart = self.listbox_startFrame.get(selectionLine)
        self.videoend = self.listbox_endFrame.get(selectionLine)
        self.contn()
        if self.videoFirst == 1:
            self.videoPlay = True
            thread2 = threading.Thread(target=self.video_open, args=(self.video2,))
            thread2.daemon = 1
            thread2.start()

    def video_open(self, label):
        cap = cv2.VideoCapture('output.avi')
        self.draw_slider()
        previous = self.videoFirst
        count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if self.videoPlay is True:
                if int(self.videostart) <= count <= int(self.videoend):
                    time.sleep(0.1)
                    img = cv2.resize(frame, (600, 350))
                    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    frame_image = ImageTk.PhotoImage(Image.fromarray(rgb))
                    label.config(image=frame_image)
                    label.image = frame_image
                    self.slider.set(count)
                    self.last = self.slider.get()
                count += 1
            else:
                while True:
                    if self.videoPlay is True:
                        break
                    if self.last != self.slider.get() and int(self.videostart) <= self.slider.get() <= int(
                            self.videoend):
                        self.last = self.slider.get()
                    if self.scrll is True:
                        self.clk = 0
                        cap = cv2.VideoCapture('output.MKV')
                        while cap.isOpened():
                            ret, frame = cap.read()
                            if self.last == self.clk:
                                img = cv2.resize(frame, (600, 350))
                                rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                                frame_image = ImageTk.PhotoImage(Image.fromarray(rgb))
                                label.config(image=frame_image)
                                label.image = frame_image
                                self.last = self.slider.get()
                                count = self.clk
                                break
                            self.clk += 1
            if cv2.waitKey(1) & self.videoFirst != previous:
                break
        # cap.release()
        # cv2.destroyAllWindows()
        self.videoPlay = True
        self.scrll = False
        self.last = 0
        self.video_open(label)

    def scrollBoth(self, *args):
        self.listbox_date.yview(*args)
        self.listbox_startFrame.yview(*args)
        self.listbox_endFrame.yview(*args)
        return None

    def stream(self, label):
        cap = cv2.VideoCapture(0)

        t_minus = cv2.cvtColor(cap.read()[1], cv2.COLOR_RGB2GRAY)
        ret, t_minus = cv2.threshold(t_minus, 70, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        #t_middle = cv2.cvtColor(cap.read()[1], cv2.COLOR_RGB2GRAY)
        #ret, t_middle = cv2.threshold(t_middle, 70, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        t_plus = cv2.cvtColor(cap.read()[1], cv2.COLOR_RGB2GRAY)
        ret, t_plus = cv2.threshold(t_plus, 70, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        print(cv2.countNonZero(t_minus))
        print(cv2.countNonZero(t_plus))

        counter = 0
        start = 0
        enterStart = False
        first = 0
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
        fbgb = cv2.createBackgroundSubtractorMOG2()
        while cap.isOpened():  # and self.camera_on:
            ret, frame = cap.read()
            out.write(frame)
            img = cv2.resize(frame, (600, 350))
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            frame_image = ImageTk.PhotoImage(Image.fromarray(rgb))
            label.config(image=frame_image)
            label.image = frame_image

            print(cv2.countNonZero(t_minus))
            
            videoMasked = fbgb.apply(frame)
            # cv2.imshow("img2", videoMasked)
            #print("difference = ", cv2.countNonZero(cv2.absdiff(t_minus, t_plus)))
            #print("threshold = ", cv2.countNonZero(t_plus))
            if cv2.countNonZero(cv2.absdiff(t_minus, t_plus)) > 81500:
                first += 1

                if first == 1:
                    enterStart = True
                    start = counter
            else:
                if enterStart:
                    end = counter
                    first = 0
                    enterStart = False
                    self.saveInListbox(start, end)
            # Read next image

            #t_minus = t_plus
            t_plus = cv2.cvtColor(cap.read()[1], cv2.COLOR_RGB2GRAY)
            # t_plus = cv2.medianBlur(t_plus, 15)
            ret, t_plus = cv2.threshold(t_plus, 70, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            # t_plus = cv2.dilate(t_plus, None, iterations=2)
            t_plus = cv2.dilate(t_plus, None, iterations=2)
            contours, _, cns = cv2.findContours(t_plus, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

            # loop over the contours
            for c in contours:
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(t_plus, (x, y), (x + w, y + h), (255, 0, 0), 2)

            img2 = cv2.resize(t_plus, (600, 380))
            frame_image2 = ImageTk.PhotoImage(Image.fromarray(img2))
            self.video3.config(image=frame_image2)
            self.video3.image = frame_image2

            key = cv2.waitKey(10)
            if key == 27:
                break
            counter += 1

    def saveInListbox(self, start_frame, end_frame):

        current_date = time.strftime("%d/%m/%Y") + "     " + time.strftime("%H:%M:%S")
        self.listbox_date.insert(END, current_date)
        self.listbox_startFrame.insert(END, start_frame)
        self.listbox_endFrame.insert(END, end_frame)

    """def quit(self):
        # self.camera_on = False
        root.destroy()"""

    def diffImg(self, t0, t1, t2):  # Function to calculate difference between images.
        d1 = cv2.absdiff(t2, t1)
        d2 = cv2.absdiff(t1, t0)
        return cv2.bitwise_and(d1, d2)


root = Tk()
root.geometry("1500x1200")
app = MainMenu(root)
root.mainloop()
