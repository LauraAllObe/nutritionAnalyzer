import re
import csv
import json
import requests
from collections import defaultdict
from rapidfuzz import process, fuzz
import pubchempy as pcp

ALIAS_CACHE_FILE = "alias_cache.json"
global_alias_set = set()

def get_pubchem_aliases(ingredient_name):
    try:
        compounds = pcp.get_compounds(ingredient_name, 'name')
        if compounds:
            synonyms = compounds[0].synonyms
            return list(set(s.lower() for s in synonyms))
        return []
    except Exception as e:
        print(f"[PubChem error for '{ingredient_name}']: {e}")
        return []

def update_alias_cache(aliases):
    for a in aliases:
        if a:
            global_alias_set.add(a.lower().strip())

def fuzzy_match_alias(name, threshold=90):
    if not global_alias_set:
        print("[Warning] Alias set is empty — did you run seed_aliases_from_open_food_facts?")
        return None
    result = process.extractOne(name, global_alias_set, scorer=fuzz.token_sort_ratio)
    return result[0] if result and result[1] >= threshold else None

def seed_aliases_from_open_food_facts(limit=10000):
    url = "https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv"
    response = requests.get(url, stream=True)
    response.encoding = 'utf-8'
    reader = csv.DictReader((line.decode('utf-8') for line in response.iter_lines()), delimiter='\t')

    langs = ['fr', 'de', 'es', 'it']
    alias_dict = defaultdict(set)

    for count, row in enumerate(reader):
        if count % 500 == 0:
            print(f"Processing row {count}...")
        if count >= limit:
            break

        ingredients_text = row.get("ingredients_text", "")
        if not ingredients_text.strip():
            continue

        for ing in ingredients_text.split(','):
            ing = ing.strip().lower()
            if not ing:
                continue
            alias_dict[ing].add(ing)

            for lang in langs:
                key = f"ingredients_text_{lang}"
                alt = row.get(key)
                if alt:
                    for alt_ing in alt.split(','):
                        alt_ing = alt_ing.strip().lower()
                        if alt_ing:
                            alias_dict[ing].add(alt_ing)
                            alias_dict[alt_ing].add(ing)

    for aliases in alias_dict.values():
        update_alias_cache(list(aliases))

    print(f"[✓] Seeded {len(global_alias_set)} unique aliases from Open Food Facts.")

def save_alias_cache(path=ALIAS_CACHE_FILE):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(sorted(global_alias_set), f, ensure_ascii=False, indent=2)
        print(f"[✓] Alias cache saved to {path}")
    except Exception as e:
        print(f"[!] Error saving alias cache: {e}")

def load_alias_cache(path=ALIAS_CACHE_FILE):
    global global_alias_set
    try:
        with open(path, "r", encoding="utf-8") as f:
            global_alias_set = set(json.load(f))
        print(f"[✓] Loaded {len(global_alias_set)} aliases from cache.")
        return True
    except FileNotFoundError:
        print(f"[ ] Alias cache not found at {path}. Will seed from source...")
        return False
    except Exception as e:
        print(f"[!] Error loading alias cache: {e}")
        return False
