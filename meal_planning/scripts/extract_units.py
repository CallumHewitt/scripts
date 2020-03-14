import argparse
import json
from pathlib import Path
from meallib import DEFAULT_UNITS_FILE, DEFAULT_RECIPE_DIR, ROOT_DIR, load_recipes_by_id


def extract_units(recipes_dir: Path, units_file: Path):
    recipes_by_id = load_recipes_by_id(recipes_dir)
    extracted_units = read_units_file(units_file)
    variant_units = set()
    for recipe in recipes_by_id.values():
        for ingredient in recipe.ingredients:
            unit = ingredient.unit
            if (unit is not None and unit != ''):
                extracted_units[unit] = set(extracted_units.get(unit, []))
                if (extracted_units[unit] != []):
                    variant_units = variant_units.union(extracted_units[unit])
    for unit in extracted_units:
        if (unit in variant_units):
            del extracted_units[unit]
        else:
            extracted_units[unit] = list(extracted_units[unit])
    save_units(units_file, extracted_units)


def read_units_file(units_file: Path):
    ingredients = []
    with units_file.open() as json_file:
        ingredients = json.loads(json_file.read() or '{}')
    return ingredients


def save_units(units_file: Path, ingredients: {}):
    with units_file.open('w') as output_file:
        output_file.write(json.dumps(ingredients, sort_keys=True))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Extracts a list of units and their variations from the recipes and existing units file. Variations to units must be added manually')
    parser.add_argument('--recipes_dir', '-r', dest='recipes_dir', type=Path, default=DEFAULT_RECIPE_DIR)
    parser.add_argument('--units_file', '-i', dest='units_file', type=Path, default=DEFAULT_UNITS_FILE)
    args = parser.parse_args()
    recipes_dir = args.recipes_dir
    units_file = args.units_file
    print(f'Extracting ingredients from {recipes_dir.relative_to(ROOT_DIR)} to {units_file.relative_to(ROOT_DIR)}')
    extract_units(recipes_dir, units_file)
