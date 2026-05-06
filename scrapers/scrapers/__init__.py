import aiohttp
import logging

BASE_URL = "https://www.vinted.fr/api/v2/catalog/items"
SESSION_URL = "https://www.vinted.fr"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "fr-FR,fr;q=0.9",
    "Referer": "https://www.vinted.fr/",
    "Origin": "https://www.vinted.fr",
    "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
}

logger = logging.getLogger(__name__)


async def get_session_cookies(session: aiohttp.ClientSession) -> None:
    try:
        async with session.get(SESSION_URL, headers={
            "User-Agent": HEADERS["User-Agent"],
            "Accept": "text/html",
        }, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            pass
    except Exception as e:
        logger.warning("Impossible de récupérer les cookies Vinted : %s", e)


async def fetch_listings(session: aiohttp.ClientSession, search_text: str, price_from: int, price_to: int, country_id: int | None = None) -> list[dict]:
    params = {
        "search_text": search_text,
        "price_from": price_from,
        "price_to": price_to,
        "order": "newest_first",
        "per_page": 20,
        "page": 1,
    }
    if country_id:
        params["country_ids[]"] = country_id
    try:
        async with session.get(BASE_URL, params=params, headers=HEADERS, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            if resp.status == 403:
                await get_session_cookies(session)
                async with session.get(BASE_URL, params=params, headers=HEADERS, timeout=aiohttp.ClientTimeout(total=10)) as resp2:
                    if resp2.status != 200:
                        return []
                    data = await resp2.json()
                    return data.get("items", [])
            if resp.status != 200:
                return []
            data = await resp.json()
            return data.get("items", [])
    except Exception as e:
        logger.error("Erreur Vinted pour '%s' : %s", search_text, e)
        return []


def build_item_url(item: dict) -> str:
    return f"https://www.vinted.fr/items/{item['id']}-{item.get('title', '').replace(' ', '-').lower()}"
