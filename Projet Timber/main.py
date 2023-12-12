import pygame, random

# Initialisation
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

# Chargement des ressources
player_images_right = {
    "normalR": pygame.image.load('./src/lib/persoD.png'),
    "cuttingR1": pygame.image.load('./src/lib/an_axeD.png'),
    "cuttingR2": pygame.image.load('./src/lib/cutD.png')
}
player_images_left = {
    "normalL": pygame.image.load('./src/lib/perso.png'),
    "cuttingL1": pygame.image.load('./src/lib/an_axe.png'),
    "cuttingL2": pygame.image.load('./src/lib/cut.png')
}
tree_image = pygame.image.load('./src/lib/buche.png')
branch_image_right = pygame.image.load('./src/lib/branche.png')
branch_image_left = pygame.image.load('./src/lib/brancheG.png')
background_image = pygame.image.load('./src/lib/fond.png')
overlay_image = pygame.image.load('./src/lib/plan.png')
background_image_50 = pygame.image.load('./src/lib/fond7.png')
overlay_image_50 = pygame.image.load('./src/lib/plan7.png')
background_image_100 = pygame.image.load('./src/lib/fond2.png')
overlay_image_100 = pygame.image.load('./src/lib/plan2.png')
background_image_150 = pygame.image.load('./src/lib/fond3.png')
overlay_image_150 = pygame.image.load('./src/lib/plan3.png')
background_image_200 = pygame.image.load('./src/lib/fond6.png')
overlay_image_200 = pygame.image.load('./src/lib/plan6.png')

hit_sound = pygame.mixer.Sound('./src/sound/move.mp3')

pygame.mixer.music.load('./src/sound/music.mp3')
pygame.mixer.music.set_volume(0.1)  # Réglez à 50% du volume maximum
pygame.mixer.music.play(-1)  # Jouer en boucle

# Redimensionnement des images de fond
background_image = pygame.transform.scale(background_image, (1280, 720))
overlay_image = pygame.transform.scale(overlay_image, (1280, 720))
background_image_50 = pygame.transform.scale(background_image_50, (1280, 720))
overlay_image_50 = pygame.transform.scale(overlay_image_50, (1280, 720))
background_image_100 = pygame.transform.scale(background_image_100, (1280, 720))
overlay_image_100 = pygame.transform.scale(overlay_image_100, (1280, 720))
background_image_150 = pygame.transform.scale(background_image_150, (1280, 720))
overlay_image_150 = pygame.transform.scale(overlay_image_150, (1280, 720))
background_image_200 = pygame.transform.scale(background_image_200, (1280, 720))
overlay_image_200 = pygame.transform.scale(overlay_image_200, (1280, 720))


# Variables du jeu
player_pos = "left"
player_state = "normalL"
cut_animation_counter = 0
tree = ["empty"] * 15
score = 0
best_score = 0
game_over = False
falling_logs = []
falling_buches = []




# Tailles et positions
tree_rect = tree_image.get_rect(midbottom=(640, 720))
player_rect = pygame.Rect(448, 584, 50, 40) if player_pos == "left" else pygame.Rect(699, 584, 50, 40)

#Score Best
def read_best_score():
    try:
        with open('./src/data.txt', 'r') as file:
            return int(file.read())
    except (IOError, ValueError):
        return 0

def save_best_score(score):
    with open('./src/data.txt', 'w') as file:
        file.write(str(score))

best_score = read_best_score()  # Lire le meilleur score au démarrage


# Générer des branches aléatoires
def generate_branch():
    last_branch_side = tree[-1] if len(tree) > 0 else "empty"
    if last_branch_side == "left":
        return random.choice(["left", "empty"])
    elif last_branch_side == "right":
        return random.choice(["right", "empty"])
    else:
        return random.choice(["left", "right", "empty"])

def generate_branches():
    last_branch_side = "empty"
    for i in range(len(tree)):
        if i < 5:
            # Les 5 premières branches sont vides
            tree[i] = "empty"
        else:
            # Générer des branches en évitant les chemins impossibles
            if last_branch_side == "left":
                new_branch = random.choice(["left", "empty"])
            elif last_branch_side == "right":
                new_branch = random.choice(["right", "empty"])
            else:
                new_branch = random.choice(["left", "right", "empty"])
            tree[i] = new_branch
            last_branch_side = new_branch if new_branch != "empty" else last_branch_side


# Fonctions de jeu
def draw_tree():
    for i, branch in enumerate(tree):
        y_pos = 588 - 110 * i
        screen.blit(tree_image, (640 - 50, y_pos - 50))
        if branch != "empty":
            branch_x = 510 if branch == "left" else 833
            branch_image = branch_image_left if branch == "left" else branch_image_right
            branch_rect = branch_image.get_rect(midtop=(branch_x, y_pos - 1))
            screen.blit(branch_image, branch_rect)
            if i == 0 and player_rect.colliderect(branch_rect):
                global game_over
                game_over = True

def player_input():
    global player_pos, player_state, cut_animation_counter, player_rect
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos = "left"
        player_rect = pygame.Rect(448, 584, 50, 40)
        if player_state not in ["cuttingL1", "cuttingL2"]:
            player_state = "cuttingL1"
            cut_animation_counter = 1
    elif keys[pygame.K_RIGHT]:
        player_pos = "right"
        player_rect = pygame.Rect(699, 584, 50, 40)
        if player_state not in ["cuttingR1", "cuttingR2"]:
            player_state = "cuttingR1"
            cut_animation_counter = 1

def update_game():
    global score, cut_animation_counter, player_state, falling_log, falling_buche, game_over, tree, best_score

    last_branch = tree[0] if len(tree) > 0 else "empty"

    if cut_animation_counter > 0:
        cut_animation_counter += 1
        if cut_animation_counter == 5:
            player_state = "cuttingL2" if player_pos == "left" else "cuttingR2"
        elif cut_animation_counter == 10:
            player_state = "normalL" if player_pos == "left" else "normalR"
            cut_animation_counter = 0
            
            if (last_branch != "left" and player_pos == "left") or (last_branch != "right" and player_pos == "right"):
                hit_sound.play()
                # Réduire la taille des images pour l'animation
                falling_log_image = pygame.transform.scale(branch_image_left if last_branch == "left" else branch_image_right, (int(branch_image_left.get_width() * 0.75), int(branch_image_left.get_height() * 0.75)))
                falling_buche_image = pygame.transform.scale(tree_image, (int(tree_image.get_width() * 0.75), int(tree_image.get_height() * 0.75)))

                # Décalage de la position de la branche
                branch_offset_x = -80 if player_pos == "right" else 80

                # Créer l'animation de chute de la branche
                if len(falling_logs) < 8:  # Limiter à 8 animations simultanées

                    falling_logs.append({
                        "image": falling_log_image,
                        "x": 640 + branch_offset_x,
                        "y": 588,
                        "velocity": -15 * 1.6,
                        "side_velocity": -10 * 1.6 if player_pos == "right" else 10 * 1.6,
                        "gravity": 1.5
                    })

               # Créer l'animation de chute de la bûche
                if len(falling_buches) < 8:  # Limiter à 8 animations simultanées

                    falling_buches.append({
                        "image": falling_buche_image,
                        "x": 640,
                        "y": 588,
                        "velocity": -15 * 1.6,
                        "side_velocity": -10 * 1.6 if player_pos == "right" else 10 * 1.6,
                        "gravity": 1.5
                    })

                tree.pop(0)
                new_branch = generate_branch()
                tree.append(new_branch)
                score += 1
                # Check and save best score here
                if score > best_score:
                    best_score = score
                    save_best_score(best_score)
    


def reset_game():
    global score, game_over, tree, falling_log, best_score
    score = 0
    game_over = False
    falling_log = None
    generate_branches()

# Boucle de jeu
while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if not game_over:
        player_input()
        update_game()

        # Sélectionner le fond et l'overlay en fonction du score
        if score >= 200:
            current_background = background_image_200
            current_overlay = overlay_image_200
        elif score >= 150:
            current_background = background_image_150
            current_overlay = overlay_image_150
        elif score >= 100:
            current_background = background_image_100
            current_overlay = overlay_image_100
        elif score >= 50:
            current_background = background_image_50
            current_overlay = overlay_image_50
        else:
            current_background = background_image
            current_overlay = overlay_image
        screen.blit(current_background, (0, 0))
        screen.blit(current_overlay, (0, 0))

        # Mettre à jour et dessiner chaque animation de chute de branche
        for falling_log in falling_logs:
            falling_log["y"] += falling_log["velocity"]
            falling_log["x"] += falling_log["side_velocity"]
            falling_log["velocity"] += falling_log["gravity"]
            if falling_log["y"] <= 720:  # Dessiner tant que l'animation est à l'écran
                screen.blit(falling_log["image"], (falling_log["x"], falling_log["y"]))

        # Supprimer les animations terminées
        falling_logs = [log for log in falling_logs if log["y"] <= 720]

        # Faire de même pour les animations de chute de bûche
        for falling_buche in falling_buches:
            falling_buche["y"] += falling_buche["velocity"]
            falling_buche["x"] += falling_buche["side_velocity"]
            falling_buche["velocity"] += falling_buche["gravity"]
            if falling_buche["y"] <= 720:
                screen.blit(falling_buche["image"], (falling_buche["x"], falling_buche["y"]))

        falling_buches = [buche for buche in falling_buches if buche["y"] <= 720]

        draw_tree()
        player_image_set = player_images_left if player_pos == "left" else player_images_right
        screen.blit(player_image_set[player_state], player_rect)
        font = pygame.font.SysFont(None, 48)
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        best_score_text = font.render(f'Best: {best_score}', True, (255, 0, 0))
        screen.blit(score_text, (10, 10))
        screen.blit(best_score_text, (10, 30)) 
    else:
        font = pygame.font.SysFont(None, 48)
        game_over_text = font.render('Game Over', True, (255, 0, 0))
        screen.blit(game_over_text, (640 - game_over_text.get_width() / 2, 360 - game_over_text.get_height() / 2))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            reset_game()
    pygame.display.update()
    clock.tick(60)
