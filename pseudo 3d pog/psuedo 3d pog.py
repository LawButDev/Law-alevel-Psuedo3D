import pygame
import math
# -- global constants
size = [640,640]

cubesize = 64
pheight = cubesize // 2
pwidth = pheight // 4
FOV = 60
mossen = 0.25
projplane = (320,200)
planedist = int((projplane[0] // 2) / math.tan((FOV // 2) / (180 / math.pi)))
rayang = 60 / 320


playerspeed = 16
strafespeedmultiplyer = 0.8

mapgrid = ["##########",
           "#  #     #",
           "#        #",
           "#  #     #",
           "#       ##",
           "#        #",
           "#        #",
           "#        #",
           "#        #",
           "##########"]


class player(pygame.sprite.Sprite):
    # initialiser
    def __init__(self,xpos,ypos,rotation):
        super().__init__()
        self.xpos = xpos
        self.ypos = ypos
        self.image = pygame.Surface([size[0] // 20, size[1] // 20], pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rot = rotation
        pygame.draw.polygon(self.image, (150,150,200,100), ((self.rect.center[0],self.rect.top),(self.rect.left,self.rect.bottom),(self.rect.right,self.rect.bottom)))           
        #self.rect.centre[0] = self.xpos
        #self.rect.centre[1] = self.ypos
        self.rect.center = (self.xpos,self.ypos)
        self.orgimage = self.image
        self.speed = playerspeed
        self.strafespeed = int(playerspeed * strafespeedmultiplyer)
    def update(self):
        # mouse movement handling
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        delta_x, delta_y = pygame.mouse.get_rel()
        self.rot += float(-delta_x * mossen)
        if self.rot > 360:
            self.rot -= 360
        elif self.rot <= 0:
            self.rot += 360
        self.image = pygame.transform.rotate(self.orgimage, -self.rot)
        self.rect.center = (self.xpos,self.ypos)

        print(self.rot)

        self.gridx = self.rect.center[0] // 64
        self.gridy = self.rect.center[1] // 64

        ray = 0
        while ray <= projplane[0]:
            temprot = self.rot
            if ray <= projplane[0] // 2:
                if self.rot - 30 <= 0:
                    temprot = self.rot + 360
            else:
                if self.rot + 30 > 360:
                    temprot = self.rot - 360
            temprot = temprot - 30 + (ray * rayang)

            # -- wall detection
            ##  - horizontal
            if 0 < temprot and temprot <= 90:
                Ay = int(self.rect.center[1] / 64) * 64 - 1
                #Yadir = -1
                Ya = -cubesize
                Xadir = 1
                temprot -= 0
                if temprot == 0: temprot += 1 / 10000
                #-between 0 and 90 x is the opposite in the triangle, so y * tan of angle
                Ax = self.rect.center[0] + (self.rect.center[1] - Ay) * math.tan(temprot * (math.pi / 180))
                Xa = Xadir * ((self.rect.center[1] - Ay) * math.tan(temprot * (math.pi / 180)))
            elif 90 < temprot and temprot <= 180:
                Ay = int(self.rect.center[1] / 64) * 64 + 64
                #Yadir = -1
                Ya = cubesize
                Xadir = -1
                #temprot -= 90
                if temprot == 0: temprot += 1 / 10000
                #between 90 and 180 x is the adjecent in the triangle, so y /tan of angle
                Ax = self.rect.center[0] + (self.rect.center[1] - Ay) / math.tan(temprot * (math.pi / 180))
                Xa = Xadir * ((self.rect.center[1] - Ay) / math.tan(temprot * (math.pi / 180)))
            elif 180 < temprot and temprot <= 270:
                Ay = int(self.rect.center[1] / 64) * 64 + 64
                #Yadir = 1
                Ya = cubesize
                Xadir = -1
                temprot -= 180
                if temprot == 0: temprot += 1 / 10000
                #-between 180 and 270 x is the opposite in the triangle, so y * tan of angle
                Ax = self.rect.center[0] + (self.rect.center[1] - Ay) * math.tan(temprot * (math.pi / 180))
                Xa = Xadir * ((self.rect.center[1] - Ay) * math.tan(temprot * (math.pi / 180)))
            elif 270 < temprot and temprot <= 360:
                Ay = int(self.rect.center[1] / 64) * 64 - 1
                #Yadir = 1
                Ya = -cubesize
                Xadir = 1
                temprot -= 270   
                if temprot == 0: temprot += 1 / 10000 
                #between 270 and 360 x is the adjecent in the triangle, so y /tan of angle
                Ax = self.rect.center[0] + (self.rect.center[1] - Ay) / math.tan(temprot * (math.pi / 180))
                Xa = Xadir * ((self.rect.center[1] - Ay) / math.tan(temprot * (math.pi / 180)))            
            
            #Ax = self.rect.center[0] + (self.rect.center[1] - Ay) / math.tan(temprot * (math.pi / 180))
            
            #Xa = Xadir * ((self.rect.center[1] - Ay) / math.tan(temprot * (math.pi / 180)))

            

            collided = False
            Oldx = Ax
            Oldy = Ay
            while collided == False:
                Oldx += Xa
                Oldy += Ya
                if int(Oldy // cubesize) < 10 and int(Oldy // cubesize) >= 0 and int(Oldx // cubesize) < 10 and int(Oldx // cubesize) >= 0:
                    if mapgrid[int(Oldy // cubesize)][int(Oldx // cubesize)] == "#":
                        collided = True
                else: collided = True
            if Oldx <= 0:
                Oldx = 0
            if Oldy <= 0:
                Oldy = 0
            if Oldx > 640:
                Oldx = 640
            if Oldy > 640:
                Oldy = 640
            pygame.draw.line(screen, (255,255,255,175), (self.rect.center), (Oldx,Oldy))
                    
            
            ray += 1
        


# -- class list definitions
debug_list = pygame.sprite.Group()
      
        


# -- Colours
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (50,50,255)
YELLOW = (255,255,0)

# -- initialise PyGame
pygame.init()

# -- Blank Screen
size = (640,450)
screen = pygame.display.set_mode(size)

# -- Title of new window/screen
pygame.display.set_caption("3dpog")

# -- Exit game flag set to false
done = False

# -- Manages how fast the screen refreshes
clock = pygame.time.Clock()

# - instantiations

PC = player(size[0] // 2, size[1] // 2, 0)
debug_list.add(PC)

### -- Game Loop

while not done:
    # -- user input and controls
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        done = True


    # -- Game Logic goes after this comment

    # -- screen background is BLACK

    screen.fill(BLACK)

    # -- Draw here
    debug_list.draw(screen)
    debug_list.update() 

    # -- flip display to reveal new position of objects
    pygame.display.flip()

    # - the clock ticks over
    clock.tick(60)

# - end of game loop

pygame.quit()
