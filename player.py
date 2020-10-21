import pygame
import random


# Create the "Player" class. This is the code that every character runs.
class Player:
    # Initialize the character with data sent by the server when the client first connected
    def __init__(self, newPlayer):
        self.usertag = newPlayer["usertag"]
        # The player index and the position in the "p2" array of the current character
        self.indx = newPlayer["indx"]
        # The X-Axis position of the top-left corner of the character for the initial spawn
        self.x = newPlayer["spawnX"]
        # The Y-Axis position of the top-left corner of the character for the initial spawn.
        # NOTE: The Y-Axis is weird. The top of the window is 0, and increases as you move towards to bottom of the window.
        self.y = newPlayer["spawnY"]
        # The width of the character and it's kick zone
        self.width = newPlayer["width"]
        # The height of the character and it's kick zone
        self.height = newPlayer["height"]
        # The random color assigned to the character
        self.color = newPlayer["color"]
        # This is the actual shape of the character itself. This is used when drawing the character onto the window.
        self.rect = (newPlayer["spawnX"], newPlayer["spawnY"], newPlayer["width"], newPlayer["height"])
        # Stores whether or not the character is currently kicking
        self.kick = newPlayer["kick"]
        # Stores the value of kick from the previous frame
        self.kickCheck = newPlayer["kickCheck"]
        # This is the downward acceleration of the characters
        self.gravity = newPlayer["gravity"]
        # This is the maximum velocity a character can travel along the X-Axis. Possible X-Axis velocities are [-velXMax, velXMax]
        self.velXMax = newPlayer["velXMax"]
        # This is the maximum velocity a character can travel along the Y-Axis. Possible Y-Axis velocities are [-velYMax, velYMax]
        self.velYMax = newPlayer["velYMax"]
        # If the magnitude of the character velocity falls below this threshold, the velocity is set to zero. This prevents drifting.
        self.velThresh = newPlayer["velThresh"]
        # This is the value added to / subtracted from the X-Axis Velocity while the left or right keys are being pressed.
        self.acc = newPlayer["acc"]
        # This is the rate at which the character will slow down along the X-Axis. Think of it as friction from the floor.
        self.accDrag = newPlayer["accDrag"]
        # This stores the current Y-Axis velocity of the character.
        self.velY = newPlayer["velY"]
        # This stores the current X-Axis velocity of the character.
        self.velX = newPlayer["velX"]
        self.kickDuration = newPlayer["kickDuration"]

    # Function used to draw the character itself, as well as a box showing the kick zone if the character is currently kicking
    def draw(self, win, myfont, platform):
        # Draw the character onto the window "win" with the color "self.color" as specified in "self.rect"
        pygame.draw.rect(win, self.color, self.rect)

        # If the character is currently kicking to the LEFT
        if self.kick == 1:  # print("Kick Left")
            # Draw the kick zone to the LEFT of the character
            pygame.draw.rect(win, (0, 0, 0), (self.x - self.width, self.y, self.width, self.height))

        # If the character is currently kicking UP
        if self.kick == 2:  # print("Kick Up")
            # Draw the kick zone ABOVE the character
            # pygame.draw.rect(win, (0, 0, 0), (self.x, self.y - self.height, self.width, self.height))
            pygame.draw.rect(win, (0, 0, 0), (self.x, self.y + self.height, self.width, self.height))

        # If the character is currently kicking to the RIGHT
        if self.kick == 3:  # print("Kick Right")
            # Draw the kick zone to the RIGHT of the character
            pygame.draw.rect(win, (0, 0, 0), (self.x + self.width, self.y, self.width, self.height))

        if self.kick == 2:
            # Add white text of the character's (indx+1) using "myfont" on top of the character
            userTagText = myfont["Times New Roman 12"].render(str(self.usertag), False, (255, 255, 255))
        else:
            # Add black text of the character's (indx+1) using "myfont" on top of the character
            userTagText = myfont["Times New Roman 12"].render(str(self.usertag), False, (0, 0, 0))
        # win.blit(userTagText, (self.x, self.y - 12))
        userTagText_width = userTagText.get_width()
        userTagText_centerSpacing = (self.width - userTagText_width) / 2
        # win.blit(userTagText, (self.x + self.width - userTagText_width - userTagText_centerSpacing, self.y - userTagText.get_height() + 2))

        # win.blit(userTagText, (self.x + self.width - userTagText_width - userTagText_centerSpacing, self.y + self.height))

        userTagText_rotated = pygame.transform.rotate(userTagText, 180)
        win.blit(userTagText_rotated, (self.x + self.width - userTagText_width - userTagText_centerSpacing, self.y + self.height - 2))

    # Function does all of the fun math on how the physically move the character, as well as pixel-perfect collision detection for the platform
    def move(self, playerKicked, keys, FrameRate, platform):

        # accMult = 60/FrameRate

        if playerKicked == 1:  # If the character has been kicked to the LEFT, set it's X-Axis velocity to MAX in the LEFT direction.
            self.velX = -self.velXMax
            self.velY = self.velYMax * (1/4)
        elif playerKicked == 2:  # If the character has been kicked UP, set it's Y-Axis velocity to MAX in the UPWARDS direction.
            self.velY = self.velYMax
        elif playerKicked == 3:  # If the character has been kicked to the RIGHT, set it's X-Axis velocity to MAX in the RIGHT direction.
            self.velX = self.velXMax
            self.velY = self.velYMax * (1 / 4)

        # Get a dictionary of all keyboard keys that contains if the specified key is currently pressed (True) or not (False)
        # keys = pygame.key.get_pressed()

        # If the "A" key is being pressed, accelerate to the left by subtracting from the X-Axis velocity
        if keys[pygame.K_a]:  # K_LEFT
            self.velX += self.acc  # * accMult

        # If the "D" key is being pressed, accelerate to the right by adding to the X-Axis velocity
        if keys[pygame.K_d]:  # K_RIGHT
            self.velX -= self.acc  # * accMult

        # NOTE: By having the "A" and "D" keypress checks as separate if statements, they cancel each other out if both are being pressed.
        #       This results in zero net-change in X-Axis velocity.

        # If both "A" and "D" are being pressed, OR if neither "A" and "D" are being pressed
        if (keys[pygame.K_a] and keys[pygame.K_a]) or (~keys[pygame.K_a] and ~keys[pygame.K_a]):
            # If the X-Axis velocity is towards the right (positive)
            if self.velX > self.velThresh:
                # Apply drag to the left (subtract) to slow down the character
                self.velX -= self.accDrag  # * accMult

            # If the X-Axis velocity is towards the left (negative)
            elif self.velX < -self.velThresh:
                # Apply drag to the right (add) to slow down the character
                self.velX += self.accDrag  # * accMult

            # If the magnitude of the X-Axis velocity is below the threshold, set the X-Axis velocity to zero.
            else:
                self.velX = 0

        # If the Y-Axis velocity is zero (i.e. character is on the platform) and the space bar is pressed
        if keys[pygame.K_SPACE] and self.velY == 0 and (self.y == platform["top"] + platform["height"]):
            # Make the character jump by setting the Y-Axis velocity
            self.velY += (1.25 * self.velYMax)

        # Add gravity to the Y-Axis velocity
        self.velY += self.gravity  # * accMult

        # If the X-Axis velocity was calculated to go above MAX
        if self.velX > self.velXMax:
            # Set X-Axis velocity to MAX
            self.velX = self.velXMax

        # If the X-Axis velocity was calculated to go below -MAX
        elif self.velX < -self.velXMax:
            # Set X-Axis velocity to -MAX
            self.velX = -self.velXMax

        # If the character is within the bounds of the platform on the X-Axis
        if platform["left"]+1 <= (self.x + self.width + self.velX) and (self.x + self.velX) <= platform["left"]+platform["width"]:
            # If the character is above, contacting, or will contact the platform on the Y-Axis
            if self.y >= platform["top"] + platform["height"] > (self.y + self.velY):
                # Set the Y-Axis velocity to zero
                self.velY = 0
                # Set the character's Y-Axis position to perfectly stand on top of the platform
                self.y = platform["top"] + platform["height"]

        # Add the X-Axis velocity to the character's X-Axis position
        self.x += self.velX

        # Add the Y-Axis velocity to the character's Y-Axis position
        self.y += self.velY

        # If the character's Y-Axis position falls below the bounds of the window (i.e. the character falls/is kicked off of the platform)
        # reset the X-Axis and Y-Axis velocities and respawn the character
        if self.y < 0 - self.height:
            self.y = 720 + 50
            self.x = random.randint(platform["left"], platform["left"]+platform["width"])
            self.velX = 0
            self.velY = 0

        self.x = round(self.x, 5)
        self.y = round(self.y, 5)

        # Call the player class function "update" to set the new position of the shape of the character itself
        self.update()

    # Function checks whether or not the character performs a kick
    def kickAction(self, keys):
        # Get a dictionary of all keyboard keys that contains if the specified key is currently pressed (True) or not (False)
        # keys = pygame.key.get_pressed()

        # If the left arrow key is being pressed AND the up arrow key is not being pressed AND the right arrow key is not being pressed
        if keys[pygame.K_LEFT] and not(keys[pygame.K_UP]) and not(keys[pygame.K_RIGHT]):
            # Update the "kick" variable to signify a kick to the left
            self.kick = 3

        # If the left arrow key is not being pressed AND the up arrow key is not being pressed AND the right arrow key is being pressed
        elif not(keys[pygame.K_LEFT]) and not(keys[pygame.K_UP]) and keys[pygame.K_RIGHT]:
            # Update the "kick" variable to signify a kick to the right
            self.kick = 1

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
