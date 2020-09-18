import pygame
import random


# Create the "Player" class. This is the code that every character runs.
class Player:
    # Initialize the character with data sent by the server when the client first connected
    def __init__(self, indx, x, y, width, height, color, kick, kickCheck):
        # The player index and the position in the "p2" array of the current character
        self.indx = indx
        # The X-Axis position of the top-left corner of the character for the initial spawn
        self.x = x
        # The Y-Axis position of the top-left corner of the character for the initial spawn.
        # NOTE: The Y-Axis is weird. The top of the window is 0, and increases as you move towards to bottom of the window.
        self.y = y
        # The width of the character and it's kick zone
        self.width = width
        # The height of the character and it's kick zone
        self.height = height
        # The random color assigned to the character
        self.color = color
        # This is the actual shape of the character itself. This is used when drawing the character onto the window.
        self.rect = (x, y, width, height)
        # Stores whether or not the character is currently kicking
        self.kick = kick
        # Stores the value of kick from the previous frame
        self.kickCheck = kickCheck
        # This is the downward acceleration of the characters
        self.gravity = 0.25
        # This is the maximum velocity a character can travel along the X-Axis. Possible X-Axis velocities are [-velXMax, velXMax]
        self.velXMax = 12
        # This is the maximum velocity a character can travel along the Y-Axis. Possible Y-Axis velocities are [-velYMax, velYMax]
        self.velYMax = 10
        # If the magnitude of the character velocity falls below this threshold, the velocity is set to zero. This prevents drifting.
        self.velThresh = 0.05
        # This is the value added to / subtracted from the X-Axis Velocity while the left or right keys are being pressed.
        self.acc = 0.5
        # This is the rate at which the character will slow down along the X-Axis. Think of it as friction from the floor.
        self.accDrag = 0.1
        # This stores the current Y-Axis velocity of the character.
        self.velY = 0
        # This stores the current X-Axis velocity of the character.
        self.velX = 0

    # Function used to draw the character itself, as well as a box showing the kick zone if the character is currently kicking
    def draw(self, win, myfont):
        # Draw the character onto the window "win" with the color "self.color" as specified in "self.rect"
        pygame.draw.rect(win, self.color, self.rect)

        # If the character is currently kicking to the LEFT
        if self.kick == 1:  # print("Kick Left")
            # Draw the kick zone to the LEFT of the character
            pygame.draw.rect(win, (0, 0, 0), (self.x - self.width, self.y, self.width, self.height))

        # If the character is currently kicking UP
        if self.kick == 2:  # print("Kick Up")
            # Draw the kick zone ABOVE the character
            pygame.draw.rect(win, (0, 0, 0), (self.x, self.y - self.height, self.width, self.height))

        # If the character is currently kicking to the RIGHT
        if self.kick == 3:  # print("Kick Right")
            # Draw the kick zone to the RIGHT of the character
            pygame.draw.rect(win, (0, 0, 0), (self.x + self.width, self.y, self.width, self.height))

        # Add black text of the character's (indx+1) using "myfont" on top of the character
        win.blit(myfont.render(str(self.indx + 1), False, (0, 0, 0)), (self.x, self.y))

    # Function does all of the fun math on how the physically move the character, as well as pixel-perfect collision detection for the platform
    def move(self, playerKicked):

        # If the character has been kicked to the LEFT, set it's X-Axis velocity to MAX in the LEFT direction.
        if playerKicked == 1:
            self.velX = -self.velXMax

        # If the character has been kicked UP, set it's Y-Axis velocity to MAX in the UPWARDS direction.
        if playerKicked == 2:
            self.velY = -self.velYMax

        # If the character has been kicked to the RIGHT, set it's X-Axis velocity to MAX in the RIGHT direction.
        if playerKicked == 3:
            self.velX = self.velXMax

        # Get a dictionary of all keyboard keys that contains if the specified key is currently pressed (True) or not (False)
        keys = pygame.key.get_pressed()

        # If the "A" key is being pressed, accelerate to the left by subtracting from the X-Axis velocity
        if keys[pygame.K_a]:  # K_LEFT
            self.velX -= self.acc

        # If the "D" key is being pressed, accelerate to the right by adding to the X-Axis velocity
        if keys[pygame.K_d]:  # K_RIGHT
            self.velX += self.acc

        # NOTE: By having the "A" and "D" keypress checks as separate if statements, they cancel each other out if both are being pressed.
        #       This results in zero net-change in X-Axis velocity.

        # If both "A" and "D" are being pressed, OR if neither "A" and "D" are being pressed
        if (keys[pygame.K_a] and keys[pygame.K_a]) or (~keys[pygame.K_a] and ~keys[pygame.K_a]):
            # If the X-Axis velocity is towards the right (positive)
            if self.velX > self.velThresh:
                # Apply drag to the left (subtract) to slow down the character
                self.velX -= self.accDrag

            # If the X-Axis velocity is towards the left (negative)
            elif self.velX < -self.velThresh:
                # Apply drag to the right (add) to slow down the character
                self.velX += self.accDrag

            # If the magnitude of the X-Axis velocity is below the threshold, set the X-Axis velocity to zero.
            else:
                self.velX = 0

        # If the Y-Axis velocity is zero (i.e. character is on the platform) and the space bar is pressed
        if keys[pygame.K_SPACE] and self.velY == 0:
            # Make the character jump by setting the Y-Axis velocity
            self.velY -= (1.25 * self.velYMax)

        # Add gravity to the Y-Axis velocity
        self.velY += self.gravity

        # If the X-Axis velocity was calculated to go above MAX
        if self.velX > self.velXMax:
            # Set X-Axis velocity to MAX
            self.velX = self.velXMax

        # If the X-Axis velocity was calculated to go below -MAX
        elif self.velX < -self.velXMax:
            # Set X-Axis velocity to -MAX
            self.velX = -self.velXMax

        # If the character is within the bounds of the platform on the X-Axis
        if 256 <= (self.x + self.width + self.velX) and (self.x + self.velX) <= 1024:
            # If the character is above, contacting, or will contact the platform on the Y-Axis
            if (self.y + self.height) <= 519 < (self.y + self.height + self.velY):
                # Set the Y-Axis velocity to zero
                self.velY = 0
                # Set the character's Y-Axis position to perfectly stand on top of the platform
                self.y = 519 - self.height

        # Add the X-Axis velocity to the character's X-Axis position
        self.x += self.velX

        # Add the Y-Axis velocity to the character's Y-Axis position
        self.y += self.velY

        # If the character's Y-Axis position falls below the bounds of the window (i.e. the character falls/is kicked off of the platform)
        # reset the X-Axis and Y-Axis velocities and respawn the character
        if self.y > 720:
            self.y = -50
            self.x = random.randint(256, 1024)
            self.velX = 0
            self.velY = 0

        # Call the player class function "update" to set the new position of the shape of the character itself
        self.update()

    # Function checks whether or not the character performs a kick
    def kickAction(self):
        # Get a dictionary of all keyboard keys that contains if the specified key is currently pressed (True) or not (False)
        keys = pygame.key.get_pressed()

        # If the left arrow key is being pressed AND the up arrow key is not being pressed AND the right arrow key is not being pressed
        if keys[pygame.K_LEFT] and not(keys[pygame.K_UP]) and not(keys[pygame.K_RIGHT]):
            # Update the "kick" variable to signify a kick to the left
            self.kick = 1

        # If the left arrow key is not being pressed AND the up arrow key is not being pressed AND the right arrow key is being pressed
        elif not(keys[pygame.K_LEFT]) and not(keys[pygame.K_UP]) and keys[pygame.K_RIGHT]:
            # Update the "kick" variable to signify a kick to the right
            self.kick = 3

        # If the left arrow key is not being pressed AND the up arrow key is being pressed AND the right arrow key is not being pressed
        elif not(keys[pygame.K_LEFT]) and keys[pygame.K_UP] and not(keys[pygame.K_RIGHT]):
            # Update the "kick" variable to signify a kick upwards
            self.kick = 2

        # If the previous three conditional statements to perform a kick all return False
        else:
            # Update the "kick" variable to signify no kick is being performed
            self.kick = 0

    # Function updates the character shape to the new position of the character
    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
