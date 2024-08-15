from datetime import datetime

class Session:
    """ 
    Classe représentant une session.
    
    Attributes:
        nom_session (str): Le nom de la session.
        code_matiere (str): Le code de la matière de la session.
        lst_cours (list): Liste des cours suivis dans cette session.
        historique_moyenne_generale (list): Historique des moyennes générales de l'utilisateur.
    """
    
    def __init__(self, nom_session: str, code_matiere: str): 
        """
        Initialise un objet Session avec son nom et son code de matière.
        
        Args:
            nom_session (str): Le nom de la session.
            code_matiere (str): Le code de la matière de la session.
        """
        self.__nom_session = nom_session
        self.__code_matiere = code_matiere
        self.__lst_cours = []
        self.__hisorique_moyenne_general = []

    def ajouter_lst_cours(self, lst_cours : list[object]):
        """
        Ajoute des cours à une session.
        Si le cours existe déjà pour l'utilisateur, il  est d'abord supprimée avant d'être ajoutée.
        """
        lst_anciens_cours = self.get_lst_cours()
        for cours in lst_cours:
            if cours in lst_anciens_cours:
                self.__lst_cours.remove(cours)
            self.__lst_cours.append(cours)

    def get_moyenne_generale(self) -> str:
        """ Calcule et retourne la moyenne générale des cours suivis par l'utilisateur. """
        return round(sum(cours.get_moyenne() for cours in self.__lst_cours) / len(self.__lst_cours), 2)

    
    def get_lst_cours(self) -> list[object]:
        """ Renvoie la liste des cours suivis dans cette session. """
        return self.__lst_cours
    
    def set_historique_moyenne_general(self, moyenne: float) -> None:
        """ Ajoute la moyenne générale à l'historique de l'utilisateur. """
        self.__hisorique_moyenne_general.append(f"{str(round(moyenne, 2))}% ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")

    def get_historique_moyenne_general(self) -> list:
        """ Renvoie l'historique des moyennes générales de l'utilisateur."""
        return self.__hisorique_moyenne_general

    def get_code_matiere(self) -> str:
        """ Renvoie le code de la matière de la session. """
        return self.__code_matiere
    
    def get_nom_session(self) -> str:
        """ Renvoie le nom de la session. """
        return self.__nom_session
