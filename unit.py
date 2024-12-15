import pygame
import random

from abc import ABC, abstractmethod

# Push Emi 13/12 22h45

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
            {"name": "Special Attack", "power": self.attack_power, "range": self.attack_range}
            ]
        self.image = image  # Image associée à l'unité
        
    def move(self, dx, dy):
        """Déplace l'unité de dx, dy."""
        # Vérifier les limites et le type de terrain
        if 0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE:
            if self.grid[self.y + dy][self.x + dx] not in ["mur", "arbre", "mer"]:  # Éviter les obstacles
                self.x = self.x + dx
                self.y = self.y + dy
                if self.grid[self.y][self.x] in ["healing_zone"] and self.health < self.max_health:  
                    self.health += 1  # Increment health 
                
    #@abstractmethod
    def attack(self, target, attack_type=0):
        """Attaque une unité cible."""
        distance_x = abs(self.x - target.x)
        distance_y = abs(self.y - target.y)
        attack_range = self.attack_types[attack_type]["range"]
        attack_power = self.attack_types[attack_type]["power"]

        if distance_x <= attack_range and distance_y <= attack_range:
            target.health -= attack_power

    def draw(self, screen):
        """Affiche l'unité avec son image"""
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

        
        # Dessiner la barre de vie
        max_health = self.max_health  # Valeur maximale de santé de l'unité
        bar_width = CELL_SIZE - 10  # Largeur totale de la barre
        bar_height = 5  # Hauteur de la barre
        health_ratio = self.health / max_health  # ratio de santé restante
        
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
        Crée un archer avec 2 attaques de portées et puissances différentes 
        """
        image = pygame.image.load("images/archer.png").convert_alpha()  # Charge l'image
        image = pygame.transform.scale(image, (CELL_SIZE-3, CELL_SIZE-3))  # Ajuste à la taille de la case
        super().__init__(x, y, health=15, attack_power=2, team=team, grid=grid, attack_range=3, image=image)
        self.attack_types = [
            {"name": "Arrow Shot", "power": self.attack_power, "range": self.attack_range}, # Attaque normale
            {"name": "Power Arrow", "power": self.attack_power * 2, "range": self.attack_range-1}  # Spécial, portée réduite à 2 cases
        ]      

    def get_attackable_cells(self,attack_type=0):
        """
        Retourne une liste des cases en direction cardinale.
        """
       
        cells = []
        attack_range = self.attack_types[attack_type]["range"]
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Cardinal directions
        
        for dx, dy in directions:
            for step in range(2, attack_range + 1):
                new_x, new_y = self.x + dx * step, self.y + dy * step
                if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
                    cells.append((new_x, new_y))

        return cells
           
class Swordsman(Unit):
    def __init__(self, x, y, team, grid):
        """
        Crée un épeiste avec 2 attaques de portées et puissances différentes.
        """
        image = pygame.image.load("images/swordsman.png").convert_alpha()  # Charge l'image
        image = pygame.transform.scale(image, (CELL_SIZE-3, CELL_SIZE-3))  # Ajuste à la taille de la case
        super().__init__(x, y, health=10, attack_power=3, team=team, grid=grid, attack_range=1, image=image)
        self.attack_types = [
            {"name": "Sword Slash", "power": self.attack_power, "range": self.attack_range}, # Attaque normale
            {"name": "Heavy Strike", "power": self.attack_power * 2, "range": self.attack_range}  # Puissant mais petite portée
        ]
        
    def get_attackable_cells(self,attack_type=0):
        """
        Retourne une liste des cases en direction cardinale.
        """
    
        cells = []
        attack_range = self.attack_types[attack_type]["range"]
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Cardinal directions

        for dx, dy in directions:
            for step in range(1, attack_range + 1):
                new_x, new_y = self.x + dx * step, self.y + dy * step
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
       """Déplace le magicien sur l'eau."""
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
    
    def get_attackable_cells(self,attack_type=0):
        """
        Retourne une liste des cases attaquables dispersées
        """
        cells = []
        attack_range = self.attack_types[attack_type]["range"]

        # Générer des cases dans la portée de l'attaque
        for dx in range(-attack_range, attack_range + 1):
            for dy in range(-attack_range, attack_range + 1):
                new_x, new_y = self.x + dx, self.y + dy
                if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
                    # Filtrer selon le type d'attaque 
                    if abs(dx) + abs(dy) <= attack_range:
                        cells.append((new_x, new_y))

        return cells

class Invincible(Unit):
    def __init__(self, x, y, team, grid):
            """
            Crée une unité invincible qui ne perd très peu de vie.
            """
            image = pygame.image.load("images/invincible.png").convert_alpha()  
            image = pygame.transform.scale(image, (CELL_SIZE-3, CELL_SIZE-3))  
            super().__init__(x, y, health=40, attack_power=4, team=team, grid=grid, attack_range=1, image=image)
            
            # Attaque sur une portée 1 case en direction circulaire et 3 cases sur une direction
            self.attack_types = [
                {"name": "Big Slash", "power": self.attack_power, "range": self.attack_range},  # Attaque circulaire 1 case
                {"name": "Two Blades Style", "power": self.attack_power*0.5, "range": self.attack_range*2} # Attaque circulaire 2 cases
            ]
            
    def get_attackable_cells(self,attack_type=0):
            """
            Retourne les cases attaquables direction circulaire
            """
            cells = []
            attack_range = self.attack_types[attack_type]["range"]
            directions = [(0, -1), (0, 1), (-1, 0), (-1, -1), (1, 0), (1, -1), (1, 1), (-1, 1),
                          (-2, -2), (-2,-1), (-2,0),(-2,1),(-2,2),
                          (-1,-2),(-1,2),(0,-2),(0,2),(1,-2),(1,2),
                          (2,-2),(2,-1),(2,0),(2,1),(2,2)]  

            for dx, dy in directions:
                    new_x, new_y = self.x + dx, self.y + dy
                    if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
                        cells.append((new_x, new_y))

            return cells

class Bomber(Unit):
    def __init__(self, x, y, team, grid):
            """
            Crée une unité bombardier qui lance des bombes.
            """
            image = pygame.image.load("images/bomber.png").convert_alpha()  
            image = pygame.transform.scale(image, (CELL_SIZE-3, CELL_SIZE-3))  
            super().__init__(x, y, health=15, attack_power=5, team=team, grid=grid, attack_range=3, image=image)
            
            # Attaque sur une portée 5 cases dispersée
            self.attack_types = [
                {"name": "Aqua Bomb", "power": self.attack_power, "range": self.attack_range}, 
                {"name": "Lava bomb", "power": self.attack_power*1.5, "range": self.attack_range*2} 
            ]

    def get_attackable_cells(self,attack_type=0):
        """
        Retourne une liste des cases attaquables loin de l'unité.
        """
        cells = []
        attack_range = self.attack_types[attack_type]["range"]
        min_distance = max(1, attack_range // 2)  # Exclure les cases proches

        for dx in range(-attack_range, attack_range + 1):
            for dy in range(-attack_range, attack_range + 1):
                distance = abs(dx) + abs(dy)
                if min_distance <= distance <= attack_range:  # Garder les cases éloignées
                    new_x, new_y = self.x + dx, self.y + dy
                    if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
                        cells.append((new_x, new_y))

        return cells

