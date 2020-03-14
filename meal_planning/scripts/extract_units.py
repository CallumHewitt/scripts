import argparse
import json
from pathlib import Path
from meallib import DEFAULT_UNITS_FILE, DEFAULT_RECIPE_DIR, ROOT_DIR, load_recipes_by_id


def extract_units(recipes_dir: Path, units_file: Path):
    recipes_by_id = load_recipes_by_id(recipes_dir)
    units_by_group = read_units_file(units_file)
    unit_variants = set()
    for recipe in recipes_by_id.values():
        for ingredient in recipe.ingredients:
            unit = ingredient.unit
            if (unit is not None):
                units_by_group[unit] = set(units_by_group.get(unit, []))
                if (len(units_by_group[unit]) != 0):
                    unit_variants = unit_variants.union(units_by_group[unit])
    filtered_units_by_group = {}
    for unit in units_by_group:
        if (unit not in unit_variants):
            filtered_units_by_group[unit] = list(units_by_group[unit])
    save_units(units_file, filtered_units_by_group)


def read_units_file(units_file: Path):
    units = {}
    if (units_file.exists()):
        with units_file.open() as json_file:
            units = json.loads(json_file.read() or '{}')
    return units


def save_units(units_file: Path, ingredients: {}):
    with units_file.open('w') as output_file:
        output_file.write(json.dumps(ingredients, sort_keys=True))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Extracts a list of units from the recipes created. Any units not already categorised in the UNITS_FILE are inserted as display units with no variations.')
    parser.add_argument('--recipes_dir', '-r', dest='recipes_dir', type=Path, default=DEFAULT_RECIPE_DIR)
    parser.add_argument('--units_file', '-u', dest='units_file', type=Path, default=DEFAULT_UNITS_FILE)
    args = parser.parse_args()
    recipes_dir = args.recipes_dir
    units_file = args.units_file
    print(f'Extracting ingredients from {recipes_dir.relative_to(ROOT_DIR)} to {units_file.relative_to(ROOT_DIR)}')
    extract_units(recipes_dir, units_file)
