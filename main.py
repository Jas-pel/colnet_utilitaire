# Import
from affichage import choisir_element_liste, afficher_contenu_liste, afficher_tableau
from colorama import Fore, Style
import pickle
from user import *
from session import Session
from creer_profil import creer_profil, actualiser_session
from messagerie import send_message
import os

 
# FONCTIONS
def load_lst_user_pickle() -> list[User]:
    """ Retourne la liste d'objet user du pickle """
    with open(PATH_PICKLE, 'rb') as fichier:
        try: lst_user = pickle.load(fichier)
        except EOFError: lst_user = [] # Si il n'y a pas de profil, créer une liste vide
    return lst_user


def dump_lst_user_pickle(lst_user):
    """ Enregistre la liste d'objet user dans le pickle """
    with open(PATH_PICKLE, 'wb') as fichier:
        pickle.dump(lst_user, fichier)


def enregistrer_pickle(user:User) :
    """ 
    Enregistre un objet user sur pickle.
    Si un user a le même nom, il sera remplacé.
    """
    lst_user = load_lst_user_pickle()

    if user in lst_user: lst_user.remove(user)
    lst_user.append(user)

    dump_lst_user_pickle(lst_user)
    print("Le profil a bien été actualisé")


def choisir_profil() -> User:
    """
    Charge le profil de l'utilisateur à partir d'un fichier pickle.
    """
    lst_user = load_lst_user_pickle()

    while True:
        # Demande à l'utilisateur de sélectionner un profil ou d'en créer un
        if lst_user: 
            profil = input("As-tu déjà un profil (oui ou non) : ").lower()
        else : profil = "non"

        # Effectue le choix
        if profil == "oui": 
            return choisir_element_liste(lst_user, "Sélectionne ton profil", "get_nom")
        elif profil == "non": 
            user = creer_profil()
            enregistrer_pickle(user)
            return user
        else : print("Entre une information valide !")


def supprimer_profil() :
    """
    Permet de supprimer un profil user venant du pickle
    """
    lst_user = load_lst_user_pickle()

    user = choisir_element_liste(lst_user, "Sélectionne ton profil", "get_nom")
    if user in lst_user: lst_user.remove(user)

    dump_lst_user_pickle(lst_user)
    print(f"Le profil - {user.get_nom()} - a bien été supprimer")


def modifier_profil(user:User) :
    """ 
    Permet à l'utilisateur de modifier son profil
    """
    while True :

        afficher_contenu_liste(["Mot de passe", "DA", "Retour menu principal"], "Sélectionne ce que tu veux modifier")
        choix = int(input("Entre ton choix : "))

        if choix == 1 : 
            user.set_password(str(input("Entre ton nouveau mot de passe : ")))
            enregistrer_pickle(user)
            break

        elif choix == 2 : 
            user.set_da(str(input("Entre ton nouveau DA : ")))
            enregistrer_pickle(user)
            break

        elif choix == 3:
            break
        
        else : print("Entre une information valide !")


def actualiser_profil(user) :
    """
    Actualise le profil et l'enregistre sur pickle
    """
    actualiser_session(user, choisir_session(user))
    enregistrer_pickle(user)


def choisir_session(user:User) -> Session :
    """
    Affiche les sessions de l'utilisateur.
    Retourne la session qu'il choisit. 
    """
    return choisir_element_liste(user.get_lst_session(), "Sélectionne la session", "get_nom_session")


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
    afficher_contenu_liste(main, f"Choisit une option {user.get_nom()}")
    return int(input((Fore.GREEN + "\nEntre le chiffre correspondant à ce que tu veux faire : " + Style.RESET_ALL)))



# MAIN
PATH_PICKLE = r"data_base_user.pickle"
if __name__ == "__main__":
    user = choisir_profil()
    while True:
        os.system('cls')
        match afficher_main():
            case 1 : 
                print(f"Ta moyenne générale total est de {choisir_session(user).get_moyenne_generale()}%")
                _ = input(Fore.GREEN + "\nTapez une touche pour continuer" + Style.RESET_ALL)
            case 2 : 
                print(afficher_tableau(choisir_session(user).get_lst_cours()))
                _ = input(Fore.GREEN + "\nTapez une touche pour continuer" + Style.RESET_ALL)
            case 3 :
                afficher_contenu_liste(choisir_session(user).get_historique_moyenne_general(), "Voici l'historique des tes moyennes générales")
                _ = input(Fore.GREEN + "\nTapez une touche pour continuer" + Style.RESET_ALL)
            case 4 : 
                actualiser_profil(user)
            case 5 :
                modifier_profil(user)
            case 6 : 
                supprimer_profil()
            case 7 : 
                send_message(user=user, number_of_message=10, search_manually=False)
            case 8 : break



# TODO
# Mettre plus de fonction dans colnet
# Regroupe fonction dans colnet
# Ajouter contact a user
# Gérer erreur de mot de passe
# Trouver le nom automatiquement
# Trouver la note finale plus rapidement
# Avoir une idée de combien de moyenne de groupe le programme a accès pour prédir la moyenne de classe. Bref un indice de confiance
# Il a un problème quand le total de point est plus que 100%, dans mon cas francais

# Pondéré moyenne générale
# Faire une fonction pour reset un pofil ou il est possible de conserver ce que l'on veux