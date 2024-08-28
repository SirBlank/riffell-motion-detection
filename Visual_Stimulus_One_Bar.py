import pygame # 2.6.0
import time # python version   
# import IR_LED 

white = (255, 255, 255)
gray = (133, 132, 131)

# Function to draw the bar
def bar_drawing(screen, bar, background_white, height, width):
    draw_background(background_white, screen, height, width)

    # For the bar, draw based on the color, position, current width and height 
    pygame.draw.rect(screen, bar['color'], (*bar['pos'], bar['width'], bar['height']))
    pygame.display.flip()


# Function to get background
def draw_background(background_white, screen, height, width):
    # White if it is true
    if background_white:
        screen.fill(white)

    # Half White & Half Gray if it is not 
    else:
        screen.fill(white)
        pygame.draw.rect(screen, gray, (0, height /2, width, height /2))



# Function for three bar horizontal animation 
# Parameters: duration, color, dimensions, speed, direction, background
def animation(duration, speed , direction, height, width, color_selected, background_white, screen):
    
    # IR_LED.init(pins)

    final_height = width * 1.125
    final_width = final_height / 5
    
    bar = {'color': color_selected, 'pos': [0,0], 'width': final_width, 'height': final_height}

    # Updating the screen with the white background 
    print("Drawing background")
    counter = 0
    draw_background(background_white, screen, height, width)
    pygame.display.flip()
    time.sleep(2)

    # Moving left 
    if(direction == 'left'):
        print("Moving Left")
        # Final bar positions
        bar["pos"][0] = width
        print(bar["pos"][0])
        bar_drawing(screen, bar, background_white, height, width)
        pygame.time.delay(10)

        # Moving off Screen animation 
        start_time = time.time()
        while time.time() - start_time < duration:
            # Updating the position of the bars
            if speed == 0:
                # bar['pos'][0] -= int( (( width / 2 + final_width) / (duration * 50 )) + ( 2 / duration ))
                bar['pos'][0] -= int( (( width + final_width) / (duration * 200) )* 1 )
                # IR_LED.LED_on(pins[4]) 
                bar_drawing(screen, bar, background_white, height, width)
                pygame.time.delay(10)
            
            elif speed == 1:
                if (time.time() - start_time < duration/2):
                    bar['pos'][0] -= int( ((( width / 2 + final_width)/300) - .45) * 2 )
                    #IR_LED.LED_on(pins[4])                    
                    #IR_LED.LED_off(pins[7])
                else:
                    bar['pos'][0] += int( ((( width / 2 + final_width)/300) - .45) * 2 )
                    #IR_LED.LED_on(pins[7])
                    #IR_LED.LED_off(pins[4])
                bar_drawing(screen, bar, background_white, height, width)
                pygame.time.delay(10)
            
            elif speed == 2:
                #IR_LED.LED_on(pins[4])
                if (time.time() - start_time < duration/3):
                    bar['pos'][0] -= int( ((( width / 2 + final_width)/300) - .45) * 2 )
                    #IR_LED.LED_on(pins[4])                    
                    #IR_LED.LED_off(pins[7])
                elif (time.time() - start_time < 2*duration/3):
                    bar['pos'][0] += int( ((( width / 2 + final_width)/300) - .45) * 2 )
                    #IR_LED.LED_on(pins[7])
                    #IR_LED.LED_off(pins[4])
                else:
                    bar['pos'][0] -= int( ((( width / 2 + final_width)/300) - .45) * 2 )

                bar_drawing(screen, bar, background_white, height, width)
                pygame.time.delay(10)
        
        #IR_LED.init(pins)           
        print("Finished duration")
        print(counter)
        print(bar["pos"][0], bar["pos"][1])
    
    # Moving Right 
    elif(direction == 'right'):
        print("Moving Right")
        # Final bar positions
        bar["pos"][0] = 0 - (final_width)
        print(bar["pos"][0])

        # Moving off Screen animation 
        start_time = time.time()
        while time.time() - start_time < duration:
            # Updating the position of the bars
            if speed == 0:
                bar['pos'][0] += int( (( width / 2 + final_width)/300) - .52)
                bar_drawing(screen, bar, background_white, height, width)
                #IR_LED.LED_on(pins[7]) 
                pygame.time.delay(10)
            
            elif speed == 1:
                if (time.time() - start_time < duration/2):
                    bar['pos'][0] += int( ((( width / 2 + final_width)/300) - .52) * 2 )
                    #IR_LED.LED_on(pins[7])
                    #IR_LED.LED_off(pins[4])

                else:
                    bar['pos'][0] -= int( ((( width / 2 + final_width)/300) - .52) * 2 )
                    #IR_LED.LED_on(pins[4])                    
                    #IR_LED.LED_off(pins[7])

                bar_drawing(screen, bar, background_white, height, width)
                pygame.time.delay(10)
            
            elif speed == 2:
                # IR_LED.LED_on(pins[4])
                if (time.time() - start_time < duration/3):
                    bar['pos'][0] += int( ((( width / 2 + final_width)/300) - .52) * 2 )
                    #IR_LED.LED_on(pins[7])
                    #IR_LED.LED_off(pins[4])

                elif (time.time() - start_time < 2*duration/3):
                    bar['pos'][0] -= int( ((( width / 2 + final_width)/300) - .52) * 2 )
                    #IR_LED.LED_on(pins[4])                    
                    #IR_LED.LED_off(pins[7])
                else: 
                    bar['pos'][0] += int( ((( width / 2 + final_width)/300) - .52) * 2 )

                bar_drawing(screen, bar, background_white, height, width)
                pygame.time.delay(10)

        print("Finished duration")
        #IR_LED.init(pins)
        print(bar["pos"][0], bar["pos"][1])
    
    # Updating the screen with the white background 
    draw_background(background_white, screen, height, width)
    pygame.display.flip()
    time.sleep(2)


