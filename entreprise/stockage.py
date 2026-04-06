import json
import os
from datetime import datetime
from config import FICHIER_ARTICLES_VUS, FICHIER_LIKES

def vérifier_dossier(chemin_fichier):
    dossier = os.path.dirname(chemin_fichier)

    if dossier and not os.path.exists(dossier):
        os.makedirs(dossier)

def lire_json(chemin_fichier, valeur_par_defaut):
    try:
        with open(chemin_fichier, "r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
        return valeur_par_defaut

    except json.JSONDecodeError:
        print(f"Fichier JSON corrompu : {chemin_fichier} - Remise à zéro")
        return valeur_par_defaut

def ecrire_json(chemin_fichier, donnees):
    vérifier_dossier(chemin_fichier)

    with open(chemin_fichier, "w", encoding="utf-8") as f:
        json.dump(donnees, f, ensure_ascii=False, indent=2)

def charger_articles_vus():
    liste = lire_json(FICHIER_ARTICLES_VUS, [])
    return set(liste)

def sauvegarder_articles_vus(articles_vus: set):
    ecrire_json(FICHIER_ARTICLES_VUS, list(articles_vus))

def sauvegarder_like(contenu_message: str, lien: str):
    likes = lire_json(FICHIER_LIKES, [])
    liens_existants = [like["lien"] for like in likes]

    if lien in liens_existants:
        print(f"Déjà dans les likes : {lien}")
        return

    nouveau_like = {
        "lien": lien,
        "apercu": contenu_message[:300],
        "date_like": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    likes.append(nouveau_like)
    ecrire_json(FICHIER_LIKES, likes)
    print("Ajouté au like")

def charger_likes(nombre: int = 5):
    likes = lire_json(FICHIER_LIKES, [])
    return likes[-nombre:]

def compter_likes():
    likes = lire_json(FICHIER_LIKES, [])
    return len(likes)
