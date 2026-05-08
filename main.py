import logging
import os
import discord
from discord.ext import tasks
import aiohttp

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN", "")
CHANNELS = {
    "pokemon":   1501642620638728292,
    "vetements": 1501642716662992946,
}
CHECK_INTERVAL = 60
VINTED_SEARCHES = [
    {"name": "Supreme Pull M/L", "search_text": "supreme sweat", "price_from": 5, "price_to": 100, "category": "vetements", "size_ids": [208, 209]},
    {"name": "Palace Pull M/L", "search_text": "palace pull", "price_from": 5, "price_to": 100, "category": "vetements", "size_ids": [208, 209]},
    {"name": "Stone Island Pull M/L", "search_text": "stone island pull", "price_from": 5, "price_to": 100, "category": "vetements", "size_ids": [208, 209]},
    {"name": "Moncler Pull M/L", "search_text": "moncler pull", "price_from": 5, "price_to": 100, "category": "vetements", "size_ids": [208, 209]},
    {"name": "Balenciaga Pull M/L", "search_text": "balenciaga sweat", "price_from": 5, "price_to": 100, "category": "vetements", "size_ids": [208, 209]},
    {"name": "Off-White Pull M/L", "search_text": "off white hoodie", "price_from": 5, "price_to": 100, "category": "vetements", "size_ids": [208, 209]},
    {"name": "Gucci Pull M/L", "search_text": "gucci pull", "price_from": 5, "price_to": 100, "category": "vetements", "size_ids": [208, 209]},
    {"name": "Louis Vuitton Pull M/L", "search_text": "louis vuitton pull", "price_from": 5, "price_to": 100, "category": "vetements", "size_ids": [208, 209]},
        {"name": "Cartes pokemon vintage", "search_text": "cartes pokemon vintage 1999 2010", "price_from": 5, "price_to": 35, "category": "pokemon", "size_ids": []},
    {"name": "Carte pokemon ancienne", "search_text": "carte pokemon ancienne française", "price_from": 5, "price_to": 35, "category": "pokemon", "size_ids": []},
    {"name": "Lot cartes pokemon anciennes", "search_text": "lot cartes pokemon anciennes", "price_from": 5, "price_to": 35, "category": "pokemon", "size_ids": []},
    {"name": "Lot pokemon vintage", "search_text": "lot pokemon vintage français", "price_from": 5, "price_to": 35, "category": "pokemon", "size_ids": []},
    {"name": "Classeur carte pokemon", "search_text": "classeur carte pokemon", "price_from": 5, "price_to": 35, "category": "pokemon", "size_ids": []},
    {"name": "Classeur pokemon complet", "search_text": "classeur pokemon complet", "price_from": 5, "price_to": 35, "category": "pokemon", "size_ids": []},
    {"name": "Lot cartes brillantes", "search_text": "lot cartes brillantes pokemon ancien", "price_from": 5, "price_to": 35, "category": "pokemon", "size_ids": []},

]

BASE_URL = "https://www.vinted.fr/api/v2/catalog/items"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "fr-FR,fr;q=0.9",
    "Referer": "https://www.vinted.fr/",
    "Origin": "https://www.vinted.fr",
}

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)
intents = discord.Intents.default()
bot = discord.Client(intents=intents)
seen_ids: set[int] = set()
http_session = None


async def get_session_cookies(session):
    try:
        async with session.get("https://www.vinted.fr", headers={"User-Agent": HEADERS["User-Agent"], "Accept": "text/html"}, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            pass
    except Exception as e:
        logger.warning("Cookies Vinted : %s", e)


async def fetch_listings(session, search_text, price_from, price_to, size_ids):
    params = {"search_text": search_text, "price_from": price_from, "price_to": price_to, "order": "newest_first", "per_page": 20, "page": 1, "country_ids[]": 1}
    for sid in size_ids:
        params.setdefault("size_ids[]", [])
        if isinstance(params["size_ids[]"], list):
            params["size_ids[]"].append(sid)
    try:
        async with session.get(BASE_URL, params=params, headers=HEADERS, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            if resp.status == 403:
                await get_session_cookies(session)
                async with session.get(BASE_URL, params=params, headers=HEADERS, timeout=aiohttp.ClientTimeout(total=10)) as resp2:
                    if resp2.status != 200:
                        return []
                    return (await resp2.json()).get("items", [])
            if resp.status != 200:
                return []
            return (await resp.json()).get("items", [])
    except Exception as e:
        logger.error("Erreur Vinted '%s': %s", search_text, e)
        return []


def make_embed(item, search_name):
    price = item.get("price", {})
    price_str = f"{price.get('amount', '?')} {price.get('currency_code', '€')}"
    url = f"https://www.vinted.fr/items/{item['id']}"
    embed = discord.Embed(title=f"🔥 {item.get('title', 'Sans titre')}", url=url, description=f"**Prix : {price_str}**\nRecherche : `{search_name}`", color=discord.Color.green())
    photos = item.get("photos", [])
    if photos:
        thumb = photos[0].get("url") or photos[0].get("full_size_url")
        if thumb:
            embed.set_thumbnail(url=thumb)
    user = item.get("user", {})
    if user:
        embed.set_footer(text=f"Vendeur : {user.get('login', '?')} • Vinted")
    size = item.get("size_title")
    brand = item.get("brand_title")
    if size or brand:
        extras = []
        if brand:
            extras.append(f"Marque : {brand}")
        if size:
            extras.append(f"Taille : {size}")
        embed.add_field(name="Détails", value="\n".join(extras), inline=False)
    return embed


@tasks.loop(seconds=CHECK_INTERVAL)
async def check_deals():
    for search in VINTED_SEARCHES:
        items = await fetch_listings(http_session, search["search_text"], search["price_from"], search["price_to"], search.get("size_ids", []))
        channel = bot.get_channel(CHANNELS.get(search["category"]))
        if not channel:
            continue
        for item in [i for i in items if i["id"] not in seen_ids]:
            seen_ids.add(item["id"])
            try:
                await channel.send(embed=make_embed(item, search["name"]))
                logger.info("Envoyé : %s", item.get("title"))
            except discord.DiscordException as e:
                logger.error("Discord : %s", e)


@bot.event
async def on_ready():
    global http_session
    logger.info("Bot connecté : %s", bot.user)
    http_session = aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar())
    await get_session_cookies(http_session)
    check_deals.start()


bot.run(DISCORD_TOKEN)
