# Ce fichier contient des fonctions permettant d'aller chercher de l'informations aux niveaux académique de l'utilisateur
from core.user import User
from core.cours import Cours
from core.session import Session
from scrapping.colnet import Colnet
from scrapping.analyse_scrapping import obtenir_note_total, separer_note_total, filtrer_range_pour_moyenne_classe, calculer_moyenne_classe


def obtenir_liste_objet_cours(bot) -> list[Cours]: # NOTE : À optimiser
    """
    Pour que le code fonctionne correctement, être dans évaluation.
    Retourne une liste d'objet cours
    """
    # Itérer à travers les cours
    there_is_cours = True
    cours = 0
    lst_objet_cours = []
    while there_is_cours:
        # Obtenir les informations sur les cours et cliquer dessus
        try:
            cours_html = bot.obtenir_objet_html_cours()[cours]
            cours +=1
        except IndexError: 
            there_is_cours = False # Signifie qu'il n'y a plus de cours dans le menu déroulant
            continue
        code_cours = cours_html.get_attribute("value")
        nom_cours = cours_html.text

        # Vérifie si le cours contient des résultats à l'aide de la première lettre du code.
        if not nom_cours[0].isdigit(): continue

        # Créer un objet, l'ajoute à une liste et clique sur le cours.
        objet_cours = Cours(nom_cours, code_cours) # Créer un objet Cours
        lst_objet_cours.append(objet_cours)  
        bot.cliquer_cours(code_cours)

        # Obtenir la moyenne de l'user et de la classe
        note_total = obtenir_note_total(bot.obtenir_td_b_elements())
        moyenne_classe_ponderation = filtrer_range_pour_moyenne_classe(bot.obtenir_row_tableau())

        # NOTE : Ajoute des informations à l'objet cours
        objet_cours.set_note_total_str(note_total) # Ajoute la note sous forme de string à l'objet
        objet_cours.set_moyenne(*separer_note_total(note_total)) # Ajoute la moyenne à l'objet
        if moyenne_classe_ponderation: 
            objet_cours.set_moyenne_classe(calculer_moyenne_classe(moyenne_classe_ponderation)) 

    return lst_objet_cours

    

def creer_profil() -> User: # NOTE : Peut-être à optimiser
    """
    Créer un objet User à partir des informations de Colnet.

    Demande le nom, le DA (numéro d'étudiant) et le mot de passe de l'utilisateur pour créer un objet User.
    Puis, utilise les fonctions de scrapping pour récupérer les informations de session.
    
    Returns:
        User: Un objet User rempli avec les informations de session.
    """

    # Demander les informations de l'utilisateur
    nom = input("Entrez votre nom : ")
    da = int(input("Entrez votre DA : "))
    mot_de_passe = input("Entrez votre mot de passe : ")
    user = User(nom, da, mot_de_passe)

    # Collecter les données
    with Colnet() as bot: 
        bot.open_colnet()
        bot.se_connecter(da, mot_de_passe)
        bot.cliquer_options_dossier("Cours")

        # Itérer à travers les sessions
        there_is_session = True
        session = 0
        click_on_evaluation = True
        while there_is_session :

            # Obtenir les informations sur la session et cliquer dessus
            try:
                session_html = bot.obtenir_objet_html_session()[session]
                session +=1
            except IndexError : 
                there_is_session = False # Signifie qu'il n'y a plus de session dans le menu déroulant
                continue
            code_session = session_html.get_attribute("value")
            nom_session = session_html.text
            session_html.click()
            
            # Vérifie s'il y a des cours dans la session, par exemple, pas de cours en automne 2022. Permet de gagner du temps. 
            if not bot.cours_in_session(): continue
            objet_session = Session(nom_session, code_session) # Créer un objet Session

            # Clique juste une fois sur évaluation, permet de gagner quelques secondes
            if click_on_evaluation :
                bot.cliquer_evaluation()
                click_on_evaluation = False

            # Créer une liste d'objets cours avec informations
            lst_objet_cours = obtenir_liste_objet_cours(bot)

            # NOTE : Ajoute des informations à l'objet session
            objet_session.ajouter_lst_cours(lst_objet_cours)
            objet_session.set_historique_moyenne_general(float(objet_session.get_moyenne_generale()))

            # NOTE : Ajoute des informations à l'objet user
            user.ajouter_session(objet_session)  
   
    return user



def actualiser_session(user:User, objet_session:Session):
    """ Permet d'actualiser une session """

    with Colnet() as bot:
        bot.open_colnet()
        bot.se_connecter(user.get_da(), user.get_password())
        bot.cliquer_options_dossier("Cours")
        bot.cliquer_session(objet_session.get_code_matiere())
        bot.cliquer_evaluation()

        # Créer une liste d'objets cours ; un objet cours contient le nom du cours, la note de l'user, la note de sa classe...
        lst_objet_cours = obtenir_liste_objet_cours(bot) 

    # NOTE : Ajoute des informations à l'objet session
    objet_session.ajouter_lst_cours(lst_objet_cours)
    objet_session.set_historique_moyenne_general(float(objet_session.get_moyenne_generale()))

    # NOTE : Ajoute des informations à l'objet user
    user.ajouter_session(objet_session)