import time
import pickle
import datetime
import numpy as np
from tkinter import ttk
from bs4 import BeautifulSoup
import pickle


def load_obj(datatype):
    with open("{}".format(datatype) + '.pkl', 'rb') as f:
        return pickle.load(f)

class msuclass:
    def __init__(self,id,driver):
        self.id = id
        self.operations = schedanalysis(self)
        self.name = self.get_name(driver)
        self.update_grades()#driver)

    def get_name(self,driver):
        driver.get("https://d2l.msu.edu/d2l/home/873465".format(self.id))
        namesoup = BeautifulSoup(driver.page_source,"html.parser")
        return namesoup.findAll("a",class_="d2l-navigation-s-link")[0].text

    def update_grades(self):#,driver):
        # driver.get("https://d2l.msu.edu/d2l/lms/grades/my_grades/main.d2l?ou={}".format(self.id))
        # gradesoup = BeautifulSoup(driver.page_source, "html.parser")

        temp = load_obj("temp")
        gradesoup = BeautifulSoup(temp, "html.parser")

        grades = {}
        for tr in gradesoup.findAll("tr"):
            data = tr.findAll("label")
            if len(data) >= 2:
                try:
                    grades["".join([char for char in data[0].text if char not in "1234567890#"])].append(
                        data[1].text.split(" / "))
                except:
                    grades["".join([char for char in data[0].text if char not in "1234567890#"])] = []
                    grades["".join([char for char in data[0].text if char not in "1234567890#"])].append(
                        data[1].text.split(" / "))


        for grade_cat in list(grades.keys()):
            for g in range(len(grades[grade_cat])):
                if grades[grade_cat][g][0] == "-":
                    del grades[grade_cat][g]
                    continue
                grades[grade_cat][g] = float(grades[grade_cat][g][0])/float(grades[grade_cat][g][1])
        self.grades = grades

        return self

    def calculate_grades(self):
        self = self.operations.calculate_grades()
        return self





# #





