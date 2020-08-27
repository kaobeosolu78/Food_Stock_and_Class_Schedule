import pickle

# class for individual recipes
class Recipe:
    def __init__(self,recipe_name,contents):
        # define name and constructs recipe from ingredients
        self.name = recipe_name
        self.construct(contents)

    # turns contents into food objects and adds to list which is defined as self.ingredients
    def construct(self,contents):
        self.ingredients = [Food(contents[0][k],contents[1][k]) for k in range(len((contents[0])))]

    # looks to see if cooking of the recipe is possible from current food inventory
    def feasible(self,inv):
        # list of food names
        recipe_ingredient_names = [item.name for item in inv]
        # iterates through ingredients required
        for inv_item in self.ingredients:
            if inv_item.name not in recipe_ingredient_names:
                return False
            elif float(inv_item.quantity) < inv[recipe_ingredient_names.index(inv_item.name)].quantity:
                return False
            return True

# main storage object for both food and ingredients
class Registry:
    def __init__(self):
        # initialize with lists for food and ingredients
        self.inventory = []
        self.recipes = []

    # method to add or remove food
    def add_or_remove_food(self,foods,quantities,op):
         # op == "operation"
         if op == "remove":
             # if removing creates list of negative amounts to remove
             quantities = [-float(quant) for quant in quantities]
         count = -1
         if self.inventory == [] and op != "remove":
             # handles case of empty inventory
             self.inventory = [Food(foods[k],float(quantities[k])) for k in range(len(foods))]
         else:
             # iterate through foodnames and add amount to be added/removed to the existing quantity
             for foodname in foods:
                 count += 1
                 if foodname in [food.name for food in self.inventory]:#similarity ind
                     ind = [food.name for food in self.inventory].index(foodname)
                     self.inventory[[food.name for food in self.inventory].index(foodname)] += float(quantities[count])
                 else:
                     self.inventory.append(Food(foodname,float(quantities[count])))

         # update pickled registry file
         pick_out = open("Registry.pkl", "wb")
         pickle.dump(self, pick_out, pickle.HIGHEST_PROTOCOL)
         pick_out.close()

         return self

    # method to add or remove recipe
    def add_update_or_remove_recipe(self,recipe,mode="add"):
        # adds recipe to recipes list
        if mode == "add":
            self.recipes.append(recipe)
        # remove recipe from recipes list
        elif mode == "remove":
            del self.recipes[[rec.name for rec in self.recipes].index(recipe.name)]
        # replaces existing recipe from recipes list with new recipe
        elif mode == "update":
            self.recipes[[rec.name for rec in self.recipes].index(recipe.name)] = recipe

        # update pickled registry file
        pick_out = open("Registry.pkl", "wb")
        pickle.dump(self, pick_out, pickle.HIGHEST_PROTOCOL)
        pick_out.close()

    # method which returns all the possible recipes which can be made from current inventory
    def makeable_recipes(self):
        return [recipe for recipe in self.recipes if recipe.feasible(self.inventory)==True]

# storage object for food
class Food:
    def __init__(self,name,quantity=1):
        # define name and quantity from given values
        self.name = name
        self.quantity = quantity

    # + method overload
    def __add__(self,quant):
        self.quantity += quant
        return self
    
    # - method overload
    def __sub__(self,quant):
        self.quantity -= quant
        return self
