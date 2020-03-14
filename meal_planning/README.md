# Meal Planning

Two scripts to help with meal planning.

## add_recipe.py

An interactive script that adds a new json file to your recipes directory. The id/file name is generated from the name of the recipe provided.

```shell script
$ python add_recipe.py -h
usage: add_recipe.py [-h] [--recipes_dir RECIPES_DIR]

Add new recipes to your recipes directory

optional arguments:
  -h, --help            show this help message and exit
  --recipes_dir RECIPES_DIR, -r RECIPES_DIR
```

## extract_ingredients.py

Extracts the ingredients from the recipes generated along with their variants. In future these ingredients will be used to help make it easier to add recipes.

```shell script
$ python meal_planning/scripts/extract_ingredients.py  -h
usage: extract_ingredients.py [-h] [--recipes_dir RECIPES_DIR] [--ingredients_file INGREDIENTS_FILE]

Extracts a list of ingredients and their variations from the recipes created. This file can be used to help create recipes faster

optional arguments:
  -h, --help            show this help message and exit
  --recipes_dir RECIPES_DIR, -r RECIPES_DIR
  --ingredients_file INGREDIENTS_FILE, -i INGREDIENTS_FILE
```

## extract_units.py

Extracts the units from the recipes generated along with their variants. In future these units will be used to help make it easier to add recipes.

```shell script
$ python meal_planning/scripts/extract_units.py  -h
usage: extract_units.py [-h] [--recipes_dir RECIPES_DIR] [--units_file UNITS_FILE]

Extracts a list of units and their variations from the recipes and existing units file. Variations to units must be added manually

optional arguments:
  -h, --help            show this help message and exit
  --recipes_dir RECIPES_DIR, -r RECIPES_DIR
  --units_file UNITS_FILE, -i UNITS_FILE
```

In the file generated, any units that are equivalent should have key giving the way the unit should be displayed in recipes/shopping lists, and an array of alternate variations.

For example:

```json
{
  "grams": ["g"],
  "kilograms": ["kilos", "kg"],
}
```

## generate_shopping_list.py

Uses a __meal planning specification__ to generate a shopping list based on the recipes in your recipes directory.

```json
[
    {
        "recipe": "spaghetti_puttanesca",
        "servings": 2
    },
    {
        "recipe": "veggie_laksa_soup",
        "servings": 4
    },
    {
        "recipe": "fried_bean_taco",
        "servings": 3
    }
]
```

```shell script
$ python generate_shopping_list.py -h
usage: generate_shopping_list.py [-h] [--spec MEALS_SPEC_FILE_NAME]
                                 [--recipes_dir RECIPES_DIR]
                                 [--output OUTPUT_FILE_NAME]

Generate a shopping list for a meal planning specification

optional arguments:
  -h, --help            show this help message and exit
  --spec MEALS_SPEC_FILE_NAME, -s MEALS_SPEC_FILE_NAME
  --recipes_dir RECIPES_DIR, -r RECIPES_DIR
  --output OUTPUT_FILE_NAME, -o OUTPUT_FILE_NAME
```
