# Best Pokemon Finder (by stats) - Jeffery Xie
# This is a personal project to familiarize myself with Pokemon's API
# Using the pokeapi, this program will create a list of the three best
# pokemon for each stat category and show you which pokemon are the strongest.

import requests


def create_enhanced_pokedex(version_link):
    """
    Opens the pokeapi and grabs the pokemon info for the desired game, and 
    finds each pokemon name, mapping it with its associated stats.
    
    :param version_link: the link to the desired pokemon version on the pokeapi
    :return: A pokedex(dictionary) with key value pairs pokemon name,pokemon stats
    """
    # Open the pokemon API and retrieve the information in json format
    pokemon_api = requests.get(version_link)
    pokedex = pokemon_api.json()

    # Creating an enhanced pokedex which goes through each pokemon's link on
    # the pokemon API, gets all of their base stats, and puts each pokemon
    # with its stats as key, value pairs into a dictionary (enhanced_pokedex)
    enhanced_pokedex = {}
    for pokemon_name in pokedex['pokemon_species']:
        pokemon_stats = {}
        pokemon_species = requests.get(pokemon_name.get("url"))
        pokemon_id = pokemon_species.json()['id']
        pokemon_info = requests.get("https://pokeapi.co/api/v2/pokemon/" + str(pokemon_id) + "/")
        for stat in pokemon_info.json()['stats']:
            pokemon_stats[stat['stat']['name']] = stat['base_stat']
        enhanced_pokedex[pokemon_name['name']] = pokemon_stats

    return enhanced_pokedex


def find_best_stats(pokedex, best_stats):
    """
    Goes through each pokemon's stats in the enhanced_pokedex, checks if any of its stats are
    higher than those found in best_pokemon_stats so far, and if so, replace the lowest value
    for that particular category with the current pokemon's stats. This algorithm also automatically
    sorts each category from highest base stat to lowest base stat.
    
    :param pokedex: Dictionary - The enhanced pokedex with pokemon names mapped to their stats
    :param best_stats: List - This will hold the best three pokemon in each stat category
    :return: list best_stats, which holds the best three pokemon in each stat category
    """

    for pokemon in pokedex:
        category = -1
        for item in pokedex[pokemon]:
            category = category + 1
            for index in range(1, len(best_stats[0])):
                if pokedex[pokemon][item] > best_stats[category][index][1]:
                    if (pokemon.capitalize(), pokedex[pokemon][item]) not in best_stats[category]:
                        best_stats[category].insert(index, (pokemon.capitalize(), pokedex[pokemon][item]))
                        best_stats[category].pop(-1)

    return best_stats


def main():
    """
    Using the pokeapi, find the pokemon for generation one pokemon and find the top
    three pokemon stat-wise for each stat category. Then, print the results.
    :return: None
    """
    # Initializing the base lists for each stat, I plan on getting the top three pokemon for each stat
    highest_hps = ["Highest Healths:", (None, 0), (None, 0), (None, 0)]
    highest_attacks = ["Highest Attacks:", (None, 0), (None, 0), (None, 0)]
    highest_defenses = ["Highest Defenses:", (None, 0), (None, 0), (None, 0)]
    highest_special_attacks = ["Highest Special Attacks:", (None, 0), (None, 0), (None, 0)]
    highest_special_defenses = ["Highest Special Defenses:", (None, 0), (None, 0), (None, 0)]
    highest_speeds = ["Highest Speeds:", (None, 0), (None, 0), (None, 0)]

    # A list of lists, containing the top three pokemon for each stat category.
    best_pokemon_stats = [highest_hps, highest_attacks, highest_defenses,
                          highest_special_attacks, highest_special_defenses, highest_speeds]

    version = input("Please enter your desired pokemon version (1-8): ")
    version_link = "https://pokeapi.co/api/v2/generation/" + version + "/"
    print("Adding pokemon to pokedex...")
    pokedex = create_enhanced_pokedex(version_link)

    print("Finding the best stats...")
    best_stats = find_best_stats(pokedex, best_pokemon_stats)

    # Print the results, note that this only shows the first three highest pokemon by their stats.
    # if there are other pokemon with the same stat as the lowest pokemon's stat in the list, the
    # oldest pokemon in the list will take priority over the ones currently being looked over.
    for pokemon in best_stats:
        print(pokemon)


if __name__ == "__main__":
    main()
