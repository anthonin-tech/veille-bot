import discord
import re
from config import DISCORD_BOT_TOKEN, DISCORD_CHANNEL_ID, EMOJI_LIKE
from stockage import sauvegarder_like, charger_likes, compter_likes

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot connecté en tant que {client.user}")
    print(f"Channel ID: {DISCORD_CHANNEL_ID}")
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="la veille IA 🔍"
        )
    )

@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    if str(payload.emoji) != EMOJI_LIKE:
        return

    if payload.user_id == client.user.id:
        return

    if payload.channel_id != DISCORD_CHANNEL_ID:
        return

    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    lien_match = re.search(r'https?://\S+', message.content)

    if not lien_match:
        await channel.send("Aucun lien trouvé dans ce message", delete_after=10)
        return

    lien = lien_match.group()

    sauvegarder_like(message.content, lien)
    await channel.send(
        f"Article sauvegardé ! ({compter_likes()} articles dans ta liste)\n"
        f"Tape `!likes` pour voir tes derniers articles.",
        delete_after=10
    )

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    if message.content.lower() == "!likes":
        derniers_likes = charger_likes(nombre=10)

        if not derniers_likes:
            await message.channel.send("Tu n'as pas encore liké d'articles")
            return

        lignes = [f"**Tes {len(derniers_likes)} derniers articles likés :**\n"]

        for i, like in enumerate(reversed(derniers_likes), start=1):
            lignes.append(f"{i}. {like['lien']}\n   _{like['date_like']}_")

        await message.channel.send("\n".join(lignes))

    elif message.content.lower() == "!stats":
        total = compter_likes()

        await message.channel.send(
            f"📊 **Statistiques de ta veille :**\n"
            f"→ Articles likés au total : **{total}**\n"
            f"→ Tape `!likes` pour voir les derniers."
        )

    elif message.content.lower() in ["!aide", "!help"]:
        aide = (
            "**Commandes disponibles :**\n"
            "→ Réagis avec 👍 sur un article pour le sauvegarder\n"
            "→ `!likes` — Voir tes 5 derniers articles sauvegardés\n"
            "→ `!stats` — Voir tes statistiques\n"
        )
        await message.channel.send(aide)

async def envoyer_article(article: dict):
    channel = client.get_channel(DISCORD_CHANNEL_ID)
    if channel is None:
        print("Channel introuvable")
        return

    resume = article.get("resume_llm") or article.get("resume", "")[:200]

    message = (
        f"📰 **{article['titre']}**\n"
        f"_{article.get('source', '')} — {article.get('date', '')}_\n\n"
        f"{resume}\n\n"
        f"🔗 {article['lien']}\n"
        f"{'─' * 40}"
    )

    await channel.send(message)
