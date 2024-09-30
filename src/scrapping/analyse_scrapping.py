# Fichier contenant les fonctions d'analyses
# Nécessite pas de driver
import re

def separer_note_total(note_total:str) -> tuple[float, float]:
    """
    Reçois un string du type "90,16/99,34".
    Sépare la note totale en note et total.
    """
    note_total = note_total.replace(",", ".")
    note, total =  note_total.split('/')
    return float(note), float(total)


def obtenir_note_total(td_b_elements) -> str:
    """
    Retourne la note total de l'utilisateur.
    Dans le format suivant -> 12,15/40,18.
    """
    for td in td_b_elements:
        texte = td.text
        # Il existe deux cas différents répertoriées
        if re.search(r'Note final', texte):
            points_accumulées = re.search(r'\d+,\d+|\d+', texte)
            note_total = f"{points_accumulées.group()},00/100,00"
            break
        
        if re.search(r'Nombre de points accumulés à ce jour', texte):
            match = re.search(r'(\d+,\d{2}) / (\d+,\d{2})', texte)  #HACK
            note_total = match.group()
    return note_total


def filtrer_range_pour_moyenne_classe(lst_rows) -> dict:
    """
    Reçois toutes les rangées du tableau.
    Retourne un dictionnaire contenant les notes et les pondérations pour calculer la moyenne général.
    """
    moyenne_classe_ponderation = {}
    note = total = ponderation = None
    for row in lst_rows:
        note_total = row[-2]
        if note_total.strip() != "": # Cela arrive si la moyenne des élèves n'est pas là
            note, total = separer_note_total(note_total)

        note_ponderation = row[-1]
        if "/" not in note_ponderation : # cela arrive si il a seulement la pondération
            note_ponderation = "1/" + note_ponderation 
        _, ponderation = separer_note_total(note_ponderation)

        if note != None and total != None and ponderation != None:
            cle = note / total
            if cle in moyenne_classe_ponderation: moyenne_classe_ponderation[cle] = moyenne_classe_ponderation[cle] + ponderation
            else: moyenne_classe_ponderation[cle] = ponderation   
    return moyenne_classe_ponderation



def calculer_moyenne_classe(dictionnaire_notes) -> float:
    """
    Calcule la moyenne de classe pondérée.
    """
    somme_produits = 0
    somme_ponderations = 0
    for note, ponderation in dictionnaire_notes.items():
        somme_produits += note * ponderation
        somme_ponderations += ponderation
    moyenne_ponderee = round(somme_produits / somme_ponderations * 100, 2)
    return moyenne_ponderee

