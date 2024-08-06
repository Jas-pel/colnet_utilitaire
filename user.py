class User:
    """Représente un utilisateur."""

    def __init__(self, nom: str, da: int, password: str):
        """ Initialise un nouvel utilisateur avec un nom, un identifiant et un mot de passe. """
        self.__nom = nom
        self.__da = da
        self.__password = password
        self.__lst_session = []

    def get_nom(self) -> str:
        """ Renvoie le nom de l'utilisateur. """
        return self.__nom
    
    def get_da(self) -> int:
        """ Renvoie le DA de l'utilisateur. """
        return self.__da
    
    def set_da(self, da: int) -> None:
        """ Modifie le DA de l'utilisateur. """
        self.__da = da
    
    def get_password(self) -> str:
        """ Renvoie le mot de passe de l'utilisateur. """
        return self.__password
    
    def set_password(self, password: str) -> None:
        """ Modifie le mot de passe de l'utilisateur. """
        self.__password = password    

    def get_lst_session(self) -> list[object]:
        """Renvoie la liste des sessions de l'utilisateur."""
        return self.__lst_session
    
    def ajouter_session(self, session:object) -> None:
        """
        Ajoute une session à la liste des sessions de l'utilisateur.
        Si la session existe déjà pour l'utilisateur, elle est d'abord supprimée avant d'être ajoutée.
        """
        if session in self.get_lst_session():
            self.__lst_session.remove(session)
        self.__lst_session.append(session)
    
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
        return isinstance(other, User) and self.__nom == other.__nom