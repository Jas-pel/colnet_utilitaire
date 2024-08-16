# Ce fichier contient les fonctions en lien avec l'affichage d'informations
from colorama import Fore, Style
from tabulate import tabulate


def choisir_element_liste(liste: list, titre: str, methode=None, nb_element=0) -> None:
    """
    Affiche les éléments d'une liste avec un titre et retourne l'élément choisi par l'utilisateur.
    """
    afficher_contenu_liste(liste, titre, methode)
    while True:
        index = int(input(f"{Fore.GREEN}\nEntre le chiffre correspondant à l'élément{' (#' + str(nb_element) + ')' if nb_element else ''} que tu veux choisir : {Style.RESET_ALL}")) - 1
        if 0 <= index < len(liste): return liste[index]
        print(Fore.RED + "L'index n'existe pas !" + Style.RESET_ALL)


def afficher_contenu_liste(liste: list, titre: str, methode=None) -> None:
    """
    Affiche les éléments d'une liste avec un titre, en utilisant une méthode spécifique si fournie.
    """
    print(f"{Fore.BLUE}\n\n{titre.upper()}\n{Style.RESET_ALL}{'-' * 60}")
    for i, element in enumerate(liste, start=1):
        if methode is not None:
            if hasattr(element, methode): print(f"{i}) {getattr(element, methode)()}")
            else: print(f"{i}) {element}")
        else: print(f"{i}) {element}")


def afficher_main() :
    """
    Affiche les options du main à l'utilisateur.
    Retourne le choix de l'utilisateur
    """
    main = [
    "Afficher moyenne général",
    "Afficher moyenne de classe et de groupe",
    "Afficher historiques des moyennes général",
    "Actualiser le profil",
    "Modifier mon profil",
    "Supprimer un profil",
    "Écrire à quelqu'un",
    "Quitter"
    ]
    afficher_contenu_liste(main, f"Choisit une option !")
    return int(input((Fore.GREEN + "\nEntre le chiffre correspondant à ce que tu veux faire : " + Style.RESET_ALL)))


def afficher_tableau(lst_objet_cours : object) -> object:
    """
    Créer un tableau contenant les moyennes de la classe et de l'utilisateur et l'affiche.
    """
    table_data = []
    for cours in lst_objet_cours:        
        if (moyenne_classe := cours.get_moyenne_classe()) == 0: moyenne_classe, ecart = "inconnu", "inconnu"
        else : 
            ecart = round(cours.get_moyenne() - moyenne_classe, 2)
            ecart =  f"{Fore.RED}{str(ecart)}{Fore.RESET}" if ecart <= 0 else f"{Fore.GREEN}{str(ecart)}{Fore.RESET}"
        table_data.append([(cours.get_nom()), cours.get_moyenne(), moyenne_classe, ecart, cours.get_note_total_str()])
    headers = ["Cours", "Moyenne (%)", "Moyenne de la classe(%)", "Écart entre les moyennes(%)", "Points accumulés"]
    return tabulate(table_data, headers=headers, tablefmt="grid", colalign=("left", "left", "left", "left", "left"))