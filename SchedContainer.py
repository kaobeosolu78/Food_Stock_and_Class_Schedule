from selenium import webdriver
from bs4 import BeautifulSoup
import numpy as np
import datetime
import pickle

# handles the hidden roots on d2l pages
def expand_shadow_element(element):
  shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
  return shadow_root

# loads pickled files
def load_obj(datatype):
    with open("{}".format(datatype) + '.pkl', 'rb') as f:
        return pickle.load(f)

# container for msuclass objects, also initializes new msuclass objs with values along with other methods
class msuclasses:
    def __init__(self):
        # init various needed variables
        self.classes = []
        self.assn_id_holder = "873465"
        self.get_assignments()#self.d2l_driver())
        
    # add a new msuclass object
    def add_new(self,id):
        # if not multiple ids then make list
        if type(id) != list:id = [id]
        # starts d2l selenium driver
        driver = self.d2l_driver()
        # add individual class data to self.classes
        [self.classes.append(msuclass(i,driver)) for i in id]

    # gets individual class pending assignments [webscraper]
    def get_assignments(self):#,driver):
        # scrapes the d2l assn webpage and initialize needed variables
        # driver.get("https://d2l.msu.edu/d2l/le/calendar/{}/home/list?year=2010&month=6&day=27".format(self.assn_id_holder))
        # assnsoup = BeautifulSoup(driver.page_source,"html.parser")
        assnsoup = BeautifulSoup(load_obj("tempassn"),"html.parser")
        assignments = assnsoup.findAll("form")[1].findAll("li")
        assns,final_prods,x_axis,y_axis = {},{},[],[]# raw data,final polished data,classnames,dates
        # format the form tags scraped and add to dictionary with date as keys
        for assn in assignments:
            temp = list(filter(None, assn.text.split("\n")))
            try:
                assns[datetime.datetime.strptime(temp[3],"%b %d, %Y %I:%M %p")].append((temp[1],temp[2]))
            except:
                assns[datetime.datetime.strptime(temp[3],"%b %d, %Y %I:%M %p")] = [(temp[1],temp[2])]

        # iterates through all dates
        for day in list(assns.keys()):
            # add dates and init temporary variables
            y_axis.append(day)
            dayassns,final_prods[day] = {},{}
            # organize data
            for assi in assns[day]:
                if assi[0] not in x_axis:
                    x_axis.append(assi[0])
                try:
                    final_prods[day][assi[0]].append(assi[1])
                except:
                    final_prods[day][assi[0]] = [(assi[1])]

        # initialize array for placing data into
        assn_array = np.zeros((len(y_axis),len(x_axis)),dtype=object)
        # more organizing and formatting of data
        for y_val in list(final_prods.keys()):
            for x_val in list(final_prods[y_val].keys()):
                for assin in final_prods[y_val][x_val]:
                    if assn_array[y_axis.index(y_val)][x_axis.index(x_val)] == 0.0:
                        assn_array[y_axis.index(y_val)][x_axis.index(x_val)] = assin
                    else:
                        assin = "; " + assin
                        assn_array[y_axis.index(y_val)][x_axis.index(x_val)] += assin
        # remove null vals and package all data together into a dictionary
        values = [[v if v!= 0 else "" for v in vals] for vals in assn_array]
        self.assignments = {"x_axis":x_axis,"y_axis":y_axis,"assignments":values}

    # calls update_grades() on all of the classes saved
    def update_all_grades(self):
        # driver = self.d2l_driver()
        self.classes = [class_.update_grades() for class_ in self.classes]#driver

    
    def d2l_driver(self):
        chromedriver = ('C:\\Users\\Kaobe\\PycharmProjects\\School\\venv\\Include\\chromedriver.exe')
        driver = webdriver.Chrome(chromedriver)
        driver.get("https://d2l.msu.edu/d2l/loginh/")
        driver.find_element_by_id("login-button").click()
        driver.find_element_by_id("msu-id").send_keys("osolukao")
        driver.find_element_by_id("password").send_keys("Kao4be123")
        driver.find_element_by_class_name("msuit_brand_submit").click()
        return driver

    def calc_assn_urgency(self):
        self.heat_data = schedanalysis(self).calculate_assn_urgency()



