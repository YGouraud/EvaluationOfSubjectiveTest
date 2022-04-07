from tkinter import *

from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
from pandas import *

from ratings_to_bew import *
from bew_to_curve import *
from all_MOS import *

import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter


class SampleApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title = "Test"

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
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def get_page(self, page_name):
        return self.frames[page_name]



class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Welcome to our tool !", background="#6680CC")
        label.pack(side="top", fill="x", pady=10)

        Button(self, height=2, width=35, text="You want to add your own dataset",
                            command=lambda: controller.show_frame("PageOne")).pack()
        Button(self, height=2, width=35, text="You want to use the datasets that we have",
                            command=lambda: controller.show_frame("PageTwo")).pack()


class PageOne(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.file = ''
        self.filetype = ''
        self.filename = ''

        label = Label(self, text="You can input a new file", background="#6680CC")
        label.pack(side="top", fill="x", pady=10)

        # open button
        open_button = Button(self, text='Open a File', command=self.select_file, padx=5, pady=5)

        Label(self, height=2, width=35, text='File', background="#99ADD6").pack()
        open_button.pack()

        button = Button(self, height=2, width=35, text="Return to the First Page",
                        command=lambda: controller.show_frame("StartPage"))
        button.pack()
        Button(self, height=2, width=35, text='Continue', bg="#78B060",
               command=lambda: controller.show_frame("PageThree")).pack()
        # button = Button(m, text='Continue', bg="green", width=10, height=5, command=window.destroy)

    def select_file(self):
        filetypes = (
            ('Csv files', '*.csv'),
            ('xsl files', '*.xls'),
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
        ft_name = filename.split("/").pop()
        ft_name = ft_name.split(".")[0]
        self.filename = ft_name


    # def get_filetype(self):
    #     filetype = ''
    #     for i in self.var:
    #         filetype += i.get()
    #     self.filetype = filetype
    #     print(self.filetype)
    #     print(type(self.filetype))

    #     return filetype

    def get_list(self):
        return [self.file, self.filetype, self.filename]


class PageTwo(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.title = "Test"
        Label(self, text="TODO", background="#6680CC").pack(side="top", fill="x", pady=10)
        Button(self, height=2, width=35, text="Return to the First Page",
                           command=lambda: controller.show_frame("StartPage")).pack()
        Button(self, height=2, width=35, text='Continue', bg="#78B060",
                      command=lambda: controller.show_frame("PageEnd")).pack()


class PageThree(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.title = "Test"

        self.number_stimuli = ''
        self.number_observers = ''
        self.sheet_number = ''

        #defining option list
        OptionSheet = [1,2,3]

        label = Label(self, text="Informations about your datasets", background="#6680CC").pack(side="top", fill="x", pady=10)

        Label(self, text="Number of stimuli").pack()
        self.e1 = Entry(self)
        self.e1.pack()

        Label(self, text="Number of observers").pack()
        self.e2 = Entry(self)
        self.e2.pack()

        self.variable = IntVar(self)
        self.variable.set(OptionSheet[0])

        Label(self, text="Which sheet to use").pack()
        opt = OptionMenu(self, self.variable, *OptionSheet)
        #opt.config(width=90, font=('Helvetica', 12))
        opt.pack(side="top")

        Button(self, height=2, width=35, text="Return to the Previous Page",
                           command=lambda: controller.show_frame("PageOne")).pack()
        Button(self, height=2, width=35, text='Continue', bg="#78B060",
               command=lambda: [self.get_text(), self.get_sheet_num(), controller.show_frame("PageFour")]).pack()

    def get_text(self):
        text = self.e1.get()
        self.number_stimuli = text
        text2 = self.e2.get()
        self.number_observers = text2
        print(text + ' ' + text2)
        return [text, text2]

    def get_sheet_num(self):
        sheet = self.variable.get()
        self.sheet_number = sheet
        return sheet

    def get_list(self):
        return [self.number_observers, self.number_stimuli]


class PageFour(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.title = "Test"
        self.text = ''
        self.tool = ''

        # defining option list
        ToolOption = ["MOS of all stimuli", "Precision of subjective test"]

        Label(self, text="Which statistical tool do you want to use ?", background="#6680CC").pack(side="top", fill="x", pady=10)

        self.variable = StringVar(self)
        self.variable.set(ToolOption[0])

        opt = OptionMenu(self, self.variable, *ToolOption)
        # opt.config(width=90, font=('Helvetica', 12))
        opt.pack(side="top")

        self.save = IntVar(self)
        check = Checkbutton(self, variable=self.save, text="Save results in a xls file ?")
        check.pack()

        Button(self, height=2, width=35, text="Return to the Previous Page",
                           command=lambda: controller.show_frame("PageThree")).pack()
        Button(self, height=2, width=35, text='Continue', bg="#78B060",
               command=lambda: [self.get_tool(),controller.show_frame("PageFive")]).pack()

    def get_tool(self):
        tool = self.variable.get()
        self.tool = tool
        return tool

    def get_list(self):
        return [self.text]

    def get_save(self):
        save = self.save.get()
        return save

class PageFive(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.title = "Test"
        self.text = ''
        Label(self, text="Informations about your datasets", background="#6680CC").pack(side="top", fill="x", pady=10)

        Label(self, text="More infos - Header").pack()
        self.text_box = Text(self, height=10, width=30)
        self.text_box.pack()

        Button(self, height=2, width=35, text="Return to the Previous Page",
                           command=lambda: controller.show_frame("PageFour")).pack()
        Button(self, height=2, width=35, text='Continue', bg="#78B060",
               command=lambda: [self.get_text(), controller.show_frame("PageEnd")]).pack()

    def get_text(self):
        self.text = self.text_box.get("1.0", END)
        print(self.text)
        return self.text

    def get_list(self):
        return [self.text]


class PageEnd(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.title = "Test"
        label = Label(self, text="Please wait ... ", background="#6680CC", padx=5)
        label.pack(side="top", fill="x", pady=10)

        Button(self, height=2, width=35, text="Return to the First Page",
                        command=lambda: controller.show_frame("StartPage")).pack()

        Button(self, height=2, width=35, text="END",
                        command=lambda: controller.destroy()).pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()

file = app.get_page("PageOne").get_list()
print(file[0])

sheet_num = app.get_page("PageThree").get_sheet_num()
print(sheet_num)

tool = app.get_page("PageFour").get_tool()
print(tool)

save = app.get_page("PageFour").get_save()
print(save)

if file[1] == 'csv':
    f = pandas.read_csv(file[0])
elif file[1] == 'xls':
    f = pandas.read_excel(file[0], sheet_name=(sheet_num-1), usecols='A:AG', index_col=0, header=1, keep_default_na=True)
elif file[1] == 'json':
    f = pandas.read_json(file[0])
elif file[1] == 'xml':
    f = pandas.read_xml(file[0])
else:
    print("Invalid Format")

print(f)

if tool == "MOS of all stimuli":
    all_means(f, save)
elif tool == "Precision of subjective test":
    B, C = ratings_to_bew('inf', f)
    D, E = bew_to_curve(B, C)
    plt.plot(E, D)
    plt.title(file[2])
    plt.xlabel('DeltaS')
    plt.ylabel('PI')
    plt.grid(True, linestyle='-')
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plt.show()


