import re
from pathlib import Path
from json import JSONEncoder
import json

ROOT_DIR = Path(__file__).absolute().parent.parent
DEFAULT_RECIPE_DIR = ROOT_DIR / 'recipes'
DEFAULT_SHOPPING_LIST_OUTPUT = ROOT_DIR / 'shopping_list.txt'
DEFAULT_MEAL_SPEC = ROOT_DIR / 'inputs' / 'meals_spec.json'
DEFAULT_INGREDIENTS_FILE = ROOT_DIR / 'inputs' / 'ingredient_groups.json'
DEFAULT_UNITS_FILE = ROOT_DIR / 'inputs' / 'unit_groups.json'

UNCATEGORISED_KEY = 'uncategorised'


def title_string(string: str):
    return f'====== {string} ====='

def underscore_text(string: str):
    string = re.sub(r"[^\w\s]", '', string)
    string = re.sub(r"\s+", '_', string).lower()
    return string


def load_recipes_by_id(recipes_path: Path):
    recipe_paths = [recipe_path for recipe_path in recipes_path.glob('**/*.json')]
    recipes = [load_recipe(recipe_path) for recipe_path in recipe_paths]
    return {recipe.id: recipe for recipe in recipes}


def load_recipe(recipe_path: Path):
    with recipe_path.open() as json_file:
       recipe_dict = json.loads(json_file.read())
       ingredients = [Ingredient(ingredient['name'], ingredient['quantity'], ingredient.get('unit', None))
                   for ingredient in recipe_dict['ingredients']
                   ]
       return Recipe(recipe_dict['name'], recipe_dict['serves'], recipe_dict['source'], ingredients)

class Ingredient:

    def __init__(self, name: str, quantity: float, unit: str):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    def __str__(self):
        return ' '.join(filter(lambda x: x != None, [str(self.quantity), self.unit, self.name]))

    def __repr__(self):
        return f'Ingredient(name={self.name}, quantity={self.quantity}, unit={self.unit})'

    def as_dict(self):
        response = {
            'name': self.name,
            'quantity': self.quantity
        }
        if (self.unit is not None):
            response['unit'] = self.unit
        return response


class Recipe:

    def __init__(self, name: str, serves: int, source: str, ingredients: [Ingredient]):
        self.id = underscore_text(name)
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
        recipe = dict(self.__dict__)
        recipe['ingredients'] = list(map(lambda ingredient: ingredient.as_dict(), recipe['ingredients']))
        return recipe
