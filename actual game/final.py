import pygame
import random
pygame.init()
win = pygame.display.set_mode((1024,416))
pygame.display.set_caption("STALIN RUN")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('ogbackground.png')
char = pygame.image.load('standing.png')
ghostimage = pygame.image.load('ghost.png')
lightsaberleft = pygame.image.load('LightsaberLeft.png')
lightsaberright = pygame.image.load('LightsaberRight.png')


clock= pygame.time.Clock()

#colours
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

#text
'''font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render(str(billy.x),True, green, blue)
textRect = text.get_rect()
textRect.center = (800, 30)'''

class player(object):
    def __init__( man , x, y, width, height):
        man.x=x
        man.y=y
        man.width=width
        man.height=height
        man.vel=5
        man.jump=False
        man.jumpspeed=10
        man.left=False
        man.right=True
        man.walkcount=0
        man.standing= True
        man.health = 100
        man.box = [man.x-((man.width//2) +10) , man.x+((man.width//2)+10) , man.y+((man.height//2)+10) , man.y-((man.height//2) +10)]
       
    def drawbilly(man,win):
        if man.walkcount+1>=27:
            man.walkcount=0
        if not(man.standing):
            if man.left:
                win.blit(walkLeft[man.walkcount//3], (man.x,man.y))
                man.walkcount+=1
            elif man.right:
                win.blit(walkRight[man.walkcount//3], (man.x,man.y))
                man.walkcount +=1
        else:
            if man.right:
                win.blit(walkRight[0], (man.x,man.y))
            else:
                win.blit(walkLeft[0], (man.x,man.y))
class bullet(object):
    def __init__ (man,x,y,radius,colour,pointing):
        man.x=x
        man.y=y
        man.radius=radius
        man.colour=colour
        man.pointing=pointing
        man.speed=10*pointing
       
    def movebullet(man):
        man.x += man.speed
    def drawbullet(man,win):
        man.movebullet()
        pygame.draw.circle(win, man.colour, (man.x,man.y), man.radius)
class enemy(object):
    def __init__(self , x , y , width , height , platform):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.platform = platform
        self.box = [self.x-((self.width//2)) , self.x+((self.width//2)) , self.y+((self.height//2)) , self.y-((self.height//2))]
        #Platform Format: [xi , xf , yi , yf]
        self.vel = 2
    def move(self):
        # X co.ordinate
        if self.vel > 0:
            if self.x + self.vel < self.platform[1]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.x += self.vel
        else:
            if self.x + self.vel > self.platform[0]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.x += self.vel
        # Y co.ordinate
        temp = self.x % 10
        temp -= 5
        self.y = self.platform[2] + temp
    def drawenemy(self , win):
        self.move()
        win.blit(ghostimage , (self.x , self.y))
       
       
#gravity
gravity=0.4
fallvel=0
enemylist = []      
def gamewindowdraw():
    win.blit(bg, (0,0))
    billy.drawbilly(win)
    for i in bullets:
        i.drawbullet(win)
    for i in enemylist:
        i.drawenemy(win)
    win.blit(text, textRect)
    if a:
        win.blit(lightsaberleft , (billy.x , billy.y+40))
    if b:
        win.blit(lightsaberright , (billy.x+20 , billy.y+40))
    pygame.display.update()
   
#main loop
cycles = 0
billy= player(10,50,64,64)
platforms = {1: (0 , 205 , 280 , 250) , 2: (255 , 550 , 235 , 215) , 3: (500 , 710 , 348 , 318) , 4: (510 , 700 , 115 , 85) , 5: (735 , 960 , 215 , 185)}
#Format for boxes: [xi , xf , yi , yf]
bullets=[]
score = 0
run = True
while run:
    clock.tick(27)
    fallvel+=gravity
    billy.y+=fallvel
    a , b , ls = False , False , False
    # HERE BEGINS THE TALE OF SPIRITS, AYE

    if cycles % 108 == 0:
        # Begin spawning
        plnumber = random.randint(1 , 5)
        platform = platforms[plnumber]
        newenemy = enemy(platform[0] , platform[2] , 64 , 64 , platform)
        enemylist.append(newenemy)
        # Dem neegus out here in enemylist BRADYOOTH  
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    for i in bullets:
        if 0<i.x<1000:
            i.movebullet
        else:
            bullets.pop(bullets.index(i))
       
    keys = pygame.key.get_pressed()
    if keys[pygame.K_z]:
        print("light saber gang")
        ls = True
        if billy.left:
            a = True
        else:
            b = True
    ''' The hits and shit go here BRADYOOTH. Length of the saber should be about 40 pixels.
    '''
    if keys[pygame.K_SPACE]:
        if billy.left:
            pointing= -1
        else:
            pointing=1
        if len(bullets)<20:
            bullets.append(bullet(round(billy.x+billy.width//2), round(billy.y+billy.height//2), 6 , (10,70,30),pointing))

    if keys[pygame.K_LEFT] and billy.x>billy.vel:
        billy.x -= billy.vel
        billy.left = True
        billy.right= False
        billy.standing= False
    elif keys[pygame.K_RIGHT] and billy.x<(1000-billy.width-billy.vel):
        billy.x += billy.vel
        billy.left=False
        billy.right= True
        billy.standing= False
    else:
        billy.standing=True
        walkcount=0
   
   
    if keys[pygame.K_UP] and fallvel==gravity==0:
        fallvel=-14
        #first platform
    if 0<billy.x<205 and 250<billy.y<280 and fallvel>=1:
        billy.y=265
        fallvel=0
        gravity=0
        #second platform
    elif 255<billy.x<550 and 215<billy.y<235 and fallvel>=1:
        billy.y=230
        fallvel=0
        gravity=0
        #lowest platform
    elif 500<billy.x<710 and 318<billy.y<348 and fallvel>=1:
        billy.y=330
        fallvel=0
        gravity=0
        #highest platform
    elif 510<billy.x<700 and 85<billy.y<115 and fallvel>=1:
        billy.y=100
        fallvel=0
        gravity=0
        #small platform
    elif 700<billy.x<750 and 245<billy.y<275 and fallvel>=1:
        billy.y=260
        fallvel=0
        gravity=0
        #last platform
    elif 735<billy.x and 185<billy.y<215 and fallvel>=1:
        billy.y=200
        fallvel=0
        gravity=0
        #stone cylinder
    elif 790<billy.x<840 and 119<billy.y<139 and fallvel>=1:
        billy.y=129
        fallvel=0
        gravity=0
    else:
        gravity=1
   
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(str((180 - cycles//27)),True, green, blue)
    textRect = text.get_rect()

    for i in enemylist:
        # Step-1: Check if enemy is hit by ls or bullets.
        if ls:
            if a:
                #if ((i.box[0])-40 < billy.x < i.box[1]) and (i.box[2] > billy.y > i.box[3]):
                if (i.box[0] < billy.x < (i.box[1]+40)) and (i.box[2] > billy.y > i.box[3]):
                    enemylist.pop(enemylist.index(i))
                    score += 1
            else:
                if ((i.box[0]-40) < billy.x < i.box[1]) and (i.box[3] < billy.y < i.box[2]):
                    enemylist.pop(enemylist.index(i))
                    score += 1
       
        for j in bullets:
            p = j.x
            q = j.y
            if (i.box[0] < p < i.box[1]) and (i.box[3] < q < i.box[2]):
                enemylist.pop(enemylist.index(i))
                bullets.pop(bullets.index(j))
                score +=1

    textRect.center = (800, 30)
    gamewindowdraw()
    cycles +=1
    if billy.y > 600:
        print("HAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHA")
        run = False
    elif (180 - cycles//27 <= 0):
        run = False
        print("HEEEHEEEEHEHEHEHEEEEHEHEHEHEHHEEEEEHEHEHEHEHASKJFLH")
   
print(score)
pygame.quit()
