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
