import re
import os
import argparse
import json
from recipe_utils import *


def create_recipe():
    name = input('What is this recipe called? ')
    print(title_string(name))
    servings = safe_int_input('How many servings does this recipe make? ')
    source = input('Where did you get this recipe come from? (URL, recipe book, etc.): ')
    id_string = re.sub(r"[^\w\s]", '', name)
    id_string = re.sub(r"\s+", '_', name).lower()
    recipe = {}
    recipe[ID_KEY] = id_string
    recipe[NAME_KEY] = name
    recipe[SERVES_KEY] = servings
    recipe[SOURCE_KEY] = source
    recipe[INGREDIENTS_KEY] = get_ingredients()
    return recipe


def safe_int_input(question: str):
    no_number = True
    number = 0
    while no_number:
        try:
            number = int(input(question))
            no_number = False
        except (ValueError, NameError):
            print('Please provide a number!')
    return number


def get_ingredients():
    ingredients = []
    new_ingredient = True
    print('Add ingredients:')
    while(new_ingredient):
        quantity = safe_float_input('How much of this ingredient is required? (eg. 5/3/100): ')
        quantity_type = input('In what unit? (eg. grams, punnets, bunches, sachets. Skip if not applicable.): ')
        ingredient_name = input(
            'What is this ingredient? (Please simplify. eg. If the ingredient is \'plum tomatoes\' respond with \'tomatoes\'): ')
        variant = input(
            'What is the variety of this ingredient? (eg. If the ingredient is \'plum tomatoes\' respond with \'plum\'. If the ingredient is generic, skip this question.): ')
        ingredient = create_ingredient(ingredient_name, variant, quantity, quantity_type)
        print(ingredient_to_string(ingredient))
        correct_ingredient = safe_bool_input('Is the ingredient above correct?')
        if (correct_ingredient):
            ingredients.append(ingredient)
            new_ingredient = safe_bool_input('Would you like to add another ingredient?')
    return ingredients


def safe_float_input(question: str):
    no_number = True
    number = 0
    while no_number:
        try:
            number = float(input(question))
            no_number = False
        except (ValueError, NameError):
            print('Please provide a number!')
    return number


def create_ingredient(ingredient_name, variant, quantity, quantity_type):
    ingredient = {}
    ingredient[INGREDIENT_KEY] = ingredient_name.lower()
    if (variant != ''):
        ingredient[VARIANT_KEY] = variant.lower()
    ingredient[QUANTITY_KEY] = quantity
    if (quantity_type != ''):
        ingredient[QUANTITY_TYPE_KEY] = quantity_type.lower()
    return ingredient


def safe_bool_input(question: str):
    input_required = True
    response = False
    while(input_required):
        response = input(f'{question} y/n ')
        if (response.lower() == 'y' or response.lower() == 'yes'):
            input_required = False
            response = True
        elif (response.lower() == 'n' or response.lower() == 'no'):
            input_required = False
            response = False
        else:
            print('Please respond with y/n or yes/no!')
    return response


def save_recipe(recipe: {}, recipes_dir: str):
    with open(os.path.join(recipes_dir, recipe[ID_KEY] + '.json'), 'w') as output_file:
        output_file.write(json.dumps(recipe))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add new recipes to your recipes directory')
    parser.add_argument('--recipes_dir', '-r', dest='recipes_dir', default='recipes')
    args = parser.parse_args()
    recipes_dir = args.recipes_dir
    print(f'Adding new recipes to {recipes_dir}')
    new_recipe = True
    while(new_recipe):
        recipe = create_recipe()
        print(recipe_to_string(recipe))
        correct_recipe = safe_bool_input('Is the recipe above correct?')
        if (correct_recipe):
            save_recipe(recipe, recipes_dir)
            new_recipe = safe_bool_input('Would you like to add another recipe?')
