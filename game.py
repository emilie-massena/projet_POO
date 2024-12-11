import pygame
import random
# Push Emi 08/12 16h30

from unit import *

#emilie 17h50

# Définir les constantes
TILE_SIZE = 45  # Taille d'une case (en pixels)
GRID_WIDTH = 17
GRID_HEIGHT = 17
SCREEN_WIDTH = GRID_WIDTH * TILE_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * TILE_SIZE

# Charger l'image de la grille
grid_image = pygame.image.load(r"images\grille.png")
grid_image = pygame.transform.scale(grid_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Grille logique (terrain)
grid = [
    ["passage_vert"] * 13 + ["arbre", "mur", "healing_zone", "passage_vert"],
    ["passage_vert"] * 13 + ["arbre", "mur", "passage_vert", "passage_vert"],
    ["passage_vert"] * 3 + ["mur", "arbre"] + ["passage_vert"] * 8 + ["arbre", "mur", "mur", "passage_vert"],
    ["mur"] * 4 + ["arbre"] + ["passage_vert"] * 4 + ["mer"] + ["passage_vert"] * 3 + ["arbre"] * 3 + ["passage_vert"],
    ["arbre"] * 5 + ["passage_vert"] * 4 + ["mer"] * 2 + ["passage_vert"] * 6,
    ["passage_vert"] * 17,
    ["passage_vert"] * 6 + ["arbre"] * 4 + ["passage_vert"] * 7,
    ["passage_vert"] * 2 + ["arbre"] + ["passage_vert"] * 3 + ["arbre", "mer", "mer", "arbre"] + ["passage_vert"] * 6 + ["mer"],
    ["passage_vert"] * 2 + ["arbre"] + ["passage_vert"] * 4 + ["mer", "mer", "arbre"] + ["passage_vert"] * 5 + ["mer"] + ["healing_zone"],
    ["arbre"] * 3 + ["passage_vert"] * 3 + ["arbre", "mer", "arbre", "arbre"] + ["passage_vert"] * 4 + ["mer"] + ["passage_vert"] * 2,
    ["passage_vert"] * 6 + ["arbre"] + ["passage_vert"] * 6 + ["mer"] + ["passage_vert"] * 3,
    ["passage_vert"] * 17,
    ["passage_vert"] * 2 + ["mur"] * 2 + ["passage_vert"] * 8 + ["arbre"] * 5,
    ["arbre"] + ["passage_vert"] * 2 + ["mur"] + ["passage_vert"] * 8 + ["arbre"] + ["mur"] * 4,
    ["arbre"] * 2 + ["passage_vert"] * 10 + ["arbre"] + ["mur"] + ["passage_vert"] * 3,
    ["passage_vert"] * 3 + ["mur"] + ["passage_vert"] * 4 + ["mer"] + ["passage_vert"] * 8,
    ["passage_vert"] * 2 + ["healing_zone"] + ["mur"] + ["passage_vert"] * 3 + ["mer"] * 3 + ["passage_vert"] * 7
]


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

    def __init__(self, screen):
        """
        Construit le jeu avec la surface de la fenêtre.

        Paramètres
        ----------
        screen : pygame.Surface
            La surface de la fenêtre du jeu.
        """
        self.screen = screen
        self.player_units = [Archer(0, 0, 'player', grid), # Case (1,1)
                             Swordsman(1, 0, 'player', grid),# Case (1,2)
                             Wizard(2, 0, 'player', grid), # Case (1,3)
                             Invincible(0,1,'player', grid)] # Case (2,1)

        self.enemy_units = [Archer(16, 16, 'enemy', grid), # Case (17,17)
                            Swordsman(15, 16, 'enemy', grid),# Case (17,16)
                            Wizard(14, 16, 'enemy', grid),  # Case(17,15)
                            Invincible(16,15,'enemy', grid)] # Case (16,17)

    def handle_player_turn(self):
        """Tour du joueur"""
        for selected_unit in self.player_units:

            # Tant que l'unité n'a pas terminé son tour
            has_acted = False
            selected_unit.is_selected = True
            self.flip_display()
            
            selected_attack_type = None # Variable qui mémorise le type d'attaque choisi
            
            while not has_acted:
                # Mise à jour de l'affichage
                self.flip_display()
                # Important: cette boucle permet de gérer les événements Pygame
                for event in pygame.event.get():

                    # Gestion de la fermeture de la fenêtre
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    # Gestion des touches du clavier
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_e:  # Touche 'E' du clavier pour exit du game
                            pygame.quit()
                            exit()
                            
                        if event.key in [pygame.K_1, pygame.K_2]:  # Touche pour sélectionner l'attaque
                            selected_attack_type = int(event.key - pygame.K_1)  # Convertit en 0 ou 1
                            print(f"Type d'attaque sélectionné : {selected_attack_type + 1}")

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

                        selected_unit.move(dx, dy)
                        self.flip_display()  # Affiche la mise à jour après le déplacement
                        
                        if event.key == pygame.K_SPACE:  # Valider la position
                            selected_unit.position_validated = True
                            print("Position validée!")
                            self.flip_display()  # Affiche les cases attaquables après validation


                        # Attaque (touche espace) met fin au tour
                        if event.key == pygame.K_SPACE and selected_attack_type is not None:
                            for enemy in self.enemy_units:
                                distance_x = abs(selected_unit.x - enemy.x)
                                distance_y = abs(selected_unit.y - enemy.y)
                                if distance_x <= selected_unit.attack_types[selected_attack_type]["range"] and \
                                        distance_y <= selected_unit.attack_types[selected_attack_type]["range"]:
                                            selected_unit.attack(enemy, selected_attack_type)
                                            if enemy.health <= 0:
                                                self.enemy_units.remove(enemy)
                                            has_acted = True
                                            break
                                        
                            selected_unit.is_selected = False
                            
                        if event.key == pygame.K_s:
                            has_acted = True  # Fin du tour immédiatement
                            selected_unit.is_selected = False  # Désélectionner l'unité
                            print("Tour du joueur passe son tour")
                            break  # Passe au tour suivant
                            
                        if event.key == pygame.K_l:  # Touche 'L' pour se soigner
                            if isinstance(selected_unit, Wizard): # Pour l'unité Wizard
                                selected_unit.heal()
                                has_acted = True
                                selected_unit.is_selected = False  # Désélectionner l'unité
                                break


    def handle_enemy_turn(self):
        """IA très simple pour les ennemis."""
        for enemy in self.enemy_units:

            # Déplacement aléatoire
            target = random.choice(self.player_units)
            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
            enemy.move(dx, dy)

            # Attaque si possible
            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                enemy.attack(target)
                if target.health <= 0:
                    self.player_units.remove(target)

    def flip_display(self):
        """Affiche le jeu."""

        # Affiche la grille
        self.screen.fill(BLACK)
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)
        """        
        # Met en surbrillance les cases attaquables
        for unit in self.player_units + self.enemy_units:
            if unit.is_selected:
                attackable_cells = unit.get_attackable_cells()
                color = YELLOW if isinstance(unit, Archer) or isinstance(unit, Swordsman) else WHITE
                for cell in attackable_cells:
                    cell_rect = pygame.Rect(cell[0] * CELL_SIZE, cell[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.screen, color, cell_rect)"""

        # Affiche les unités
        self.screen.blit(grid_image, (0, 0))  # Afficher l'image de la grille
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)
        
        
        # Affiche le panneau d'information (partie noire à droite)
        panel_rect = pygame.Rect(SCREEN_WIDTH, 0, 16 * TILE_SIZE, SCREEN_HEIGHT)
        pygame.draw.rect(self.screen, (30, 30, 30), panel_rect)  # Fond du panneau en gris foncé
        
        # Si une unité est sélectionnée, affiche ses types d'attaques
        for unit in self.player_units:
            if unit.is_selected:
                font = pygame.font.Font(None, 24)
                y_offset = 20  # Distance verticale de départ dans le panneau
                title_text = font.render(f"Unit: {unit.__class__.__name__}", True, YELLOW)
                self.screen.blit(title_text, (SCREEN_WIDTH + 10, y_offset))
                y_offset += 30
                
                # Affiche les instructions de chaque unité
                instruction_text = font.render("Instructions -> 'E' pour quitter  et  'S' pour sauter son tour", True, WHITE)
                self.screen.blit(instruction_text, (SCREEN_WIDTH + 10, y_offset))
                y_offset += 30
                if isinstance (unit, Wizard):
                   instruction_text = font.render("Pouvoir spécial -> 'L' pour régénérer 4 PV", True, GREEN)
                   self.screen.blit(instruction_text, (SCREEN_WIDTH + 10, y_offset))
                   y_offset += 30 
                # Affiche les types d'attaques
                for i, attack in enumerate(unit.attack_types):
                    text = font.render(f"{i + 1}. {attack['name']} (Power: {attack['power']}, Range: {attack['range']})",True,WHITE)
                    self.screen.blit(text, (SCREEN_WIDTH + 10, y_offset))
                    y_offset += 30        
               
        # Met en surbrillance les cases attaquables
        for unit in self.player_units + self.enemy_units:
            if unit.is_selected:
                attackable_cells = unit.get_attackable_cells()
                
                # Crée une surface semi-transparente
                overlay = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                overlay.fill((0, 0, 255, 120)) # Transparence environ 50% 
                
                for cell in attackable_cells:
                    cell_x, cell_y = cell
                    # Blit la surface semi-transparente sur l'écran
                    self.screen.blit(overlay, (cell_x * TILE_SIZE, cell_y * TILE_SIZE))
                    
        # Rafraîchit l'écran
        pygame.display.flip()
      
def main():

    # Initialisation de Pygame
    pygame.init()

    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((SCREEN_WIDTH + 16*TILE_SIZE, SCREEN_HEIGHT))
    pygame.display.set_caption("Mon jeu avec grille PNG")

    # Instanciation du jeu
    game = Game(screen)


    # Boucle principale du jeu
    while True:
        if not game.player_units:
            print("L'IA a gagné !")
            break
        elif not game.enemy_units:
            print("Vous avez gagné !")
            pygame.quit()
            break
        game.handle_player_turn()
        game.handle_enemy_turn()
        

if __name__ == "__main__":
    main()