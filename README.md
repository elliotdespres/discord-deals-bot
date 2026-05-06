# Discord Deals Bot 🔥

Bot Discord qui surveille Vinted et envoie des alertes quand des petites prix apparaissent.

## Installation

```bash
cd C:\Users\DESPRESElliotS25-26S\discord-deals-bot
pip install -r requirements.txt
```

## Configuration

### 1. Créer le bot Discord
1. Va sur https://discord.com/developers/applications
2. "New Application" → donne un nom
3. Onglet "Bot" → "Add Bot" → copie le **Token**
4. Onglet "OAuth2" → "URL Generator" → coche `bot` + permissions `Send Messages`, `Embed Links`
5. Ouvre l'URL générée et invite le bot sur ton serveur

### 2. Récupérer l'ID de ton salon
1. Discord → Paramètres → Avancé → Active "Mode développeur"
2. Clic droit sur le salon → "Copier l'identifiant"

### 3. Modifier config.py
```python
DISCORD_TOKEN = "ton_vrai_token"
CHANNELS = {
    "vetements": 123456789,   # ID du salon vêtements
    "pokemon":   987654321,   # ID du salon pokemon
}
```

### 4. Lancer
```bash
python main.py
```

## Personnaliser les recherches

Dans `config.py`, modifie `VINTED_SEARCHES` :
```python
{
    "name":        "Nom affiché",
    "search_text": "mots clés vinted",
    "price_to":    50,          # prix max en euros
    "category":    "vetements", # ou "pokemon"
},
```
