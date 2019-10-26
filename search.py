from tkinter import *
from db import search

class SampleApp:
    def __init__(self, root):
        self.frame1 = Frame(root, width=800)
        self.root = root
        self.frame1.pack()
        self.frame2 = Frame(root, width=800)
        self.entry = Entry(self.frame1)
        self.button = Button(self.frame1, text="Search", width=8, command=self.on_button, fg='blue')
        self.label = Label(self.frame1, text="First Name")
        self.label.pack(side=LEFT)
        self.entry.pack(side=LEFT)
        self.button.pack(side=RIGHT)
        self.main = Frame(self.root, width=800, bg="grey")
        self.main.pack()
        self.frame2.pack()
        self.results = []
        self.index1 = 0
        self.index2 = 0
        self.bookkeeping = {}
        # self.result = Frame(root, width=100, height=100, background="bisque")
        # self.result.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height
        # self.result.grid(row=1, column=0)

    def on_button(self):
        self.index1 = 0
        self.index2 = 0
        for widget in self.main.winfo_children():
                widget.destroy()
        query = self.entry.get()
        self.results = search(query)
        if len(self.results) > 0:
            import json

            with open('bookkeeping.json') as f:
                self.bookkeeping = json.load(f)
        if len(self.results) >= self.index1 + 10:
            self.index2 = 10
        else:
            self.index2 = len(self.results)
        for index in range(self.index1, self.index2):
            result = self.results[index]
            document_id = result[2]
            document_id = document_id[54:]
            link = self.bookkeeping[document_id]
            data_string = StringVar()
            data_string.set(link)
            messeage = Entry(self.main,textvariable=data_string,fg="black",bg="white",bd=0,state="readonly", width=800)
            # messeage = Entry(self.main, text=link, width=800)
            messeage.pack(fill='both', pady=(10, 10))
        if len(self.results) > 10:
            for widget in self.frame2.winfo_children():
                widget.destroy()
            next_btn = Button(self.frame2, text="Next", width=8, command=self.next_button, fg='blue')
            prev_btn = Button(self.frame2, text="Prev", width=8, command=self.prev_button, fg='blue')
            prev_btn.pack(side=LEFT)
            next_btn.pack(side=RIGHT)
        self.index1 = self.index2
    
    def next_button(self):
        if len(self.results) >= self.index1 + 10:
            self.index2 += 10
        else:
            self.index2 = len(self.results)
        if len(self.results) > self.index1:
            for widget in self.main.winfo_children():
                widget.destroy()

            for index in range(self.index1, self.index2):
                result = self.results[index]
                document_id = result[2]
                document_id = document_id[54:]
                link = self.bookkeeping[document_id]
                data_string = StringVar()
                data_string.set(link)
                messeage = Entry(self.main,textvariable=data_string,fg="black",bg="white",bd=0,state="readonly", width=800)
                messeage.pack(fill='both', pady=(10, 10))
            self.index1 = self.index2
    
    def prev_button(self):
        if self.index1 >= 20:
            self.index2 -= 10
            self.index1 -= 20
        else:
            self.index1 = 0
            if len(self.results) >= self.index1 + 10:
                self.index2 = 10
            else:
                self.index2 = len(self.results)
        if len(self.results) > self.index1:
            for widget in self.main.winfo_children():
                widget.destroy()

            for index in range(self.index1, self.index2):
                result = self.results[index]
                document_id = result[2]
                document_id = document_id[54:]
                link = self.bookkeeping[document_id]
                data_string = StringVar()
                data_string.set(link)
                messeage = Entry(self.main,textvariable=data_string,fg="black",bg="white",bd=0,state="readonly", width=800)
                messeage.pack(fill='both', pady=(10, 10))
            self.index1 = self.index2

root = Tk()
sizex = 800
sizey = 600
posx  = 100
posy  = 100
root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
app = SampleApp(root)
root.mainloop()