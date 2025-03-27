import re
import spacy
from langdetect import detect
from googletrans import Translator
from ingredient_aliases import get_pubchem_aliases, fuzzy_match_alias, update_alias_cache

nlp = spacy.load("en_core_web_sm")
translator = Translator()

def standardize_ingredient_name(name):
    name = name.lower().strip()

    aliases = get_pubchem_aliases(name)
    if aliases:
        update_alias_cache(aliases)
        return aliases[0], aliases

    fuzzy = fuzzy_match_alias(name)
    if fuzzy:
        return fuzzy, [fuzzy]

    return name, [name]

def translate_to_english(text):
    try:
        lang = detect(text)
        return translator.translate(text, src=lang, dest='en').text if lang != 'en' else text
    except Exception:
        return text

def preprocess_ingredient_list(text):
    raw_ingredients = re.split(r'[,\n;/••]+', text)
    processed = []

    for raw in raw_ingredients:
        raw = raw.strip()
        if raw:
            translated = translate_to_english(raw)
            standard, aliases = standardize_ingredient_name(translated)
            processed.append((standard, aliases))

    return processed
