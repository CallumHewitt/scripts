import json
import itertools
import functools
import os
import argparse
import copy
from pathlib import Path
from meallib import Recipe, Ingredient, load_recipes_by_id, title_string, DEFAULT_MEAL_SPEC, DEFAULT_RECIPE_DIR, DEFAULT_INGREDIENTS_FILE, DEFAULT_SHOPPING_LIST_OUTPUT, UNCATEGORISED_KEY, ROOT_DIR


def generate_shopping_list(meal_spec_file: Path, recipes_dir: Path, ingredients_file: Path, output_file: Path):
    recipes_by_id = load_recipes_by_id(recipes_dir)
    meals = get_specified_meals(recipes_by_id, meal_spec_file)
    ingredients = [
        ingredient for meal in meals for ingredient in meal.ingredients
    ]
    merged_ingredients = merge_ingredients_list(ingredients)
    category_by_ingredient = get_category_by_ingredient(ingredients_file)
    def key_func(ingredient): return category_by_ingredient.get(ingredient.name, UNCATEGORISED_KEY)
    ingredients_by_category_iter = itertools.groupby(sorted(merged_ingredients, key=key_func), key_func)
    ingredients_by_category = {category: list(ingredients) for category, ingredients in ingredients_by_category_iter}
    save_shopping_list(ingredients_by_category, output_file)


def get_specified_meals(recipes_by_id: {}, meal_spec_file: Path):
    meals_spec = []
    with meal_spec_file.open() as meals_spec_file:
        meals_spec = json.loads(meals_spec_file.read())
    meals = []
    for spec in meals_spec:
        recipe = recipes_by_id[spec['recipe']]
        serves = recipe.serves
        normalised_recipe = normalise_recipe(recipe, serves)
        for _ in range(spec['servings']):
            meals.append(normalised_recipe)
    return meals


def normalise_recipe(recipe: {}, serves: int):
    norm_recipe = copy.deepcopy(recipe)
    for ingredient in norm_recipe.ingredients:
        ingredient.quantity = ingredient.quantity/serves
    return norm_recipe


def merge_ingredients_list(ingredients: []):
    merged_ingredients = []
    for _, matching_ingredients in itertools.groupby(sorted(ingredients, key=ingredient_merge_key), ingredient_merge_key):
        merged_ingredients.append(functools.reduce(
            lambda i1, i2: merge_ingredients(i1, i2), list(matching_ingredients)
        ))
    return merged_ingredients


def ingredient_merge_key(ingredient):
    return ingredient.name + (ingredient.unit or '')


def merge_ingredients(i1, i2):
    return Ingredient(
        i1.name,
        i1.quantity + i2.quantity,
        i1.unit
    )


def get_category_by_ingredient(ingredients_file: Path):
    category_by_ingredient = {}
    if (ingredients_file.exists()):
        with ingredients_file.open() as json_file:
            ingredients_by_category = json.loads(json_file.read() or '{}')
            for category in ingredients_by_category:
                for ingredient in ingredients_by_category[category]:
                    category_by_ingredient[ingredient] = category
    return category_by_ingredient


def save_shopping_list(ingredients_by_category: {}, output_file: str):
    with output_file.open('w+') as output:
        for category in ingredients_by_category:
            output.write(title_string(category) + '\n')
            for ingredient in ingredients_by_category[category]:
                output.write(str(ingredient) + '\n')
            output.write('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a shopping list for a meal planning specification')
    parser.add_argument('--spec', '-s', dest='meal_spec_file', type=Path, default=DEFAULT_MEAL_SPEC)
    parser.add_argument('--recipes_dir', '-r', dest='recipes_dir', type=Path, default=DEFAULT_RECIPE_DIR)
    parser.add_argument('--ingredients_file', '-i', dest='ingredients_file', type=Path, default=DEFAULT_INGREDIENTS_FILE)
    parser.add_argument('--output', '-o', dest='output_file', type=Path, default=DEFAULT_SHOPPING_LIST_OUTPUT)
    args = parser.parse_args()
    meal_spec_file = args.meal_spec_file
    recipes_dir = args.recipes_dir
    ingredients_file = args.ingredients_file
    output_file = args.output_file
    print(
        f'Generating shopping list into \'{output_file.relative_to(ROOT_DIR)}\' ' +
        f'using recipes in \'{recipes_dir.relative_to(ROOT_DIR)}\' ' +
        f'and meal planning specification \'{meal_spec_file.relative_to(ROOT_DIR)}\''
    )
    generate_shopping_list(meal_spec_file, recipes_dir, ingredients_file, output_file)
    print('Shopping list complete')
