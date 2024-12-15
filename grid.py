import pygame 

# Définition des constantes
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

TILE_SIZE = 45  # Taille d'une case (en pixels)


class Grill:
    """
    Classe pour générer la grille du terrain avec une image de fond.
    """

    def __init__(self, monde_type, taille):
        """
        :param monde_type: 1, 2 type de monde
        :param taille: "petite" pour 10x10, "grande" pour 17x17
        """
        self.monde_type = monde_type
        self.taille = taille
        self.grid, self.image, self.size = self.generer_monde()

    def generer_monde(self):
        """
        Génère la grille et son image en fonction du type de monde et de la taille.
        """
        # Création des grilles logiques
        monde_1_10 = [["passage_vert"] * 7 + ["arbre", "passage_vert", "healing_zone"],
            ["mur"] +["passage_vert"] + [ "mur"]+ ["passage_vert"]*2 + ["mer","passage_vert"] + ["arbre"]*2 + ["passage_vert"],
            ["passage_vert"] * 2 + ["passage_vert"] * 8 ,
            ["passage_vert"] * 6 + ["mer"] + ["passage_vert"] * 3 , 
            ["passage_vert","arbre","passage_vert","arbre", "mer","arbre"] +["passage_vert"]*3+["mer"],
            ["arbre"],["passage_vert"]*2,["arbre", "mer","arbre"] +["passage_vert"]*2+["mer"]+["passage_vert"],
            ["passage_vert"] *7 ,["mer"],["passage_vert"] *2,
            ["passage_vert"] * 10,
            ["passage_vert"] + ["mur"]  + ["passage_vert"] * 6 +["mur"]*2,
            ["healing_zone"] + ["mur"] +  ["passage_vert"] * 2+ ["mer"]*2 + ["passage_vert"] *4
            ]  
        monde_2_10 = monde_1_10
        

        monde_1_17 = [["passage_vert"] * 13 + ["arbre", "mur", "healing_zone", "passage_vert"],
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
        monde_2_17 = monde_1_17
        

        # Sélection de la grille et de sa taille
        if self.taille == "petite":
            size = 10
            if self.monde_type == 1:
                grid = monde_1_10
                try:
                    image = pygame.image.load(r"Grids/grid_10_1.png")
                    image = pygame.transform.scale(image, (size * TILE_SIZE, size * TILE_SIZE))
                except pygame.error as e:
                   raise FileNotFoundError(f"Erreur lors du chargement de l'image de la grille : {e}")


            elif self.monde_type == 2:
                grid = monde_2_10

                try:
                    image = pygame.image.load(r"Grids/grid_10_2.png")
                    image = pygame.transform.scale(image, (size * TILE_SIZE, size * TILE_SIZE))
                except pygame.error as e:
                   raise FileNotFoundError(f"Erreur lors du chargement de l'image de la grille : {e}")


            else:
                raise ValueError("Type de monde invalide. Choisissez entre 1, 2 ou 3.")
            
        elif self.taille == "grande":
            size = 17
            if self.monde_type == 1:
                grid = monde_1_17

                try:
                    image = pygame.image.load(r"Grids/grid_17_1.png")
                    image = pygame.transform.scale(image, (size * TILE_SIZE, size * TILE_SIZE))
                except pygame.error as e:
                   raise FileNotFoundError(f"Erreur lors du chargement de l'image de la grille : {e}")



            elif self.monde_type == 2:
                grid = monde_2_17

                try:
                    image = pygame.image.load(r"Grids/grid_17_2.png")
                    image = pygame.transform.scale(image, (size * TILE_SIZE, size * TILE_SIZE))
                except pygame.error as e:
                   raise FileNotFoundError(f"Erreur lors du chargement de l'image de la grille : {e}")
            
            else:
                raise ValueError("Type de monde invalide. Choisissez entre 1, 2 ou 3.")
        else:
            raise ValueError("Taille invalide. Utilisez 'petite' ou 'grande'.")

        return grid, image, size

