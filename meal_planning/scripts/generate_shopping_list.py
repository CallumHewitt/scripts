import json
import itertools
import functools
import os
import argparse
import copy
from pathlib import Path
from meallib import Recipe, Ingredient, DEFAULT_MEAL_SPEC, DEFAULT_RECIPE_DIR, DEFAULT_SHOPPING_LIST_OUTPUT, ROOT_DIR


def generate_shopping_list(meal_spec_path: Path, recipes_path: Path, output_path: Path):
    recipes_by_id = load_recipes_by_id(recipes_path)
    meals = get_specified_meals(recipes_by_id, meal_spec_path)
    ingredients = [
        ingredient for meal in meals for ingredient in meal.ingredients
    ]
    merged_ingredients = merge_ingredients_list(ingredients)
    sorted_ingredients = sorted(merged_ingredients, key=lambda ingredient: ingredient.core)
    save_shopping_list(sorted_ingredients, output_path)


def load_recipes_by_id(recipes_path: Path):
    recipe_paths = [recipe_path for recipe_path in recipes_path.glob('*.json')]
    recipes = [load_recipe(recipe_path) for recipe_path in recipe_paths]
    return {recipe.id: recipe for recipe in recipes}


def load_recipe(recipe_path: Path):
    with recipe_path.open() as json_file:
        recipe_dict = json.loads(json_file.read())
        ingredients = [Ingredient(ingredient['core'], ingredient.get('variant', ''), ingredient['quantity'], ingredient.get('unit', ''))
                       for ingredient in recipe_dict['ingredients']
                       ]
        return Recipe(recipe_dict['name'], recipe_dict['serves'], recipe_dict['source'], ingredients)


def get_specified_meals(recipes_by_id: {}, meal_spec_path: Path):
    meals_spec = []
    with meal_spec_path.open() as meals_spec_file:
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
    return ingredient.core + ingredient.variant + ingredient.unit


def merge_ingredients(i1, i2):
    return Ingredient(
        i1.core,
        i1.variant,
        i1.quantity + i2.quantity,
        i1.unit
    )


def save_shopping_list(ingredients: [], output_path: str):
    open(output_path, 'w').close()
    with open(output_path, 'a') as output_file:
        for ingredient in ingredients:
            output_file.write(str(ingredient) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a shopping list for a meal planning specification')
    parser.add_argument('--spec', '-s', dest='meal_spec_path', type=Path, default=DEFAULT_MEAL_SPEC)
    parser.add_argument('--recipes_path', '-r', dest='recipes_path', type=Path, default=DEFAULT_RECIPE_DIR)
    parser.add_argument('--output', '-o', dest='output_path', type=Path, default=DEFAULT_SHOPPING_LIST_OUTPUT)
    args = parser.parse_args()
    meal_spec_path = args.meal_spec_path
    recipes_path = args.recipes_path
    output_path = args.output_path
    print(
        f'Generating shopping list into \'{output_path.relative_to(ROOT_DIR)}\' ' +
        f'using recipes in \'{recipes_path.relative_to(ROOT_DIR)}\' ' +
        f'and meal planning specification \'{meal_spec_path.relative_to(ROOT_DIR)}\''
    )
    generate_shopping_list(meal_spec_path, recipes_path, output_path)
    print('Shopping list complete')
