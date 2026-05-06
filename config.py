import os
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN", "")

# ID des salons Discord où envoyer les alertes
CHANNELS = {
    "pokemon":   1501642620638728292,
    "vetements": 1501642716662992946,
}

# Intervalle de vérification en secondes
CHECK_INTERVAL = 60

# ── Recherches Vinted ─────────────────────────────────────────────────────────
VINTED_SEARCHES = [
    # ── Vêtements à fort potentiel de revente (5€ - 100€) ────────────────────
    {
        "name": "Supreme",
        "search_text": "supreme",
        "price_from": 5,
        "price_to": 100,
        "category": "vetements",
        "country_id": 1,
    },
    {
        "name": "Palace",
        "search_text": "palace",
        "price_from": 5,
        "price_to": 100,
        "category": "vetements",
        "country_id": 1,
    },
    {
        "name": "Jordan 1",
        "search_text": "jordan 1",
        "price_from": 5,
        "price_to": 100,
        "category": "vetements",
        "country_id": 1,
    },
    {
        "name": "Stone Island",
        "search_text": "stone island",
        "price_from": 5,
        "price_to": 100,
        "category": "vetements",
        "country_id": 1,
    },
    {
        "name": "Moncler",
        "search_text": "moncler",
        "price_from": 5,
        "price_to": 100,
        "category": "vetements",
        "country_id": 1,
    },
    {
        "name": "Balenciaga",
        "search_text": "balenciaga",
        "price_from": 5,
        "price_to": 100,
        "category": "vetements",
        "country_id": 1,
    },
    {
        "name": "Off-White",
        "search_text": "off white",
        "price_from": 5,
        "price_to": 100,
        "category": "vetements",
        "country_id": 1,
    },
    {
        "name": "Louis Vuitton",
        "search_text": "louis vuitton",
        "price_from": 5,
        "price_to": 100,
        "category": "vetements",
        "country_id": 1,
    },
    {
        "name": "Gucci",
        "search_text": "gucci",
        "price_from": 5,
        "price_to": 100,
        "category": "vetements",
        "country_id": 1,
    },
    {
        "name": "Nike Vintage",
        "search_text": "nike vintage",
        "price_from": 5,
        "price_to": 100,
        "category": "vetements",
        "country_id": 1,
    },
    # ── Cartes Pokémon françaises (5€ - 100€) ────────────────────────────────
    {
        "name": "Carte Pokemon VF",
        "search_text": "carte pokemon vf",
        "price_from": 5,
        "price_to": 100,
        "category": "pokemon",
        "country_id": 1,
    },
    {
        "name": "Carte Pokemon française",
        "search_text": "carte pokemon française",
        "price_from": 5,
        "price_to": 100,
        "category": "pokemon",
        "country_id": 1,
    },
    {
        "name": "Booster Pokémon FR",
        "search_text": "booster pokemon francais",
        "price_from": 5,
        "price_to": 100,
        "category": "pokemon",
        "country_id": 1,
    },
    {
        "name": "Dracaufeu holo",
        "search_text": "dracaufeu holo",
        "price_from": 5,
        "price_to": 100,
        "category": "pokemon",
        "country_id": 1,
    },
    {
        "name": "Coffret Pokémon",
        "search_text": "coffret pokemon",
        "price_from": 5,
        "price_to": 100,
        "category": "pokemon",
        "country_id": 1,
    },
]
