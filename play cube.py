import pygame
import random
import time

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
largeur, hauteur = 800, 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Jeu avec Obstacles et Timer")

# Couleurs
blanc = (255, 255, 255)
noir = (0, 0, 0)
gris = (169, 169, 169)
vert = (0, 255, 0)
rouge = (255, 0, 0)
marron = (139, 69, 19)

# Police pour le timer
font = pygame.font.Font(None, 36)

# Dimensions du personnage
personnage_largeur = 40
personnage_hauteur = 40

# Position initiale
spawn_x, spawn_y = largeur // 2, hauteur - 30 - personnage_hauteur
x, y = spawn_x, spawn_y

# Vitesse et gravité
vitesse_x = 5
vitesse_y = 0
gravite = 0.5
impulsion_saut = -12
au_sol = True

# Obstacles
obstacles = []
vitesse_obstacle = 5
intervalle_obstacle = 150  # Intervalle en frames entre chaque obstacle
frame_counter = 0  # Compteur de frames

# Timer
debut_temps = time.time()  # Temps de début du jeu

# Fonction pour dessiner le personnage
def dessiner_brique(surface, x, y):
    pygame.draw.rect(surface, gris, (x, y, personnage_largeur, personnage_hauteur))

# Fonction pour dessiner les obstacles
def dessiner_obstacle(surface, obstacle):
    pygame.draw.rect(surface, rouge, (obstacle["x"], obstacle["y"], obstacle["largeur"], obstacle["hauteur"]))

# Réinitialiser la position du joueur
def respawn():
    global x, y, vitesse_y, au_sol, vitesse_obstacle
    x, y = spawn_x, spawn_y
    vitesse_y = 0
    au_sol = True
    vitesse_obstacle = 5  # Réinitialise la vitesse des obstacles

# Boucle principale
clock = pygame.time.Clock()
en_cours = True
while en_cours:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False

    # Récupération des touches
    touches = pygame.key.get_pressed()

    # Saut
    if touches[pygame.K_UP] and au_sol:
        vitesse_y = impulsion_saut
        au_sol = False

    # Gravité
    vitesse_y += gravite
    y += vitesse_y

    # Vérification des limites verticales (sol)
    if y >= hauteur - 30 - personnage_largeur:
        y = hauteur - 30 - personnage_largeur
        vitesse_y = 0
        au_sol = True

    # Génération d'obstacles
    frame_counter += 1
    if frame_counter >= intervalle_obstacle:
        frame_counter = 0
        hauteur_obstacle = random.randint(50, 120)  # Hauteur de l'obstacle
        obstacle = {
            "x": largeur,
            "y": hauteur - 30 - hauteur_obstacle,
            "largeur": random.randint(30, 50),  # Largeur de l'obstacle
            "hauteur": hauteur_obstacle,
        }
        obstacles.append(obstacle)

    # Déplacement des obstacles
    for obstacle in obstacles[:]:
        obstacle["x"] -= vitesse_obstacle
        if obstacle["x"] + obstacle["largeur"] < 0:
            obstacles.remove(obstacle)

    # Collision avec les obstacles
    for obstacle in obstacles:
        if (
            x < obstacle["x"] + obstacle["largeur"] and
            x + personnage_largeur > obstacle["x"] and
            y < obstacle["y"] + obstacle["hauteur"] and
            y + personnage_hauteur > obstacle["y"]
        ):
            respawn()  # Respawn si collision
            obstacles.clear()  # Supprime les obstacles existants

    # Augmentation progressive de la vitesse des obstacles
    vitesse_obstacle += 0.001

    # Remplir l'écran
    fenetre.fill(blanc)

    # Dessiner le sol
    pygame.draw.rect(fenetre, vert, (0, hauteur - 30, largeur, 30))
    pygame.draw.rect(fenetre, marron, (0, hauteur - 20, largeur, 20))

    # Dessiner le personnage
    dessiner_brique(fenetre, x, y)

    # Dessiner les obstacles
    for obstacle in obstacles:
        dessiner_obstacle(fenetre, obstacle)

    # Afficher le timer
    temps_ecoule = time.time() - debut_temps
    texte_timer = font.render(f"Temps : {int(temps_ecoule)} s", True, noir)
    fenetre.blit(texte_timer, (largeur - 200, 20))

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Limiter la vitesse de la boucle
    clock.tick(60)

# Quitter Pygame
pygame.quit()
