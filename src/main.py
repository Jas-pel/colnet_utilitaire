# Import
from affichage.affichage import afficher_contenu_liste, afficher_tableau, afficher_main
from menu.messagerie import send_message
from menu.profil_service import choisir_profil, actualiser_profil, modifier_profil, supprimer_profil, choisir_session
from colorama import Fore, Style
import os
import sys
sys.stderr = open(os.devnull, 'w')
 

# MAIN
if __name__ == "__main__":
    user = choisir_profil()
    while True:
        os.system('cls')
        match afficher_main():
            case 1 : 
                print(f"Ta moyenne générale total est de {choisir_session(user).get_moyenne_generale()}%")
            case 2 : 
                afficher_tableau(choisir_session(user).get_lst_cours())
            case 3 :
                afficher_contenu_liste(choisir_session(user).get_historique_moyenne_general(), "Voici l'historique des tes moyennes générales")
            case 4 : 
                actualiser_profil(user)
            case 5 :
                modifier_profil(user)
            case 6 : 
                supprimer_profil()
            case 7 : 
                send_message(user=user, message="Salut", object="Test", number_of_message=50, search_manually=False)
            case 8 : break

        _ = input(Fore.GREEN + "\nTapez une touche pour continuer" + Style.RESET_ALL)


# TODO
# Enlever les messages d'erreurs etranges
# Mettre plus de fonction dans colnet
# Gérer erreur de mot de passe
# Trouver la note finale plus rapidement
# Avoir une idée de combien de moyenne de groupe le programme a accès pour prédir la moyenne de classe. Bref un indice de confiance
# Il a un problème quand le total de point est plus que 100%, dans mon cas francais
# Pondéré moyenne générale