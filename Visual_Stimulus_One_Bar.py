import pygame # 2.6.0
import sys # python version 
import time # python version   
import random # python version


pygame.init()


# Duration: How long the animation should last
# Initial: 6 seconds  

# Speed: How fast the animation moves in one direction
# Select between slow, normal, fast     

# Direction: Where the animation moves to. 
# Choose between left (1) or right (2)





# Background: What the background of the animation is 
# Choose between white background (True) or white & gray background (False)  
# Intial: Randomly selected | CHANGE BACKGROUND OF THE SCREEN HERE 
background_white = random.choice([True, False])

# Dimesions: Size of the Animation Screen (Width, Height)  
# CHANGE DIMENSIONS OF THE SCREEN HERE 
width, height = 1920, 1080

# Color: Color of the bar. 
# Initial: Red | Blue
# Adding color -> color = {R,G,B} 
white = (255, 255, 255)
red = (255, 0, 0)
gray = (133, 132, 131)

# CHANGE COLOR OF THE BAR HERE
color_selected = red 


# Bar properties (Doesn't need to be changed ) 
final_height = width * 1.125
final_width = final_height / 5

# Setup
# CHANGE DISPLAY TO 0 FOR MAIN MONITOR
screen = pygame.display.set_mode((width, height), flags = pygame.NOFRAME, display=0)

# Function to draw the bar
def bar_drawing(screen, bar):
    draw_background()

    # For the bar, draw based on the color, position, current width and height 
    pygame.draw.rect(screen, bar['color'], (*bar['pos'], bar['width'], bar['height']))
    pygame.display.flip()


# Function to get background
def draw_background():
    # White if it is true
    if background_white:
        screen.fill(white)

    # Half White & Half Gray if it is not 
    else:
        screen.fill(white)
        pygame.draw.rect(screen, gray, (0, height /2, width, height /2))



# Function for three bar horizontal animation 
# Parameters: duration, color, dimensions, speed, direction, background
def three_bars_hor_animation(duration, speed, direction):
    
    bar = [{'color': color_selected[0], 'pos': [0,0], 'width': final_height, 'height': final_width}]

    # Updating the screen with the white background 
    draw_background()
    pygame.display.flip()
    time.sleep(2)

    # Moving left 
    if(direction == 'left'):
        print("Moving Left")
        # Final bar positions
        bar['pos'][1] = (height / 2 ) - (final_height / 2)
        bar["pos"][0] = (width / 2) - (final_width / 2)
        bar['height'] = final_height
        bar['width'] = final_width


        # Holding the bar
        bar_drawing(screen, bar)
        time.sleep(1)

        # Moving off Screen animation 
        start_time = time.time()
        while time.time() - start_time < 5:
            # Updating the position of the bars
            total_time = time.time() - start_time
            bar['pos'][0] -= int( ( width / 2 + final_width)/45 * (total_time / 10))
            bar_drawing(screen, bar)
            pygame.time.delay(10)
    
    # Moving Right 
    elif(direction == 'right'):
        print("Moving Right")
        # Final bar positions
        bar['pos'][1] = (height / 2 ) - (final_height / 2)
        bar["pos"][0] = (width / 2) - (final_width / 2)
        bar['height'] = final_height
        bar['width'] = final_width


        # Holding the bar
        bar_drawing(screen, bar)
        time.sleep(1)

        # Moving off Screen animation 
        start_time = time.time()
        while time.time() - start_time < 5:
            # Updating the position of the bars
            total_time = time.time() - start_time
            bar['pos'][0] -= int( ( width / 2 + final_width)/45 * (total_time / 10))
            bar_drawing(screen, bar)
            pygame.time.delay(10)
    
    # Updating the screen with the white background 
    draw_background()
    pygame.display.flip()
    time.sleep(2)

# Main function
def main():
    # Pressing 'b' starts the animation
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_b:
                    print("Choosing Animation")
                    three_bars_hor_animation(0,0,'left')

        draw_background()
        pygame.display.flip()
   
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pygame.quit()
        sys.exit()
    finally:
        pygame.quit()
        sys.exit()