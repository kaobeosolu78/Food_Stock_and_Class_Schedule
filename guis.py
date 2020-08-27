import pickle
import plotly
import plotly.plotly as py
import plotly.graph_objs as goo
import requests, bs4
import tkinter as tk
from tkinter import ttk
import datetime
from analysis import schedanalysis

class msugui(tk.Tk):
    def __init__(self, main):
        self.classes = main

    def assn_num_show(self):
        numwin = tk.Toplevel()
        numwin.title("Show n Assignments")
        ttk.Label(numwin, text="How many assignments do you want the homepage to show?").pack()
        num = ttk.Entry(numwin)
        num.pack(pady=3)
        num.insert(0, self.options["Assn Num"])
        ttk.Button(numwin, text="Submit").pack()
        self.options["Assn Num"] = num.get()

    def assns_table(self):
        gradeframe = ttk.Frame(self)
        gradeframe.grid(row=0,column=0,rowspan=7,columnspan=len(self.classes.assignments["x_axis"]))
        ttk.Label(gradeframe, text="Current Grades:").grid(row=0, column=0, sticky="W")

        r, c = 0, 0
        for cl in self.classes.classes:
            ttk.Label(gradeframe, text=str(schedanalysis(cl).calculate_grades(self.options["Weights"]) * 100) + "%").grid(
                row=r, column=c + 2)
            r += 1
        self.max_row = r

        self.heat_data = schedanalysis(self.classes).calculate_assn_urgency()
        classes, color_values, values = self.heat_data
        ttk.Label(gradeframe, text="Upcoming Assignments:").grid(row=self.max_row + 3, column=0, pady=5,padx=3)

        r, c = self.max_row + 3, 1
        [ttk.Label(gradeframe, text=classes[cla]).grid(row=r, column=cla + 1, padx=10) for cla in range(len(classes))]
        for rl in range(self.options["Assn Num"]):
            ttk.Label(gradeframe, text=values[0][rl]).grid(row=rl + r + 1, column=0)
            for cl in range(len(classes)):
                ttk.Label(gradeframe, text=values[cl + 1][rl]).grid(row=rl + r + 1, column=c + cl)
        self.max_row = rl + r + 1

    def weight_option_query(self):
        def helper_func(self, inp):
            weights = {}
            count = -1
            for class_ in self.classes.classes:
                weights[class_.name] = {}
                for assn in list(class_.grades.keys()):
                    count += 1
                    weights[class_.name][assn] = inp[class_.name][count]

            pickle_out = open("options.pkl", 'wb')
            pickle.dump({"Weights": weights}, pickle_out, pickle.HIGHEST_PROTOCOL)
            pickle_out.close()
            self.options["Weights"] = weights

        woqwin = tk.Toplevel(self)
        woqwin.title("Configure Weights")
        ttk.Label(woqwin, text="""Fill in any assignment weights as a percent, leaving unweighted boxes blank.""").grid(
            row=0, column=0, columnspan=12, sticky="WE")
        woqwin.grid_rowconfigure(0, weight=1)
        woqwin.grid_columnconfigure(0, weight=1)

        r, c, entries = 0, 0, {}
        for class_ in self.classes.classes:
            entries[class_.name] = []
            r += 2
            ttk.Label(woqwin, text=class_.name + ":").grid(row=r, column=0)
            for assn in list(class_.grades.keys()):
                c += 1
                ttk.Label(woqwin, text=assn).grid(row=r - 1, column=c)
                ent = ttk.Entry(woqwin, width=5)
                ent.grid(row=r, column=c, padx=20, pady=3)
                try:
                    ent = float(ent.get())
                except:
                    ent = 1.0
                entries[class_.name].append(ent)

        ttk.Button(woqwin, text="Submit", command=lambda: [helper_func(self, entries)]).grid(row=r + 1, column=0,
                                                                                             columnspan=8)

    def input_codes(self):
        new_win = tk.Toplevel()
        new_win.title("Input Codes")
        ttk.Label(new_win, text="Input class codes: ").grid(row=0, column=0)
        codes = []
        [codes.append(ttk.Entry(new_win)) for k in range(5)]
        [codes[k].grid(row=k + 1, column=0, padx=8, pady=3) for k in range(len(codes))]
        ttk.Button(new_win, text="Submit", command=lambda: [self.classes.add_new(codes), des(new_win)]).grid(row=6,
                                                                                                             column=0)

    def display_assns(self):
        classes, color_values, values = self.heat_data
        trace0 = goo.Table(
            header=dict(
                values=[[head] for head in (["Due Dates"] + classes)],
                line=dict(color='#506784'),
                fill=dict(color='grey'),
                align=['left', 'center'],
                font=dict(color='white', size=12)
            ),
            cells=dict(
                values=values,
                line=dict(color='#506784'),
                fill=dict(color=[color_values, color_values, color_values]),
                align=['left', 'center'],
                font=dict(color='black', size=15)
            ))

        plotly.offline.plot({"data": [trace0]})

    def manual_add_assns(self):
        def query_data(self, dates):
            def helper_func(self, name, temp_assns, dates):
                x_ax, y_ax, assignments = self.assignments["x_axis"], self.assignments["y_axis"], self.assignments[
                    "assignments"]
                x_ax.append(name.get())
                hold = len(assignments[0])
                for k in range(len(dates)):
                    if dates[k] in y_ax:
                        if len(temp_assns[k].get()) == 0:
                            assignments[
                                y_ax.index(dates[k])].append("")
                        else:
                            assignments[
                                y_ax.index(dates[k])].append(temp_assns[k].get())
                    else:
                        y_ax.append(dates[k])
                        if len(temp_assns[k].get()) == 0:
                            assignments.append(["" for k in range(hold + 1)])
                        else:
                            assignments.append(["" for k in range(hold)] + [temp_assns[k].get()])
                [ass.append("") for ass in assignments if len(ass) == hold]
                sorted_assns = [assignments for _, assignments in sorted(zip(y_ax, assignments))]
                self.assignments = {"x_axis": x_ax, "y_axis": sorted(y_ax), "assignments": sorted_assns}

            qwin = tk.Toplevel()
            qwin.title("Assignment Add")
            ttk.Label(qwin, text="Enter Class Name:").grid(row=0, column=0)
            qwin.grid_rowconfigure(0, weight=1)
            name = ttk.Entry(qwin)
            name.grid(row=0, column=1, pady=3)
            ttk.Label(qwin, text="Assignment Names:").grid(row=1, column=0, columnspan=3)

            r = 2
            temp_assns = []
            for date in dates:
                ttk.Label(qwin, text=date.strftime("%Y-%m-%d:")).grid(row=r, column=0, sticky="W")
                class_ = ttk.Entry(qwin)
                class_.grid(row=r, column=1, padx=5, pady=3)
                temp_assns.append(class_)
                r += 1

            ttk.Button(qwin, text="Add", command=lambda: [helper_func(self, name, temp_assns, dates), des(qwin)]).grid(
                row=r, column=0, columnspan=2)

        impwin = tk.Toplevel()
        impwin.title("Due Dates")
        ttk.Label(impwin, text="Select Due Dates:").pack(side=tk.TOP)
        # ttk.Label(impwin,text=[""+cla for cla in self.classes.assignments["x_axis"]])
        dates = tk.Listbox(impwin, selectmode=tk.MULTIPLE)
        dates.pack(padx=5, pady=2)
        date_vals = [datetime.date.today() + datetime.timedelta(days=k) for k in range(100)]
        [dates.insert(tk.END, day) for day in date_vals]
        ttk.Button(impwin, text="Select",
                   command=lambda: query_data(self.classes, [date_vals[days] for days in dates.curselection()])).pack(
            side=tk.BOTTOM)

    def modify_class(self):
        def mod_class(self, class_):
            def helper_func(self, changes, ind):
                for k in range(len(changes)):
                    self.classes.assignments["assignments"][k][ind] = changes[k].get()

            mwin = tk.Toplevel()
            mwin.title("Make Modification")
            ind, r, entries, c = class_[0], 1, [], 0
            ttk.Label(mwin, text="Make Modifications on \"{}\" Then Submit".format(
                self.classes.assignments["x_axis"][ind])).grid(row=0, column=0, columnspan=9)
            for date in self.classes.assignments["y_axis"]:
                if r == 12:
                    c += 2
                    r = 1
                ttk.Label(mwin, text=date).grid(row=r, column=c)
                ent = ttk.Entry(mwin)
                ent.insert(0, self.classes.assignments["assignments"][r - 1][ind])
                entries.append(ent)
                ent.grid(row=r, column=c + 1, pady=3, padx=2)
                r += 1
            ttk.Button(mwin, text="Submit", command=lambda: [helper_func(self, entries, ind), des(mwin)]).grid(row=13,
                                                                                                               column=0,
                                                                                                               columnspan=9,
                                                                                                               pady=2)

        modwin = tk.Toplevel()
        modwin.title("Modify Class")
        ttk.Label(modwin, text="Choose Class to Modify:").pack(side=tk.TOP)
        class_ = tk.Listbox(modwin)
        class_.pack()
        [class_.insert(tk.END, c) for c in self.classes.assignments["x_axis"]]
        ttk.Button(modwin, text="Select", command=lambda: mod_class(self, class_.curselection())).pack(side=tk.BOTTOM)

class foodgui(tk.Tk):
    # def __init__(self,registry):
    #     self.registry = registry

    def reset_reg(self):
        self.registry = Registry()
        temp = self.grid_slaves()
        [l.grid_remove() for l in self.grid_slaves() if l.widgetName == "label"]
        label = tk.Label(self,text="Registry Contents:").grid(row=0,column=0,sticky="NW")

    def update_inv_table(self,maxr):
        invframe = ttk.Frame(self)
        invframe.grid(row=maxr+1,column=0,rowspan=4,columnspan=10,sticky="W")

        label = tk.Label(invframe, text="Registry:").grid(row=1, column=0, sticky="NW")

        c,r = 0,1
        for k in range(len(self.registry.inventory)):
            r += 1
            for c2 in range(2):
                if k % 5 == 0 and k != 0 and c2 == 0:#fix
                    c += 2
                    r = 2
                if c2 == 0:
                    ttk.Label(invframe,text=self.registry.inventory[k].name).grid(column = c2+c,row = r,sticky="WE",padx=4)
                elif c2 == 1:
                    ttk.Label(invframe,text=self.registry.inventory[k].quantity).grid(column = c2+c,row = r,sticky="WE",padx=4)
        makeables = self.registry.makeable_recipes()

        invframe.grid_columnconfigure(c+1,minsize=100,weight=1)
        invframe.grid_rowconfigure(0,minsize=40)
        ttk.Label(invframe,text="You can cook...").grid(row=1,column=c+2)
        rr = 1
        if makeables == []:ttk.Label(invframe,text="Nothing").grid(row=2,column=c+2)
        for r in range(len(makeables)):
            rr += 1
            if r%5==0 and r != 0:
                rr=2
                c+=1
            ttk.Label(invframe,text=makeables[r].name).grid(row=rr,column=c+2,padx=5,sticky="W")

    def add_food(self):
        af_win = tk.Toplevel(self)
        af_win.title("Add to Inventory")
        ttk.Label(af_win,text="Enter Food:").grid(row=0,column=0)
        ttk.Label(af_win,text="Enter Food Quantitiy:").grid(row=0,column=2)
        self.food = ttk.Entry(af_win)
        self.food.grid(row=1,column=0,padx=5)
        self.quantity = ttk.Entry(af_win)
        self.quantity.grid(row=1,column=2,padx=5)
        ttk.Button(af_win,text="Add Food",command=lambda: [self.registry.add_or_remove_food([self.food.get()],[self.quantity.get()],"add"),self.update_rec_table(),self.update_inv_table()]).grid(row=2,column=0)
        ttk.Button(af_win,text="Remove Food",command=lambda: self.registry.add_or_remove_food([self.food.get()],[self.quantity.get()],"remove")).grid(row=2,column=1)
        ttk.Button(af_win,text="Exit",command=af_win.destroy).grid(row=2,column=2)
        self.update()

    def add_recipe(self):
        def add_rec(self, num, name):
            rec_win = tk.Toplevel(self)
            rec_win.title("Add Recipe")
            ttk.Label(rec_win, text="Enter Foods:").grid(row=0, column=0)
            ttk.Label(rec_win, text="Enter Quantities:").grid(row=0, column=1)
            # ttk.Label(rec_win, text="Enter Units").grid(row=0, column=2)
            ingredients = [ttk.Entry(rec_win) for k in range(num)]
            quantities = [ttk.Entry(rec_win) for k in range(num)]
            # units = [ttk.Entry(rec_win) for k in range(num)]
            [(ingredients[k].grid(padx=8, pady=3, row=k + 1, column=0),
              quantities[k].grid(padx=8, pady=3, row=k + 1, column=1)) for k in range(num)]
            ttk.Button(rec_win, text="Submit Recipe", command=lambda: self.registry.add__update_or_remove_recipe(
                Recipe(name, [[ing.get() for ing in ingredients], [quant.get() for quant in quantities],self.des(rec_win)]))).grid(
                row=num + 1, column=0)

        recnum_win = tk.Toplevel(self)
        recnum_win.title("New Recipe")
        ttk.Label(recnum_win, text="Enter the name of the recipe:").grid(row=0,column=0,padx=8,pady=3)
        ttk.Label(recnum_win, text="Enter the number of ingredients:").grid(row=1,column=0,padx=8,pady=3)
        name = ttk.Entry(recnum_win)
        num = ttk.Entry(recnum_win)
        name.grid(row=0,column=1,padx=8,pady=3)
        num.grid(row=1, column=1,pady=3,padx=8)
        ttk.Button(recnum_win, text="Submit", command=lambda: [add_rec(self,int(num.get()),name.get()),self.des(recnum_win)]).grid(row=2,column=0)


    def modify_recipe(self):
        def mod(self,selection):
            mod_win = tk.Toplevel(self)
            mod_win.title("Modify Recipe")
            recipe = self.registry.recipes[[rep.name for rep in self.registry.recipes].index(selection)]
            food,quant = [],[]
            [(food.append(ttk.Entry(mod_win)),quant.append(ttk.Entry(mod_win))) for ing in recipe.ingredients]
            ttk.Label(mod_win, text="Enter Foods:").grid(row=0, column=0)
            ttk.Label(mod_win, text="Enter Quantities:").grid(row=0, column=1)
            for k in range(len(food)):
                (food[k].grid(row=k+1,column=0,padx=8,pady=3),quant[k].grid(row=k+1,column=1,padx=8,pady=3))
                (food[k].insert(0,recipe.ingredients[k].name),quant[k].insert(0,recipe.ingredients[k].quantity))
            ttk.Button(mod_win,text="Submit",command=lambda: [self.registry.add_update_or_remove_recipe(Recipe(recipe.name,[[f.get() for f in food],[q.get() for q in quant]]),"update"),self.des(mod_win)]).grid(row=k+2,column=0)


        modsel_win = tk.Toplevel(self)
        modsel_win.title("Select Recipe")
        ttk.Label(modsel_win, text="Select a Recipe to Modify").pack()
        lb = tk.Listbox(modsel_win)
        [lb.insert(tk.END, item) for item in [rec.name for rec in self.registry.recipes]]
        lb.pack()
        ttk.Button(modsel_win,text="Select",command=lambda:[mod(self,[rec.name for rec in self.registry.recipes][lb.curselection()[0]]),self.des(modsel_win)]).pack()

    def des(self,win):
        win.destroy()





