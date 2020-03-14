import argparse
import json
from pathlib import Path
from meallib import DEFAULT_INGREDIENTS_FILE, DEFAULT_RECIPE_DIR, ROOT_DIR, load_recipes_by_id


def extract_ingredients(recipes_dir: Path, ingredients_file: Path):
    recipes_by_id = load_recipes_by_id(recipes_dir)
    extracted_ingredients = read_ingredients_file(ingredients_file)
    for recipe in recipes_by_id.values():
        for ingredient in recipe.ingredients:
            extracted_ingredients[ingredient.core] = set(extracted_ingredients.get(ingredient.core, []))
            if (ingredient.variant is not None and ingredient.variant != ''):
                extracted_ingredients[ingredient.core].add(ingredient.variant)
    for ingredient in extracted_ingredients:
        extracted_ingredients[ingredient] = list(extracted_ingredients[ingredient])
    save_ingredients(ingredients_file, extracted_ingredients)


def read_ingredients_file(ingredients_file: Path):
    ingredients = []
    with ingredients_file.open() as json_file:
        ingredients = json.loads(json_file.read() or '{}')
    return ingredients


def save_ingredients(ingredients_file: Path, ingredients: {}):
    with ingredients_file.open('w') as output_file:
        output_file.write(json.dumps(ingredients, sort_keys=True))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Extracts a list of ingredients and their variations from the recipes created. This file can be used to help create recipes faster')
    parser.add_argument('--recipes_dir', '-r', dest='recipes_dir', type=Path, default=DEFAULT_RECIPE_DIR)
    parser.add_argument('--ingredients_file', '-i', dest='ingredients_file', type=Path, default=DEFAULT_INGREDIENTS_FILE)
    args = parser.parse_args()
    recipes_dir = args.recipes_dir
    ingredients_file = args.ingredients_file
    print(f'Extracting ingredients from {recipes_dir.relative_to(ROOT_DIR)} to {ingredients_file.relative_to(ROOT_DIR)}')
    extract_ingredients(recipes_dir, ingredients_file)
