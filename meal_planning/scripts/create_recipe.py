import re
import os
import argparse
import json
from meallib import Recipe, Ingredient, DEFAULT_RECIPE_DIR, DEFAULT_UNITS_FILE, DEFAULT_INGREDIENTS_FILE, ROOT_DIR, title_string
from pathlib import Path
from extract_ingredients import extract_ingredients
from extract_units import extract_units


def create_recipe(units_file: Path, ingredients_file: Path):
    name = input('What is this recipe called? ')
    print(title_string(name))
    servings = safe_int_input('How many servings does this recipe make? ')
    source = input('Where did you get this recipe come from? (URL, recipe book, etc.): ')
    unit_name_by_variant = get_unit_name_by_variant(units_file)
    known_ingredient_names = get_known_ingredient_names(ingredients_file)
    recipe = Recipe(name, servings, source, create_ingredients(unit_name_by_variant, known_ingredient_names))
    return recipe


def safe_int_input(question: str):
    no_number = True
    number = 0
    while no_number:
        try:
            number = int(input(f'{question.strip()} '))
            no_number = False
        except (ValueError, NameError):
            print('Please provide a number!')
    return number


def get_unit_name_by_variant(units_file: Path):
    unit_name_by_variant = {}
    if (units_file.exists()):
        with units_file.open() as json_file:
            variants_by_unit_name = json.loads(json_file.read() or '{}')
            for unit_name in variants_by_unit_name:
                unit_name_by_variant[unit_name] = unit_name
                for variant in variants_by_unit_name[unit_name]:
                    unit_name_by_variant[variant] = unit_name
    return unit_name_by_variant


def get_known_ingredient_names(ingredients_file: Path):
    known_ingredient_names = []
    if (ingredients_file.exists()):
        with ingredients_file.open() as json_file:
            ingredients_by_category = json.loads(json_file.read() or '{}')
            for category in ingredients_by_category:
                known_ingredient_names += ingredients_by_category[category]
    return known_ingredient_names


def create_ingredients(unit_name_by_variant: {}, known_ingredient_names: []):
    ingredients = []
    more_ingredients = True
    print('Add ingredients: (Type \'done\' when complete.)')
    while(more_ingredients):
        ingredient = create_ingredient(unit_name_by_variant, known_ingredient_names)
        if (ingredient is None):
            more_ingredients = False
        else:
            ingredients.append(ingredient)
    correct_ingredients = False
    while(not correct_ingredients):
        for index in range(len(ingredients)):
            print(f'{index+1}. {ingredients[index]}')
        correct_ingredients = safe_bool_input('Are the ingredients above correct?')
        if (not correct_ingredients):
            index = safe_int_input('Which ingredient is not correct? (Give the number)') - 1
            if (index >= len(ingredients)):
                print("Invalid number.")
                continue
            delete = safe_bool_input('Should this ingredient be deleted?')
            if (delete):
                del ingredients[index]
            else:
                ingredients[index] = create_ingredient_interactive()
    return ingredients


def create_ingredient(unit_name_by_variant: {}, known_ingredient_names: []):
    ingredient_text = input('Describe the ingredient (<quantity?> <unit?> <name>): ')
    split_text = ingredient_text.strip().split()
    ingredient = None
    if (ingredient_text.lower() == 'done'):
        ingredient = None
    elif (len(split_text) < 1):
        print('Ingredient text could not be parsed.')
        ingredient = create_ingredient_interactive()
    elif (len(split_text) == 1):
        ingredient = Ingredient(ingredient_text, 1.0, None)
    elif(not is_number(split_text[0])):
        unit = get_unit(ingredient_text, unit_name_by_variant, known_ingredient_names)
        if (unit is None):
            ingredient = Ingredient(ingredient_text, 1.0, None)
        else:
            ingredient = Ingredient(' '.join(split_text[len(unit.split()):]), 1.0, unit)
    elif (len(split_text) == 2):
        ingredient = Ingredient(split_text[1], float(split_text[0]), None)
    else:
        ingredient_text_no_quantity = ' '.join(split_text[1:])
        unit = get_unit(ingredient_text_no_quantity, unit_name_by_variant, known_ingredient_names)
        if (unit is None):
            ingredient = Ingredient(' '.join(split_text[1:]), float(split_text[0]), None)
        else:
            ingredient = Ingredient(' '.join(split_text[len(unit.split()) + 1:]), float(split_text[0]), unit)
    return ingredient


def create_ingredient_interactive():
    quantity = safe_float_input('How much of this ingredient is required? (eg. 5/3/100): ')
    unit = input('In what unit? (eg. grams, punnets, bunches, sachets. Skip if not applicable.): ')
    name = input('What is this ingredient? ')
    return Ingredient(name.lower(), quantity, None if unit.strip() == '' else unit)


def safe_float_input(question: str):
    no_number = True
    number = 0
    while no_number:
        try:
            number = float(input(f'{question.strip()} '))
            no_number = False
        except (ValueError, NameError):
            print('Please provide a number!')
    return number


def is_number(string: str):
    try:
        float(string)
        return True
    except ValueError:
        return False


def get_unit(ingredient_text_no_quantity: str, unit_name_by_variant: {}, known_ingredient_names: []):
    unit = None
    if (any(ingredient_name is ingredient_text_no_quantity for ingredient_name in known_ingredient_names)):
        unit = None
    else:
        variants = [variant for variant in unit_name_by_variant if ingredient_text_no_quantity.startswith(variant)]
        if (len(variants) >= 1):
            variant = max(variants, key=len)
            unit = unit_name_by_variant[variant]
        else:
            contains_new_unit = safe_bool_input(f'Does {ingredient_text_no_quantity} contain a new unit?')
            if (contains_new_unit):
                unit = input('What is the new unit? ')
                unit_name_by_variant[unit] = unit
    return unit


def safe_bool_input(question: str):
    input_required = True
    response = False
    while(input_required):
        response = input(f'{question.strip()} y/n ')
        if (response.lower() == 'y' or response.lower() == 'yes'):
            input_required = False
            response = True
        elif (response.lower() == 'n' or response.lower() == 'no'):
            input_required = False
            response = False
        else:
            print('Please respond with y/n or yes/no!')
    return response


def save_recipe(recipe: Recipe, recipes_dir: Path):
    with (recipes_dir / (recipe.id + '.json')).open('w') as output_file:
        output_file.write(json.dumps(recipe.as_dict()))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add new recipes to your recipes directory')
    parser.add_argument('--recipes_dir', '-r', dest='recipes_dir', type=Path, default=DEFAULT_RECIPE_DIR)
    parser.add_argument('--units_file', '-u', dest='units_file', type=Path, default=DEFAULT_UNITS_FILE)
    parser.add_argument('--ingredients_file', '-i', dest='ingredients_file', type=Path, default=DEFAULT_INGREDIENTS_FILE)
    parser.add_argument('--refresh_inputs', '-f', dest='refresh_inputs', type=bool, default=True)
    args = parser.parse_args()
    recipes_dir = args.recipes_dir
    units_file = args.units_file
    ingredients_file = args.ingredients_file
    refresh_inputs = args.refresh_inputs
    print(f'Adding new recipes to {recipes_dir.relative_to(ROOT_DIR)}. Using units from {units_file.relative_to(ROOT_DIR)} and known ingredients from {ingredients_file.relative_to(ROOT_DIR)}')
    new_recipe = True
    while(new_recipe):
        recipe = create_recipe(units_file, ingredients_file)
        save_recipe(recipe, recipes_dir)
        print(recipe)
        new_recipe = safe_bool_input('Would you like to add another recipe?')
    if (refresh_inputs):
        extract_ingredients(recipes_dir, ingredients_file)
        extract_units(recipes_dir, units_file)
