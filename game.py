import pygame
import random
 
from unit import *
from grid import Grill


# Définition des constantes
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

TILE_SIZE = 45  # Taille d'une case (en pixels)
CELL_SIZE = 45 


class Game:
    """
    Classe pour représenter le jeu.

    ...
    Attributs
    ---------
    screen: pygame.Surface
        La surface de la fenêtre du jeu.
    player_units : list[Unit]
        La liste des unités du joueur.
    enemy_units : list[Unit]
        La liste des unités de l'adversaire.
    """

    def __init__(self, screen, grid, image, size):
        """
        Construit le jeu avec la surface de la fenêtre.

        Paramètres
        ----------
        screen : pygame.Surface
            La surface de la fenêtre du jeu.
        """
        self.grid = grid
        self.image = image
        self.size = size
        self.screen = screen
        self.player_units = []
        self.enemy_units = []
       
                # Chargement de l'image de fond
        try:
            self.background_image = pygame.image.load(r"images/menu_background.png")
            self.background_image = pygame.transform.scale(self.background_image, ((self.size + 16) * TILE_SIZE, self.size * TILE_SIZE))
        except pygame.error as e:
            raise FileNotFoundError(f"Erreur lors du chargement de l'image de fond : {e}")
    
    def select_units(self, player_name):
        """
        Permet à un joueur de sélectionner ses unités.
        """
        font = pygame.font.Font(None, 30)
        title_font = pygame.font.Font(None, 50)
        small_font = pygame.font.Font(None, 24)
        clock = pygame.time.Clock()

        # Liste des unités disponibles avec leurs caractéristiques
        all_units = [
            {
                "class": Archer,
                "name": "Archer",
                "stats": "15 PV, Zone d'Effet : direction cardinale",
                "attacks": [
                    "1. Arrow Shot : -2PV sur une portée de 3 cases",
                    "2. Power Arrow : -4PV sur une portée de 2 cases"
                ],
                "image": pygame.image.load(r"images/archer.png")
            },
            {
                "class": Swordsman,
                "name": "Swordsman",
                "stats": "10 PV, Zone d'Effet : direction cardinale",
                "attacks": [
                    "1. Sword Slash : -3PV sur une portée de 1 case",
                    "2. Heavy Strike : -6PV sur une portée de 1 case"
                ],
                "image": pygame.image.load(r"images/swordsman.png")
            },
            {
                "class": Wizard,
                "name": "Wizard",
                "stats": "12 PV, Zone d'Effet : direction dispersée",
                "attacks": [
                    "1. Gladio : -4PV sur une portée de 2 cases",
                    "2. Incendio : -8PV sur une portée de 2 cases",
                    "'L' pour se régénérer 4PV (valider la position avant d'utiliser ce pouvoir)"
                ],
                "image": pygame.image.load(r"images/wizard.png")
            },
            {
                "class": Invincible,
                "name": "Invincible",
                "stats": "40 PV, Zone d'Effet : direction circulaire",
                "attacks": [
                    "1. Big Slash : -4PV sur une portée de 1 case",
                    "2. Two Blade Style : -6PV sur une portée de 2 cases"
                ],
                "image": pygame.image.load(r"images/invincible.png")
            },
            {
                "class": Bomber,
                "name": "Bomber",
                "stats": "15 PV, Zone d'Effet : direction dispersée",
                "attacks": [
                    "1. Aqua bomb : -5PV sur une portée de 3 cases",
                    "2. Lava bomb : -7.5PV sur une portée de 6 cases"
                ],
                "image": pygame.image.load(r"images/bomber.png")
            }
        ]

        selected_units = []

        while len(selected_units) < 3:
            self.screen.blit(self.background_image, (0, 0))  # Afficher l'image de fond

            # Afficher le titre
            title = title_font.render(f"Equipe : {player_name}, choisissez vos unités", True, (255, 255, 255))
            self.screen.blit(title, (1485 // 2 - title.get_width() // 2, 20))

            # Afficher les unités disponibles
            for i, unit in enumerate(all_units):
                x_pos = 100 + i * 270
                y_pos = 100

                # Afficher le nom
                name_text = font.render(f"{i + 1}. {unit['name']}", True, (255, 255, 255))
                self.screen.blit(name_text, (x_pos, y_pos))

                # Afficher l'image
                unit_image = pygame.transform.scale(unit['image'], (100, 100))
                self.screen.blit(unit_image, (x_pos, y_pos + 30))

                # Afficher les stats avec gestion du texte long
                stats_lines = self.wrap_text(unit['stats'], small_font, 250)
                for j, line in enumerate(stats_lines):
                    stats_text = small_font.render(line, True, (0, 0, 0))
                    self.screen.blit(stats_text, (x_pos, y_pos + 140 + j * 20))

                # Afficher les attaques avec gestion du texte long
                for k, attack in enumerate(unit['attacks']):
                    attack_lines = self.wrap_text(attack, small_font, 250)
                    for l, line in enumerate(attack_lines):
                        attack_text = small_font.render(line, True, (0, 0, 0))
                        self.screen.blit(attack_text, (x_pos, y_pos + 160 + len(stats_lines) * 20 + k * 40 + l * 20))

            # Afficher les unités sélectionnées
            selected_title = title_font.render(f"Unités sélectionnées : {len(selected_units)}/3", True, (255, 255, 255))
            self.screen.blit(selected_title, (1485 // 2 - selected_title.get_width() // 2, 600))

            pygame.display.flip()

            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                        index = event.key - pygame.K_1
                        if index < len(all_units) and all_units[index]['class'] not in [unit.__class__ for unit in selected_units]:
                            unit_class = all_units[index]['class']
                            selected_units.append(unit_class(0, 0, player_name, self.grid))

            clock.tick(30)

        return selected_units
    
    def wrap_text(self, text, font, max_width):
        """
        Découpe un texte en plusieurs lignes pour qu'il tienne dans une largeur donnée.
        """
        if not text:  # Vérifiez si le texte est vide ou None
            return []

        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "

        if current_line:
            lines.append(current_line.strip())

        return lines


    def main_menu(self):
        pygame.init()
        font = pygame.font.Font(None, 74)
        clock = pygame.time.Clock()

        menu_options = ["Start", "Instructions", "Quit"]
        selected_option = 0

        while True:
            self.screen.blit(self.background_image, (0, 0))  # Afficher l'image de fond

            for i, option in enumerate(menu_options):
                color = (255, 255, 255) if i == selected_option else (100, 100, 100)
                text = font.render(option, True, color)
                text_rect = text.get_rect(center=(1485 // 2, 765 // 3 + i * 80))
                self.screen.blit(text, text_rect.topleft)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(menu_options)
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN:
                        if selected_option == 0:  # Start
                            # Sélection des unités
                            self.player_units = self.select_units('player')
                            self.enemy_units = self.select_units('enemy')

                            # Positionner les unités
                            self.player_units[0].x, self.player_units[0].y = 0, 0
                            self.player_units[1].x, self.player_units[1].y = 1, 0
                            self.player_units[2].x, self.player_units[2].y = 0, 1

                            self.enemy_units[0].x, self.enemy_units[0].y = 16, 16
                            self.enemy_units[1].x, self.enemy_units[1].y = 16, 15
                            self.enemy_units[2].x, self.enemy_units[2].y = 15, 16

                            return "start"
                        elif selected_option == 1:  # Instructions
                            self.show_instructions()
                        elif selected_option == 2:  # Quit
                            pygame.quit()
                            exit()

            clock.tick(30)


    def show_instructions(self):
        font = pygame.font.Font(None, 30)
        clock = pygame.time.Clock()
        instructions = [
            "Bienvenue dans notre jeu!",
            " ",
            " ",
            "Instructions:",
            "- Le 1er joueur 'player' et le 2ème joueur 'enemy' possèdent chacun son équipe d'unités.",
            "- Pour finir un tour, il faut utiliser toutes les unités de son équipe soit en jouant l'unité soit en sautant le tour de l'unité.",
            "- ATTENTION : Il faudra obligatoirement valider sa position avec 'ESPACE' avant d'attaquer, sauter son tour ou encore quitter le jeu.",
            "- Les instructions et directives correspondant à chaque unité seront rappelés sur la fenêtre d'informations lors du jeu.",
            "--> L'objectif est d'éliminer toutes les unités de l'équipe adversaire",
            " ",
            "BONNE CHANCE !",
            " ",
            "Press ESC to return to the menu.",
        ]

        while True:
            self.screen.blit(self.background_image, (0, 0))  # Afficher l'image de fond

            # Calculer le point de départ vertical pour centrer toutes les lignes
            total_text_height = len(instructions) * 40  # Hauteur totale du texte (40 pixels par ligne)
            start_y = (765 - total_text_height) // 2  # Centrer verticalement dans l'écran de hauteur 765

            for i, line in enumerate(instructions):
                text = font.render(line, True, (255, 255, 255))
                text_rect = text.get_rect(center=(1485 // 2, start_y + i * 40))  # Centrer horizontalement et ajuster verticalement
                self.screen.blit(text, text_rect.topleft)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            clock.tick(30)

    def start_game(self):
        while True:
            if not self.player_units:
                print("Le joueur 1 a gagné !")
                break
            elif not self.enemy_units:
                print("Le joueur 2 a gagné !")
                pygame.quit()
                break
            self.handle_player_turn()
            self.handle_enemy_turn()

    def handle_player_turn(self):
        """Tour du joueur"""
        for selected_unit in self.player_units:

            # Tant que l'unité n'a pas terminé son tour
            selected_unit.is_selected = True
            self.flip_display()
                
            selected_attack_type = None # Variable qui mémorise le type d'attaque choisi
            has_validated_position = False
            has_attacked = False
            remaining_moves = selected_unit.movement_speed
            movable_cells = selected_unit.get_movable_cells()

            #while not has_validated_position:
            while remaining_moves > 0:

                
                self.flip_display(movable_cells=movable_cells)  # Affiche les cases atteignables

                for event in pygame.event.get():

                    # Gestion de la fermeture de la fenêtre
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    
                    # Gestion des touches du clavier
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_e:  # Touche 'E' pour quitter le jeu
                            pygame.quit()
                            exit()
                                                        
                        # Déplacement (touches fléchées)
                        dx, dy = 0, 0
                        if event.key == pygame.K_LEFT:
                            dx = -1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                        elif event.key == pygame.K_UP:
                            dy = -1
                        elif event.key == pygame.K_DOWN:
                            dy = 1
                            
                        if dx != 0 or dy != 0:
                            selected_unit.move(dx, dy)
                            remaining_moves -= 1
                            print(f"Déplacements restants : {remaining_moves}")

                        if event.key == pygame.K_SPACE:
                            remaining_moves = 0    
                        
                        #selected_unit.move(dx, dy)
                        self.flip_display()
                        
                        # Valider la position avec "Espace"
                        if event.key == pygame.K_SPACE:
                            has_validated_position = True
                            break

            # Une fois la position validée, afficher les cases attaquables
            attackable_cells = selected_unit.get_attackable_cells()
            while not has_attacked:
                self.flip_display()

               # Obtenez les cases attaquables
                normal_cells = selected_unit.get_attackable_cells(attack_type=0)
                special_cells = selected_unit.get_attackable_cells(attack_type=1)
                 
                # Affichez les portées
                self.flip_display(normal_cells, special_cells, unit_team='player')

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                        
                    if event.type == pygame.KEYDOWN:
                   
                        if event.key == pygame.K_1:  # Attaque normale
                            self.execute_attack(selected_unit, normal_cells,self.enemy_units, attack_type=0)
                            has_attacked = True
                        elif event.key == pygame.K_2:  # Attaque spéciale
                            self.execute_attack(selected_unit, special_cells,self.enemy_units, attack_type=1)
                            has_attacked = True

                        if event.key == pygame.K_SPACE and selected_attack_type is not None:
                            for enemy in self.enemy_units:
                                if (enemy.x, enemy.y) in attackable_cells:  # Attaquer seulement si l'ennemi est sur une case attaquable
                                    selected_unit.attack(enemy, selected_attack_type)
                                    if enemy.health <= 0:
                                        self.enemy_units.remove(enemy)
                                    has_attacked = True
                                    break

                            if not has_attacked:
                                print("Aucun ennemi n'est sur une case attaquable.")

                        if event.key == pygame.K_s:  # Passer le tour
                            has_attacked = True
                            selected_unit.is_selected = False
                            print("Tour du joueur passé.")
                            break
                            selected_unit.is_selected = False
                            
                            
                        if event.key == pygame.K_l:  # Touche 'L' pour se soigner
                            if isinstance(selected_unit, Wizard):  # Vérifie si l'unité est un Wizard
                                if selected_unit.health < selected_unit.max_health:  # Vérifie que la santé n'est pas déjà au maximum
                                    selected_unit.heal()  # Appelle la méthode de soin
                                    print(f"{selected_unit.__class__.__name__} régénère 4 PV. Santé actuelle : {selected_unit.health}")
                                    has_attacked = True  # Terminer le tour après guérison
                                    selected_unit.is_selected = False
            
            selected_unit.is_selected = False
                                            
    def handle_enemy_turn(self):
        
        for selected_unit in self.enemy_units:

            # Tant que l'unité n'a pas terminé son tour
            selected_unit.is_selected = True
            self.flip_display()
            
            selected_attack_type = None # Variable qui mémorise le type d'attaque choisi
            has_validated_position = False
            has_attacked = False
            remaining_moves = selected_unit.movement_speed
            movable_cells = selected_unit.get_movable_cells()
            
            #while not has_validated_position:
            while remaining_moves > 0:   
                
                self.flip_display(movable_cells=movable_cells)  # Affiche les cases atteignables


                for event in pygame.event.get():
                    # Gestion de la fermeture de la fenêtre
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                        
                    # Gestion des touches du clavier
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_e:  # Touche 'E' pour quitter le jeu
                            pygame.quit()
                            exit()
                    
                        # Déplacement (touches fléchées)
                        dx, dy = 0, 0
                        if event.key == pygame.K_LEFT:
                            dx = -1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                        elif event.key == pygame.K_UP:
                            dy = -1
                        elif event.key == pygame.K_DOWN:
                            dy = 1
                        
                        # Déplace l'unité et réduit le nombre de déplacements restants
                        if dx != 0 or dy != 0:
                            selected_unit.move(dx, dy)
                            remaining_moves -= 1
                            print(f"Déplacements restants : {remaining_moves}")
                        
                        if event.key == pygame.K_SPACE:
                            remaining_moves = 0    
                        
                        #selected_unit.move(dx, dy)
                        self.flip_display()
                        
                        # Valider la position avec "Espace"
                        if event.key == pygame.K_SPACE:
                            has_validated_position = True
                            break

            # Une fois la position validée, afficher les cases attaquables
            attackable_cells = selected_unit.get_attackable_cells()
            
            while not has_attacked:
                self.flip_display()
                
                # Obtenez les cases attaquables
                normal_cells = selected_unit.get_attackable_cells(attack_type=0)
                special_cells = selected_unit.get_attackable_cells(attack_type=1)
                 
                # Affichez les portées
                self.flip_display(normal_cells, special_cells, unit_team='enemy')

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                                            
                    if event.type == pygame.KEYDOWN:
            
                        if event.key == pygame.K_1:  # Attaque normale
                            self.execute_attack(selected_unit, normal_cells,self.player_units, attack_type=0)
                            has_attacked = True
                        elif event.key == pygame.K_2:  # Attaque spéciale
                            self.execute_attack(selected_unit, special_cells,self.player_units, attack_type=1)
                            has_attacked = True

                        if event.key == pygame.K_SPACE and selected_attack_type is not None:
                            for player in self.player_units:
                                if (player.x, player.y) in attackable_cells:  # Attaquer seulement si player_1 est sur une case attaquable
                                    selected_unit.attack(player, selected_attack_type)
                                    if player.health <= 0:
                                        self.player_units.remove(player)
                                    has_attacked = True
                                    break

                            if not has_attacked:
                                print("Aucun ennemi n'est sur une case attaquable.")

                        if event.key == pygame.K_s:  # Passer le tour
                            has_attacked = True
                            selected_unit.is_selected = False
                            print("Tour du joueur passé.")
                            break
                            selected_unit.is_selected = False
                            
                            
                        if event.key == pygame.K_l:  # Touche 'L' pour se soigner
                            if isinstance(selected_unit, Wizard):  # Vérifie si l'unité est un Wizard
                                if selected_unit.health < selected_unit.max_health:  # Vérifie que la santé n'est pas déjà au maximum
                                    selected_unit.heal()  # Appelle la méthode de soin
                                    print(f"{selected_unit.__class__.__name__} régénère 4 PV. Santé actuelle : {selected_unit.health}")
                                    has_attacked = True  # Terminer le tour après guérison
                                    selected_unit.is_selected = False
                                                         
            selected_unit.is_selected = False


    def execute_attack(self, unit, attackable_cells, target_units, attack_type):
        """Exécute une attaque d'une unité sur les ennemis dans les cases attaquables."""
        for target in target_units:
            if (target.x, target.y) in attackable_cells:
                unit.attack(target, attack_type)
                if target.health <= 0:
                    target_units.remove(target)

         
    def flip_display(self, normal_cells=None, special_cells=None, movable_cells=None, unit_team=None):
        """Affiche le jeu."""

        # Affiche la grille
        self.screen.fill(BLACK)
        for x in range(0, self.size*CELL_SIZE, CELL_SIZE):
            for y in range(0, self.size*CELL_SIZE, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

        # Affiche les unités
        self.screen.blit(self.image, (0, 0))  # Afficher l'image de la grille
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)
                    
        # Définir les couleurs en fonction de l'équipe
        normal_color = (0, 0, 255, 120) if unit_team == 'player' else (255, 0, 0, 120)  # Bleu ou Rouge
        special_color = (0, 0, 255, 130) if unit_team == 'player' else (255, 0, 0, 130)  # Teintes plus sombres

        # Affiche les cases atteignables pour les déplacements
        if movable_cells:
            for x, y in movable_cells:
                overlay = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                overlay.fill((0, 255, 0, 100))  # Vert pour les déplacements
                self.screen.blit(overlay, (x * TILE_SIZE, y * TILE_SIZE))
            
        # Affiche les cases attaquables pour attaque normale
        if normal_cells:
            for x, y in normal_cells:
                overlay = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                overlay.fill(normal_color)  # Claire pour attaque normale 
                self.screen.blit(overlay, (x * TILE_SIZE, y * TILE_SIZE))

        # Affiche les cases attaquables pour attaque spéciale
        if special_cells:
            for x, y in special_cells:
                overlay = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                overlay.fill(special_color)  # Foncée pour attaque spéciale
                self.screen.blit(overlay, (x * TILE_SIZE, y * TILE_SIZE))
               
        # Affiche le panneau d'information (partie noire à droite)
        panel_rect = pygame.Rect(self.size*CELL_SIZE, 0, 16 * TILE_SIZE, self.size*CELL_SIZE)
        pygame.draw.rect(self.screen, (30, 30, 30), panel_rect)  # Fond du panneau en gris foncé
   
        
        # Si une unité est sélectionnée, affiche ses types d'attaques
        for unit in self.player_units + self.enemy_units:
            if unit.is_selected:
                font = pygame.font.Font(None, 24)
                y_offset = 20  # Distance verticale de départ dans le panneau
                title_text = font.render(f"Unit: {unit.__class__.__name__}", True, YELLOW)
                self.screen.blit(title_text, (self.size*CELL_SIZE+ 10, y_offset))
                y_offset += 40
                
                # Affiche les instructions de chaque unité
                directive_text = font.render("Instructions -> Valider sa position avec 'ESPACE' pour voir la portée des attaques de l'unité", True, WHITE)
                self.screen.blit(directive_text, (self.size*CELL_SIZE + 10, y_offset))
                y_offset += 30
                
                directive2_text = font.render("Instructions -> Pensez à valider avec 'ESPACE' avant de faire quoique ce soit !", True, WHITE)
                self.screen.blit(directive2_text, (self.size*CELL_SIZE + 10, y_offset))
                y_offset += 30 
                
                if isinstance (unit, Archer):
                   instruction_text = font.render("Attaque normale et spéciale en direction cardinale sur 3 et 2 cases respectivement", True, WHITE)
                   self.screen.blit(instruction_text, (self.size*CELL_SIZE+ 10, y_offset))
                   y_offset += 40 
                   
                if isinstance (unit, Swordsman):
                    instruction_text = font.render("Attaque normale et spéciale en direction cardinale sur 1 case", True, WHITE)
                    self.screen.blit(instruction_text, (self.size*CELL_SIZE + 10, y_offset))
                    y_offset += 40  
                    
                if isinstance (unit, Wizard):
                    instruction_text = font.render("Attaques normale et spéciale en direction dispersée", True, WHITE)
                    self.screen.blit(instruction_text, (self.size*CELL_SIZE + 10, y_offset))
                    y_offset += 40 
                    power_text = font.render("Pouvoir spécial -> 'L' pour regénérer +4 PV", True, GREEN)
                    self.screen.blit(power_text, (self.size*CELL_SIZE + 10, y_offset))
                    y_offset += 40
                    
                if isinstance (unit, Invincible):
                    instruction_text = font.render("Attaque normale et spéciale en direction circulaire sur 1 case", True, WHITE)
                    self.screen.blit(instruction_text, (self.size*CELL_SIZE + 10, y_offset))
                    y_offset += 40
                    
                if isinstance (unit, Bomber):
                    instruction_text = font.render("Attaque normale et spéciale sur une zone dispersée", True, WHITE)
                    self.screen.blit(instruction_text, (self.size*CELL_SIZE+ 10, y_offset))
                    y_offset += 40                
                   
                # Affiche les types d'attaques
                for i, attack in enumerate(unit.attack_types):
                    text = font.render(f"{i + 1}. {attack['name']} (Power: {attack['power']}, Range: {attack['range']})",True,WHITE)
                    self.screen.blit(text, (self.size*CELL_SIZE + 10, y_offset))
                    y_offset += 30 

                defense_text=font.render(f"Défense:  {unit.defense}",True,WHITE)
                self.screen.blit(defense_text, (self.size*CELL_SIZE + 10, y_offset))
                y_offset+=30


                y_offset += 10
                directive_text = font.render("Si aucun ennemi n'est sur une case attaquable, passer son tour 'S' ", True, YELLOW)
                self.screen.blit(directive_text, (self.size*CELL_SIZE + 10, y_offset))
                y_offset += 40  
                
                option_text = font.render("'S' pour sauter son tour et 'E' pour quitter le jeu", True, RED)
                self.screen.blit(option_text, (self.size*CELL_SIZE + 10, y_offset))
                y_offset += 50
                
                remarque_text = font.render("Il est possible de quitter le jeu avant d'avoir valider sa position", True, RED)
                remarque2_text = font.render("En revanche après validation de sa position, il faudra sauter son tour avant de quitter",True, RED)
                self.screen.blit(remarque_text, (self.size*CELL_SIZE + 10, y_offset))
                y_offset += 30
                self.screen.blit(remarque2_text, (self.size*CELL_SIZE + 10, y_offset))
                y_offset += 40
           
        # Rafraîchit l'écran
        pygame.display.flip()
    
def main():
    """
    Point d'entrée principal du jeu.
    """
    pygame.init()

    try:
        pygame.mixer.init()
        pygame.mixer.music.load(r"sounds/sound_free_copyright.mp3")
        pygame.mixer.music.play(-1)
    except pygame.error:
        print("Erreur lors du chargement de la musique.")

    # Initialisation de l'écran
    screen = pygame.display.set_mode((17 * TILE_SIZE + 16 * TILE_SIZE, 17 * TILE_SIZE))
    pygame.display.set_caption("Mon jeu avec grille PNG")

    # Création d'une instance du jeu (temporaire pour accéder au menu)
    game = Game(screen, None, None, 17)

    # Affichage du menu principal
    menu_choice = game.main_menu()

    if menu_choice == "Start":
        print("Lancement du jeu!")
        # Affichage du menu pour choisir le monde
        monde = game.select_monde()
        if monde is None:
            print("Aucun monde sélectionné, retour au menu principal.")
            return

        # Affichage du menu pour choisir la taille
        taille = game.select_taille()
        if taille is None:
            print("Aucune taille sélectionnée, retour au menu principal.")
            return

        print(f"Monde sélectionné : {monde}, Taille sélectionnée : {taille}")

        # Création de la grille en fonction des choix
        grille = Grill(monde_type=monde, taille=taille)

        # Re-création de l'instance du jeu avec la grille sélectionnée
        game = Game(screen, grille.grid, grille.image, grille.size)

        # Démarrer la partie
        game.start_game()

    elif menu_choice == "Instructions":
        game.show_instructions()
    elif menu_choice == "Quit" or menu_choice is None:
        pygame.quit()

if __name__ == "__main__":
    main()