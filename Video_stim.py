import pygame
import sys
import time
import random

pygame.init()

# Screen resolution

width, height = 1024, 768

# Colors
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
colors_three = [green, red, black]
colors_two = [green, red]

# Bar properties 
initial_height = 50
final_height = 864
initial_width = initial_height / 5
final_width = final_height / 5
initial_gap = initial_width / 3
final_gap = final_width / 3

# Setup
screen = pygame.display.set_mode((width, height))

def bar_drawing(screen, bars):
    screen.fill(white)
    for bar in bars:
        pygame.draw.rect(screen, bar['color'], (*bar['pos'], bar['width'], bar['height']))
    pygame.display.flip()

# Function for two bar animation 
def two_bars_hor_animation():
    
    # Randomizing the colors of two bars
    random.shuffle(colors_two)
    bars = [
        {'color': colors_two[0], 'pos': [0,0], 'width': initial_width, 'height': initial_height},
        {'color': colors_two[1], 'pos': [0,0], 'width': initial_width, 'height': initial_height}  
    ]

    # Updating the screen with the white background 
    screen.fill(white)
    pygame.display.flip()
    time.sleep(2)

    # Growing animation
    start_time = time.time()
    while time.time() - start_time < 4.75:
        # Setting the dimenstions
        total_time = time.time() - start_time
        current_height = int(initial_height + (final_height - initial_height) * (total_time / 5))
        current_width = int(initial_width + (final_width - initial_width) * (total_time / 5))
        current_gap = int(initial_gap + (final_gap - initial_gap) * (total_time / 5))

        # Updating the position of the bars
        bars[0]['pos'] = [(width / 2) - current_width - (current_gap / 2), (height / 2) - (current_height / 2)]
        bars[1]['pos'] = [(width / 2) + (current_gap / 2), (height / 2) - (current_height / 2)]

        for bar in bars:
            bar['height'] = current_height
            bar['width'] = current_width

        # Drawing the bars 
        bar_drawing(screen, bars)
        pygame.time.delay(10)
    
    # Final bar positions
    for bar in bars:
        bar['pos'][1] = (height / 2 ) - (final_height / 2)
        bar['height'] = final_height
        bar['width'] = final_width

    bars[0]["pos"][0] = (width / 2) - final_width - (final_gap / 2)
    bars[1]["pos"][0] = (width / 2) + (final_gap / 2)

    bar_drawing(screen, bars)
    time.sleep(1)

    # Moving off Screen animation 
    start_time = time.time()
    while time.time() - start_time < 3:
        # Updating the position of the bars
        total_time = time.time() - start_time
        for bar in bars:
            if bar == bars[0]:
                bar['pos'][0] -= int( ( width / 2 + final_width + final_gap)/45 * (total_time / 10))
            else:
                bar['pos'][0] += int( ( width / 2 + final_width + final_gap)/45 * (total_time / 10))
        bar_drawing(screen, bars)
        pygame.time.delay(10)

    # Updating the screen with the white background 
    screen.fill(white)
    pygame.display.flip()
    time.sleep(2)

# Function for three bar animation 
def three_bars_hor_animation():
    
    # Randomizing the colors of three bars
    random.shuffle(colors_three)
    bars = [
        {'color': colors_three[0], 'pos': [0,0], 'width': initial_width, 'height': initial_height},
        {'color': colors_three[1], 'pos': [0,0], 'width': initial_width, 'height': initial_height},  
        {'color': colors_three[2], 'pos': [0,0], 'width': initial_width, 'height': initial_height}  
    ]

    # Updating the screen with the white background 
    screen.fill(white)
    pygame.display.flip()
    time.sleep(2)

    # Growing animation
    start_time = time.time()
    while time.time() - start_time < 4.75:
        # Setting the dimenstions
        total_time = time.time() - start_time
        current_height = int(initial_height + (final_height - initial_height) * (total_time / 5))
        current_width = int(initial_width + (final_width - initial_width) * (total_time / 5 ))
        current_gap = int(initial_gap + (final_gap - initial_gap) * total_time / 5)

        # Updating the position of the bars
        bars[0]['pos'] = [(width / 2) - (current_width * 1.5 + current_gap), (height / 2) - (current_height / 2)]
        bars[1]['pos'] = [(width / 2) - (current_width / 2), (height / 2) - (current_height / 2)]
        bars[2]['pos'] = [(width / 2) + (current_width / 2 + current_gap), (height / 2) - (current_height / 2)]
        
        for bar in bars:
            bar['height'] = current_height
            bar['width'] = current_width

        # Drawing the bars 
        bar_drawing(screen, bars)
        pygame.time.delay(10)

    # Final bar positions
    for bar in bars:
        bar['pos'][1] = (height / 2 ) - (final_height / 2)
        bar['height'] = final_height
        bar['width'] = final_width

    bars[0]["pos"][0] = (width / 2) - (final_width *1.5 + final_gap )
    bars[1]["pos"][0] = (width / 2) - (final_width / 2)
    bars[2]["pos"][0] = (width / 2) + (final_width / 2 + final_gap)

    # Holding the bar
    bar_drawing(screen, bars)
    time.sleep(1)

    # Moving off Screen animation 
    start_time = time.time()
    while time.time() - start_time < 3:
        # Updating the position of the bars
        total_time = time.time() - start_time
        for bar in bars:
            if bar == bars[0]:
                bar['pos'][0] -= int( ( width / 2 + final_width + final_gap)/45 * (total_time / 10))
            elif bar == bars[2]:
                bar['pos'][0] += int( ( width / 2 + final_width + final_gap)/45 * (total_time / 10))
        bar_drawing(screen, bars)
        pygame.time.delay(10)
    
    # Updating the screen with the white background 
    screen.fill(white)
    pygame.display.flip()
    time.sleep(2)

def two_bar_ver_animation():

    # Randomizing the colors of two bars   
    random.shuffle(colors_two)
    bars = [
        {'color': colors_two[0], 'pos': [0,0], 'width': initial_width, 'height': initial_height},
        {'color': colors_two[1], 'pos': [0,0], 'width': initial_width, 'height': initial_height}  
    ]

    # Updating the screen with the white background 
    screen.fill(white)
    pygame.display.flip()
    time.sleep(2)

    start_time = time.time()
    while time.time() - start_time < 4.75:
        # Setting the dimenstions
        total_time = time.time() - start_time
        current_height = int(initial_height + (final_height - initial_height) * (total_time / 5))
        current_width = int(initial_width + (final_width - initial_width) * (total_time / 5))
        current_gap = int(initial_gap + (final_gap - initial_gap) * (total_time / 5))

        # Updating the position of the bars
        bars[0]['pos'] = [(width / 2) - current_width - (current_gap / 2), (height / 2) - (current_height / 2)]
        bars[1]['pos'] = [(width / 2) + (current_gap / 2), (height / 2) - (current_height / 2)]

        for bar in bars:
            bar['height'] = current_height
            bar['width'] = current_width

        # Drawing the bars 
        bar_drawing(screen, bars)
        pygame.time.delay(10)

    # Final bar positions
    for bar in bars:
        bar['pos'][1] = (height / 2 ) - (final_height / 2)
        bar['height'] = final_height
        bar['width'] = final_width

    bars[0]["pos"][0] = (width / 2) - final_width - (final_gap / 2)
    bars[1]["pos"][0] = (width / 2) + (final_gap / 2)

    bar_drawing(screen, bars)
    time.sleep(1)

    # Moving off Screen animation 
    start_time = time.time()
    while time.time() - start_time < 4:
        # Updating the position of the bars
        total_time = time.time() - start_time
        for bar in bars:
            if bar == bars[0]:
                bar['pos'][1] -= int( ( height / 2 + final_height + final_gap)/45 * (total_time / 10))
            else:
                bar['pos'][1] += int( ( height / 2 + final_height + final_gap)/45 * (total_time / 10))
        bar_drawing(screen, bars)
        pygame.time.delay(10)

    # Updating the screen with the white background 
    screen.fill(white)
    pygame.display.flip()
    time.sleep(2)

# Function for three bar animation 
def three_bars_ver_animation():
    
    # Randomizing the colors of three bars
    random.shuffle(colors_three)
    bars = [
        {'color': colors_three[0], 'pos': [0,0], 'width': initial_width, 'height': initial_height},
        {'color': colors_three[1], 'pos': [0,0], 'width': initial_width, 'height': initial_height},  
        {'color': colors_three[2], 'pos': [0,0], 'width': initial_width, 'height': initial_height}  
    ]

    # Updating the screen with the white background 
    screen.fill(white)
    pygame.display.flip()
    time.sleep(2)

    # Growing animation
    start_time = time.time()
    while time.time() - start_time < 4.75:
        # Setting the dimenstions
        total_time = time.time() - start_time
        current_height = int(initial_height + (final_height - initial_height) * (total_time / 5))
        current_width = int(initial_width + (final_width - initial_width) * (total_time / 5 ))
        current_gap = int(initial_gap + (final_gap - initial_gap) * total_time / 5)

        # Updating the position of the bars
        bars[0]['pos'] = [(width / 2) - (current_width * 1.5 + current_gap), (height / 2) - (current_height / 2)]
        bars[1]['pos'] = [(width / 2) - (current_width / 2), (height / 2) - (current_height / 2)]
        bars[2]['pos'] = [(width / 2) + (current_width / 2 + current_gap), (height / 2) - (current_height / 2)]
        
        for bar in bars:
            bar['height'] = current_height
            bar['width'] = current_width

        # Drawing the bars 
        bar_drawing(screen, bars)
        pygame.time.delay(10)

    # Final bar positions
    for bar in bars:
        bar['pos'][1] = (height / 2 ) - (final_height / 2)
        bar['height'] = final_height
        bar['width'] = final_width

    bars[0]["pos"][0] = (width / 2) - (final_width *1.5 + final_gap )
    bars[1]["pos"][0] = (width / 2) - (final_width / 2)
    bars[2]["pos"][0] = (width / 2) + (final_width / 2 + final_gap)

    # Holding the bar
    bar_drawing(screen, bars)
    time.sleep(1)

    # Moving off Screen animation 
    start_time = time.time()
    while time.time() - start_time < 4:
        # Updating the position of the bars
        total_time = time.time() - start_time
        for bar in bars:
            if bar == bars[0]:
                bar['pos'][1] -= int( ( height / 2 + final_height + final_gap)/45 * (total_time / 10))
            elif bar == bars[2]:
                bar['pos'][1] += int( ( height / 2 + final_height + final_gap)/45 * (total_time / 10))
        bar_drawing(screen, bars)
        pygame.time.delay(10)
    
    # Updating the screen with the white background 
    screen.fill(white)
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
                if event.key == pygame.K_b:
                    animation = random.choice([1, 2, 3, 4])
                    if animation == 1:
                        two_bars_hor_animation()
                    elif animation == 2:
                        three_bars_hor_animation()
                    elif animation == 3:
                        two_bar_ver_animation()
                    else:
                        three_bars_ver_animation()
        screen.fill(white)
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