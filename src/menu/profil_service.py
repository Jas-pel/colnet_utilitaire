# Contient les fonctions liées au profil
from src.core.user import User
from src.core.session import Session
from src.storage.pickle import load_lst_user_pickle, enregistrer_pickle, dump_lst_user_pickle
from src.affichage.affichage import choisir_element_liste, afficher_contenu_liste
from src.menu.creer_profil import creer_profil, actualiser_session


def choisir_profil() -> User:
    """
    Retourne un objet user deja existant, ou en creer un et le retourne.
    """
    lst_user = load_lst_user_pickle()

    while True:
    
        if lst_user: 
            profil = input("As-tu déjà un profil (oui ou non) : ").lower()
        else: profil = "non"

        if profil == "oui": 
            return choisir_element_liste(lst_user, "Sélectionne ton profil", "get_nom")
        elif profil == "non": 
            user = creer_profil()
            enregistrer_pickle(user)
            return user
        else : print("Entre une information valide !")


def supprimer_profil() :
    """
    Permet de supprimer un profil user venant du pickle.
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


def choisir_session(user:User) -> Session :
    """
    Affiche les sessions de l'utilisateur.
    Retourne la session qu'il choisit. 
    """
    return choisir_element_liste(user.get_lst_session(), "Sélectionne la session", "get_nom_session")


def actualiser_profil(user) :
    """
    Actualise le profil et l'enregistre sur pickle
    """
    actualiser_session(user, choisir_session(user))
    enregistrer_pickle(user)