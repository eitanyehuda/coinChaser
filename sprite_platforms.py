#########################################
# Programmer: Eitan Yehuda
# Date: 07/01/2016
# File Name: sprite_platforms.py
# Description: Demonstrates how to use Sprite platforms to support a Sprite object under gravity
#########################################
import pygame,random,math
pygame.init()

####### Game Screen Dimensions #######
HEIGHT = 800
WIDTH  = 1200
screen=pygame.display.set_mode((WIDTH,HEIGHT))

####### Variable Declarations #######
BLACK = (  0,  0,  0)
WHITE = (255,255,255)
PLAYER1CLR = (227, 129, 85)
PLAYER2CLR = (138, 48, 156)
size = 50
timer = 60 
font = pygame.font.SysFont("Digital Tech",size)
font2 = pygame.font.SysFont("Digital Tech",size+20)
collected=True

####### Movement Variables #######
GROUND = HEIGHT
GRAVITY = 2.5
RUN_SPEED = 15
JUMP_SPEED = -30

####### image loadings #######
coin=pygame.image.load("coin.png")
coin= coin.convert_alpha()
coin=pygame.transform.scale(coin,(50,50))
intro = pygame.image.load("intro.jpg")
intro = intro.convert_alpha()
intro = pygame.transform.scale(intro, (WIDTH,HEIGHT))
background = pygame.image.load("background.jpg")
background = background.convert_alpha()
background = pygame.transform.scale(background, (WIDTH,HEIGHT))
background2 = pygame.image.load("background2.jpg")
background2 = background2.convert_alpha()
background2 = pygame.transform.scale(background2, (2040,HEIGHT+50))
gameOver = pygame.image.load("gameOver.jpg")                    
gameOver = gameOver.convert_alpha()                             
gameOver = pygame.transform.scale(gameOver, (WIDTH,HEIGHT))          
controls = pygame.image.load("controls.png")                    
controls = controls.convert_alpha()

####### Music and sound #######
music = pygame.mixer.music.load("music.wav")                #loads background music
pygame.mixer.music.play(-1, 0)
jump_sound = pygame.mixer.Sound("jump.wav")
coin_sound = pygame.mixer.Sound("coin.wav") 

####### Movement for Sprites #######
move_right=1            #player 1
move_left=1

move_right2=1           #Player 2
move_left2=1

face_right=True         #Facing direction(for jump and stand)
face2_right=False

####### Score Keeping #######
score1=0
score2=0

#---------------------------------------#
#   classes                             #
#---------------------------------------#
class Player(pygame.sprite.Sprite):
    """ (fileName)
        Visible game object.
        Inherits Sprite to use its Rect property.
        See Sprite documentation here: 
        http://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite
    """
    def __init__(self, picture=None):
        pygame.sprite.Sprite.__init__(self)
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.picture=picture
        self.visible = False
        self.image = pygame.image.load(picture)
        self.rect = self.image.get_rect()
        self.update()
##    def __str__ (self):
##        return str(self.y) +"  "+str(self.vy)+"  "+str(self.vy)

    def spawn(self, x, y):
        """ Assign coordinates to the center of the object and make it visible.
        """
        self.x = x-self.rect.width/2
        self.y = y-self.rect.height/2
        self.rect = pygame.Rect(self.x, self.y, self.rect.width, self.rect.height)
        self.visible = True
        self.update()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        self.rect = pygame.Rect(self.x,self.y,self.rect.width,self.rect.height)
        self.image = pygame.image.load(self.picture)

    def run(self):
        self.x = self.x + self.vx
        self.update()
        
    def stop(self):
        self.vx = 0

    def fall(self):
        self.y = self.y + self.vy
        self.update()

    def nudge(self, horizontal_kick):
        self.vx = horizontal_kick

    def jump(self, vertical_kick):
        self.vy = vertical_kick
                     
    def accellerate(self, gravity):
        self.vy = self.vy + gravity
        
    def settle_on(self, level):
        self.y = level - self.rect.height
        self.vy = 0
        self.update()
        
    def settled_on(self, level):
        return self.y + self.rect.height == level and self.vy == 0

    def above(self, level):
        return self.y+self.rect.height<=level

    def below(self, level):
        return self.y+self.rect.height>level

    def falling(self):
        return self.vy > 0

    def next_rect(self):
        return pygame.Rect(self.x+self.vx, self.y+self.vy, self.rect.width, self.rect.height)
       
#---------------------------------------#
class Platform(pygame.sprite.Sprite):
    def __init__(self, picture=None):
        pygame.sprite.Sprite.__init__(self)
        self.x = 0
        self.y = 0
        self.visible = False
        self.image = pygame.image.load(picture)
        self.rect = self.image.get_rect()
        self.update()

    def spawn(self, x, y):
        self.x = x-self.rect.width/2
        self.y = y-self.rect.height/2
        self.rect = pygame.Rect(self.x, self.y, self.rect.width, self.rect.height)
        self.visible = True
        self.update()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
    def update(self):
        self.rect = pygame.Rect(self.x,self.y,self.rect.width,self.rect.height)

#---------------------------------------#
# function that calculates distance     #
# between two points in coordinate system
#---------------------------------------#
def distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)# Pythagorean theorem    
#---------------------------------------#
# function that redraws all objects     #
#---------------------------------------#
def redraw_screen():
    ####### Background for level 1 and 2 #######
    if inPlay == 2:
        screen.blit(background,(0,0))
    elif inPlay == 3:
        screen.blit(background2,(0,0))
    screen.blit(coin,(coinX[location]-25,coinY[location]-75))

    ####### Blit all text on game screen #######
    text = font.render("Player 1:"+ str(score1),1,PLAYER1CLR)
    text2 = font.render("Player 2:"+ str(score2),1,PLAYER2CLR)
    text3 = font.render(str(int(round(timer))),1,WHITE)#
    screen.blit(text,(0,0))
    screen.blit(text2,(WIDTH-195,0))
    screen.blit(text3,(580,0))

    ####### Draw players and platforms #######
    for platform in platforms:
        platform.draw(screen)
    player.draw(screen)
    player2.draw(screen)
    pygame.display.update()
    
#---------------------------------------#
# main program starts here              #
#---------------------------------------#

####### Loads player images and spawns players #######
player = Player("player1/player1-1.png")
player.spawn(50,700)

player2 = Player("player1/player1-1.png")
player2.spawn(WIDTH-50,700)

####### Posible coin locations #######
coinX = [100,1100,600,300,900,50,1150,300,900,600,350,850]
coinY = [GROUND-100,GROUND-100,GROUND-250,GROUND-400,GROUND-400,GROUND-550,GROUND-550,GROUND-200,GROUND-200,GROUND-540,GROUND-650,GROUND-650]

####### Platform locations #######
platforms = []
platformX = [100,1100,600,300,900,50,1150,300,900,600,350,850]
platformY = [GROUND-100,GROUND-100,GROUND-250,GROUND-400,GROUND-400,GROUND-550,GROUND-550,GROUND-200,GROUND-200,GROUND-540,GROUND-650,GROUND-650]
location=random.randint(0,8)

####### Platform for loop going through all locations #######
####### try platform + i otherwise except platform 3  #######
for i in range(len(platformX)):
    try:
        platform = Platform("platforms/platform"+str(i)+".png")
    except:
        platform = Platform("platforms/platform3.png")
    platform.spawn(platformX[i],platformY[i])       ##Spawns platforms and appends them to list
    platforms.append(platform)

level = GROUND
level2 = GROUND
#---------------------------------------#
####### other basic gae variables #######
clock = pygame.time.Clock()
FPS = 30
inPlay = 1      #in Play determines phase in game


 #######################
#########################
 #####             ##### 
#######   Intro   #######
 #####             #####  
#########################
 #######################


while inPlay == 1:

    ####### Blit all pictures and text in intro screen #######
    screen.blit(intro,(0,0))
    screen.blit(controls, (700,550))
    
    text0 = font2.render("Crazy Coin Chasers",1,WHITE)#
    text4 = font.render("Grab coins before time runs out",1,WHITE)#
    text5 = font.render("Player 1",1,PLAYER1CLR)#
    text6 = font.render("Player 2",1,PLAYER2CLR)#
    text7 = font.render("Use the following controls:",1,WHITE)#
    text8 = font.render("Press any key to begin",1,WHITE)#
    text10 = font.render("2 rounds which last 60 sec each",1,WHITE)#
    
    screen.blit(text0,(625,325))
    screen.blit(text4,(600,375))
    screen.blit(text5,(700,500))
    screen.blit(text6,(900,500))
    screen.blit(text7,(650,450))
    screen.blit(text8,(675,675))
    screen.blit(text10,(600,410))

    for event in pygame.event.get():    # check for any events
        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:     ## if any key is pressed, start game
            inPlay = 2              ## go to level 1
        if event.type == pygame.QUIT:                               ## if x is clicked quit game
            inPlay = 5
        if event.type == pygame.KEYDOWN:                            ## if esc is pressed quit game
            if  keys[pygame.K_ESCAPE]:
                inPlay = 5
            
    pygame.display.update()             # display must be updated, in order
                                        # to show the drawings

 #######################
#########################
 #####             ##### 
#######  level 1  #######
 #####             #####  
#########################
 #######################

                                        
while inPlay == 2:               
    clock.tick(FPS)
                                 
    for event in pygame.event.get():    # check for any events
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:       ##exit if esc key is pressed
            inPlay = 5
        if event.type == pygame.QUIT:   ## exit if x is clicked
            inPlay = 5
            
    if timer<= 0:
        inPlay = 3      ## go to level 2
        ###### Restates all values for second level ######
        timer = 60
        player.spawn(50,700)
        player2.spawn(WIDTH-50,700)

        ###### Platform locations are moved ######
        platforms = []
        platformX = [100,1100,600,300,900,50,1150,300,900,350,850,600]
        platformY = [GROUND-500,GROUND-500,GROUND-250,GROUND-350,GROUND-350,GROUND-200,GROUND-200,GROUND-100,GROUND-100, GROUND-650, GROUND-650, GROUND-500]

        ####### Platform for loop going through all locations #######
        ####### try platform + i otherwise except platform 3  #######
        for i in range(len(platformX)):
            try:
                platform = Platform("platforms/platform"+str(i)+".png")
            except:
                platform = Platform("platforms/platform3.png")
            platform.spawn(platformX[i],platformY[i])
            platforms.append(platform)


########################        
######  player 1 #######
########################

    ###### Standing sprite of player ######        
    if player.settled_on(level):
        
        if face_right:
            player.picture = ("player1/player1-1.png")
        else:
            player.picture = ("player1/player1-1_left.png")
    
    ###### jump action and sprite ######
    if keys[pygame.K_UP] and player.settled_on(level):
        player.jump(JUMP_SPEED)
        jump_sound.play()
        if face_right:
           player.picture = ("player1/player_jump.png")
        elif face_right == False:
            player.picture = ("player1/player_jump_left.png")

    ###### Left action and sprites ######        
    if keys[pygame.K_LEFT]:
        player.nudge(-RUN_SPEED)
        
        if player.x<RUN_SPEED:
            player.x = 10
            
        face_right=False
        
        if player.settled_on(level):
            if move_left == 1:
                player.picture = ("player1/player1-2_left.png")
                move_left=2
                
            elif move_left == 2:
                player.picture = ("player1/player1-4_left.png")
                move_left=3
                
            elif move_left == 3:
                player.picture = ("player1/player1-5_left.png")
                move_left=4
                
            elif move_left == 4:
                player.picture = ("player1/player1-6_left.png")
                move_left=1
        else:
             player.picture = ("player1/player_jump_left.png")
             
    ###### Right action and sprites ######    
    elif keys[pygame.K_RIGHT]:
        player.nudge(RUN_SPEED)
        
        if player.x>WIDTH-RUN_SPEED-60:
            player.x = WIDTH-60
            
        face_right=True
        
        if player.settled_on(level):
            if move_right == 1:
                player.picture = ("player1/player1-2.png")
                move_right=2
                
            elif move_right == 2:
                player.picture = ("player1/player1-4.png")
                move_right=3
                
            elif move_right == 3:
                player.picture = ("player1/player1-5.png")
                move_right=4
                
            elif move_right == 4:
                player.picture = ("player1/player1-6.png")
                move_right=1
        else:
            player.picture = ("player1/player_jump.png")
    else:
        player.stop()



#########################
######## player2 ########
#########################

        
    ###### Standing sprite of player ######    
    if player2.settled_on(level2):
        if face2_right:
            player2.picture = ("player2/player2-1.png")
        else:
            player2.picture = ("player2/player2-1_left.png")
    ###### jump action and sprite ######       
    if keys[pygame.K_w] and player2.settled_on(level2):
        player2.jump(JUMP_SPEED)
        jump_sound.play()
        if face2_right:
            player2.picture = ("player2/player2_jump.png")
        else:
            player2.picture = ("player2/player2_jump_left.png")

    ###### Left action and sprites ######         
    if keys[pygame.K_a]:
        player2.nudge(-RUN_SPEED)
        
        if player2.x<RUN_SPEED:
            player2.x = 10
            
        face2_right=False
        
        if player2.settled_on(level2):
            if move_left2 == 1:
                player2.picture = ("player2/player2-2_left.png")
                move_left2=2
                
            elif move_left2 == 2:
                player2.picture = ("player2/player2-4_left.png")
                move_left2=3
                
            elif move_left2 == 3:
                player2.picture = ("player2/player2-5_left.png")
                move_left2=4
                
            elif move_left2 == 4:
                player2.picture = ("player2/player2-6_left.png")
                move_left2=1
        else:
             player2.picture = ("player2/player2_jump_left.png")  

    ###### Right action and sprites ######
    elif keys[pygame.K_d]:
        player2.nudge(RUN_SPEED)

        if player2.x>WIDTH-RUN_SPEED-60:
            player2.x = WIDTH-60
            
        face2_right=True
        if player2.settled_on(level2):
            if move_right2 == 1:
                player2.picture = ("player2/player2-2.png")
                move_right2=2
                
            elif move_right2 == 2:
                player2.picture = ("player2/player2-4.png")
                move_right2=3
                
            elif move_right2 == 3:
                player2.picture = ("player2/player2-5.png")
                move_right2=4
                
            elif move_right2 == 4:
                player2.picture = ("player2/player2-6.png")
                move_right2=1
        else:
             player2.picture = ("player2/player2_jump.png")            
    else:
        player2.stop()
########## 
        
    ###### players' function calling ######    
    player.run()
    player.accellerate(GRAVITY)
    for platform in platforms:
        if player.above(platform.y) and player.next_rect().colliderect(platform.rect) and player.falling():
            level = platform.y
            player.settle_on(level)
    player.fall()
    
    player2.run()
    player2.accellerate(GRAVITY)
    for platform in platforms:
        if player2.above(platform.y) and player2.next_rect().colliderect(platform.rect) and player2.falling():
            level2 = platform.y
            player2.settle_on(level2)
    player2.fall()
#    

    ###### Coin grab and addition to score ######
    if player.below(GROUND):
        level = GROUND
        player.settle_on(level)

    if player2.below(GROUND):
        level2 = GROUND
        player2.settle_on(level2)
        
    ###### Coin grab and addition to score ######
    if distance(player.x,player.y,coinX[location]-25,coinY[location]-75)<50:
        collected=True
        coin_sound.play()
        score1+=1
    if distance(player2.x,player2.y,coinX[location]-25,coinY[location]-75)<50:
        collected=True
        coin_sound.play()
        score2+=1
        
    if collected==True:
        location=random.randint(0,8)
        collected=False
        
    redraw_screen()         ##redraws gamefield indefinately
    timer-=0.001*FPS        ##timer (decreasing)


 #######################
#########################
 #####             ##### 
#######  level 2  #######
 #####             #####  
#########################
 #######################

    
collected=True
coinX = [100,1100,600,300,900,50,1150,300,900,350,850,600]
coinY = [GROUND-500,GROUND-500,GROUND-250,GROUND-350,GROUND-350,GROUND-200,GROUND-200,GROUND-100,GROUND-100, GROUND-650, GROUND-650, GROUND-500]

while inPlay==3:               
    clock.tick(FPS)
    
    if timer<=0:
        inPlay = 4          ## go to gameOver screen

    for event in pygame.event.get():    # check for any events    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            inPlay = 5
        if event.type == pygame.QUIT:   ## exit if x is clicked
                inPlay = 5
    

#########################
#######  player 1 #######
#########################

    ###### Standing sprite of player ###### 
    if player.settled_on(level):
        if face_right:
            player.picture = ("player1/player1-1.png")
        else:
            player.picture = ("player1/player1-1_left.png")
    
    ###### jump action and sprite ######
    if keys[pygame.K_UP] and player.settled_on(level):
        player.jump(JUMP_SPEED)
        jump_sound.play()
        if face_right:
           player.picture = ("player1/player_jump.png")
        else:
            player.picture = ("player1/player_jump_left.png")

    ###### Left action and sprites ######        
    if keys[pygame.K_LEFT]:
        player.nudge(-RUN_SPEED)

        if player.x<RUN_SPEED:
            player.x = 10
        face_right=False
        
        if player.settled_on(level):
            if move_left == 1:
                player.picture = ("player1/player1-2_left.png")
                move_left=2
                
            elif move_left == 2:
                player.picture = ("player1/player1-4_left.png")
                move_left=3
                
            elif move_left == 3:
                player.picture = ("player1/player1-5_left.png")
                move_left=4
                
            elif move_left == 4:
                player.picture = ("player1/player1-6_left.png")
                move_left=1
        else:
             player.picture = ("player1/player_jump_left.png")
            
    ###### Right action and sprites ######    
    elif keys[pygame.K_RIGHT]:
        player.nudge(RUN_SPEED)

        if player.x>WIDTH-RUN_SPEED-60:
            player.x = WIDTH-60
            
        face_right=True
        if player.settled_on(level):
            if move_right == 1:
                player.picture = ("player1/player1-2.png")
                move_right=2
                
            elif move_right == 2:
                player.picture = ("player1/player1-4.png")
                move_right=3
                
            elif move_right == 3:
                player.picture = ("player1/player1-5.png")
                move_right=4
                
            elif move_right == 4:
                player.picture = ("player1/player1-6.png")
                move_right=1
        else:
             player.picture = ("player1/player_jump.png")                   
    else:
        player.stop()



#########################
######## player2 ########
#########################

        
    ###### Standing sprite of player ######     
    if player2.settled_on(level2):
        if face2_right:
            player2.picture = ("player2/player2-1.png")
        else:
            player2.picture = ("player2/player2-1_left.png")

    ###### jump action and sprite ######        
    if keys[pygame.K_w] and player2.settled_on(level2):
        player2.jump(JUMP_SPEED)
        jump_sound.play()
        if face2_right:
            player2.picture = ("player2/player2_jump.png")
        else:
            player2.picture = ("player2/player2_jump_left.png")

    ###### Left action and sprites ######        
    if keys[pygame.K_a]:
        player2.nudge(-RUN_SPEED)

        if player2.x<RUN_SPEED:
            player2.x = 10
        face2_right=False
        if player2.settled_on(level2):
            if move_left2 == 1:
                player2.picture = ("player2/player2-2_left.png")
                move_left2=2
                
            elif move_left2 == 2:
                player2.picture = ("player2/player2-4_left.png")
                move_left2=3
                
            elif move_left2 == 3:
                player2.picture = ("player2/player2-5_left.png")
                move_left2=4
                
            elif move_left2 == 4:
                player2.picture = ("player2/player2-6_left.png")
                move_left2=1
        else:
             player2.picture = ("player2/player2_jump_left.png")            

    ###### Right action and sprites ######
    elif keys[pygame.K_d]:
        player2.nudge(RUN_SPEED)

        if player2.x>WIDTH-RUN_SPEED-60:
            player2.x = WIDTH-60
        
        face2_right=True
        if player2.settled_on(level2):
            if move_right2 == 1:
                player2.picture = ("player2/player2-2.png")
                move_right2=2
                
            elif move_right2 == 2:
                player2.picture = ("player2/player2-4.png")
                move_right2=3
                
            elif move_right2 == 3:
                player2.picture = ("player2/player2-5.png")
                move_right2=4
                
            elif move_right2 == 4:
                player2.picture = ("player2/player2-6.png")
                move_right2=1
        else:
             player2.picture = ("player2/player2_jump.png")    
    else:
        player2.stop()
##########

    ###### players' function calling ######   
    player.run()
    player.accellerate(GRAVITY)
    for platform in platforms:
        if player.above(platform.y) and player.next_rect().colliderect(platform.rect) and player.falling():
            level = platform.y
            player.settle_on(level)
    player.fall()
    
    player2.run()
    player2.accellerate(GRAVITY)
    for platform in platforms:
        if player2.above(platform.y) and player2.next_rect().colliderect(platform.rect) and player2.falling():
            level2 = platform.y
            player2.settle_on(level2)
    player2.fall() 
#
    ###### Players settle on ground function ######
    if player.below(GROUND):
        level = GROUND
        player.settle_on(level)

    if player2.below(GROUND):
        level2 = GROUND
        player2.settle_on(level2)

    ###### Coin grab and addition to score ######
    if distance(player.x,player.y,coinX[location]-25,coinY[location]-75)<50:
        collected=True
        coin_sound.play()
        score1+=1
    if distance(player2.x,player2.y,coinX[location]-25,coinY[location]-75)<50:
        collected=True
        coin_sound.play()
        score2+=1
        
    if collected==True:
        location=random.randint(0,8)
        collected=False
        
    redraw_screen()         ##redraws game field indefinately
    timer-=0.001*FPS        ##timer


 #######################
#########################
 #####             ##### 
####### Game Over #######
 #####             #####  
#########################
 #######################


while inPlay == 4:
    ###### blit gamover pic and text depending on win conditions ######
    screen.blit(gameOver,(0,0))
    if score1>score2:       ## if player 1 won
        text9 = font2.render("Player 1 won with "+ str(score1)+ " coins",1,PLAYER1CLR)#
    elif score1<score2:     ## if player 2 won
        text9 = font2.render("Player 2 won with "+ str(score2)+ " coins",1,PLAYER2CLR)#
    else:                   ## if it was a tie
        text9 = font2.render("It was a draw at "+ str(score2)+ " coins",1,WHITE)#

    screen.blit(text9,(WIDTH/4,HEIGHT/2))
    pygame.display.update()

    for event in pygame.event.get():    # check for any events
        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN: ## exit if esc is pressed
            if  keys[pygame.K_ESCAPE]:
                inPlay = 5
        if event.type == pygame.QUIT:   ## exit if x is clicked
            inPlay = 5
        
    
#---------------------------------------# 
pygame.quit()
