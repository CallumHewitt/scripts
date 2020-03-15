# Meal Planning

Scripts to help with meal planning.

## Arguments and input files

```RECIPES_DIR``` is where recipe files are stored. These recipes are created by ```create_recipe.py``` and can be read and used by ```generate_shopping_list.py```. This argument defaults to ```./recipes```. Files are stored under subdirectories dictated by the source. If the source is a URL the directory will be named after the first part of the domain name (eg. http://www.google.com -> google). If the source is a book, please provide the page number after the book title by using a semicolon (eg. The Joy of Cooking;25). For any other sources, in general aim to put any information not required for the subdirectory after a semicolon.

```json
{
  "id": "just_a_bunch_of_bananas",
  "name": "Just a Bunch of Bananas",
  "serves": 1,
  "source": "Nature;Not the magazine",
  "ingredients": [
    {
      "name": "banana",
      "quantity": 1,
      "unit": "bunch"
    }
  ]
}
```

```UNITS_FILE``` is a mapping from how a unit should be displayed to the user or stored in a recipe file, to all of the ways in which it could be input (known as variants). Any mappings need to be performed manually by the user. This argument defaults to ```inputs/unit_groups.json```.

```json
"clove": [
  "cloves"
],
"grams": [
  "gram",
  "g"
],
```

```INGREDIENTS_FILE``` is a file where ingredients are categorised by type. This categorisation needs to be done manually by the user. This argument defaults to ```inputs/ingredient_groups.json```.

```json
{
  "bread": [
    "burger buns",
    "flour tortillas"
  ],
  "dairy": [
    "feta cheese",
    "halloumi"
  ]
}
```

## create_recipe.py

An interactive script that adds new recipe files to the recipes directory. The id/file name is generated from the name of the recipe provided. If ```REFRESH_INPUTS``` is true, the ```extract_ingredients``` and ```extract_units``` scripts will be run before the script exits normally. This input is true by default.

```shell script
$ python meal_planning/scripts/create_recipe.py -h
usage: create_recipe.py [-h] [--recipes_dir RECIPES_DIR] [--units_file UNITS_FILE] [--ingredients_file INGREDIENTS_FILE]
                        [--refresh_inputs REFRESH_INPUTS]

Add new recipes to your recipes directory

optional arguments:
  -h, --help            show this help message and exit
  --recipes_dir RECIPES_DIR, -r RECIPES_DIR
  --units_file UNITS_FILE, -u UNITS_FILE
  --ingredients_file INGREDIENTS_FILE, -i INGREDIENTS_FILE
  --refresh_inputs REFRESH_INPUTS, -f REFRESH_INPUTS
```

## extract_ingredients.py

Extracts the ingredients from the recipes generated into ```INGREDIENTS_FILE```. Any existing groupings in the file are maintained. New ingredients are added to the uncategorised section of the file.

```shell script
$ python meal_planning/scripts/extract_ingredients.py -h
usage: extract_ingredients.py [-h] [--recipes_dir RECIPES_DIR] [--ingredients_file INGREDIENTS_FILE]

Extracts a list of ingredients from the recipes created. Any ingredients not already categorised in the INGREDIENTS_FILE are inserted into the uncategorised section.

optional arguments:
  -h, --help            show this help message and exit
  --recipes_dir RECIPES_DIR, -r RECIPES_DIR
  --ingredients_file INGREDIENTS_FILE, -i INGREDIENTS_FILE

```

## extract_units.py

Extracts the units from the recipes generated into ```UNITS_FILE```.  Any existing variation mappings are maintained. New units are inserted as 'display units' with no variations.

```shell script
$ python meal_planning/scripts/extract_units.py -h
usage: extract_units.py [-h] [--recipes_dir RECIPES_DIR] [--units_file UNITS_FILE]

Extracts a list of units from the recipes created. Any units not already categorised in the UNITS_FILE are inserted as display units with no variations.

optional arguments:
  -h, --help            show this help message and exit
  --recipes_dir RECIPES_DIR, -r RECIPES_DIR
  --units_file UNITS_FILE, -u UNITS_FILE
```

## generate_shopping_list.py

Uses a meal planning specification to generate a shopping list based on the recipes in your recipes directory. The ```MEAL_SPEC_FILE``` defines the number of servings of each recipe that the shopping list will be for. The shopping list is grouped by the categories in the ```INGREDIENTS_FILE``` and will be output to ```OUTPUT_FILE```.

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
$ python meal_planning/scripts/generate_shopping_list.py -h
usage: generate_shopping_list.py [-h] [--spec MEAL_SPEC_FILE] [--recipes_dir RECIPES_DIR] [--ingredients_file INGREDIENTS_FILE] [--output OUTPUT_FILE]

Generate a shopping list for a meal planning specification

optional arguments:
  -h, --help            show this help message and exit
  --spec MEAL_SPEC_FILE, -s MEAL_SPEC_FILE
  --recipes_dir RECIPES_DIR, -r RECIPES_DIR
  --ingredients_file INGREDIENTS_FILE, -i INGREDIENTS_FILE
  --output OUTPUT_FILE, -o OUTPUT_FILE
```
