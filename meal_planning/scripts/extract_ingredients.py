import argparse
import json
from pathlib import Path
from meallib import DEFAULT_INGREDIENTS_FILE, DEFAULT_RECIPE_DIR, ROOT_DIR, UNCATEGORISED_KEY, load_recipes_by_id


def extract_ingredients(recipes_dir: Path, ingredients_file: Path):
    recipes_by_id = load_recipes_by_id(recipes_dir)
    ingredients_by_category = read_ingredients_file(ingredients_file)
    categorised_ingredient_names = set(
        [ingredient for category in ingredients_by_category for ingredient in ingredients_by_category[category]])
    for recipe in recipes_by_id.values():
        for ingredient in recipe.ingredients:
            if (ingredient.name not in categorised_ingredient_names):
                ingredients_by_category[UNCATEGORISED_KEY].append(ingredient.name)
    for category in ingredients_by_category:
        ingredients_by_category[category] = sorted(list(set(ingredients_by_category[category])))
    save_ingredients(ingredients_file, ingredients_by_category)


def read_ingredients_file(ingredients_file: Path):
    ingredients = {UNCATEGORISED_KEY: []}
    if (ingredients_file.exists()):
        with ingredients_file.open('r+') as json_file:
            ingredients = json.loads(json_file.read() or '{\"' + UNCATEGORISED_KEY + '\": []}')
    return ingredients


def save_ingredients(ingredients_file: Path, ingredients: {}):
    with ingredients_file.open('w+') as output_file:
        output_file.write(json.dumps(ingredients, sort_keys=True))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Extracts a list of ingredients from the recipes created. Any ingredients not already categorised in the INGREDIENTS_FILE are inserted into the uncategorised section.')
    parser.add_argument('--recipes_dir', '-r', dest='recipes_dir', type=Path, default=DEFAULT_RECIPE_DIR)
    parser.add_argument('--ingredients_file', '-i', dest='ingredients_file', type=Path, default=DEFAULT_INGREDIENTS_FILE)
    args = parser.parse_args()
    recipes_dir = args.recipes_dir
    ingredients_file = args.ingredients_file
    print(f'Extracting ingredients from {recipes_dir.relative_to(ROOT_DIR)} to {ingredients_file.relative_to(ROOT_DIR)}')
    extract_ingredients(recipes_dir, ingredients_file)
