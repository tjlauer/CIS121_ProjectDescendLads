import pygame
import random

class Player():
    def __init__(self, indx, x, y, width, height, color, kick, kickCheck):
        self.indx = indx
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.kick = kick
        self.kickCheck = kickCheck
        self.gravity = 0.25
        self.velXMax = 12
        self.velYMax = 10
        self.velThresh = 0.05
        self.acc = 0.5
        self.accDrag = 0.1
        self.velY = 0
        self.velX = 0
        self.velXKick = 0


    def draw(self, win, myfont):
        pygame.draw.rect(win, self.color, self.rect)
        if self.kick == 1:
            # print("Kick Left")
            pygame.draw.rect(win, (0, 0, 0), (self.x - self.width, self.y, self.width, self.height))
        elif self.kick == 2:
            # print("Kick Up")
            pygame.draw.rect(win, (0, 0, 0), (self.x, self.y - self.height, self.width, self.height))
        elif self.kick == 3:
            # print("Kick Right")
            pygame.draw.rect(win, (0, 0, 0), (self.x + self.width, self.y, self.width, self.height))

        win.blit(myfont.render(str(self.indx + 1), False, (0, 0, 0)), (self.x, self.y))


    def move(self, playerKicked):

        if playerKicked == 1:
            self.velX = -self.velXMax
        elif playerKicked == 2:
            self.velY = -self.velYMax
        elif playerKicked == 3:
            self.velX = self.velXMax

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:  # K_LEFT
            self.velX -= self.acc
            # self.x -= self.velX
        if keys[pygame.K_d]:  # K_RIGHT
            self.velX += self.acc
            # self.x += self.velX

        if (keys[pygame.K_a] and keys[pygame.K_a]) or (~keys[pygame.K_a] and ~keys[pygame.K_a]):
            if self.velX > self.velThresh:
                self.velX -= self.accDrag
            elif self.velX < -self.velThresh:
                self.velX += self.accDrag
            else:
                self.velX = 0

        # if keys[pygame.K_w]:  # K_UP
        #     self.velY -= self.acc
        #     # self.y -= self.velY
        # elif keys[pygame.K_s]:  # K_DOWN
        #     self.velY += self.acc
        #     # self.y += self.velY
        # else:
        #     if self.velY > self.velThresh:
        #         self.velY -= self.accDrag
        #     elif self.velY < -self.velThresh:
        #         self.velY += self.accDrag
        #     else:
        #         self.velY = 0

        if keys[pygame.K_SPACE] and self.velY == 0:
            self.velY -= (1.25 * self.velYMax)

        self.velY += self.gravity

        if self.velX > self.velXMax:
            self.velX = self.velXMax
        elif self.velX < -self.velXMax:
            self.velX = -self.velXMax

        # if self.velY > self.velMax:
        #     self.velY = self.velMax
        # elif self.velY < -self.velMax:
        #     self.velY = -self.velMax

        if 256 <= (self.x + self.width + self.velX) and (self.x + self.velX) <= 1024:
            if 519 >= (self.y + self.height) and (self.y + self.height + self.velY) > 519:
                self.velY = 0
                self.y = 519 - self.height

        self.x += self.velX
        self.y += self.velY

        if self.y > 720:
            self.y = -50
            self.x = random.randint(256, 1024)
            self.velX = 0
            self.velY = 0

        self.update()

    def kickAction(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and not(keys[pygame.K_UP]) and not(keys[pygame.K_RIGHT]):
            self.kick = 1
        elif not(keys[pygame.K_LEFT]) and not(keys[pygame.K_UP]) and keys[pygame.K_RIGHT]:
            self.kick = 3
        elif not(keys[pygame.K_LEFT]) and keys[pygame.K_UP] and not(keys[pygame.K_RIGHT]):
            self.kick = 2
        else:  # elif not(keys[pygame.K_LEFT]) and not(keys[pygame.K_UP]) and not(keys[pygame.K_RIGHT])
            self.kick = 0


    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)