import tkinter
from tkinter import *
import threading

from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
from tkinter import ttk

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  NavigationToolbar2Tk)
from pandas import *
from pandastable import Table, AutoScrollbar
from PIL import ImageTk, Image

from precision_ACR5 import *
from precision_ACR100 import *
from all_MOS import *
from load_dataset import *
from import_file import *
from calculCI import *
from accuracy import *
from Sta__Dev_MOS import *
from trans import *



class SampleApp(Tk):
    """The main frame window"""

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

        for F in (StartPage, FileSelection, OurDatasets, DatasetSelection, NewDatasetSelection, StatisticalTools, ShowResults, About):
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
    """The starting page of our tool"""

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
                   command=lambda: controller.show_frame("StartPage"),foreground="#011f3d", background="#007fff",borderwidth=0, highlightthickness=0, cursor="hand2")\
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
    """Use an user provided dataset"""
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.sheet_number = None
        self.controller = controller
        self.file = ''
        self.filetype = ''
        self.name = ''
        self.filename = None
        self.dataset = None

        for i in range(6):
            self.grid_columnconfigure(i, weight=1)

        for i in range(9):
            self.grid_rowconfigure(i, weight=1)

        #Menu
        label = ttk.Label(self, text=" ", background="#007fff")
        label.grid(row=0, column=0, sticky = EW, columnspan=7, ipadx = 10, ipady =20)

        ttk.Label(self, text="PTRANS", foreground="#ffffff", background="#007fff", font="bold").grid(row=0,column=0, sticky=W)
        Button(self, text="Home",
                   command=lambda: controller.show_frame("StartPage"),foreground="#ffffff", background="#007fff",borderwidth=0, highlightthickness=0, cursor="hand2")\
            .grid(row=0,column=1,sticky=E)
        Button(self, text="Add a dataset",
               command=lambda: controller.show_frame("FileSelection"), foreground="#011f3d", background="#007fff",
               borderwidth=0, highlightthickness=0, cursor="hand2").grid(row=0, column=2, sticky=E)
        Button(self, text="Statistical tools",
               command=lambda: controller.show_frame("StatisticalTools"), foreground="#ffffff", background="#007fff",
               borderwidth=0, highlightthickness=0, cursor="hand2").grid(row=0, column=3, sticky=E)
        Button(self, text="About",
               command=lambda: controller.show_frame("About"), foreground="#ffffff", background="#007fff",
               borderwidth=0, highlightthickness=0, cursor="heart").grid(row=0, column=4, sticky=E)

        #File input
        ttk.Label(self, text="You can input a new file").grid(row=1, column=2, columnspan=2)

        open_button = ttk.Button(self, text='Open a File', command=lambda: [self.select_file(), self.show_name_of_file()], cursor="hand2")

        open_button.grid(row=2, column=2, columnspan=2)

        # the button open a popup with more info about the dataset structure
        ttk.Button(self, text='Information',
                   command=lambda: self.popup_info(), cursor='hand2')\
            .grid(row=1, column=4)

        ttk.Button(self, text='Continue', style="Accent.TButton",
                   command=lambda: [controller.get_page("NewDatasetSelection").get_new_dataset(),
                                    controller.get_page("NewDatasetSelection").sheet_option(),
                                    controller.show_frame("NewDatasetSelection"),
                                    self.filename.destroy()],
                   cursor="hand2")\
            .grid(row=5,column=2, columnspan=2, sticky=EW)

    def select_file(self):
        """Function that let the user select a file to use"""
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
        self.name = filename.split("/").pop()

    """
    def sheet_number(self):
        Give the number of sheet in a xls or xlsx file
        df = pandas.read_excel(self.file, sheet_name=None)  # read all sheets
        sheet = len(df)
        return sheet
    """

    def popup_info(self):
        popup = Toplevel()
        popup.geometry("800x550")
        popup.wm_title("Information on Datasets")

        quote ='''
        In this format, observers' ratings of each individual stimuli are presented like a matrix.
        For example, the highlighted cell represents the rating result of stimulus 2 by observer 2. This format can be directly entered into the system for analysis.
                - The first column gives the names of all stimuli, no column names are required for this column. 
                - There are no requirements for stimuli names.
                - The last column name is MOS (Mean Opinion Score). 
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
        return [self.file, self.filetype, self.name]

    def get_current_dataset(self, sheet_number):
        filename = self.get_file()

        if filename[1] == 'csv':
            self.dataset = pandas.read_csv(filename[0])
        elif filename[1] == 'xls' or filename[1] == 'xlsx':
            self.dataset = pandas.read_excel(filename[0], sheet_name=(sheet_number - 1), keep_default_na=True)
        elif filename[1] == 'json':
            self.dataset = pandas.read_json(filename[0])
        elif filename[1] == 'xml':
            self.dataset = pandas.read_xml(filename[0])
        else:
            print("Invalid Format")
            self.dataset = None

        return self.dataset

    def show_name_of_file(self):
        """Show the name of the selected datafile"""

        ttk.Label(self, text="Name of the file : ").grid(row=3, column=1)
        self.filename = ttk.Label(self, text=self.name)
        self.filename.grid(row=3, column=2, columnspan=2)


class NewDatasetSelection(Frame):
    """Select the part of user provided dataset needed to formalize it and ingest it"""

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.table = None
        self.dataset = None
        #self.subdataset = None
        self.stimuli = None
        self.observer = None
        self.rating = None
        self.formalized = None
        self.img = []

        for i in range(8):
            self.grid_columnconfigure(i, weight=1)

        for i in range(6):
            self.grid_rowconfigure(i, weight=1)

        # Menu
        label = ttk.Label(self, text=" ", background="#007fff")
        label.grid(row=0, column=0, sticky='ew', columnspan=8, ipadx=10, ipady=20)

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



        label = Label(self, text="To simplify the ingestion of your dataset, please select the three necessary parts",
                      foreground="#ffffff", background="#007fff")
        label.grid(column=0, row=1, columnspan=5, sticky=N)



        Button(self, height=2, width=35, text="Name of stimuli column/row",
               command=lambda: [self.select_attributes('stimuli')])\
            .grid(column=6, row=3, sticky='ew')

        Button(self, height=2, width=35, text="Name of observers column/row",
               command=lambda: [self.select_attributes('observer')])\
            .grid(column=6, row=4, sticky='ew')

        Button(self, height=2, width=35, text="Name of ratings column/row",
               command=lambda: [self.select_attributes('rating')])\
            .grid(column=6, row=5, sticky='ew')

        Button(self, height=2, width=35, text="End of selection",
               command=lambda: [self.save_formalized_data(transform_data(self.dataset, self.stimuli, self.observer, self.rating)),
                                controller.get_page("DatasetSelection").get_existing_dataset(),
                                controller.show_frame("DatasetSelection")])\
            .grid(column=6, row=6, sticky='ew')

    def get_new_dataset(self, sheet_number=1):
        """Show the dataset inputted by the user"""

        if sheet_number == 0:
            sheet_number = 1

        if self.table is not None:
            self.table.remove()

        window = Frame(self)
        window.grid(column=0, row=2, rowspan=4, columnspan=4, sticky='news')

        df = self.controller.get_page("FileSelection").get_current_dataset(sheet_number)

        self.dataset = df

        self.table = Table(window, dataframe=df, showtoolbar=False, showstatusbar=False)
        self.table.showIndex()
        self.table.show()
        return

    def select_attributes(self, attr):
        """Take the selected row/column of a specific criteria"""
        switch = {
            'stimuli': 3,
            'observer': 4,
            'rating': 5
        }

        df = self.table.getSelectedDataFrame()
        attribute = switch.get(attr)
        if attribute == 3:
            self.stimuli = df.columns[0]
        elif attribute == 4:
            self.observer = df.columns[0]
        elif attribute == 5:
            self.rating = df.columns[0]

        im = Image.open("image/green_check.png")
        size = 32, 32
        im.thumbnail(size)
        img = ImageTk.PhotoImage(im)
        label = Label(self, image=img, width=32, height=32)
        label.grid(column=7, row=attribute, sticky='ew')
        label.image = img
        self.img.append(label)


    def save_formalized_data(self, data):
        """Save formalized data into a variable to be used later"""
        self.formalized = data
        self.controller.get_page("OurDatasets").current_dataset = data

    def reset_selected(self):
        """Reset the selected column/rows"""
        self.rating = None
        self.stimuli = None
        self.observer = None

        for i in self.img:
            i.destroy()



    def sheet_option(self):
        """If the user inputted an Excel file, give the option to select which
        """
        file, filetype, name = self.controller.get_page("FileSelection").get_file()

        if filetype == 'xls' or filetype == 'xlsx':
            df = pandas.read_excel(file, sheet_name=None)  # read all sheets
            sheet = len(df)
            option_sheet = [i for i in range(sheet + 1)]

            self.variable = IntVar(self)
            self.variable.set(option_sheet[0])
            self.opt = ttk.OptionMenu(self, self.variable, *option_sheet,
                                      command=lambda x: [self.get_new_dataset(self.variable.get())])

            ttk.Label(self, text="Which sheet to use ?").grid(row=1, column=6)
            self.opt.grid(column=6, row=2, columnspan=2)


class OurDatasets(Frame):
    """Select an existing dataset from the University of Nantes you want to use"""

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
                  ).grid(row=2, column=2, columnspan=2)

        #Create a text widget with a scrollbar for buttons
        self.text_box = Text(self, wrap="none", borderwidth=0, spacing1=5)
        self.text_box.tag_configure("center", justify='center')
        vsb = Scrollbar(self, command=self.text_box.yview)

        self.text_box.configure(yscrollcommand=vsb.set)
        self.text_box.grid(column=2, columnspan=2)

        self.dataset_name = ''
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
        
        return ttk.Button(self, text=name, command=lambda: [self.assign_dataset(name), self.start(name), self.set_name(name)],
                          style='SunkableButton.TButton', width=60)


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

    def set_name(self, name):
        self.dataset_name = name
        pass

    def get_name(self):
        return self.dataset_name

class DatasetSelection(Frame):
    """Select the part of an existing dataset you want to use"""

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.table = None
        self.dataset = None

        for i in range(6):
            self.grid_columnconfigure(i, weight=1)
        for i in range(8):
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



        label = Label(self, text="Choose precisely what part of the file you want to use")
        label.grid(column=0, row=1, columnspan=5, sticky=N)

        Button(self, height=2, width=35, text="Select this SubDataset ?",
               command=lambda: [self.table.remove(), controller.show_frame("StatisticalTools")])\
            .grid(column=1, row=4, columnspan=3,  sticky='ew')

        Button(self, height=2, width=35, text="Use the full dataset ?",
               command=lambda: [self.table.remove(), controller.show_frame("StatisticalTools")])\
            .grid(column=1, row=5,columnspan=3,sticky='ew')

    def get_existing_dataset(self):
        window = Frame(self)
        window.grid(column=0, row=2, rowspan=1, columnspan=5, sticky='news')

        self.dataset = self.controller.get_page("OurDatasets").get_current_dataset()

        self.table = Table(window, dataframe=self.dataset, showtoolbar=False, showstatusbar=False)
        self.table.showIndex()
        self.table.show()
        return

    def use_subdataset(self):
        df = self.table.getSelectedDataFrame()
        # flatten multi-index
        df.columns = df.columns.get_level_values(0)
        self.dataset = df




class StatisticalTools(Frame):
    """Select which statistical tool you want to use on the selected dataset"""

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.text = ''
        self.tool = ''

        self.result = None

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
               command=lambda: controller.show_frame("StatisticalTools"), foreground="#011f3d", background="#007fff",
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

        ttk.Button(self, text='Start', style="Accent.TButton",
                    command=lambda: [self.get_tool(), controller.show_frame("ShowResults"), self.go_bg()], cursor="hand2").grid(row=5,column=2, sticky=EW, columnspan=2)


    def get_tool(self):
        tool = self.variable.get()
        self.tool = tool
        return tool

    def definition(self, event):
        ToolOption = ["MOS of all stimuli", "Precision of subjective test (ACR-5)", "Precision of subjective test (ACR-100)", "Confidence Interval","Accuracy","Standard deviation of MOS"]

        if self.variable.get() == ToolOption[0]:
            self.label.destroy()
            description = '''
            Using the evaluation given by all of the observers, the tool computes the MOS for all the stimuli.
            '''

            self.label = Text(self, wrap='word', borderwidth=0)
            self.label.tag_configure('tag-center', justify='left')
            self.label.insert(END, description, 'tag-center')
            self.label['state'] = 'disabled'
            self.label.grid(row=4, column=1, columnspan=4)

            check = Checkbutton(self, variable=self.save, text="Save results in a xls file ?")
            check.grid(row=4, column=2, columnspan=2)

        if self.variable.get() == ToolOption[1]:
            self.label.destroy()
            description='''
            The Precision of subjective test is a statistical tool developed by Margaret H.Pinson as seen in “Confidence Intervals for Subjective Tests and Objective Metrics That Assess Image, Video, Speech, or Audiovisual Quality”.

            It uses the Student t-test on all pairs of stimuli A and B, where both stimuli were rated by the same subjects and the stimuli are drawn from the same dataset, to compare their rating distribution at 95% confidence level.
            
            This tool is for ACR-5 ratings !'''

            self.label = Text(self, wrap='word',borderwidth=0)
            self.label.tag_configure('tag-center', justify='left')
            self.label.insert(END,description, 'tag-center')
            self.label['state'] = 'disabled'
            self.label.grid(row=4, column=1, columnspan=4)

        if self.variable.get() == ToolOption[2]:
            self.label.destroy()
            description = '''
            The Precision of subjective test is a statistical tool developed by Margaret H.Pinson as seen in “Confidence Intervals for Subjective Tests and Objective Metrics That Assess Image, Video, Speech, or Audiovisual Quality”.

            It uses the Student t-test on all pairs of stimuli A and B, where both stimuli were rated by the same subjects and the stimuli are drawn from the same dataset, to compare their rating distribution at 95% confidence level.

            This tool is for ACR-100 ratings !'''

            self.label = Text(self, wrap='word', borderwidth=0)
            self.label.tag_configure('tag-center', justify='left')
            self.label.insert(END, description, 'tag-center')
            self.label['state'] = 'disabled'
            self.label.grid(row=4, column=1, columnspan=4)

        if self.variable.get() == ToolOption[3]:
            self.label.destroy()
            description = '''
            The Confidence Interval is a statistical tool developed by Yana Nehmé as seen in ‘Exploring Crowdsourcing for Subjective Quality Assessment of 3D Graphics’.
            It draws several sample of N observers and calculates the evolution of the MOS and its 95% CI according to the number of observers.
            '''

            self.label = Text(self, wrap='word', borderwidth=0)
            self.label.tag_configure('tag-center', justify='left')
            self.label.insert(END, description, 'tag-center')
            self.label['state'] = 'disabled'
            self.label.grid(row=4, column=1, columnspan=4)
        if self.variable.get() == ToolOption[4]:
            self.label.destroy()
            description = '''
            The Accuracy test is a statistical tool developed by Yana Nehmé as seen in ‘Comparison of subjective methods for quality assessment of 3d graphics in virtual reality’.
            It draws several sample of N observers and uses an unpaired two-samples Wilcoxon test  to find wich sample are statistically different.
            '''

            self.label = Text(self, wrap='word', borderwidth=0)
            self.label.tag_configure('tag-center', justify='left')
            self.label.insert(END, description, 'tag-center')
            self.label['state'] = 'disabled'
            self.label.grid(row=4, column=1, columnspan=4)

        if self.variable.get() == ToolOption[5]:
            self.label.destroy()
            description = '''
            The Standard deviation of the MOS is computed by drawing several sample of N observers in the dataset and computing their average SD of the MOS.
            Showed on the curves is also distribution interval of the SD in a light shade of blue.
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

    def go_bg(self):
        threading.Thread(target=self.go()).start()
        print("test")

    def go(self):

        filename = app.get_page("FileSelection").get_file()
        print('File : ' + filename[0])

        tool = app.get_page("StatisticalTools").get_tool()
        print('Tool : ' + tool)

        save = app.get_page("StatisticalTools").get_save()
        #print(save)

        name = app.get_page("OurDatasets").get_name()

        #Getting the dataset that is going to be used
        f = app.get_page("DatasetSelection").dataset

        #print(f)

        if tool == "MOS of all stimuli":
            self.result = all_means(f, save)
            self.controller.get_page("ShowResults").show_data(self.result)
        elif tool == "Precision of subjective test (ACR-5)":
            self.result = precision_ACR5(f, name)
            self.controller.get_page("ShowResults").show_plot(self.result)
        elif tool == "Precision of subjective test (ACR-100)":
            self.result = precision_ACR100(f, name)
            self.controller.get_page("ShowResults").show_plot(self.result)
        elif tool == "Confidence Interval":
            self.result = CI(f)
            self.controller.get_page("ShowResults").show_plot(self.result)
        elif tool == "Accuracy":
            self.result = accuracy(f)
            self.controller.get_page("ShowResults").show_plot(self.result)
        elif tool == "Standard deviation of MOS":
            self.result = standard_deviation(f)
            self.controller.get_page("ShowResults").show_plot(self.result)

    def precision_ACR5_bg(self, f, name):
        threading.Thread(target=precision_ACR5(f, name)).start()
        print("saucisse")

class ShowResults(Frame):
    """Showing the result of the statistical tool on the dataset"""

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.results = None
        self.subdataset = None

        for i in range(6):
            self.grid_columnconfigure(i, weight=1)
        for i in range(6):
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


        label = Label(self, text="Here are the results",
                      foreground="#ffffff", background="#007fff")
        label.grid(column=0, row=1, columnspan=2, rowspan=2, sticky="new")


    def show_data(self, results):
        if self.results is not None:
            self.results.remove()

        window = Frame(self)
        window.grid(column=0, row=3, rowspan=4, columnspan=4, sticky='news')
        self.results = Table(window, dataframe=results, showtoolbar=False, showstatusbar=False)
        self.results.showIndex()
        self.results.show()

    def show_plot(self, results):
        #if self.results is not None:
            #self.results.remove()

        window = Frame(self)
        window.grid(column=0, row=2, rowspan=4, columnspan=4, sticky='news')

        canvas = FigureCanvasTkAgg(results, window)
        canvas.draw()

        toolbar = NavigationToolbar2Tk(canvas, window)
        toolbar.update()
        canvas.get_tk_widget().pack()





class About(Frame):
    """Information about our tool"""

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
               command=lambda: controller.show_frame("About"), foreground="#011f3d", background="#007fff",
               borderwidth=0, highlightthickness=0, cursor="heart").grid(row=0, column=4, sticky=E)

        description = '''
        This project is part of the Transversal projects (PTRANS) organized by the Graduate School of Engineering of the University of Nantes, Polytech Nantes that happened throughout the year 2021-2022. 
        This project involved three 4th year students of the school :
            - Chama El Majeny
            - Yvann Gouraud
            - Jiawen Liu
        They worked on a project under the tutelage of Professor Patrick Le Callet from Polytech Nantes.
        This project was commissioned by Doctor Margaret H.Pinson from the Institute for Telecommunication Sciences (ITS), the research branch of the National Telecommunications and Information Administration (NTIA).
        
        The aim of this project was to provide a centralized tool that could analyze datasets obtained from subjective test quality assessment. Our tool can run several statistical analysis such as calculating the average MOS of each stimulus, and calculating the precision of the dataset using methods developed by Doctor Pinson and Ms Yana Nehmé.

        '''
        label = Text(self, wrap='word', borderwidth=0)
        label.insert(END, description, 'tag-center')
        label['state'] = 'disabled'
        label.grid(row=2, column=1, columnspan=5,rowspan=5)


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()

