import pygame
from network import Network

# Define window width and height (in pixels)
width = 1280
height = 720

# Initialize the font functionality of pygame
pygame.font.init()
# Create a font for text using Times New Roman size 30
myfont_sml = pygame.font.SysFont('Times New Roman', 12)
myfont_med = pygame.font.SysFont('Times New Roman', 20)
myfont_lrg = pygame.font.SysFont('Times New Roman', 30)

# Create the pygame window with the previously defined width and height
win = pygame.display.set_mode((width, height))
# Set the window title to "Client" as a placeholder
pygame.display.set_caption("Client")


# This function receives the array "p2" (containing the character data for all players) send from the server.
# It loops through all array elements and draws each player character onto the pygame window.
def redrawWindow(p2):
    # Set the window background to white
    win.fill((255, 255, 255))

    # Draw the black platform onto the window
    pygame.draw.rect(win, (0, 0, 0), (256, 519, 768, 50))

    # Loop through all elements in the "p2" array as "player"
    for player in p2:
        # Call the player class function "draw" for the current character
        player.draw(win, [myfont_sml, myfont_med, myfont_lrg])

    # Once everything has been redrawn onto the window, show it to the user
    pygame.display.update()


# This is the main client function which runs all client side functions, which is why it is called "main"
def main():
    # Initialize the while-loop conditional variable as True
    run = True

    # Get the "Network" class from "network.py" to communicate with the server
    n = Network()

    # Get this specific client's player data, i.e. the data sent to the client when it first connected
    p = n.getP()

    # Set the window title permanently to "Player #" to replace the placeholder, where # is this client's indx number plus 1
    pygame.display.set_caption("Player "+str(p.indx + 1))

    # Initiate the pygame clock, which is used to lock the window frame rate
    clock = pygame.time.Clock()

    # Start the while loop
    while run:
        # The method "clock.tick()" computes how many milliseconds have passed since the previous call
        # By calling the method "clock.tick(60)" with the added argument, the method will delay to keep the game running SLOWER than 60 FPS
        clock.tick(60)

        # Send this client's character data to the server. It will reply with an array of data for ALL characters, which we store as "p2"
        p2 = n.send(p)

        # Create a temporary variable to store whether or not this client's character has gotten kicked and in which direction
        playerKicked = 0

        # Loop through all characters in the array "p2" as "player"
        for player in p2:
            # If the current character has kicked to the LEFT
            if player.kick == 1:
                # Check to see if this client's character is inside of the kick zone
                if ((player.x - player.width) <= (p.x + p.width) < player.x) and ((p.y <= player.y + player.height) and (p.y + p.height) >= player.y):
                    # This client's character is, indeed, inside of the kick zone. Update the temporary variable, which will be used when updating this client's character's position
                    playerKicked = 1
            # If the current character has kicked UP
            if player.kick == 2:
                # Check to see if this client's character is inside of the kick zone
                if ((p.x <= player.x + player.width) and (p.x + p.width) >= player.x) and ((player.y - player.height) <= (p.y + p.height) < player.y):
                    # This client's character is, indeed, inside of the kick zone. Update the temporary variable, which will be used when updating this client's character's position
                    playerKicked = 2
            # If the current character has kicked to the RIGHT
            if player.kick == 3:
                # Check to see if this client's character is inside of the kick zone
                if ((player.x + player.width) <= p.x < (player.x + (2 * player.width))) and ((p.y <= player.y + player.height) and (p.y + p.height) >= player.y):
                    # This client's character is, indeed, inside of the kick zone. Update the temporary variable, which will be used when updating this client's character's position
                    playerKicked = 3

        # Move the character by calling the player class function "move" for the current character and passing it the temporary "playerKicked" variable
        p.move(playerKicked)

        # Check whether or not to perform a kick with this client's character by calling the player class function "kickAction"
        p.kickAction()

        # Call the "redrawWindow" function and pass it the information sent by the server, which is stored in the "p2" variable
        redrawWindow(p2)

        # Get a dictionary of all keyboard keys that contains if the specified key is currently pressed (True) or not (False)
        keys = pygame.key.get_pressed()

        # If the keyboard "ESCAPE" key is pressed
        if keys[pygame.K_ESCAPE]:
            # Set the while-loop conditional variable to False
            run = False
            # Call the pygame "quit" method to close the window
            pygame.quit()

        # Get all pygame events
        for event in pygame.event.get():
            # If the "pygame.QUIT" event is found
            if event.type == pygame.QUIT:
                # Set the while-loop conditional variable to False
                run = False
                # Call the pygame "quit" method to close the window
                pygame.quit()
                # Break out of the current for-loop
                break

        # If the current kick value is different from that of the previous frame
        if p.kick != p.kickCheck:
            # Update kickCheck so that it matches. This check variable is used so that a character kick event is only
            # registered ONCE when the key is pressed, instead of repeating while the key is help down.
            p.kickCheck = p.kick


# Now that all functions have been compiled by the interpreter, call the "main" function to run the game.
main()
