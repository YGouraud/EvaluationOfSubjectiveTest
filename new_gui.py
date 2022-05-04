import tkinter
from tkinter import *

from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
from tkinter import ttk

from pandas import *
from pandastable import Table, AutoScrollbar
from PIL import ImageTk, Image

from ratings_to_bew import *
from bew_to_curve import *
from bew_to_curve_100 import *
from all_MOS import *
from load_dataset import *
from import_file import *
from calculCI import *
from accuracy import *
from Sta__Dev_MOS import *

#global img

import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

class SampleApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title("PTRANS")
        self.geometry('1000x500')
        self.state("zoomed")

        # We change the style of the interface
        self.style = ttk.Style(self)
        self.call("source", "Azure-ttk-theme-main/azure.tcl")
        self.call("set_theme", "light")

        # the container is where we'll stack the frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, FileSelection, OurDatasets, DatasetSelection, StatisticalTools, About):
            #, FileSelection, OurDatasets, DatasetsInfo, DatsetsInfo2, StatisticalTools, PageEnd
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

        for i in range(6):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)

        #Menu
        label = ttk.Label(self, text=" ", background="#007fff")
        label.grid(row=0, column=0, sticky = EW, columnspan=7, ipadx = 10, ipady =20)

        ttk.Label(self, text="PTRANS", foreground="#ffffff", background="#007fff", font="bold").grid(row=0,column=0, sticky=W)
        Button(self, text="Home",
                   command=lambda: controller.show_frame("StartPage"),foreground="#ffffff", background="#007fff",borderwidth=0, highlightthickness=0, cursor="hand2")\
            .grid(row=0,column=1, sticky=E)
        Button(self, text="Add a dataset",
               command=lambda: controller.show_frame("FileSelection"), foreground="#ffffff", background="#007fff",
               borderwidth=0, highlightthickness=0, cursor="hand2").grid(row=0, column=2, sticky=E)
        Button(self, text="Statistical tools",
               command=lambda: controller.show_frame("StatisticalTools"), foreground="#ffffff", background="#007fff",
               borderwidth=0, highlightthickness=0, cursor="hand2").grid(row=0, column=3, sticky=E)
        Button(self, text="About",
               command=lambda: controller.show_frame("About"), foreground="#ffffff", background="#007fff",
               borderwidth=0, highlightthickness=0, cursor="heart").grid(row=0, column=4, sticky=E)

        ttk.Label(self, text="Welcome to our tool !").grid(row=1, column=2,columnspan=2)
        ttk.Button(self, text="You want to add your own dataset",
                            command=lambda: controller.show_frame("FileSelection"), cursor="hand2")\
            .grid(row=2,column=2, sticky =EW, columnspan =2, ipady=10)
        ttk.Button(self, text="You want to use the datasets that we have",
                            command=lambda: controller.show_frame("OurDatasets"), cursor="hand2")\
            .grid(row=3,column=2, sticky =EW, columnspan =2, ipady=10)

class FileSelection(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.sheet_number = None
        self.controller = controller
        self.file = ''
        self.filetype = ''
        self.dataset = None

        for i in range(6):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)

        #Menu
        label = ttk.Label(self, text=" ", background="#007fff")
        label.grid(row=0, column=0, sticky = EW, columnspan=7, ipadx = 10, ipady =20)

        ttk.Label(self, text="PTRANS", foreground="#ffffff", background="#007fff", font="bold").grid(row=0,column=0, sticky=W)
        Button(self, text="Home",
                   command=lambda: controller.show_frame("StartPage"),foreground="#ffffff", background="#007fff",borderwidth=0, highlightthickness=0, cursor="hand2")\
            .grid(row=0,column=1,sticky=E)
        Button(self, text="Add a dataset",
               command=lambda: controller.show_frame("FileSelection"), foreground="#ffffff", background="#007fff",
               borderwidth=0, highlightthickness=0, cursor="hand2").grid(row=0, column=2, sticky=E)
        Button(self, text="Statistical tools",
               command=lambda: controller.show_frame("StatisticalTools"), foreground="#ffffff", background="#007fff",
               borderwidth=0, highlightthickness=0, cursor="hand2").grid(row=0, column=3, sticky=E)
        Button(self, text="About",
               command=lambda: controller.show_frame("About"), foreground="#ffffff", background="#007fff",
               borderwidth=0, highlightthickness=0, cursor="heart").grid(row=0, column=4, sticky=E)

        #File input
        ttk.Label(self, text="You can input a new file").grid(row=1, column=2, columnspan=2)

        open_button = ttk.Button(self, text='Open a File', command=lambda: [self.select_file(), self.option()], cursor="hand2")

        open_button.grid(row=2, column=2, columnspan=2)

        # defining option list for the dropdown menu
        # the menu only appears if the file is an xls file
        OptionSheet = [1, 1, 2, 3]

        self.variable = IntVar(self)
        self.variable.set(OptionSheet[0])

        self.opt = ttk.OptionMenu(self, self.variable, *OptionSheet)

        # the button open a popup with more info about the dataset structure
        ttk.Button(self, text='Information',
                   command=lambda: self.popup_info(), cursor='hand2')\
            .grid(row=1, column=4)

        ttk.Button(self, text='Continue', style="Accent.TButton",
                   command=lambda: [controller.get_page("DatasetSelection").get_new_dataset(),controller.show_frame("DatasetSelection")],
                   cursor="hand2")\
            .grid(row=5,column=2, columnspan=2, sticky=EW)

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
            ttk.Label(self, text="Which sheet to use ?").grid(row=3, column=1)
            self.opt.grid(row=3, column=2)
        else:
            pass

    def popup_info(self):
        popup = Toplevel()
        popup.geometry("800x550")
        popup.wm_title("Information on Datasets")

        quote ='''
        In this format, observers' ratings of each individual stimuli are presented like a matrix.
        For example, the 5 highlighted represents the rating result of stimulus 2 by observer 2. This format can be directly entered into the system for analysis.
                - The first column gives the names of all stimuli, no column names are required for this column, i.e. cellA1 is empty. 
                - There are no requirements for stimuli names.
                - The last column name is MOS (main opinion score). 
                - Each remaining column represents an observer. The column name is the observer's number or name. 
                - The number of columns can vary depending on the number of observers.
                '''

        title = Text(popup, height=2, font=("Helvetica", 16), borderwidth=0, padx=15)
        title.insert(END, "\n Standard Format\n")
        title['state'] = 'disabled'
        title.pack(side=TOP, fill=X)
        text = Text(popup, height=10, wrap='word', borderwidth=0, padx=5)
        text.insert(END, quote)
        text['state'] = 'disabled'
        text.pack(side=TOP, fill=X)

        img = ImageTk.PhotoImage(Image.open("image/data_structure.gif"))
        label2 = Label(popup, image=img)
        label2.pack(fill=X)
        label2.image = img

        ttk.Button(popup, text="Continue", command=lambda: [self.popup_info2(), popup.destroy()], cursor="hand2").pack()

    def popup_info2(self):
        popup = Toplevel()
        popup.geometry("800x550")
        popup.wm_title("Information on Datasets")

        quote = '''
            In this format, each row records an observational experiment, and it contains all the data generated by a stimuli seen by an observer.
            The data in this format needs to be converted into our standard format and then entered into the system for analysis. 
            Please follow the system prompts and enter the corresponding column name.

            Three columns of information are necessary: observer, stimulus name, score.
            Datasets can contain additional attribute columns (but these attributes will be ignored).
            There is no requirement for column names, but you need to enter column name information during format conversion.
            '''

        title = Text(popup, height=2, font=("Helvetica", 16), borderwidth=0, padx=15)
        title.insert(END, "\n Other format\n")
        title['state'] = 'disabled'
        title.pack(side=TOP, fill=X)
        text = Text(popup, height=10, wrap='word', borderwidth=0, padx=5)
        text.insert(END, quote)
        text['state'] = 'disabled'
        text.pack(side=TOP, fill=X)

        img = ImageTk.PhotoImage(Image.open("image/other_structure.gif"))
        label2 = Label(popup, image=img)
        label2.pack(fill=X)
        label2.image = img

        ttk.Button(popup, text="Continue", command=popup.destroy, cursor="hand2").pack(side=RIGHT, padx=30)
        ttk.Button(popup, text="Back", command=lambda: [popup.destroy(), self.popup_info()], cursor="hand2").pack(side=LEFT, padx=30)

    def get_file(self):
        return [self.file, self.filetype]

    def get_sheet_num(self):
        sheet = self.variable.get()
        self.sheet_number = sheet
        return sheet

    def get_current_dataset(self):
        filename = self.get_file()

        if filename[1] == 'csv':
            self.dataset = pandas.read_csv(filename[0])
        elif filename[1] == 'xls':
            self.dataset = pandas.read_excel(filename[0], sheet_name=(self.get_sheet_num() - 1), keep_default_na=True)
        elif filename[1] == 'json':
            self.dataset = pandas.read_json(filename[0])
        elif filename[1] == 'xml':
            self.dataset = pandas.read_xml(filename[0])
        else:
            print("Invalid Format")
            self.dataset = None

        return self.dataset




class OurDatasets(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        for i in range(6):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)

        self.button_dict = {}

        #Menu
        label = ttk.Label(self, text=" ", background="#007fff")
        label.grid(row=0, column=0, sticky = EW, columnspan=7, ipadx = 10, ipady =20)

        ttk.Label(self, text="PTRANS", foreground="#ffffff", background="#007fff", font="bold").grid(row=0,column=0, sticky=W)
        Button(self, text="Home",
                   command=lambda: controller.show_frame("StartPage"),foreground="#ffffff", background="#007fff",borderwidth=0, highlightthickness=0, cursor="hand2")\
            .grid(row=0,column=1, sticky=E)
        Button(self, text="Add a dataset",
               command=lambda: controller.show_frame("FileSelection"), foreground="#ffffff", background="#007fff",
               borderwidth=0, highlightthickness=0, cursor="hand2").grid(row=0, column=2, sticky=E)
        Button(self, text="Statistical tools",
               command=lambda: controller.show_frame("StatisticalTools"), foreground="#ffffff", background="#007fff",
               borderwidth=0, highlightthickness=0, cursor="hand2").grid(row=0, column=3, sticky=E)
        Button(self, text="About",
               command=lambda: controller.show_frame("About"), foreground="#ffffff", background="#007fff",
               borderwidth=0, highlightthickness=0, cursor="heart").grid(row=0, column=4, sticky=E)

        ttk.Label(self, text="Here are the already available datasets, you may choose one to use.",
                  background="#007fff").grid(row=2, column=2, columnspan=2)

        #Create a text widget with a scrollbar for buttons
        self.text_box = Text(self, wrap="none")
        self.text_box.tag_configure("center", justify='center')
        vsb = Scrollbar(self, command=self.text_box.yview)
        self.text_box.configure(yscrollcommand=vsb.set)
        self.text_box.grid(column=2, columnspan=2)


        self.datasets = None
        self.datasets_name = []
        self.current_dataset = None
        self.title = "Test"

        # Create a button for each dataset to select it
        self.dataset_list()

        ttk.Button(self, text="  Return to the first page   ",
                   command=lambda: controller.show_frame("StartPage")).grid(column=2, columnspan=2)
        ttk.Button(self, text='            Continue               ', style="Accent.TButton",
                   command=lambda: [controller.get_page("DatasetSelection").get_existing_dataset(),
                                    controller.show_frame("DatasetSelection")]).grid(column=2, columnspan=2)

    def dataset_list(self):
        dataset_dict = load_dataset()
        self.datasets = dataset_dict

        for name in dataset_dict:
            self.datasets_name.append(name)
            button = self.create_Button(name)
            self.text_box.window_create("end", window=button)
            self.text_box.insert("end", "\n")
            #button.grid(column=2, columnspan=2)
            self.button_dict[name] = button

        self.text_box.tag_add("center", "1.0", "end")
        self.text_box.config(state="disabled")

        return

    def create_Button(self, name):
        style = ttk.Style()
        style.configure('SunkableButton.TButton')
        style.map("SunkableButton.TButton",
                  foreground=[('disabled','red'),('!disabled','black')],
                  background=[('disabled','#007fff'),('!disabled','red')],
                  activebackground=[('disabled','#007fff'),('!disabled','red')])
        return ttk.Button(self, text=name, command=lambda: [self.assign_dataset(name), self.start(name)],
                          style='SunkableButton.TButton')

    #Change the state of a pressed button
    def start(self, name):
        for a in self.button_dict:
            if a != name:
                self.button_dict[a].state(['!disabled'])
                pass
        self.button_dict[name].state(['disabled'])
        return

    def assign_dataset(self, name):
        self.current_dataset = self.datasets[name]
        return

    def get_current_dataset(self):
        return self.current_dataset

class DatasetSelection(Frame):
    """Basic test frame for the table"""

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        #self.geometry = '500x500'
        self.table = None

        for i in range(6):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)

        # Menu
        label = ttk.Label(self, text=" ", background="#007fff")
        label.grid(row=0, column=0, sticky='ew', columnspan=7, ipadx=10, ipady=20)

        ttk.Label(self, text="PTRANS", foreground="#ffffff", background="#007fff", font="bold").grid(row=0, column=0,
                                                                                                     sticky=W)

        Button(self, text="Home",
               command=lambda: controller.show_frame("StartPage"), foreground="#ffffff", background="#007fff",
               borderwidth=0, highlightthickness=0, cursor="hand2") \
            .grid(row=0, column=1, sticky='e', padx=10)
        Button(self, text="Add a dataset",
               command=lambda: controller.show_frame("FileSelection"), foreground="#ffffff", background="#007fff",
               borderwidth=0, highlightthickness=0, cursor="hand2").grid(row=0, column=2, sticky='e', padx=10)
        Button(self, text="Statistical tools",
               command=lambda: controller.show_frame("StatisticalTools"), foreground="#ffffff", background="#007fff",
               borderwidth=0, highlightthickness=0, cursor="hand2").grid(row=0, column=3, sticky='e',padx=10)
        Button(self, text="About",
               command=lambda: controller.show_frame("About"), foreground="#ffffff", background="#007fff",
               borderwidth=0, highlightthickness=0, cursor="heart").grid(row=0, column=4, sticky='e', padx=10)



        label = Label(self, text="Choose precisely what part of the file you want to use", foreground="#ffffff", background="#007fff")
        label.grid(column=0, row=1, columnspan=5, sticky=N)

        Button(self, height=2, width=35, text="Select this SubDataset ?",
               command=lambda: [self.table.remove(), controller.show_frame("StatisticalTools")]).grid(column=1, row=7, columnspan=3,  sticky='ew')

    def get_new_dataset(self):
        window = Frame(self)
        window.grid(column=0, row=2, rowspan=1, columnspan=5, sticky='news')

        df = self.controller.get_page("FileSelection").get_current_dataset()

        self.table = Table(window, dataframe=df, showtoolbar=False, showstatusbar=False)
        self.table.showIndex()
        self.table.show()
        return

    def get_existing_dataset(self):
        window = Frame(self)
        window.grid(column=0, row=2, rowspan=1, columnspan=5, sticky='news')

        df = self.controller.get_page("OurDatasets").get_current_dataset()

        self.table = Table(window, dataframe=df, showtoolbar=False, showstatusbar=False)
        self.table.showIndex()
        self.table.show()
        return

    def use_dataset(self):
        return self.table.getSubdata()

class StatisticalTools(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.text = ''
        self.tool = ''

        for i in range(6):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)

        #Menu
        label = ttk.Label(self, text=" ", background="#007fff")
        label.grid(row=0, column=0, sticky = EW, columnspan=7, ipadx = 10, ipady =20)

        ttk.Label(self, text="PTRANS", foreground="#ffffff", background="#007fff", font="bold").grid(row=0,column=0, sticky=W)
        Button(self, text="Home",
                   command=lambda: controller.show_frame("StartPage"),foreground="#ffffff", background="#007fff",borderwidth=0, highlightthickness=0, cursor="hand2")\
            .grid(row=0,column=1, sticky=E)
        Button(self, text="Add a dataset",
               command=lambda: controller.show_frame("FileSelection"), foreground="#ffffff", background="#007fff",
               borderwidth=0, highlightthickness=0, cursor="hand2").grid(row=0, column=2, sticky=E)
        Button(self, text="Statistical tools",
               command=lambda: controller.show_frame("StatisticalTools"), foreground="#ffffff", background="#007fff",
               borderwidth=0, highlightthickness=0, cursor="hand2").grid(row=0, column=3, sticky=E)
        Button(self, text="About",
               command=lambda: controller.show_frame("About"), foreground="#ffffff", background="#007fff",
               borderwidth=0, highlightthickness=0, cursor="heart").grid(row=0, column=4, sticky=E)

        ttk.Label(self, text="Which statistical tool do you want to use ? ") \
            .grid(row=1, column=2, columnspan=2)

        # defining option list
        ToolOption = ["Choose an option", "MOS of all stimuli", "Precision of subjective test (ACR-5)", "Precision of subjective test (ACR-100)", "Confidence Interval","Accuracy","Standard deviation of MOS"]

        self.variable = StringVar(self)
        self.variable.set(ToolOption[0])

        opt = ttk.OptionMenu(self, self.variable, *ToolOption, command= self.definition)
        opt.grid(row=2, column=2, columnspan=2)


        self.label = Text(self, borderwidth=0)
        self.label['state'] = 'disabled'
        self.label.grid(row=3,column=2, columnspan=2)

        self.save = IntVar(self)
        check = Checkbutton(self, variable=self.save, text="Save results in a xls file ?")
        check.grid(row=4, column=2, columnspan=2)

        ttk.Button(self, text='Start', style="Accent.TButton",
                   command=lambda: [self.get_tool(),self.go()], cursor="hand2").grid(row=5,column=2, sticky=EW, columnspan=2)


    def get_tool(self):
        tool = self.variable.get()
        self.tool = tool
        return tool

    def definition(self, event):
        ToolOption = ["MOS of all stimuli", "Precision of subjective test", "Confidence Interval","Accuracy","Standard deviation of MOS"]

        if self.variable.get() == ToolOption[0]:
            self.label.destroy()
            description = '''
            Using the evaluation given by all of the observers, the tool computes the MOS for all the stimuli.
            You can choose to save the result as a .csv by clicking the checkbox below.'''

            self.label = Text(self, wrap='word', borderwidth=0)
            self.label.tag_configure('tag-center', justify='left')
            self.label.insert(END, description, 'tag-center')
            self.label['state'] = 'disabled'
            self.label.grid(row=4, column=1, columnspan=4)
        if self.variable.get() == ToolOption[1]:
            self.label.destroy()
            description='''
            The Precision of subjective test is a statistical tool developed by Margaret H.Pinson as seen in “Confidence Intervals for Subjective Tests and Objective Metrics That Assess Image, Video, Speech, or Audiovisual Quality”.

            It uses the Student t-test on all pairs of stimuli A and B, where both stimuli were rated by the same subjects and the stimuli are drawn from the same dataset, to compare their rating distribution at 95% confidence level.'''

            self.label = Text(self, wrap='word',borderwidth=0)
            self.label.tag_configure('tag-center', justify='left')
            self.label.insert(END,description, 'tag-center')
            self.label['state'] = 'disabled'
            self.label.grid(row=4,column=1, columnspan=4)

        if self.variable.get() == ToolOption[2]:
            self.label.destroy()
            description = '''CI.'''

            self.label = Text(self, wrap='word', borderwidth=0)
            self.label.tag_configure('tag-center', justify='left')
            self.label.insert(END, description, 'tag-center')
            self.label['state'] = 'disabled'
            self.label.grid(row=4, column=1, columnspan=4)
        if self.variable.get() == ToolOption[3]:
            self.label.destroy()
            description = '''
                        The Accuracy test is a statistical tool developed by Yana Nehmé as seen in ‘Comparison of subjective methods for quality assessment of 3d graphics in virtual reality’.

                        To study the difference of accuracy between the two methods, Yana Nehme used an unpaired two-samples Wilcoxon test. 
                        '''

            self.label = Text(self, wrap='word', borderwidth=0)
            self.label.tag_configure('tag-center', justify='left')
            self.label.insert(END, description, 'tag-center')
            self.label['state'] = 'disabled'
            self.label.grid(row=4, column=1, columnspan=4)

    def get_list(self):
        return [self.text]

    def get_save(self):
        save = self.save.get()
        return save

    def go(self):

        filename = app.get_page("FileSelection").get_file()
        print('File : ' + filename[0])

        sheet_num = app.get_page("FileSelection").get_sheet_num()
        print('sheet_number')
        print(sheet_num)

        tool = app.get_page("StatisticalTools").get_tool()
        print('Tool : ' + tool)

        save = app.get_page("StatisticalTools").get_save()
        print(save)

        #Getting the dataset that is going to be used
        f = app.get_page("DatasetSelection").use_dataset()

        print(f)

        if tool == "MOS of all stimuli":
            all_means(f, save)
        elif tool == "Precision of subjective test (ACR-5)":
            B, C = ratings_to_bew('inf', f)
            D, E = bew_to_curve(B, C)
            plt.plot(E, D)
            plt.title(filename[2])
            plt.xlabel('DeltaS')
            plt.ylabel('PI')
            plt.grid(True, linestyle='-')
            plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
            plt.show()

        elif tool == "Precision of subjective test (ACR-100)":
            B, C = ratings_to_bew('inf', f)
            D, E = bew_to_curve_100(B, C)
            plt.plot(E, D)
            plt.title(filename[2])
            plt.xlabel('DeltaS')
            plt.ylabel('PI')
            plt.grid(True, linestyle='-')
            plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
            plt.show()

        elif tool == "Confidence Interval":
            CI(f)
        elif tool == "Accuracy":
            accuracy(f)
        elif tool == "Standard deviation of MOS":
            standard_deviation(f)


class About(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.text = ''
        self.tool = ''

        for i in range(6):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)

        #Menu
        label = ttk.Label(self, text=" ", background="#007fff")
        label.grid(row=0, column=0, sticky = EW, columnspan=7, ipadx = 10, ipady =20)

        ttk.Label(self, text="PTRANS", foreground="#ffffff", background="#007fff", font="bold").grid(row=0,column=0, sticky=W)
        Button(self, text="Home",
                   command=lambda: controller.show_frame("StartPage"),foreground="#ffffff", background="#007fff",borderwidth=0, highlightthickness=0, cursor="hand2")\
            .grid(row=0,column=1, sticky=E)
        Button(self, text="Add a dataset",
               command=lambda: controller.show_frame("FileSelection"), foreground="#ffffff", background="#007fff",
               borderwidth=0, highlightthickness=0, cursor="hand2").grid(row=0, column=2, sticky=E)
        Button(self, text="Statistical tools",
               command=lambda: controller.show_frame("StatisticalTools"), foreground="#ffffff", background="#007fff",
               borderwidth=0, highlightthickness=0, cursor="hand2").grid(row=0, column=3, sticky=E)
        Button(self, text="About",
               command=lambda: controller.show_frame("About"), foreground="#ffffff", background="#007fff",
               borderwidth=0, highlightthickness=0, cursor="heart").grid(row=0, column=4, sticky=E)


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()

