ID_KEY = 'id'
NAME_KEY = 'name'
SOURCE_KEY = 'source'
SERVES_KEY = 'serves'
INGREDIENTS_KEY = 'ingredients'

INGREDIENT_KEY = 'ingredient'
VARIANT_KEY = 'variant'
QUANTITY_KEY = 'quantity'
QUANTITY_TYPE_KEY = 'quantity_type'


def ingredient_to_string(ingredient: {}):
    return ' '.join(filter(lambda x: x != '', [str(ingredient[QUANTITY_KEY]), ingredient.get(QUANTITY_TYPE_KEY, ''), ingredient.get(VARIANT_KEY, ''), ingredient[INGREDIENT_KEY]]))


def recipe_to_string(recipe: {}):
    str_list = []
    str_list.append(title_string(recipe[NAME_KEY]))
    str_list.append(f'Source: {recipe[SOURCE_KEY]}')
    str_list.append(f'Serves: {str(recipe[SERVES_KEY])}')
    str_list.append(f'Ingredients')
    ingredient_strings = list(map(lambda ingredient: '  - ' + ingredient_to_string(ingredient), recipe[INGREDIENTS_KEY]))
    str_list = str_list + ingredient_strings
    return '\n'.join(str_list)

def title_string(string: str):
    return f'====== {string} ====='