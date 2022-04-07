from tkinter import *

from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
from tkinter import ttk
from pandas import *

from ratings_to_bew import *
from bew_to_curve import *
from all_MOS import *
from import_file import *
from calculCI import *
##import xlrd

import matplotlib.pyplot as plt


class SampleApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title("PTRANS")
        self.geometry('250x400')
        self.style = ttk.Style(self)
        # Just simply import the azure.tcl file
        self.call("source", "Azure-ttk-theme-main/azure.tcl")

        # Then set the theme you want with the set_theme procedure
        self.call("set_theme", "light")
        #self.style.set_theme("light")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour, PageFive, PageEnd):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def get_page(self, page_name):
        return self.frames[page_name]



class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text="\n            Welcome to our tool !\n", background="#007fff")
        #, background="#6680CC")
        label.pack(side="top", fill="x", pady=15, padx=10)

        ttk.Button(self, text="You want to add your own dataset \n",
                            command=lambda: controller.show_frame("PageOne")).pack(pady=10, padx=5)
        ttk.Button(self, text="   You want to use the datasets     \n              that we have",
                            command=lambda: controller.show_frame("PageTwo")).pack(padx=5)


class PageOne(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.file = ''
        self.filetype = ''

        label = ttk.Label(self, text="\n          You can input a new file \n", background="#007fff")
                      #, background="#6680CC")
        label.pack(side="top", fill="x", pady=15, padx=10)

        open_button = ttk.Button(self, text='Open a File', command=lambda: [self.select_file(), self.option()])

        ttk.Label(self, text='File :').pack()
        open_button.pack()

        # defining option list
        OptionSheet = [1, 1, 2, 3]

        self.variable = IntVar(self)
        self.variable.set(OptionSheet[0])

        self.opt = ttk.OptionMenu(self, self.variable, *OptionSheet)
        # opt.config(width=90, font=('Helvetica', 12))

        button = ttk.Button(self, text="  Return to the first page   ",
                        command=lambda: controller.show_frame("StartPage"))
        button.pack(side="bottom", pady=5, padx=5)
        ttk.Button(self, text='            Continue               ', style="Accent.TButton",
               command=lambda: controller.show_frame("PageThree")).pack(side="bottom", pady=5, padx=5)
        # button = Button(m, text='Continue', bg="green", width=10, height=5, command=window.destroy)

    def select_file(self):
        filetypes = (
            ('csv files', '*.csv'),
            ('xls files', '*.xls'),
            ('Json files', '*.json'),
            ('XML files', '*.xml'),
            ('All files', '*.*')
        )

        filename = askopenfilename(
            title='Open a file',
            initialdir='./',
            filetypes=filetypes)

        showinfo(
            title='Selected File',
            message=filename
        )

        ft = filename.split(".").pop()
        self.file = filename
        self.filetype = ft

    def option(self):
        if self.filetype == 'xls':
            ttk.Label(self, text="Which sheet to use ?").pack()
            self.opt.pack(side="top")
        else:
            pass

    def get_file(self):
        return [self.file, self.filetype]

    def get_sheet_num(self):
        sheet = self.variable.get()
        self.sheet_number = sheet
        return sheet


class PageTwo(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        ttk.Label(self, text="TODO", background="#007fff").pack(side="top", fill="x", pady=10)
        ttk.Button(self, text="  Return to the first page   ",
                           command=lambda: controller.show_frame("StartPage")).pack(side="bottom", pady=5, padx=5)
        ttk.Button(self, text='            Continue               ', style="Accent.TButton",
                      command=lambda: controller.show_frame("PageEnd")).pack(side="bottom", padx=5, pady=5)


class PageThree(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.number_stimuli = ''
        self.number_observers = ''
        self.sheet_number = ''

        label = ttk.Label(self, text="\n       Informations about your datasets \n", background="#007fff").pack(side="top", fill="x", pady=10)

        ttk.Label(self, text="Number of stimuli").pack()
        self.e1 = ttk.Entry(self)
        self.e1.pack()

        ttk.Label(self, text="Number of observers").pack()
        self.e2 = ttk.Entry(self)
        self.e2.pack()

        ttk.Button(self, text="Return to the previous page",
                           command=lambda: controller.show_frame("PageOne")).pack(side="bottom", padx=5, pady=5)
        ttk.Button(self, text='            Continue               ', style="Accent.TButton",
                   command=lambda:  [self.get_text(), controller.show_frame("PageFour")]).pack(side="bottom", padx=5, pady=5)


    def get_text(self):
        text = self.e1.get()
        self.number_stimuli = text
        text2 = self.e2.get()
        self.number_observers = text2
        print(text + ' ' + text2)
        return [text, text2]

    def get_info(self):
        return [self.number_observers, self.number_stimuli]

class PageFour(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.title = "Test"
        self.text = ''
        ttk.Label(self, text="\n       Informations about your datasets \n", background="#007fff").pack(side="top", fill="x", pady=10)

        self.stimuli_column = ''
        self.observers_column = ''
        self.score_column = ''
        self.observers_prefix = ''

        ttk.Label(self, text="Name of stimuli column").pack()
        self.e1 = ttk.Entry(self)
        self.e1.pack()

        ttk.Label(self, text="Name of observers column").pack()
        self.e2 = ttk.Entry(self)
        self.e2.pack()

        ttk.Label(self, text="Prefix for the observers").pack()
        self.e3 = ttk.Entry(self)
        self.e3.pack()

        ttk.Label(self, text="Name of score column").pack()
        self.e4 = ttk.Entry(self)
        self.e4.pack()

        ttk.Button(self, text="Return to the previous page",
                           command=lambda: controller.show_frame("PageThree")).pack(side="bottom", padx=5, pady=5)
        ttk.Button(self, text='            Continue               ', style="Accent.TButton",
               command=lambda: [self.get_text(), controller.show_frame("PageFive")]).pack(side="bottom", padx=5, pady=5)

    def get_text(self):
        text = self.e1.get()
        text2 = self.e2.get()
        text3 = self.e3.get()
        text4 = self.e4.get()

        self.stimuli_column = text
        self.observers_column = text2
        self.score_column = text4
        self.observers_prefix = text3
        return [text, text2]

    def get_info(self):
        return [self.observers_column, self.observers_prefix, self.stimuli_column,  self.score_column]

class PageFive(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.title = "Test"
        self.text = ''
        self.tool = ''


        # defining option list
        ToolOption = ["Choose an option", "MOS of all stimuli", "Precision of subjective test", "Confidence Interval"]


        ttk.Label(self, text=" \n           Which statistical tool do you \n   "
                             "                  want to use ? ", background="#007fff")\
            .pack(side="top", fill="x", pady=10)

        self.variable = StringVar(self)
        self.variable.set(ToolOption[0])

        opt = ttk.OptionMenu(self, self.variable, *ToolOption, command= self.definition)
        # opt.config(width=90, font=('Helvetica', 12))
        opt.pack(side="top")


        self.label = ttk.Label(self, text="  ")
        #self.label.config(height=3, width=20)
        self.label.pack(expand=YES, fill=BOTH)

        ttk.Button(self, text="Return to the previous page",
                           command=lambda: controller.show_frame("PageFour")).pack(side="bottom", padx=5, pady=5)
        ttk.Button(self, text='            Continue               ', style="Accent.TButton",
               command=lambda: [self.get_tool(),controller.show_frame("PageEnd")]).pack(side="bottom", padx=5, pady=5)



    def get_tool(self):
        tool = self.variable.get()
        self.tool = tool
        return tool

    def definition(self, event):
        ToolOption = ["MOS of all stimuli", "Precision of subjective test", "Confidence Interval"]

        if self.variable.get() == ToolOption[0]:
            self.label.destroy()
            self.label = Label(self,
                               text="The MOS of all stimuli allows the user \n to see the computed MOS of the stimuli \n in their dataset.")
            self.label.config(height=3, width=20)
            self.label.pack(expand=YES, fill=BOTH)
        if self.variable.get() == ToolOption[1]:
            self.label.destroy()
            self.label = Label(self, text="The Precision of subjective test is \n a statistical tool developped \n by Margaret Pinson. ")
            self.label.config(height=3, width=20)
            self.label.pack(expand=YES, fill=BOTH)
        if self.variable.get() == ToolOption[2]:
            self.label.destroy()
            self.label = Label(self,
                               text="CI ")
            self.label.config(height=3, width=20)
            self.label.pack(expand=YES, fill=BOTH)

    def get_list(self):
        return [self.text]



class PageEnd(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.title = "Test"
        label = ttk.Label(self, text="\n Please wait ... \n ", background="#007fff")
        label.pack(side="top", fill="x", pady=10)

        ttk.Button(self, text="Return to the first page",
                        command=lambda: controller.show_frame("StartPage")).pack(padx=5,pady=5)

        ttk.Button(self, text="              End               ", style="Accent.TButton",
                        command=lambda: controller.destroy()).pack(padx=5, pady=5)


if __name__ == "__main__":
    app = SampleApp()
    # Just simply import the azure.tcl file
    #app.call("source", "Azure-ttk-theme-main/azure.tcl")

    # Then set the theme you want with the set_theme procedure
    #app.call("set_theme", "light")
    app.mainloop()

filename = app.get_page("PageOne").get_file()
print('File : ' + filename[0])

sheet_num = app.get_page("PageOne").get_sheet_num()
print('sheet_number')
print(sheet_num)

fileinfo = app.get_page("PageFour").get_info()
print('INFOS')
print(fileinfo)

tool = app.get_page("PageFive").get_tool()
print('Tool : ' + tool)

if filename[1] == 'csv':
    f = pandas.read_csv(filename[0])
elif filename[1] == 'xls':
    f = pandas.read_excel(filename[0], sheet_name=(sheet_num-1), usecols='A:AG', index_col=0, header=1, keep_default_na=True)
elif filename[1] == 'json':
    f = pandas.read_json(filename[0])
elif filename[1] == 'xml':
    f = pandas.read_xml(filename[0])
else:
    print("Invalid Format")

print(f)

if tool == "MOS of all stimuli":
    all_means(f)
elif tool == "Precision of subjective test":
    B, C = ratings_to_bew('inf', f)
    D, E = bew_to_curve(B, C)
    plt.plot(E, D)
    plt.show()
elif tool == "Confidence Interval":
    CI(filename[0])


