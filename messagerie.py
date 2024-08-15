# Ce fichier contient des fonctions en lien avec la messagerie de colnet
from user import User
from colnet import Colnet

def automatically_find_target_information(bot):
    """ 
    Permet de trouver les informations de la cible grâce au nom.
    Retourne la liste des informations pour contacter la cible.
    """
    while True:
        target_name = input("Entre le prénom de la personne comme ceci 'Pelletier, jasmin' : ").lower().strip().replace(" ", "")

        # Parcourir chaque session
        nb_sessions = len(bot.obtenir_objet_html_session())
        for session_index in range(nb_sessions):
            session = bot.obtenir_objet_html_session()[session_index]
            session_test = session.text
            session.click()

            # Parcourir chaque catégorie
            nb_categories = len(bot.obtenir_categorie_personne_message())
            for category_index in range(nb_categories):
                category = bot.obtenir_categorie_personne_message()[category_index]
                category_text = category.text
                category.click()

                # Parcourir chaque cours
                if category_text == "Mes camarades":
                    nb_cours = len(bot.obtenir_objet_html_cours_message())
                    for course_index in range(nb_cours):
                        cours = bot.obtenir_objet_html_cours_message()[course_index]
                        cours_text = cours.text
                        cours.click()

                        # Parcourir chaque personne
                        personnes = bot.obtenir_info_nom_message()[2:]
                        for person_index, person in enumerate(personnes):
                            person_text = person.text
                            print(person.text.lower())
                            if target_name in person.text.lower().strip().replace(" ", ""): 
                                confirmation = input(f"\nConfirmez-vous ce profil ?\nNom : {person_text}\nCatégorie : {category_text}\nSession : {session_test}\nCours : {cours_text}\nEntrez 'oui' ou 'non' : ").lower()
                                if confirmation == "oui":
                                    print(f"\nInformations sélectionnées : Session - {session_index}, Catégorie - {category_index}, Cours - {course_index}, Personne - {person_index}")
                                    return [session_index, category_index, course_index, person_index]
                            
                else:
                    # Parcourir chaque personne
                    personnes = bot.obtenir_info_nom_message()[2:]
                    for person_index, person in enumerate(personnes):
                        person_text = person.text
                        print(person.text.lower())
                        if target_name in person.text.lower().strip().replace(" ", ""): 
                            confirmation = input(f"\nConfirmez-vous ce profil ?\nNom : {person_text}\nCatégorie : {category_text}\nSession : {session_test}\nCours : {cours_text}\nEntrez 'oui' ou 'non' : ").lower()
                            if confirmation == "oui":
                                print(f"\nInformations sélectionnées : Session - {session_index}, Catégorie - {category_index}, Cours - {course_index}, Personne - {person_index}")
                                return [session_index, category_index, -1, person_index]

    
def manually_find_target_information(bot) -> list[int, int, int, int]:
    """ 
    Permet de trouver les informations de la cible de manière manuelle.
    Retourne la liste des informations pour contacter la cible.
    """
    while True:
        try:
            # Choisir la session
            sessions = bot.obtenir_objet_html_session()
            for i, session in enumerate(sessions):
                print(f"{i} : {session.text}")
            choix_session = int(input("Entrez le numéro correspondant à votre choix de session : "))
            selected_session = sessions[choix_session].text
            sessions[choix_session].click()

            # Choisir la catégorie
            categories = bot.obtenir_categorie_personne_message()
            for i, categorie in enumerate(categories):
                print(f"{i} : {categorie.text}")
            choix_categorie = int(input("Entrez le numéro correspondant à votre choix de catégorie : "))
            selected_categorie = categories[choix_categorie].text
            categories[choix_categorie].click()
            
            # Choisir le cours (if applicable)
            choix_cours = None
            if selected_categorie == "Mes camarades":
                courses = bot.obtenir_objet_html_cours_message()
                for i, cours in enumerate(courses):
                    print(f"{i} : {cours.text}")
                choix_cours = int(input("Entrez le numéro correspondant à votre choix de cours : "))
                selected_cours = courses[choix_cours].text
                courses[choix_cours].click()                
            else:
                selected_cours = "N/A"

            # Choisir la personne
            personnes = bot.obtenir_info_nom_message()[2:]  # Enlever les deux premiers éléments inutiles
            for i, personne in enumerate(personnes):
                print(f"{i} : {personne.text}")
            choix_personne = int(input("Entrez le numéro correspondant à votre choix de personne : "))
            selected_personne = personnes[choix_personne].text

            # Confirmer le profil
            confirmation = input(f"\nConfirmez-vous ce profil ?\nNom : {selected_personne}\nCatégorie : {selected_categorie}\nSession : {selected_session}\nCours : {selected_cours}\nEntrez 'oui' ou 'non' : ").lower()
            if confirmation == "oui":
                print(f"\nInformations sélectionnées : Session - {choix_session}, Catégorie - {choix_categorie}, Cours - {choix_cours}, Personne - {choix_personne}")
                break
            
        except (IndexError, ValueError):
            print("Choix invalide. Veuillez entrer un nombre valide correspondant aux options affichées.\n")

    return [choix_session, choix_categorie, choix_cours, choix_personne]
 

def send_message(
    user: User, 
    message: str = "Yo", 
    object: str = "Test", 
    number_of_message: int = 1, 
    target_information: list[int, int, int, int] = [],
    search_manually: bool = True
):
    """
    Permet d'envoyer un ou des messages à quelqu'un sur Colnet.

    Parameters:
    user (User): Instance de la classe User contenant les informations de l'utilisateur.
    message (str): Le message à envoyer. Default: "Yo".
    object (str): L'objet du message. Default: "You have b33n h@ck3d!".
    number_of_message (int): Le nombre de messages à envoyer. Default: 1.
    target_information (list[int, int, int, int]): Informations sur la cible [session, catégorie, cours, personne]. Default: [1, 1, 7, 4].
    search_manually (bool): Indique si la recherche des informations de la cible doit être effectuée manuellement. Default: True.
    """
    
    with Colnet() as bot:
        bot.open_colnet()
        bot.se_connecter(user.get_da(), user.get_password())

        for i in range(number_of_message):
            # Naviguer vers le menu courriels
            bot.cliquer_options_dossier("Courriels")
            bot.click_on_button("btnNouvMess15")  # Nouveau message
            bot.click_on_button("btnA5")  # Sélectionner le destinataire
            bot.switch_to_new_window() 

            # Trouver les informations de la cible
            if not target_information:
                if search_manually:
                    target_information = manually_find_target_information(bot)
                else:
                    target_information = automatically_find_target_information(bot)
            session, categorie, cours, personne = target_information

            # Sélectionner le profil de la cible
            bot.obtenir_objet_html_session()[session].click()
            bot.obtenir_categorie_personne_message()[categorie].click()
            bot.obtenir_objet_html_cours_message()[cours].click()
            table_rows = bot.obtenir_info_nom_message()[2:]
            bot.selectionner_checkbox_message(table_rows[personne])
            bot.click_on_button("btnSelB5")  # Confirmer le destinataire

            # Envoyer le message
            bot.switch_to_new_window() 
            bot.ecrire_objet(object)  # Écrire l'objet
            bot.ecrire_message(message)  # Écrire le message
            bot.click_on_button("btnEnvoyer5")  # Envoyer le message

            # Afficher confirmation
            print(f"Message {i+1} envoyé avec succès.")