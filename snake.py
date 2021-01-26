import pygame
import time
import random

pygame.init()

#define game colours

#colour = (red, green , blue)
white = (255,255,255)
black = (0,0,0)
red = (255 , 0 , 0)
green = (0, 155, 0)

display_width = 800
display_height = 800

#first get a surface
game_display = pygame.display.set_mode((display_width,display_height))

#give game a title
pygame.display.set_caption('Slither')

#will update specific area of surface/whole surface if no parameters entered
pygame.display.update()

#block size is thickness of snake
block_size = 20
fps = 20

direction = 'right'

#get font for texts
smallfont = pygame.font.SysFont('comicsansms',25)
mediumfont = pygame.font.SysFont('comicsansms',35)
largefont = pygame.font.SysFont('comicsansms',50)

#getting snakehead image 
img = pygame.image.load('snakehead.png')
appleimg = pygame.image.load('apple.png')

def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        game_display.fill(white)
        message_to_screen('Paused ' , black, -100 , size = 'large')
        message_to_screen('Press C to continue or Q to quit',
                         black,
                         25)
        pygame.display.update()
        clock.tick(5)

def score(score):
    text = smallfont.render('Score : ' + str(score), True , black)
    game_display.blit(text, [0,0])

def rand_apple_gen():
    rand_apple_x = round(random.randrange(0, display_width-block_size))#/10.0)*10.0
    rand_apple_y = round(random.randrange(0, display_height-block_size))#/10.0)*10.0
    return rand_apple_x , rand_apple_y


def game_intro():
    intro = True
    
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                    intro = False
        game_display.fill(white)
        message_to_screen('Welcome to Slither !',
                         green,
                         y_displace = -100,
                         size = 'large')
        message_to_screen('The objective of the game is to eat red apples !',
                         black,
                         -30,
                         size = 'small')
        message_to_screen('The more apples you eat, the longer you get !',
                         black,
                         10,
                         size = 'small')
        message_to_screen('If you run into yourself, or the edges, you die !',
                         black,
                         50,
                         size = 'small')
        message_to_screen('Press C to play or Q to quit or P to pause',
                         black,
                         180,
                         size = 'small')
        pygame.display.update()
        clock.tick(15)

def snake(block_size, snakelist):
    #ensuring snakehead is pointing correct direction
    if direction == 'right':
        head = pygame.transform.rotate(img,270)
    if direction == 'left':
        head = pygame.transform.rotate(img,90)
    if direction == 'up':
        head = img
    if direction == 'down':
        head = pygame.transform.rotate(img,180)
        
    #put snakehead on screen - x and y coordinate of last tuple in snake list - i.e the first box/start of snake
    game_display.blit(head, (snakelist[-1][0], snakelist[-1][1]))
    
    #we do [:-1] to ensure the snake head is unchanged
    for XnY in snakelist[:-1]:
        #drawing a rectangle for snake - [coordinate x , coordinate y, width, height]
        pygame.draw.rect(game_display, green, [XnY[0],XnY[1],block_size,block_size])

def text_objects(text, colour,size):
    if size == 'small':
        text_surface = smallfont.render(text, True, colour)
    elif size == 'medium':
        text_surface = mediumfont.render(text, True, colour)
    elif size == 'large':
        text_surface = largefont.render(text, True, colour)
    #return text_surface, text_rect
    return text_surface , text_surface.get_rect()
    
        
#function to put text on the screen, y_displace is displacement from center
def message_to_screen(msg,colour,y_displace = 0,size = 'small'):
    text_surface, text_rect = text_objects(msg, colour,size)
    text_rect.center = (display_width/2), (display_height/2) + y_displace
    game_display.blit(text_surface, text_rect)
    
 
    
#setting fps
clock = pygame.time.Clock()

#game loop
def game_loop():
    input("ENter yeysys")
    global direction
    direction = 'right'
    
    game_exit = False
    game_over = False

    #lead x is top left of snake
    lead_x = display_width / 2
    lead_y = display_height / 2
    
    lead_x_change = 10
    lead_y_change = 0
    
    snakelist = []
    snakelength = 1
    
    #you round the number to a multiple of 10 to ensure snake and apple crossover exactly
    rand_apple_x, rand_apple_y = rand_apple_gen()

#event handling loop
    while not game_exit:
        #loop if game is over - asks user to quit or play again
        while game_over == True:
            game_display.fill(white)
            #display message of game over
            message_to_screen('GAME OVER',
                              red, 
                              y_displace =  -50, 
                              size = 'large')
            message_to_screen('PRESS C TO PLAY AGAIN OR Q TO QUIT',
                              black,
                              y_displace = 50,
                             size = 'medium')
            #show on display
            pygame.display.update()
            
            #perform action depending on user input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                    game_over = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_exit = True
                        game_over = False
                    if event.key == pygame.K_c:
                        game_loop()
        #an event is basically the game detecting user input eg clicking the arrow keys
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            #when you press a key
            if event.type == pygame.KEYDOWN:
                #left arrow key
                if event.key == pygame.K_LEFT:
                    lead_x_change =- block_size
                    lead_y_change = 0
                    direction = 'left'
                #right arrow key
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = block_size
                    lead_y_change = 0
                    direction = 'right'
                #up
                elif event.key == pygame.K_UP:
                    lead_y_change =- block_size
                    lead_x_change = 0
                    direction = 'up'
                #down
                elif event.key == pygame.K_DOWN:
                    lead_y_change = block_size
                    lead_x_change = 0
                    direction = 'down'
                #pause
                elif event.key == pygame.K_p:
                    pause()
        #setting boundaries
        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            game_over = True


            #when you let go of a key - stop the movement
            #if event.type == pygame.KEYUP:
                #if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    #lead_x_change = 0

        #i.e when you click left key - x coordinate is -10
        lead_x += lead_x_change
        lead_y += lead_y_change
        
        #set display to white
        game_display.fill(white)
        
        apple_thickness = 30
        #draw an apple
        #pygame.draw.rect(game_display,red, [rand_apple_x,rand_apple_y,  apple_thickness,  apple_thickness])
        game_display.blit(appleimg,(rand_apple_x,rand_apple_y))

        snakehead = []

        snakehead.append(lead_x)
        snakehead.append(lead_y)
        
        snakelist.append(snakehead)
        
        if len(snakelist) > snakelength:
            del snakelist[0]
        
        #check if snake has hit itself
        for eachsegment in snakelist[:-1]:
            if eachsegment == snakehead:
                game_over = True
        
        #draw snake
        snake(block_size, snakelist)
        
        #update the score
        score(snakelength - 1)
        
        #do the changes
        pygame.display.update()
        
        #eating the apple
        #if lead_x == rand_apple_x and lead_y == rand_apple_y:
        
        #if lead_x >= rand_apple_x and lead_x <= rand_apple_x + apple_thickness:
            #if lead_y >= rand_apple_y and lead_y <= rand_apple_y + apple_thickness:
                #generate a new apple
                #rand_apple_x = round(random.randrange(0, display_width-block_size))#/10.0)*10.0
                #rand_apple_y = round(random.randrange(0, display_height-block_size))#/10.0)*10.0
                #make the snake bigger
                #snake
                #length +=1
                
        #eating the apple
        #first check if snake is within x range of the apple, rand_apple_x corresponds 
        #to coordinate of top left of apple. add the apple thickness to get top right
        #repeat this to find if top right of snake is within paramaeters of apple
        if lead_x > rand_apple_x and lead_x < rand_apple_x + apple_thickness or lead_x + block_size > rand_apple_x and lead_x + block_size < rand_apple_x + apple_thickness:
            #repeat this for y cross over
            if lead_y > rand_apple_y and lead_y < rand_apple_y + apple_thickness or lead_y + block_size > rand_apple_y and lead_y + block_size < rand_apple_y + apple_thickness:
                #generate a new apple
                rand_apple_x, rand_apple_y = rand_apple_gen()
                #make the snake bigger
                snakelength +=1
                
            
            
        #set frames per second
        clock.tick(fps)


    #exit pygame
    pygame.quit()
    quit()


input("Enter y")    
game_intro()
game_loop()