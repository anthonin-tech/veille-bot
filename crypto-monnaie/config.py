import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", "0"))

if not DISCORD_BOT_TOKEN:
    raise ValueError("Discord token manquant")

if DISCORD_CHANNEL_ID == 0:
    raise ValueError("Discord id manquant")

EMOJI_LIKE = "👍"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SOURCES_RSS = [
    "https://blog.langchain.dev/rss/",
    "https://simonwillison.net/atom/everything/",
    "https://huggingface.co/blog/feed.xml",
    "https://korben.info/feed",
    "https://www.lemondeinformatique.fr/flux-rss-1.xml",
]

MOTS_CLES = [
    "agent",
    "agentic",
    "llm",
    "tool use",
    "planning",
    "multi-agent",
    "autonomous",
    "workflow",
    "automation",
    "agent ia", 
    "automatisation", 
    "intelligence artificielle",
    "modèle de langage", 
    "flux de travail", 
    "autonome",
]

INTERVALLE_VEILLE = 3600

FICHIER_ARTICLES_VUS = os.path.join(BASE_DIR, "data", "articles_vus.json")
FICHIER_LIKES = os.path.join(BASE_DIR, "data", "likes.json")


