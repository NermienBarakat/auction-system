import pygame

def bid_screen():
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 750, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Place Your Bid")

    font = pygame.font.Font(None, 36)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((30, 30, 50))
        text = font.render("This is the Bid Screen!", True, (255, 105, 180))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 20))
        pygame.display.flip()

    pygame.quit()