from ingredient_aliases import load_alias_cache, seed_aliases_from_open_food_facts, save_alias_cache

def initialize_aliases():
    if not load_alias_cache():
        seed_aliases_from_open_food_facts(limit=5000)
        save_alias_cache()

# Call this at the beginning of your app
initialize_aliases()
