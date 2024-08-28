import Visual_Stimulus_One_Bar
import pygame # 2.6.0
import sys # python version 

pygame.init()


# Duration: How long the animation should last
# Initial: 6 seconds  
duration = 6

# Speed: How fast the animation moves in one direction
# Select between slow (0), normal(1), fast(2)
speed = 0   

# Direction: Where the animation moves to. 
# Choose between left or right 
direction = 'left' 

# Background: What the background of the animation is 
# Choose between white background (True) or white & gray background (False)  
# Intial: Randomly selected | CHANGE BACKGROUND OF THE SCREEN HERE 
background_white = False

# Dimesions: Size of the Animation Screen (Width, Height)  
# CHANGE DIMENSIONS OF THE SCREEN HERE 
width, height = 1920, 1080

# Color: Color of the bar. 
# Initial: Red | Blue
# Adding color -> color = {R,G,B} 
red = (255, 0, 0)

# CHANGE COLOR OF THE BAR HERE
color_selected = red 


# Setup
# CHANGE DISPLAY TO 0 FOR MAIN MONITOR
screen = pygame.display.set_mode((width, height), flags = pygame.NOFRAME, display=0)

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
                    Visual_Stimulus_One_Bar.animation(duration, speed , direction, height, width, color_selected, background_white, screen)

        Visual_Stimulus_One_Bar.draw_background(background_white, screen, height, width)
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