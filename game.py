# TDL :
    # gestion erreurs avec logging

# TO GO FURTHER : 
    # Add User interace
    # Transform in app / exe

# Importations
from pathlib import Path 
import json 
import os
from datetime import datetime
from random import randint
import logging

BASE_DIR = Path(__file__).resolve().parent
SAVE_RESULTS = BASE_DIR / "game_last_scores.json"

# CLASS
class Character: 
    def __init__(self, name: str="default_name", _lifes: int=50, _damages_min: int=0, _damages_max: int=0, _nb_potions: int=0, _heal_min: int=0, _heal_max: int=0):
        self.name = name
        self._lifes = _lifes
        self._damages_min = _damages_min
        self._damages_max = _damages_max
        self._nb_potions = _nb_potions
        self._heal_min = _heal_min
        self._heal_max = _heal_max

    def __str__(self): 
         return f"""Nom : {self.name}
        - Vie : {self._lifes}
        - Degats Min: {self._damages_min} 
        - Degats max : {self._damages_max}
        - Potions : {self._nb_potions}
        - Heal Min: {self._heal_min}
        - Heal Max: {self._heal_max}
        """
 
    @property
    def damages(self) -> int: 
        """ Return random value to set damage inflected by a player (depending of _max_magages & _damages_min)
        """
        return randint(self._damages_min, self._damages_max)

    def damages_inflected(self, target: "Character") -> int: 
        """ Manage attacking of the Character
        """
        damages_inflected = self.damages
        target._lifes -= damages_inflected
        print(f"\n{self.name} attaque et inflige {damages_inflected} points de degat ⚔")
        print(f"Il ne reste plus que {target._lifes} points de vie à {target.name}\n")
        return damages_inflected
    
    @property
    def potions(self) -> int: 
        """ Return random value to set heal received by a player when using a potion (depending o _heal_max_hea)
        """
        return randint(self._heal_min, self._heal_max)
    
    def potions_usage(self) -> bool: 
        """ Manage usage of a potion
        """
        _max_lifes = 50  
        if self._nb_potions > 0:
            heal_received = self.potions
            self._lifes += heal_received
            print(f"\nVous vous soignez de {heal_received} points de vie 💖")
            if self._lifes > _max_lifes:
                print("Vous avez atteints le nombre de points de vie maximal (50)")
                _final_heal = heal_received - (self._lifes - _max_lifes)
                print(f"Vous vous soignez donc seulement de {_final_heal} points de vie 💖")
                self._lifes = _max_lifes
            self._nb_potions -= 1
            print(f"Vous avez maintenant {self._lifes} points de vie, mais vous perdez votre prochain tour! ")
            print(f"Il vous reste maintenant {self._nb_potions} potions 🧪 \n")
            skip_turn = True
        return skip_turn

# CREATION INSTANCES : magician & foe
def character_creation(level) -> Character:
    """Create both instances for player and opponent depending of the level choosen by user

    Args:
        level (str): level chosen by user (returned in fonction _menu_selection_level)

    Returns:
        Character: Return both instance from class Character, named magician and foe
    """

    if level == "Facile": 
        magician = Character(name = "Gandalf", _lifes = 50, _damages_min = 5, _damages_max = 15, _nb_potions = 3, _heal_min = 15, _heal_max = 25)
        foe = Character(name = "Balrog", _lifes = 30, _damages_min = 5, _damages_max = 10)
    elif level == "Normal": 
        magician = Character(name = "Gandalf", _lifes = 50, _damages_min = 5, _damages_max = 15, _nb_potions = 3, _heal_min = 15, _heal_max = 25)
        foe = Character(name = "Balrog", _lifes = 50, _damages_min = 5, _damages_max = 15)
    elif level == "Difficile": 
        magician = Character(name = "Gandalf", _lifes = 50, _damages_min = 5, _damages_max = 15, _nb_potions = 3, _heal_min = 15, _heal_max = 25)
        foe = Character(name = "Balrog", _lifes = 60, _damages_min = 5, _damages_max = 20)
    return magician, foe

# MENUS 
def _menu_welcoming():
    """Display the starting Menu
    """

    print("-" * 70)
    print(" 🕹 Bienvenue dans le jeu de Role 🎮 : 🧙‍♂️ Gandalf vs. THE Balrog 👹 ")
    print("-" * 70)

def _menu_main() -> str:
    """Display the main menu where user can choose between playing or displaying last games results

    Returns:
        str: Return the action choosen by the user in the variable choice_start
    """
    valid_choice_start = ["1", "2"]
    choice_start = ""
    while choice_start not in valid_choice_start: 
        print("""
        Choisissez parmi les options suivantes :
        1: Jouer ! 
        2: Voir les derniers résultats.
        """)
        choice_start = input("Que souhaitez-vous faire ? ")
        if choice_start not in valid_choice_start: 
                print("Erreur: Action inconnue")
    return choice_start 

def _menu_choose_name() -> str: 
    """Allow user to choose a name

    Returns:
        str: Return named chosen by user to be used in the game
    """
    user_name = input("Veuillez entrer votre nom : ")
    print(f"\nEnchanté {user_name} !")
    return user_name

def _menu_selection_level(level="N") -> str:
    """Allow user to choose the level of difficulty

    Args:
        level (str): level chosen by user (returned in fonction _menu_selection_level)

    Returns:
        str: Return the level of difficulties chosen by user
    """

    valid_choice_level = ["F", "f", "N", "n", "D", "d"]
    level = ""
    while level not in valid_choice_level: 
        level = input("Veuillez choisir un niveau de difficulté (F=Facile | N=Normal | D=Difficile): ")
        if level not in valid_choice_level:
            print("Veuillez entrer une commande valide pour la difficulté du jeu ! ")
    print(f"Niveau Choisit: {level}")
    if level in ["F", "f"]: 
        level = "Facile"
    elif level in ["N", "n"]: 
        level = "Normal"
    elif level in ["D", "d"]: 
        level = "Difficile"
    return level

def _menu_display_instructions(magician: "Character", foe: "Character", level): 
    """Display the instructions to user depending of level chosen.

    Args:
        magician (Character): Instance magician create from class Character (returned in function character_creation)
        foe (Character): Instance magician create from class Character (returned in function character_creation)
        level (str): Level chosen by user (returned in fonction _menu_selection_level)
    """
    valid_choice_instructions = ["O", "N"]
    choice_instructions = ""
    while choice_instructions not in valid_choice_instructions:
        choice_instructions = input("Souhaitez vous voir les instructions ? (O: Oui | N: Non) ")
        if choice_instructions not in valid_choice_instructions:
            print("Attention ! Veuillez entrer une commande valide.")
    if choice_instructions== "O": 
        print(f"""\n Vous allez pouvoir affrontez le Balrog de Morgoth ! (Mode de difficulté : {level}) 
                [_Vous_]
        Vous incarnez Gandalf le gris :
        -> Vous commencez la partie avec {magician._lifes} points de vie (et {magician._nb_potions} potions)
        -> A chaque tour vous pouvez, soit : 
            1/ Attaquer (via 'a' ou 'A') et vous infligerez aléatoirement entre {magician._damages_min} et {magician._damages_max} points de dégâts au Balrog.
            2/ Utiliser une potion (via 'p' ou 'P') et vous récupérerez entre {magician._heal_min} et {magician._heal_max} points de vie, mais vous passerez votre tour.
                [_Votre adversaire_]
        Vous combattrez contre le balrog de Morgoth !
        -> Le Balrog, quant à lui, commence la partie avec {foe._lifes} points de vie.
        -> Chaque tour le Balrog vous attaquera à son tour et vous infligera entre {foe._damages_min} et {foe._damages_max} points de dégâts.
        """)
    input("Êtes-vous prêt ? (Appuyez simplement sur une touche pour commencer) 💬 \n")

def _menu_display_end_of_turn(turn, magician, foe):
    """Display the Menu : End of the Turn

    Args:
        magician (Character): Instance magician create from class Character (returned by function character_creation)
        foe (Character): Instance magician create from class Character (returned by function character_creation)
        turn (int): Actual turn of the game (returned by function _game_structure)
    """
    print(f"""
-------------------------------------------
- FIN DU TOUR {turn} - 
🧙‍♂️ Gandalf le gris a {magician._lifes} points de vie restants.
👹 Le balrog, quant à lui, a {foe._lifes} points de vie restants.
-------------------------------------------
""")
    input("Appuyez simplement sur une touche pour passer au prochain tour 💬 \n")

def _menu_restart_game():
    """Allow user to choose if he wants to restart the game

    Returns:
        str: Return choice of user, if he wants to restart
    """
    restart = input("Souhaitez vous refaire une partie ? (O: Oui | N: Non) ")
    print("\n" * 2)
    return restart
    
def _menu_display_greetings(user_name): 
    """Display the final menu of greetings
    """

    print(f""" - FIN DU JEU -
    Meri d'avoir joué {user_name} ! 
    A bientôt
    """)

# RESULTS MANAGEMENT
def _result(user_name: str, level: str, turn: int, magician: "Character", foe: "Character") -> str:
    """Collect the results of the game and return it as an f-string

    Args:
        level (str): Level chosen by user (returned in fonction _menu_selection_level)
        turn (int): Actual turn of the game (returned by function _game_structure)
        magician (Character): Instance magician create from class Character (returned in function character_creation)
        foe (Character): Instance magician create from class Character (returned in function character_creation)

    Returns:
        str: Return the results of the game in f-string
    """
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M')
    if magician._lifes > 0:
        result = f"{current_date} - Nom: {user_name} - Mode: {level} - Victoire! : {user_name}, à défait le Balrog de Morgoth au tour {turn} (alors qu'il lui restait {magician._lifes} points de vie)"
    else: 
        result = f"{current_date} - Nom: {user_name} - Mode: {level} - Défaite! : {user_name}, à été défait par le Balrog de Morgoth au tour {turn} (à qui il restait encore {foe._lifes} points de vie)"
    return result

def _display_last_results(SAVE_RESULTS):
    """Saving the results in the end of each game in a file located in the same folder that the script

    Args:
        SAVE (Path): Path type variable which contain the pathway of the saving file
    """
    if not os.path.exists(SAVE_RESULTS): 
        with open (SAVE_RESULTS, "w") as file:
            json.dump([], file)

    with open (SAVE_RESULTS, "r") as file: 
        contents = json.load(file)
        if contents:
            print("-" * 50)
            print(f"Voici les 10 derniers résultats ")
            for i, item in enumerate(contents, 1):
                print(f"{i}. {item}")
            print("-" * 50)
            print("\n")
        else: 
            print("Il n'y a malheuresement pas de résultat récent à afficher \n")

# SAVING
def _savings_result(SAVE_RESULTS, results: str):
    
    # Create file if not existing
    if not os.path.exists(SAVE_RESULTS): 
        with open (SAVE_RESULTS, "w") as file:
            json.dump([], file)

    # Reading File
    with open (SAVE_RESULTS, "r") as file: 
        contents = json.load(file)

    # Check  number of entries game_last_scores.json to delete oldest if it reach 10
    lenght_contents = len(contents)
    
    if lenght_contents > 9:
        del contents[0]

    # Write new results list in game_last_scores.json 
    contents.append(results)

    with open (SAVE_RESULTS, "w") as file: 
        json.dump(contents, file, indent=4)

# STRUCTURE GAME
def _game_structure(user_name, magician: "Character", foe: "Character", skip_turn: bool) -> int: 
    """Execution of the game part of the script

    Args:
        user_name(str): Name chosen by user (returned in function _menu_choose_name)
        magician (Character): Instance magician create from class Character (returned in function character_creation)
        foe (Character): Instance magician create from class Character (returned in function character_creation)
        skip_turn (bool): Indicated the value of skip_turn which is True when magician used a potion of the previous turn. Defaults to "False".

    Returns:
        int: Return the final turn when game is over in variable turn
    """

    turn = 1
    valid_choice = ["a", "A", "p", "P"]
    while True:
        print("*" * 50)
        print(f"[ TOUR  {turn} ]")
        print("*" * 50)
        if skip_turn:
            print("👉 C'est votre tour Gandalf 🧙‍♂️ ")
            print("Oups! Vous passez votre tour puisque vous avez utiliser une Po-Pooooo au tour précédent! \n")
            skip_turn = False
        else: 
            # TOUR : PLAYER
                # User Select Action
            user_choice = ""
            while user_choice not in valid_choice:
                print("👉 C'est votre tour Gandalf 🧙‍♂️ ")
                user_choice = input("""Que souhaitez vous faire ? 
                Entrez 'A' pour attaquer !
                Entrer 'P' pour utiliser une potion !
                Que faites-vous ? : """)
                if user_choice not in valid_choice: 
                    print("ATTENTION! Gandalf ne connait pas ce sort... veuillez entrer une commande valide \n")
                # User Choice : Attacking
            if user_choice == "A" or user_choice == "a":
                magician.damages_inflected(foe)
                # Vérification : Vie restantes Balrog
                if foe._lifes <= 0: 
                    print("*" * 50)
                    print(f"Félicitation {user_name} ! 🏆 Vous avez pourfendu le Balrog de Morgoth et devenez Gandalf le Blanc 🏆")
                    print("*" * 50)
                    print("\n")
                    break
                # User Choice : Potions
            elif user_choice == "P" or user_choice == "p":
                if magician._nb_potions > 0:
                    skip_turn = magician.potions_usage()
                else:
                    print("Vous n'avez malheuresement plus de potions 🧪 !")
                    print("Veuillez effectuer une autre action... ")
                    user_choice = ""
                    continue   
            # TOUR : BALROG
        print("👉 C'est au tour du Balrog d'agir... 👹 ")
        foe.damages_inflected(magician)
            # Vérification : Vie restantes Gandalf
        if magician._lifes <= 0: 
            print("*" * 50)
            print(f"☠ Catastrophe ! Le balrog à pourfendre Gandalf ! Honte à vous {user_name} ☠")
            print("*" * 50)
            print("\n")
            break
        _menu_display_end_of_turn(turn, magician, foe)
        turn +=1
    return turn

# EXECUTION GAME
def start(SAVE_RESULTS, user_name="Test"):
    """Main Structure of the scripts

    Args:
        SAVE (Path): Path of the saving file
        user_name (str): Name chosen by user (returned in function _menu_choose_name). Defaults to "Test".
    """

    continue_playing = "O"
    while continue_playing == "O":
        _menu_welcoming() # Return choice_start = 1/2
        choice_main_menu = _menu_main()
        if choice_main_menu == "1":
            user_name = _menu_choose_name() # Return user_name = string
            level = _menu_selection_level() # Return level = F/N/D  
            magician, foe = character_creation(level) # Return characters magician & foe, Instance from Class Character, depending the level chosen
            _menu_display_instructions(magician, foe, level)
            turn = _game_structure(user_name, magician, foe, skip_turn=False)
            results = _result(user_name, level, turn, magician, foe)
            _savings_result(SAVE_RESULTS, results)
            continue_playing = _menu_restart_game() # Return restart
            if continue_playing != "O":
                _menu_display_greetings(user_name)
        elif choice_main_menu == "2": 
            _display_last_results(SAVE_RESULTS)
            continue
        else: 
            print("Erreur: Action inconnue")

# MAIN
start(SAVE_RESULTS)