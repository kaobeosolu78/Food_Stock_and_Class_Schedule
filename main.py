import pickle
import tkinter as tk
from tkinter import ttk
from food_classes import Registry,Food,Recipe
from get import msuclass
from SchedContainer import msuclasses
from guis import foodgui,msugui
# global Recipe,Registry,Food,msuclass,msuclasses,schedanalysis,msuclasses,foodgui,msugui

# gui for handling upcoming d2l assignments, a schedule, current food registry and recipes
def load_obj(datatype):
    with open("{}".format(datatype) + '.pkl', 'rb') as f:
        return pickle.load(f)
# classurls = ["873465"]
# #
# classes = SchedContainer.msuclasses()
# for url in classurls:

# if existing food registry data exists, loads it from pickled file
temp = load_obj("tempassn")
try:
    reg = load_obj("Registry")
except:
    reg = Registry()
# if existing class data exists, loads it from pickled file
try:
    classes = load_obj("classes")
except:
    classes = msuclasses()

# gui initialization class
class main(foodgui,msugui):
    def __init__(self,sched,reg):
        # initialize gui and define the separate parts of it
        tk.Tk.__init__(self)
        self.classes = sched
        self.registry = reg
        
        # defines options from preexisting pickle file or default values
        try:
            self.options = load_obj("options")
        except:
            self.options = {"Assn Num": 5,"Weights":{name.name:{cat:1 for cat in list(name.grades.keys())} for name in self.classes.classes}}#fix

        # formatting
        self.grid()
        self.geometry("800x350+200+200")
        self.title("Main")

        # add all menus
        menubar = tk.Menu(self)
        optionmenu = tk.Menu(menubar, tearoff=0)
        optionmenu.add_command(label="Add/Modify Weight Config", command=self.weight_option_query)
        optionmenu.add_command(label="Clear Inventory", command=lambda: (self.reset_reg()))
        menubar.add_cascade(label="Options", menu=optionmenu)
        recipemenu = tk.Menu(menubar, tearoff=0)
        recipemenu.add_command(label="Add Recipe", command=self.add_recipe)
        recipemenu.add_command(label="Modify Existing Recipe", command=self.modify_recipe)
        menubar.add_cascade(label="Recipes", menu=recipemenu)
        classmenu = tk.Menu(menubar, tearoff=0)
        classmenu.add_command(label="Manually Add Class", command=self.manual_add_assns)
        classmenu.add_command(label="Modify Existing Class", command=self.modify_class)
        classmenu.add_command(label="Adjust Number of Assns", command=self.assn_num_show)
        menubar.add_cascade(label="Classes", menu=classmenu)
        tk.Tk.config(self, menu=menubar)

        # adds tables to gui
        self.assns_table()
        self.update_inv_table(self.max_row)
        
        # increments max row for formatting
        self.max_row+=5

        # mainbuttons added
        mainbuttonframe = tk.Frame(self)
        mainbuttonframe.grid(row=50,column=0,columnspan=15,pady=15,sticky="EWNS")
        ttk.Button(mainbuttonframe, text="Add New D2l Class", command=lambda: self.input_codes()).grid(row=0,
                                                                                            column=0,padx=15)
        ttk.Button(mainbuttonframe, text="Display All Assignments", command=lambda: self.display_assns()).grid(
            row=0, column=1,padx=15)
        ttk.Button(mainbuttonframe, text="Add Food", command=self.add_food).grid(row=0, column=2,padx=15)
        ttk.Button(mainbuttonframe, text="Exit", command=quit).grid(row=0, column=3,padx=15)

# classes.add_new(classurls[0])
# # #
# classes.update_all_grades()
# print()
#
# pickle_out = open("classes.pkl", 'wb')
# pickle.dump(classes, pickle_out, pickle.HIGHEST_PROTOCOL)
# pickle_out.close()

# call gui init class and starts tkinter mainloop
app = main(classes,reg)
app.mainloop()
