import pygame
import random

from unit import *

# Définir les constantes
TILE_SIZE = 35  # Taille d'une case (en pixels)
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



# Classe Game
class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player_units = [Unit(0, 0, 10, 2, 'player',grid),  # Case (1,1)
                     Unit(1, 0, 10, 2, 'player',grid)]  # Case (1,2)

        self.enemy_units = [Unit(16, 16, 8, 1, 'enemy',grid),  # Case (17,17)
                    Unit(15, 16, 8, 1, 'enemy',grid)]  # Case (17,16)


    def handle_player_turn(self):
        for selected_unit in self.player_units:
            has_acted = False
            selected_unit.is_selected = True
            self.flip_display()

            while not has_acted:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.KEYDOWN:
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
                        self.flip_display()

                        if event.key == pygame.K_SPACE:
                            for enemy in self.enemy_units:
                                if abs(selected_unit.x - enemy.x) <= 1 and abs(selected_unit.y - enemy.y) <= 1:
                                    selected_unit.attack(enemy)
                                    if enemy.health <= 0:
                                        self.enemy_units.remove(enemy)
                            has_acted = True
                            selected_unit.is_selected = False

    def handle_enemy_turn(self):
        for enemy in self.enemy_units:
            target = random.choice(self.player_units)
            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
            enemy.move(dx, dy)
            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                enemy.attack(target)
                if target.health <= 0:
                    self.player_units.remove(target)

    def flip_display(self):
        self.screen.blit(grid_image, (0, 0))  # Afficher l'image de la grille
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)
        pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Mon jeu avec grille PNG")
    game = Game(screen)

    while True:
        game.handle_player_turn()
        game.handle_enemy_turn()

if __name__ == "__main__":
    main()
