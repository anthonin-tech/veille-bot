import feedparser
import requests
from datetime import datetime

def formater_date(entry):
    if hasattr(entry, 'published_parsed') and entry.published_parsed:
        try:
            dt = datetime(*entry.published_parsed[:6])
            return dt.strftime("%Y-%m-%d %H:%M")

        except Exception:
            pass

    return datetime.now().strftime("%Y-%m-%d %H:%M")

def collecteur_rss(url: str) -> list[dict]:
    try:
        flux = feedparser.parse(url)
        articles = []

        for entry in flux.entries[:30]:
            article = {
                "titre": entry.get("title", "Sans titre"),
                "lien": entry.get("link", ""),
                "resume": entry.get("summary", "")[:500],
                "date": formater_date(entry),
                "source": url
            }

            if article["lien"]:
                articles.append(article)

        print(f"{len(articles)} article récupéré depuis {url}")
        return articles

    except Exception as e:
        print(f"Erreur sur {url} : {e}")
        return []

def collecter_arxiv(mots_cles: list[str], max_resultats: int = 10) -> list[dict]:
    requete = " OR ".join([f"ti:{mot}" for mot in mots_cles])
    params = {
        "search_query": requete,
        "start": 0,
        "max_results": max_resultats,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }

    try:
        response = requests.get(
            "http://export.arxiv.org/api/query",
            params=params,
            timeout=10
        )

        response.raise_for_status()
        flux = feedparser.parse(response.text)
        articles = []

        for entry in flux.entries:
            articles.append({
                "titre": entry.get("title", "").replace("\n", " ").strip(),
                "lien": entry.get("link", ""),
                "resume": entry.get("summary", "")[:500],
                "date": formater_date(entry),
                "source": "arxiv.org"
            })

        print(f"{len(articles)} article récupéré depuis Arxiv")
        return articles

    except requests.Timeout:
        print("Arxiv: timeout")
        return []

    except Exception as e:
        print(f"Arxiv: erreur inattendue : {e}")
        return []

def tout_collecter(sources_rss: list[str], mots_cles_arxiv: list[str]) -> list[dict]:
    tous_les_articles = []

    for url in sources_rss:
        articles = collecteur_rss(url)
        tous_les_articles.extend(articles)

    articles_arxiv = collecter_arxiv(mots_cles_arxiv)
    tous_les_articles.extend(articles_arxiv)

    print(f"\n Total collecté: {len(tous_les_articles)} articles")
    return tous_les_articles
