import datetime

class schedanalysis:
    def __init__(self,master):
        self.master = master

    def calculate_grades(self,weights):
        final, tot = 0, 0
        for assn in list(self.master.grades.keys()):
            for subassn in self.master.grades[assn]:
                try:
                    float(subassn)
                    tot += 1
                except:
                    continue
                final += float(subassn)*float(weights[self.master.name][assn])

        return round(final/tot,2)


    def calculate_assn_urgency(self):
        data = self.master.assignments
        data["y_axis"] = [dat.date() for dat in data["y_axis"]]
        colors = [(3, "red"), (7, "orange"), (14, "yellow"), (21, "green")]
        color_values, values, headers = [], [], data["x_axis"]
        for y in range(len(data["y_axis"])):
            for color in colors:
                if (data["y_axis"][y] - datetime.date(2019, 1, 23)).days >= color[0]:  ####
                    if [data["y_axis"][y]] + list(data["assignments"][y]) in values:
                        del color_values[-1]
                        del values[-1]
                    color_values.append(color[1])
                    values.append([data["y_axis"][y]] + list(data["assignments"][y]))
        values = list(map(list, zip(*values)))
        return headers, color_values, values
