import pygame
import random

from abc import ABC, abstractmethod

# Push Emi 07/12 16h45
# Constantes
GRID_SIZE = 17
CELL_SIZE = 45
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)


class Unit(ABC):
    """
    Classe pour représenter une unité.

    ...
    Attributs
    ---------
    x : int
        La position x de l'unité sur la grille.
    y : int
        La position y de l'unité sur la grille.
    health : int
        La santé de l'unité.
    attack_power : int
        La puissance d'attaque de l'unité.
    team : str
        L'équipe de l'unité ('player' ou 'enemy').
    is_selected : bool
        Si l'unité est sélectionnée ou non.

    Méthodes
    --------
    move(dx, dy)
        Déplace l'unité de dx, dy.
    attack(target)
        Attaque une unité cible.
    draw(screen)
        Dessine l'unité sur la grille.
    """

    def __init__(self, x, y, health, attack_power, team, grid, attack_range=1, image=None):
        """
        Construit une unité avec une position, une santé, une puissance d'attaque et une équipe.

        Paramètres
        ----------
        x : int
            La position x de l'unité sur la grille.
        y : int
            La position y de l'unité sur la grille.
        health : int
            La santé de l'unité.
        attack_power : int
            La puissance d'attaque de l'unité.
        team : str
            L'équipe de l'unité ('player' ou 'enemy').
        """
        self.x = x
        self.y = y
        self.health = health
        self.max_health = health 
        self.attack_power = attack_power
        self.team = team  # 'player' ou 'enemy'
        self.is_selected = False
        self.grid = grid  # La grille est maintenant un attribut de l'unité
        self.attack_range = attack_range
        self.attack_types = [
            {"name": "Basic Attack", "power": self.attack_power, "range": self.attack_range},   # Dictionnaire pour le nom des attaques, puissance et leur portée
            {"name": "Special Attack", "power": self.attack_power * 2, "range": self.attack_range // 2}
            ]
        self.image = image  # Image associée à l'unité
        
    def move(self, dx, dy):
        """Déplace l'unité de dx, dy."""
        # Vérifier les limites et le type de terrain
        if 0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE:
            if self.grid[self.y + dy][self.x + dx] not in ["mur", "arbre", "mer"]:  # Éviter les obstacles
                self.x = self.x + dx
                self.y = self.y + dy
    #@abstractmethod
    def attack(self, target, attack_type=0):
        """Attaque une unité cible."""
        """Attaque une unité cible."""
        distance_x = abs(self.x - target.x)
        distance_y = abs(self.y - target.y)
        attack_range = self.attack_types[attack_type]["range"]
        attack_power = self.attack_types[attack_type]["power"]

        if distance_x <= attack_range and distance_y <= attack_range:
            target.health -= attack_power

    def draw(self, screen):
        """Affiche l'unité avec son image si elle est définie."""
        # Définir la couleur de la case en fonction de l'équipe
        case_color = BLUE if self.team == 'player' else RED

        # Dessiner la case colorée derrière l'unité
        pygame.draw.rect(screen, case_color, 
                     (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        if self.image:
            # Position centrée dans la case
            img_rect = self.image.get_rect(center=(
                self.x * CELL_SIZE + CELL_SIZE // 2,
                self.y * CELL_SIZE + CELL_SIZE // 2
            ))
            screen.blit(self.image, img_rect)
        else:    
            """Affiche l'unité cercle sur l'écran."""
            color = BLUE if self.team == 'player' else RED
            pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //2, 
                                               self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
        
        # Dessiner la barre de vie
        max_health = self.max_health  # Valeur maximale de santé de l'unité
        bar_width = CELL_SIZE - 10  # Largeur totale de la barre
        bar_height = 5  # Hauteur de la barre
        health_ratio = self.health / max_health  # Proportion de santé restante
        
        # Calcul de la position et de la taille de la barre
        bar_x = self.x * CELL_SIZE + 5  # Décalage pour centrer la barre dans la case
        bar_y = self.y * CELL_SIZE + 35 # Position en-dessous de l'unité sur la même case
        bar_current_width = int(bar_width * health_ratio)
        
        # Barre de vie (fond en rouge, santé restante en vert)
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))  # Fond rouge
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, bar_current_width, bar_height))  # Santé verte
        
    @abstractmethod
    def get_attackable_cells(self):
        """Retourne une liste des cases que cette unité peut attaquer."""
        pass

class Archer(Unit):
    def __init__(self, x, y, team, grid):
        """
        Crée un archer avec une portée d'attaque de 2 cases et une santé élevée.
        """
        image = pygame.image.load("images/archer.png").convert_alpha()  # Charge l'image
        image = pygame.transform.scale(image, (CELL_SIZE-3, CELL_SIZE-3))  # Ajuste à la taille de la case
        super().__init__(x, y, health=15, attack_power=2, team=team, grid=grid, attack_range=2, image=image)
        self.attack_types = [
            {"name": "Arrow Shot", "power": self.attack_power, "range": self.attack_range}, # Attaque normale
            {"name": "Power Arrow", "power": self.attack_power * 2, "range": 2}  # Spécial, portée réduite à 2 cases
        ]      

    def get_attackable_cells(self):
        """Retourne une liste des cases que cette unité peut attaquer."""
        cells=[]
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  
            for step in range(1, self.attack_range + 1): 
                new_x = self.x + dx * step
                new_y = self.y + dy * step
                if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
                    cells.append((new_x, new_y))
        return cells
           
class Swordsman(Unit):
    def __init__(self, x, y, team, grid):
        """
        Crée un épeiste avec une portée d'attaque de 1 case et une santé faible.
        """
        image = pygame.image.load("images/swordsman.png").convert_alpha()  # Charge l'image
        image = pygame.transform.scale(image, (CELL_SIZE-3, CELL_SIZE-3))  # Ajuste à la taille de la case
        super().__init__(x, y, health=10, attack_power=3, team=team, grid=grid, attack_range=1, image=image)
        self.attack_types = [
            {"name": "Sword Slash", "power": self.attack_power, "range": self.attack_range}, # Attaque normale
            {"name": "Heavy Strike", "power": self.attack_power * 2, "range": 1}  # Puissant mais petite portée
        ]
    def get_attackable_cells(self):
        """Retourne une liste des cases que cette unité peut attaquer."""
        cells=[]
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  
            for step in range(1, self.attack_range + 1): 
                new_x = self.x + dx * step
                new_y = self.y + dy * step
                if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
                    cells.append((new_x, new_y))
        return cells
           


class Wizard (Unit):
    def __init__(self, x, y, team, grid):
       """
       Crée un sorcier capable d'attaquer à un portée circulaire de 2 cases et de marcher sur l'eau.
       """
       image = pygame.image.load("images/wizard.png").convert_alpha()  # Charge l'image
       image = pygame.transform.scale(image, (CELL_SIZE-3, CELL_SIZE-3))  # Ajuste à la taille de la case
       super().__init__(x, y, health=12, attack_power=4, team=team, grid=grid, attack_range=2, image=image)
       
       # Attaques
       self.attack_types = [
           {"name": "Gladio", "power": self.attack_power, "range": self.attack_range},  # Attaque normale
           {"name": "Incendio", "power": self.attack_power * 2, "range": self.attack_range}  # Attaque puissante
       ]

    def move(self, dx, dy):
       """Déplace le magicien de 2 cases ou 1, même sur l'eau."""
       new_x = self.x + dx
       new_y = self.y + dy
       if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
           if self.grid[new_y][new_x] not in ["mur", "arbre"]:
               self.x = new_x
               self.y = new_y
               return  
        

    def heal(self):
       """Ajoute 4 points de vie au magicien."""
       self.health = min(self.max_health, self.health + 4)  # Santé maximale
    
    def get_attackable_cells(self):
        #Retourne une liste des cases que cette unité peut attaquer.
        cells = []
        grid_size = len(self.grid)  # Taille de la grille

        # Liste des décalages pour les cases attaquables
        offsets = [
            (0, -2), (0, -1), (0, 1), (0, 2),
            (-1, -1), (-1, 0), (-1, 1),
            (1, -1), (1, 0), (1, 1),
            (-2, 0), (2, 0)
        ]

        for dx, dy in offsets:
            new_x = self.x + dx
            new_y = self.y + dy

            # Vérifie si la case est valide (dans les limites de la grille)
            if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
                cells.append((new_x, new_y))
        
        return cells

class Invincible(Unit):
    def __init__(self, x, y, team, grid):
            """
            Crée une unité invincible qui ne perd pas de vie.
            """
            image = pygame.image.load("images/invincible.png").convert_alpha()  
            image = pygame.transform.scale(image, (CELL_SIZE-3, CELL_SIZE-3))  
            super().__init__(x, y, health=40, attack_power=4, team=team, grid=grid, attack_range=1, image=image)
            
            # Attaque sur une portée 1 case en direction circulaire et 3 cases sur une direction
            self.attack_types = [
                {"name": "Big Slash", "power": self.attack_power, "range": self.attack_range},  # Attaque circulaire 1 case
                {"name": "Two Blades Style", "power": self.attack_power, "range": 2} # Attaque circulaire 2 cases
            ]
            
    def get_attackable_cells(self):
            """
            Retourne les cases attaquables selon le type d'attaque :
            - attack_type 0 : Big Slash (circulaire).
            - attack_type 1 : Two Blades Style ( circulaire).
            """
            cells = []

            for dx in range(-1, 2):  # -1 à +1 pour couvrir les cases autour circulaire
                for dy in range(-1, 2):
                    new_x = self.x + dx
                    new_y = self.y + dy
                    if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:  # Vérifier les limites de la grille
                        cells.append((new_x, new_y))
                           
            return cells