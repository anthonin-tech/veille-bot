import requests
from config import MOTS_CLES

def pre_filtre_mots_cles(article: dict) -> bool:
    texte = (article.get("titre", "") + " " + article.get("resume", "")).lower()
    return any(mot.lower() in texte for mot in MOTS_CLES)

def filtrer_par_mots_cles(articles: list[dict]) -> list[dict]:
    candidats = []
    for a in articles:
        if pre_filtre_mots_cles(a):
            candidats.append(a)

    print(f"Filtre mots-clés: {len(candidats)}/{len(articles)} articles retenus")
    return candidats

def appeler_ollama(prompt: str, max_tokens: int = 10) -> str:
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0,
                    "num_predict": max_tokens
                }
            },
            timeout=60
        )

        response.raise_for_status()
        return response.json()["response"].strip()

    except requests.Timeout:
        print("Ollama: timeout")
        return ""

    except requests.ConnectionError:
        print("Ollama: impossible de se connecter")
        return ""

    except Exception as e:
        print(f"Ollama: erreur : {e}")
        return ""

def est_pertinent_llm(article: dict) -> bool:
    print(f"🤖 Analyse : {article['titre'][:60]}...")
    prompt = f"""Tu es un assistant de veille technologique francophone.
Dis-moi si cet article est pertinent pour quelqu'un qui s'intéresse
à l'optimisation des agents IA pour des usages quotidiens.
Titre : {article['titre']}
Résumé : {article['resume'][:300]}

Réponds UNIQUEMENT par OUI ou NON, sans explication."""

    reponse = appeler_ollama(prompt, max_tokens=10)
    return reponse.upper().startswith("OUI")

def generer_resume(article: dict) -> str:
    prompt = f"""Résume en français cet article en 2 phrases maximum.
Commence directement par l'information clé. Sois factuel et concis.

Titre : {article['titre']}
Résumé original : {article['resume'][:400]}"""

    resume = appeler_ollama(prompt, max_tokens=150)
    return resume if resume else article.get("resume", "")[:200]

def filtrer_et_enrichir(articles: list[dict], utiliser_llm: bool = True) -> list[dict]:
    candidats = filtrer_par_mots_cles(articles)

    if not utiliser_llm:
        return candidats

    articles_pertinents = []

    for article in candidats:
        if est_pertinent_llm(article):
            article["resume_llm"] = generer_resume(article)
            articles_pertinents.append(article)

    return articles_pertinents
