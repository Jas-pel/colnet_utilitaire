# Fonctions liées à la gestion des fichiers pickle
import pickle
from core.user import User


def load_lst_user_pickle() -> list[User] | list:
    """ 
    Retourne la liste d'objet user du pickle.
    Si il y a aucun user retourne une liste vide.
    """
    with open("data_base_user.pickle", 'rb') as fichier:
        try: lst_user = pickle.load(fichier)
        except EOFError: lst_user = []
    return lst_user


def dump_lst_user_pickle(lst_user:list[User]):
    """ 
    Enregistre la liste d'objet user dans le pickle.
    """
    with open("data_base_user.pickle", 'wb') as fichier:
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