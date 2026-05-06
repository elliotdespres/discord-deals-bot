import logging
import discord
from discord.ext import tasks
import aiohttp

from config import DISCORD_TOKEN, CHANNELS, CHECK_INTERVAL, VINTED_SEARCHES
from scrapers.vinted import fetch_listings, build_item_url, get_session_cookies

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
bot = discord.Client(intents=intents)

seen_ids: set[int] = set()
http_session: aiohttp.ClientSession | None = None


def make_embed(item: dict, search_name: str) -> discord.Embed:
    title = item.get("title", "Sans titre")
    price = item.get("price", {})
    price_str = f"{price.get('amount', '?')} {price.get('currency_code', '€')}"
    url = build_item_url(item)

    embed = discord.Embed(
        title=f"🔥 {title}",
        url=url,
        description=f"**Prix : {price_str}**\nRecherche : `{search_name}`",
        color=discord.Color.green(),
    )

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
    global http_session
    for search in VINTED_SEARCHES:
        items = await fetch_listings(http_session, search["search_text"], search["price_from"], search["price_to"], search.get("country_id"))
        channel_id = CHANNELS.get(search["category"])
        if not channel_id:
            continue
        channel = bot.get_channel(channel_id)
        if not channel:
            logger.warning("Canal introuvable : %s", channel_id)
            continue

        new_items = [i for i in items if i["id"] not in seen_ids]
        for item in new_items:
            seen_ids.add(item["id"])
            embed = make_embed(item, search["name"])
            try:
                await channel.send(embed=embed)
                logger.info("Envoyé : %s (%s)", item.get("title"), search["name"])
            except discord.DiscordException as e:
                logger.error("Erreur envoi Discord : %s", e)

        if new_items:
            logger.info("%d nouvelle(s) annonce(s) pour '%s'", len(new_items), search["name"])


@bot.event
async def on_ready():
    global http_session
    logger.info("Bot connecté : %s (ID %s)", bot.user, bot.user.id)
    http_session = aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar())
    await get_session_cookies(http_session)
    logger.info("Session Vinted initialisée")
    check_deals.start()


bot.run(DISCORD_TOKEN)
