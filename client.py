import pygame
from network import Network
import time
import descendLadsGeneral

windowTitle = "Descend Lads: Australia [ALPHA v2.2.1]"

# Define window width and height (in pixels)
width = 1280
height = 720
FrameRateLock = 20

# Initialize the font functionality of pygame
pygame.font.init()
# Create a font for text using Times New Roman size 30
# myfont_sml = pygame.font.SysFont('Times New Roman', 12)
# myfont_med = pygame.font.SysFont('Times New Roman', 20)
# myfont_lrg = pygame.font.SysFont('Times New Roman', 30)
myfont = {
  "Times New Roman 12": pygame.font.SysFont('Times New Roman', 12),
  "Times New Roman 20": pygame.font.SysFont('Times New Roman', 20),
  "Times New Roman 30": pygame.font.SysFont('Times New Roman', 30)
}

# Create the pygame window with the previously defined width and height
win = pygame.display.set_mode((width, height))
# Set the window title permanently to "Player #" to replace the placeholder, where # is this client's indx number plus 1
pygame.display.set_caption(windowTitle)


# This function receives the array "p2" (containing the character data for all players) send from the server.
# It loops through all array elements and draws each player character onto the pygame window.
def redrawWindow(p2, playerUsertag, playerColor, latencyCheck, FPSCheck):
    # Set the window background to white
    win.fill((255, 255, 255))

    # Draw the black platform onto the window
    pygame.draw.rect(win, (0, 0, 0), (256, 519, 768, 50))

    FPSCheckNew = time.time()
    FPSCheckOld = FPSCheckNew - FPSCheck

    # Loop through all elements in the "p2" array as "player"
    for player_key in p2:
        player = p2[player_key]
        # Call the player class function "draw" for the current character
        player.draw(win, myfont)

    latency = (time.time() - latencyCheck)

    win.blit(myfont["Times New Roman 20"].render("USERTAG: " + str(playerUsertag), False, (0, 0, 0)), (0, 0))
    pygame.draw.rect(win, playerColor, (75, 23, 130, 20))
    win.blit(myfont["Times New Roman 20"].render("COLOR: " + str(playerColor), False, (0, 0, 0)), (0, 20))
    win.blit(myfont["Times New Roman 12"].render("Latency: " + str(latency * 1000), False, (0, 0, 0)), (0, 45))
    if latency == 0:
        win.blit(myfont["Times New Roman 12"].render("Theoretical FPS: INF", False, (0, 0, 0)), (0, 60))
    else:
        win.blit(myfont["Times New Roman 12"].render("Theoretical FPS: " + str(1 / latency), False, (0, 0, 0)), (0, 60))

    if FPSCheckOld == 0:
        win.blit(myfont["Times New Roman 12"].render("FPS: INF", False, (0, 0, 0)), (0, 75))
        FrameRate = FrameRateLock
    else:
        win.blit(myfont["Times New Roman 12"].render("FPS: " + str(1 / FPSCheckOld), False, (0, 0, 0)), (0, 75))
        FrameRate = 1 / FPSCheckOld

    # Once everything has been redrawn onto the window, show it to the user
    pygame.display.update()

    return FPSCheckNew, FrameRate


def redrawTitleWindow(serverIP, serverIPFailed):
    win.fill((255, 255, 255))
    win.blit(myfont["Times New Roman 30"].render(windowTitle, False, (0, 0, 0)), (0, 0))
    win.blit(myfont["Times New Roman 30"].render("Server IP: "+serverIP, False, (0, 0, 0)), (0, 50))
    if serverIPFailed:
        win.blit(myfont["Times New Roman 20"].render("Server Not Responding or Invalid IP. Please Try Again.", False, (255, 0, 0)), (0, 100))
    pygame.display.update()


def titleScreen(serverIPFailed):
    # Initiate the pygame clock, which is used to lock the window frame rate
    clock = pygame.time.Clock()

    serverIPEntered = False
    serverIP = ""

    while not serverIPEntered:
        clock.tick(FrameRateLock)

        # Get a dictionary of all keyboard keys that contains if the specified key is currently pressed (True) or not (False)
        keys = pygame.key.get_pressed()

        # If the keyboard "ESCAPE" key is pressed
        if keys[pygame.K_ESCAPE]:
            serverIP = "QUIT"
            serverIPEntered = True
            break
        if keys[pygame.K_RETURN]:
            serverIPEntered = True

        redrawTitleWindow(serverIP, serverIPFailed)

        # Get all pygame events
        for event in pygame.event.get():
            # If the "pygame.QUIT" event is found
            # if event.type == pygame.QUIT:
            #     # Call the pygame "quit" method to close the window
            #     pygame.quit()
            #     serverIP = "QUIT"
            #     # Break out of the current for-loop
            #     break
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_COMMA:
                    serverIP = "localhost"
                elif event.key == pygame.K_BACKSPACE:
                    if serverIP == "localhost":
                        serverIP = ""
                    else:
                        serverIP = serverIP[0:(len(serverIP) - 1)]
                else:
                    serverIP += descendLadsGeneral.IPAddressKey(event.key)

    return serverIP


# This is the main client function which runs all client side functions, which is why it is called "main"
def main():
    # Initiate the pygame clock, which is used to lock the window frame rate
    clock = pygame.time.Clock()

    # Initialize the while-loop conditional variable as False
    run = False

    # serverIP = "localhost"

    serverIPFailed = False
    titleScreenQuit = False

    while not titleScreenQuit:
        try:
            serverIP = titleScreen(serverIPFailed)
            if serverIP == "QUIT":
                titleScreenQuit = True
            else:
                # Get the "Network" class from "network.py" to communicate with the server
                n = Network(serverIP)
                titleScreenQuit = True
                run = True
        except RuntimeError:
            serverIPFailed = True

    if run:
        # Get this specific client's player data, i.e. the data sent to the client when it first connected
        p = n.getP()
        FPSCheck = time.time()
        FrameRate = FrameRateLock

    # Start the while loop
    while run:
        # The method "clock.tick()" computes how many milliseconds have passed since the previous call
        # By calling the method "clock.tick(60)" with the added argument, the method will delay to keep the game running SLOWER than 60 FPS
        clock.tick(FrameRateLock)  # clock.tick(60)

        latencyCheck = time.time()

        # Send this client's character data to the server. It will reply with an array of data for ALL characters, which we store as "p2"
        p2 = n.send(p)

        # Create a temporary variable to store whether or not this client's character has gotten kicked and in which direction
        playerKicked = 0

        # Loop through all characters in the array "p2" as "player"
        for player_key in p2:
            player = p2[player_key]
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
        p.move(playerKicked, FrameRate)

        # Check whether or not to perform a kick with this client's character by calling the player class function "kickAction"
        p.kickAction()

        # Call the "redrawWindow" function and pass it the information sent by the server, which is stored in the "p2" variable
        (FPSCheck, FrameRate) = redrawWindow(p2, p.usertag, p.color, latencyCheck, FPSCheck)

        # Get a dictionary of all keyboard keys that contains if the specified key is currently pressed (True) or not (False)
        keys = pygame.key.get_pressed()

        # If the keyboard "ESCAPE" key is pressed
        if keys[pygame.K_ESCAPE]:
            # Set the while-loop conditional variable to False
            run = False
            # Call the pygame "quit" method to close the window
            # pygame.quit()

        # noinspection PyBroadException
        try:
            # Get all pygame events
            for event in pygame.event.get():
                # If the "pygame.QUIT" event is found
                if event.type == pygame.QUIT:
                    # Set the while-loop conditional variable to False
                    run = False
                    # Call the pygame "quit" method to close the window
                    # pygame.quit()
                    # Break out of the current for-loop
                    break
        except Exception as e:
            # print(e)
            run = False

        # If the current kick value is different from that of the previous frame
        if p.kick != p.kickCheck:
            # Update kickCheck so that it matches. This check variable is used so that a character kick event is only
            # registered ONCE when the key is pressed, instead of repeating while the key is help down.
            p.kickCheck = p.kick


# Now that all functions have been compiled by the interpreter, call the "main" function to run the game.
main()
