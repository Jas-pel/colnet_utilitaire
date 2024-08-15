class Cours:
    """ Créer un objet cours. """
    def __init__(self, nom_matiere, code_matiere): # Possibilité de faire un dictionnaire avec les deux premiers
        self.__nom = nom_matiere
        self.__code = code_matiere
        self.__moyenne_classe = 0
        self.__note_total_str = ""
    
    def get_nom(self) -> str:
        """ Retourne le nom de la matière. """
        return self.__nom
    
    def set_moyenne(self, note:float, total:float) -> float:
        """ Définis la moyenne du cours. """
        self.__note_cours = round(note/total*100, 2)

    def get_moyenne(self) -> float:
        """ Retourne la moyenne de la matière. """
        return self.__note_cours
    
    def set_moyenne_classe(self, moyenne_classe:float):
        """ Définis la moyenne de la classe. """
        self.__moyenne_classe = moyenne_classe

    def get_moyenne_classe(self) -> float:
        """ Retourne la moyenne de la classe. """
        return float(self.__moyenne_classe) 
    
    def set_note_total_str(self, note_total:str):
        """ Définis la moyenne de la classe. """
        self.__note_total_str = note_total.replace(",", ".")

    def get_note_total_str(self) -> str:
        """ Définis la moyenne de la classe. """
        return self.__note_total_str
    
    def get_code_cours(self) -> str:
        """ Retourne le code du cours. """
        return self.__code
    
    def __eq__(self, other):
        """ 
        Vérifie si deux utilisateurs sont égaux en comparant leurs noms.
        Example : 
            User 1 = User("Alice")
            User 2 = User("Alice")
            User 3 = User("Bob")
            User 1 == user 2 -> True
            User 1 == User 3 -> False
        """
        return isinstance(other, Cours) and self.get_code_cours() == other.get_code_cours()
