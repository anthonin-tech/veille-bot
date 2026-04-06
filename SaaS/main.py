import asyncio
from config import MOTS_CLES, SOURCES_RSS, INTERVALLE_VEILLE, DISCORD_BOT_TOKEN
from collecteurs import tout_collecter
from filtres import filtrer_et_enrichir
from stockage import charger_articles_vus, sauvegarder_articles_vus
from bot_discord import client, envoyer_article

async def boucle_veille():
    await client.wait_until_ready()
    print("✅")
    articles_vus = charger_articles_vus()

    while True:
        print("\n" + "=" * 50)
        print("⏳ Nouvelle vérification en cours...")

        tous_les_articles = tout_collecter(SOURCES_RSS, MOTS_CLES)
        nouveaux = [a for a in tous_les_articles if a["lien"] not in articles_vus]
        print(f"{len(nouveaux)} nouveaux articles")

        if nouveaux:
            pertinents = filtrer_et_enrichir(nouveaux, utiliser_llm=True)

            for article in pertinents:
                await envoyer_article(article)
                await asyncio.sleep(2)

            for article in nouveaux:
                articles_vus.add(article["lien"])

            sauvegarder_articles_vus(articles_vus)

        else:
            print("Aucun nouvel article")

        await asyncio.sleep(INTERVALLE_VEILLE)

async def main():
    async with client:
        client.loop.create_task(boucle_veille())
        await client.start(DISCORD_BOT_TOKEN)

if __name__ == "__main__":
    print("Lancement du système de veille IA...")
    print(f"Sources configurées : {len(SOURCES_RSS)} flux RSS + Arxiv")
    print(f"Mots-clés surveillés : {', '.join(MOTS_CLES[:5])}...")

    asyncio.run(main())
