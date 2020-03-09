import json
import itertools
import functools
import os
import argparse
from recipe_utils import *


def generate_shopping_list(meal_spec_file_name: str, recipes_dir: str, output_file_name: str):
    recipes_by_id = load_recipes(recipes_dir)
    meals = get_specified_meals(recipes_by_id, meal_spec_file_name)
    ingredients = [
        ingredient for meal in meals for ingredient in meal[INGREDIENTS_KEY]
    ]
    merged_ingredients = merge_ingredients_list(ingredients)
    sorted_ingredients = sorted(merged_ingredients, key=lambda x: x[INGREDIENT_KEY])
    save_shopping_list(merged_ingredients, output_file_name)


def load_recipes(recipes_dir: str):
    file_names = [file_name for file_name in os.listdir(recipes_dir) if file_name.endswith('.json')]
    recipes = [load_file(file_name, recipes_dir) for file_name in file_names]
    return {recipe['id']: recipe for recipe in recipes}


def get_specified_meals(recipes_by_id: {}, meals_spec_file_name: str):
    meals_spec = []
    with open(meals_spec_file_name) as meals_spec_file:
        meals_spec = json.loads(meals_spec_file.read())
    meals = []
    for spec in meals_spec:
        recipe = recipes_by_id[spec['recipe']]
        serves = recipe[SERVES_KEY]
        normalised_recipe = normalise_recipe(recipe, serves)
        for i in range(spec['servings']):
            meals.append(normalised_recipe)
    return meals


def normalise_recipe(recipe: {}, serves: int):
    norm_recipe = recipe.copy()
    for ingredient in norm_recipe[INGREDIENTS_KEY]:
        ingredient[QUANTITY_KEY] = ingredient[QUANTITY_KEY]/serves
    return norm_recipe


def merge_ingredients_list(ingredients: []):
    merged_ingredients = []
    for key, matching_ingredients in itertools.groupby(sorted(ingredients, key=ingredient_key_func), ingredient_key_func):
        merged_ingredients.append(functools.reduce(
            lambda i1, i2: merge_ingredients(i1, i2), list(matching_ingredients)
        ))
    return merged_ingredients


def load_file(file_name: str, recipes_dir: str):
    with open(os.path.join(recipes_dir, file_name)) as json_file:
        return json.loads(json_file.read())


def ingredient_key_func(ingredient):
    return ingredient[INGREDIENT_KEY] + ingredient.get(VARIANT_KEY, '') + ingredient.get(QUANTITY_TYPE_KEY, '')


def merge_ingredients(i1, i2):
    return {
        INGREDIENT_KEY: i1[INGREDIENT_KEY],
        VARIANT_KEY: i1.get(VARIANT_KEY, ''),
        QUANTITY_KEY: i1[QUANTITY_KEY] + i2[QUANTITY_KEY],
        QUANTITY_TYPE_KEY: i1.get(QUANTITY_TYPE_KEY, '')
    }


def save_shopping_list(ingredients: [], output_file_name: str):
    open(output_file_name, 'w').close()
    with open(output_file_name, 'a') as output_file:
        for ingredient in ingredients:
            output_file.write(ingredient_to_string(ingredient) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a shopping list for a meal planning specification')
    parser.add_argument('--spec', '-s', dest='meals_spec_file_name', default='meals_spec.json')
    parser.add_argument('--recipes_dir', '-r', dest='recipes_dir', default='recipes')
    parser.add_argument('--output', '-o', dest='output_file_name', default='shopping_list.txt')
    args = parser.parse_args()
    meals_spec_file_name = args.meals_spec_file_name
    recipes_dir = args.recipes_dir
    output_file_name = args.output_file_name
    print(
        f'Generating shopping list at \'{output_file_name}\' ' +
        f'using recipes in \'{recipes_dir}\' ' +
        f'and meal planning specification \'{meals_spec_file_name}\''
    )
    generate_shopping_list(meals_spec_file_name, recipes_dir, output_file_name)
