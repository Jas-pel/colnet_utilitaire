# Contient la classe permettant d'automatiser la collecte d'informations
# Import seulement des packages en lien avec l'automatisation
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
import os


class Colnet(webdriver.Chrome):
    def __init__(self, driver_path="C:\\Kingston\\Programmation\\JAsmin\\Lib\\site-packages\\selenium\\webdriver"):
        self.driver_path = driver_path
        os.environ["PATH"] += self.driver_path
        super(Colnet, self).__init__()
        self.maximize_window()

    def wait_until(self, condition, timeout=10):
        """ Utilitaire pour attendre une condition. """
        return WebDriverWait(self, timeout).until(condition)

    def open_colnet(self):
        """ Ouvre Colnet. """
        self.get("https://enligne.cegepjonquiere.ca/colnet/login.asp?NoRegr=1")

    def se_connecter(self, da, password):
        """ Connecte l'utilisateur en utilisant son DA et son mot de passe. """
        username_field = self.wait_until(EC.presence_of_element_located((By.ID, "txtCodeUsager")))
        password_field = self.wait_until(EC.presence_of_element_located((By.ID, "txtMotDePasse")))
        username_field.send_keys(da)
        password_field.send_keys(password)
        self.click_on_button("btnConnecter")

    def cliquer_options_dossier(self, nom_option):
        """ Clique sur l'onglet spécifié dans le système en ligne. """
        element = self.wait_until(EC.presence_of_element_located((By.CSS_SELECTOR, f'a[title="{nom_option}"]')))
        element.click()

    def cliquer_session(self, code_session):
        """ Clique sur la session selon le code de la session choisie. """
        element = self.wait_until(EC.presence_of_element_located((By.CSS_SELECTOR, f'option[value="{code_session}"]')))
        element.click()

    def cliquer_evaluation(self):
        """ Clique sur l'onglet 'Évaluations' dans le système en ligne. """
        evaluation_button = self.wait_until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Évaluations']")))
        evaluation_button.click()

    def cliquer_cours(self, code_cours):
        """ Clique sur le cours demandé dans le système en ligne. """
        element = self.wait_until(EC.presence_of_element_located((By.CSS_SELECTOR, f'option[value="{code_cours}"]')))
        element.click()

    def obtenir_categorie_personne_message(self):
        """ Utili dans spam. Retourne les différents objets html avec id : ongPersonnes"""
        return self.wait_until(EC.presence_of_all_elements_located((By.ID, "ongPersonnes")))

    def obtenir_objet_html_cours(self) -> list:
        """ Retourne une liste des objets HTML des cours. """
        dropdown_element_session = self.wait_until(EC.presence_of_element_located((By.ID, "cboCours")))
        dropdown = Select(dropdown_element_session)
        return dropdown.options
    
    def obtenir_objet_html_cours_message(self) -> list: # TODO
        """ Retourne une liste des objets HTML des cours. """
        dropdown_element_session = self.wait_until(EC.presence_of_element_located((By.ID, "cboCam")))
        dropdown = Select(dropdown_element_session)
        return dropdown.options

    def obtenir_objet_html_session(self) -> list:
        """ Retourne une liste des objets HTML des sessions. """
        dropdown_element_session = self.wait_until(EC.presence_of_element_located((By.ID, "cboAnneeSession")))
        dropdown = Select(dropdown_element_session) # Sélecte isole les sessions, possible de l'utiliser car objet select dans le code html
        return dropdown.options # Retourne une liste des options

    def obtenir_td_b_elements(self) -> list:
        """
        "td b" est le sélecteur CSS.
        Cible tous les éléments <b> se trouvant à l'intérieur des éléments <td>.
        """
        td_b_elements = self.wait_until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td b")))
        return td_b_elements

    def obtenir_row_tableau(self) -> list:
        """
        Retourne toutes les rangées d'un tableau contenant des notes.
        Doit être appelé dans un cours contenant des notes.
        """
        # NOTE : Pour l'instant seul les trois dernières informations m'intéresse, possible de changer cela.
        tbody = self.wait_until(EC.presence_of_all_elements_located((By.CLASS_NAME, "BlueTableau")))[1]

        # Sélectionner toutes les lignes à partir de la 1ère (exclure l'en-tête s'il y en a un)
        lst_tr = tbody.find_elements(By.XPATH, ".//tr[position() > 1]")
        lst_rows = []
        for tr in lst_tr: 
            lst_rows.append([item.text for item in tr.find_elements(By.XPATH, ".//td[position() > last()-2]")])
        return lst_rows

    def cours_in_session(self) -> bool:
        """ Vérifie s'il y a des cours dans le code HTML de la session. """
        test = self.find_elements(By.CSS_SELECTOR, "div.Panel")[0].text
        if "Aucun cours pour la session" in test: return False
        return True

    def switch_to_new_window(self):
        """ Basculer vers la nouvelle fenêtre ou onglet ouvert. """
        # Récupérer les identifiants de toutes les fenêtres actuellement ouvertes
        all_windows = self.window_handles

        # Regarde si il a juste une fenêtre
        if len(all_windows) == 1:
            self.switch_to.window(all_windows[0])

        # Changer le focus vers la nouvelle fenêtre
        else : 
            for window in all_windows:
                if window != self.current_window_handle:
                    self.switch_to.window(window)
                    break  # Sortie de la boucle une fois que nous avons changé de fenêtre

    def obtenir_info_nom_message(self):
        """ Retourne chaque rangés. """
        return self.wait_until(EC.presence_of_all_elements_located((By.XPATH, "//table[@class='BlueTableau']/tbody/tr")))
    
    def selectionner_checkbox_message(self, row):
        """ Clique sur la checkbox. """
        checkbox = row.find_element(By.XPATH, "./td/input[@type='checkbox']")
        checkbox.click()

    def ecrire_objet(self, objet):
        """ Écrit l'objet reçus. """
        input_text = self.wait_until(EC.presence_of_element_located((By.ID, "txtObjet")))
        input_text.send_keys(objet)

    def ecrire_message(self, message):
        """ Écrit le message reçus. """
        input_text = self.wait_until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[title='Éditeur de texte enrichi, txtMess']")))
        input_text.send_keys(message)

    def click_on_button(self, id):
        """ Clique sur l'id du button à l'aide du by id. """
        self.wait_until(EC.presence_of_element_located((By.ID, id))).click()


