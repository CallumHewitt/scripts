import re
from pathlib import Path
from json import JSONEncoder

ROOT_DIR = Path(__file__).absolute().parent.parent
DEFAULT_RECIPE_DIR = ROOT_DIR / 'recipes'
DEFAULT_SHOPPING_LIST_OUTPUT = ROOT_DIR / 'shopping_list.txt'
DEFAULT_MEAL_SPEC = ROOT_DIR / 'meals_spec.json'
DEFAULT_FOOD_TYPES = ROOT_DIR / 'ingredients.json'
DEFAULT_MEASUREMENTS = ROOT_DIR / 'measurements.json'

def title_string(string: str):
    return f'====== {string} ====='

class Ingredient:

    def __init__(self, core: str, variant: str, quantity: float, unit: str):
        self.core = core
        self.variant = variant
        self.quantity = quantity
        self.unit = unit

    def __str__(self):
        return ' '.join(filter(lambda x: x != '', [str(self.quantity), self.unit, self.variant, self.core]))

    def __repr__(self):
        return f'Ingredient(core={self.core}, variant={self.variant}, quantity={self.quantity}, unit={self.unit})'

class Recipe:

    def __init__(self, name: str, serves: int, source: str, ingredients: [Ingredient]):
        id_string = re.sub(r"[^\w\s]", '', name)
        id_string = re.sub(r"\s+", '_', name).lower()
        self.id = id_string
        self.name = name
        self.serves = serves
        self.source = source
        self.ingredients = ingredients

    def __str__(self):
        str_list = []
        str_list.append(title_string(self.name))
        str_list.append(f'Source: {self.source}')
        str_list.append(f'Serves: {str(self.serves)}')
        str_list.append(f'Ingredients')
        ingredient_strings = list(map(lambda ingredient: f'  - {str(ingredient)}', self.ingredients))
        str_list = str_list + ingredient_strings
        return '\n'.join(str_list)

    def __repr__(self):
        return f'Recipe(id={self.id}, name={self.name}, serves={self.serves}, source={self.source}, ingredients={self.ingredients})'

    def as_dict(self):
        recipe=dict(self.__dict__)
        recipe['ingredients']=list(map(lambda ingredient: dict(ingredient.__dict__), recipe['ingredients']))
        return recipe