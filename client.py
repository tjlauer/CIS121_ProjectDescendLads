import pygame
from network import Network


width = 1280
height = 720

pygame.font.init()
myfont = pygame.font.SysFont('Times New Roman', 30)

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


def redrawWindow(p2):
    win.fill((255, 255, 255))

    pygame.draw.rect(win, (0, 0, 0), (256, 519, 768, 50))

    for player in p2:
        player.draw(win, myfont)

    pygame.display.update()


def main():
    run = True
    n = Network()
    p = n.getP()
    pygame.display.set_caption("Player "+str(p.indx + 1))
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)

        p2 = n.send(p)

        playerKicked = 0

        for player in p2:
            if player.kick == 1:
                if ((player.x - player.width) <= (p.x + p.width) < player.x) and ((p.y <= player.y + player.height) and (p.y + p.height) >= player.y):
                    playerKicked = 1
            if player.kick == 2:
                if ((p.x <= player.x + player.width) and (p.x + p.width) >= player.x) and ((player.y - player.height) <= (p.y + p.height) < player.y):
                    playerKicked = 2
            if player.kick == 3:
                if ((player.x + player.width) <= p.x < (player.x + (2 * player.width))) and ((p.y <= player.y + player.height) and (p.y + p.height) >= player.y):
                    playerKicked = 3

        p.move(playerKicked)
        p.kickAction()

        redrawWindow(p2)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            run = False
            pygame.quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                break

        if p.kick != p.kickCheck:
            p.kickCheck = p.kick


main()
