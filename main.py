import pygame
import math
import asteroidGameObject
import time
from random import *

pygame.init()

clock = pygame.time.Clock()
display_width = 1200#x
display_height = 800#y
gameDisplay = pygame.display.set_mode((display_width,display_height))
bulletList=[]
asteroidList=[]
alienShipList=[]
alienBulletList=[]
bossBulletList=[]
    
def isOffScreen(x,y):
    global display_width
    global display_height
    
    retBool=False
    if x<display_width-display_width:
        x=display_width
        retBool=True
    elif x>display_width:
        x=display_width-display_width
        retBool=True
    if y<display_height-display_height:
        y=display_height
        retBool=True
    elif y>display_height:
        y=display_height-display_height
        retBool=True
    return x,y
        

def blitShip(ship,x,y,angleIn):
    global gameDisplay
    new_image = pygame.transform.rotate(ship, angleIn)
    newRect=new_image.get_rect(center=(x,y))
    gameDisplay.blit(new_image, newRect)
    return newRect


def rocketLocation(movement,angle,xIn,yIn):
    global gameDisplay
    newX=xIn
    newY=yIn
    x2=(movement*math.cos(math.radians(angle)))+xIn
    y2=(movement*math.sin(math.radians(angle)))+yIn
    newX=x2
    newY=y2
    return newX,newY
    
def correctAngle(angleIn):
    retAngle=0
    if angleIn<0:
        retAngle=abs(angleIn)%360
        retAngle=360-retAngle
    elif angleIn>360:
        retAngle=angleIn%360
    else:
        retAngle=angleIn
    return retAngle

def findRocketRotationAngle(angleIn):
    retAngle=0
    if 90>angleIn>=0:
        change=90-angleIn
        retAngle=180+change
    if 180>angleIn>=90:
        change=angleIn-90
        retAngle=180-change
    if 270>angleIn>=180:
        change=angleIn-180
        retAngle=90-change
    if 360>=angleIn>=270:
        change=angleIn-270
        retAngle=360-change
    return retAngle
    
def generateBullet(xspeed,yspeed,image,currPosition,angle):
    global bulletList
    aBullet=asteroidGameObject.Object(xspeed,yspeed,image,currPosition,angle)
    bulletList.append(aBullet)

def deleteOffScreenBullets(i):
    global bulletList
    if len(bulletList)>0:
        if bulletList[i].centerx<0 or bulletList[i].centerx>1200:
            del bulletList[i]
        elif bulletList[i].centery<0 or bulletList[i].centery>800:
            del bulletList[i]
        if i<len(bulletList)-1:
            i=i+1
            deleteOffScreenBullets(i) 
        
def updateBulletLocs():
    global bulletList
    global gameDisplay
    deleteOffScreenBullets(0)
    for i in range(len(bulletList)):
        x,y=calcObjectLocChange(bulletList[i])
        bulletList[i].centerx=x
        bulletList[i].centery=y
        newRect=bulletList[i].image.get_rect(center=(x,y))
        gameDisplay.blit(bulletList[i].image,newRect)
        
def calcObjectLocChange(object):
    iHat=(math.cos(math.radians(object.angle))*object.xspeed)+object.centerx
    jHat=(math.sin(math.radians(object.angle))*object.yspeed)+object.centery
    return iHat,jHat
    
def pickAsteroid(asteroidImageList):
    image=randint(0,4)
    retImage=''
    if image==0:
        retImage=asteroidImageList[image]
    elif image==1:
        retImage=asteroidImageList[image]
    elif image==2:
        retImage=asteroidImageList[image]
    elif image==3:
        retImage=asteroidImageList[image]
    elif image==4:
        retImage=asteroidImageList[image]
    return retImage

def sizeAsteroid(image,size):
    retImage=pygame.transform.scale(image,(size[0],size[1]))
    return retImage
    
def generateObjectNums():
    x=randint(0,1200)
    y=randint(0,800)
    angle=randint(1,360)
    return x,y,angle
    
    
def generateAsteroid(asteroidImageList,numbertoGenerate):
    # image,currPosition,angle
    global asteroidList
    for i in range(numbertoGenerate):
        x,y,angle=generateObjectNums()
        image=pickAsteroid(asteroidImageList)
        image=sizeAsteroid(image,[200,200])
        currPosition=[x,y]
        aAsteroid=asteroidGameObject.Object(6,6,image,currPosition,angle)
        asteroidList.append(aAsteroid)


def asteroidBounce():
    global asteroidList
    # print ("hello")
    retAngle=0
    for i in range(len(asteroidList)):
        if asteroidList[i].centerx<0 or asteroidList[i].centerx>1200:
            asteroidList[i].xspeed=asteroidList[i].xspeed*-1
        elif asteroidList[i].centery<0 or asteroidList[i].centery>800:
            asteroidList[i].yspeed=asteroidList[i].yspeed*-1
        
    
def updateAsteroidLocs():
    global asteroidList
    global gameDisplay
    asteroidBounce()
    
    for i in range(len(asteroidList)):
        x,y=calcObjectLocChange(asteroidList[i])
        asteroidList[i].centerx=x
        asteroidList[i].centery=y
        newRect=asteroidList[i].image.get_rect(center=(x,y))
        gameDisplay.blit(asteroidList[i].image,newRect)

def calDistBetweenTwoObjects(object1,object2,radius):
    retBool=False
    x1=object1.centerx
    y1=object1.centery
    x2=object2.centerx
    y2=object2.centery
    realDistance=math.sqrt((x2-x1)**2+(y2-y1)**2)
    if realDistance<radius:
        retBool=True
    return retBool

def compareShipToAsteroids(shipRect):
    global asteroidList
    isCollide=False
    for i in range(len(asteroidList)):
        isCollide=calDistBetweenTwoObjects(asteroidList[i],shipRect,40)
        if isCollide:
            break
    return isCollide    

def cycleAsteroids(shipRect,i):
    global asteroidList
    if i<len(asteroidList):
        asteroid=asteroidList[i]        
        cycleBullets(asteroid,0,i)
        i=i+1
        cycleAsteroids(shipRect,i)
        
def cycleBullets(asteroid,i,asteroidIndex):
    global bulletList
    isCollide=False
    if i<len(bulletList):
        bullet=bulletList[i]
        isCollide=calDistBetweenTwoObjects(asteroid,bullet,25)
        if isCollide:
            del bulletList[i]
            divideAsteroid(asteroid,asteroidIndex)
        i=i+1
        cycleBullets(asteroid,i,asteroidIndex)

def divideAsteroid(asteroid,asteroidIndex):
    global asteroidList
    if asteroid.timesDivided==0:
        del asteroidList[asteroidIndex]
        asteroid2=asteroidGameObject.Object(randint(1,9),randint(1,9),sizeAsteroid(asteroid.image,[125,125]),[asteroid.centerx,asteroid.centery],randint(1,360))
        asteroid2.timesDivided=1
        asteroid1=asteroidGameObject.Object(randint(1,9),randint(1,9),sizeAsteroid(asteroid.image,[125,125]),[asteroid.centerx,asteroid.centery],randint(1,360))
        asteroid1.timesDivided=1
        asteroidList.append(asteroid1)
        asteroidList.append(asteroid2)
    elif asteroid.timesDivided==1:
        del asteroidList[asteroidIndex]
        asteroid2=asteroidGameObject.Object(randint(1,12),randint(1,12),sizeAsteroid(asteroid.image,[75,75]),[asteroid.centerx,asteroid.centery],randint(1,360))
        asteroid2.timesDivided=2
        asteroid1=asteroidGameObject.Object(randint(1,12),randint(1,12),sizeAsteroid(asteroid.image,[75,75]),[asteroid.centerx,asteroid.centery],randint(1,360))
        asteroid1.timesDivided=2
        asteroidList.append(asteroid1)
        asteroidList.append(asteroid2)
    elif asteroid.timesDivided==2:
        asteroid.timesDivided=3
        
def deleteDestroyedAsteroids(i):
    global asteroidList    
    if i<len(asteroidList):
        if asteroidList[i].timesDivided==3:
            del asteroidList[i]
        i=i+1
        deleteDestroyedAsteroids(i)
    if len(asteroidList)==0:
        return len(asteroidList)

def generateAlienShip(alienShipCount,shipImage,bulletImage):
    global alienShipList
    for i in range(alienShipCount):
        x,y,angle=generateObjectNums()
        alienShip=asteroidGameObject.AlienShip(6,6,shipImage,bulletImage,[x,y],angle)
        alienShipList.append(alienShip)
        
def updateAlienShipLocs():
    global alienShipList
    for i in range(len(alienShipList)):
        ship=alienShipList[i]
        x,y=calcObjectLocChange(ship)
        x,y=isOffScreen(x,y)
        ship.centerx=x
        ship.centery=y
        newRect=ship.shipImage.get_rect(center=(x,y))
        gameDisplay.blit(ship.shipImage,newRect)
        
def compareAlienToBullets(i):
    global alienShipList
    if i<len(alienShipList):
        compareBulletsToAlien(alienShipList[i],0)
        i=i+1
        compareAlienToBullets(i)
    removeShotAlienShips(0)
    
        
def compareBulletsToAlien(alienShip,i):
    global bulletList
    if i<len(bulletList):
        isCollide=calDistBetweenTwoObjects(alienShip,bulletList[i],25)
        if isCollide:
            del bulletList[i]
            alienShip.isHit=True
        i=i+1
        compareBulletsToAlien(alienShip,i)

def removeShotAlienShips(i):
    global alienShipList
    if i<len(alienShipList):
        if alienShipList[i].isHit:
            del alienShipList[i]
        i=i+1
        removeShotAlienShips(i)
        
def fireAlienShips(shipRect):
    global alienShipList
    global alienBulletList
    fire=randint(1,100)
    if fire%20==0:
        for i in range(len(alienShipList)):
            aBullet=asteroidGameObject.Object(10,10,alienShipList[i].bulletImage,[alienShipList[i].centerx,alienShipList[i].centery],randint(1,360))
            alienBulletList.append(aBullet)
            
def updateAlienBulletLocs():
    global alienBulletList
    global gameDisplay
    deleteOffScreenAlienBullets(0)
    for i in range(len(alienBulletList)):
        x,y=calcObjectLocChange(alienBulletList[i])
        alienBulletList[i].centerx=x
        alienBulletList[i].centery=y
        newRect=alienBulletList[i].image.get_rect(center=(x,y))
        gameDisplay.blit(alienBulletList[i].image,newRect)
    
def deleteOffScreenAlienBullets(i):
    global alienBulletList
    if len(alienBulletList)>0:
        if alienBulletList[i].centerx<0 or alienBulletList[i].centerx>1200:
            del alienBulletList[i]
        elif alienBulletList[i].centery<0 or alienBulletList[i].centery>800:
            del alienBulletList[i]
        if i<len(alienBulletList)-1:
            i=i+1
            deleteOffScreenAlienBullets(i)
            
def compareShipToAlienBullets(shipRect):
    global alienBulletList
    isCollide=False
    for i in range(len(alienBulletList)):
        isCollide=calDistBetweenTwoObjects(alienBulletList[i],shipRect,25)
        if isCollide:
            break
    return isCollide   
    
def updateBoss(boss): 
    global gameDisplay
    global asteroidList
    global alienBulletList
    global alienShipList
    del asteroidList[:]
    del alienBulletList[:]
    del alienShipList[:]
    x,y=calcObjectLocChange(boss)
    x,y=isOffScreen(x,y)
    boss.centerx=x
    boss.centery=y
    newRect=boss.shipImage.get_rect(center=(x,y))
    gameDisplay.blit(boss.shipImage,newRect) 
    return boss
    
def generateBossBullets(boss):
    global bossBulletList
    isGenerate=randint(1,100)
    if isGenerate%4==0:
        aBullet=asteroidGameObject.Object(8,8,boss.bulletImage,[boss.centerx,boss.centery],randint(1,360))
        bossBulletList.append(aBullet)
    
def updateBossBullets():
    global bossBulletList
    for i in range(len(bossBulletList)):
        x,y=calcObjectLocChange(bossBulletList[i])
        bossBulletList[i].centerx=x
        bossBulletList[i].centery=y
        newRect=bossBulletList[i].image.get_rect(center=(x,y))
        gameDisplay.blit(bossBulletList[i].image,newRect)
            
def deleteOffScreenBossBullets(i):
    global bossBulletList
    if len(bossBulletList)>0:
        if bossBulletList[i].centerx<0 or bossBulletList[i].centerx>1200:
            del bossBulletList[i]
        elif bossBulletList[i].centery<0 or bossBulletList[i].centery>800:
            del bossBulletList[i]
        if i<len(bossBulletList)-1:
            i=i+1
            deleteOffScreenAlienBullets(i)

def compareShipToBossBullets(shipRect):
    global bossBulletList
    isCollide=False
    for i in range(len(bossBulletList)):
        isCollide=calDistBetweenTwoObjects(bossBulletList[i],shipRect,25)
        if isCollide:
            break
    return isCollide 
    
def compareBulletsToBoss(boss,i):
    global bulletList
    if i<len(bulletList):
        isCollide=calDistBetweenTwoObjects(boss,bulletList[i],25)
        if isCollide:
            del bulletList[i]
            boss.numberofTimesShot=boss.numberofTimesShot+1
        i=i+1
        compareBulletsToBoss(boss,i)
        
def generateBoss(alienBoss,bulletGreen):
    boss=asteroidGameObject.AlienShip(6,6,alienBoss,bulletGreen,[600,200],180)
    return boss
    
def text_objects(text, font):
    black=(0,0,0)
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()
    
def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            return False         
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)
    
def game_intro():
    global gameDisplay
    intro = True
    white=(255,255,255)
    rollovergreen=(0,215,0)
    rolloverblue=(0,215,215)
    green=(0,128,128)
    blue=(0,0,215)
    
    
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        click = pygame.mouse.get_pressed()
        mouse = pygame.mouse.get_pos()
        gameDisplay.fill(white)
        largeText = pygame.font.Font("SEASRN__.ttf",115)
        TextSurf, TextRect = text_objects("ASTEROIDS", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)
            
        if click[0]==1:
            if 550+100>mouse[0]>550 and 450+50>mouse[1]>450:            
                intro=False
                
        pygame.draw.rect(gameDisplay, blue,(550,450,100,50))
        smallText = pygame.font.Font("OpenSans-Regular.ttf",20)
        textSurf, textRect = text_objects("PLAY", smallText)
        textRect.center = ( (550+(100/2)), (450+(50/2)) )
        gameDisplay.blit(textSurf, textRect)    
            
            
        pygame.display.update()
        clock.tick(100)
        
def resetGame(arr):
    global bulletList
    global asteroidList
    global alienShipList
    global alienBulletList
    global bossBulletList
    asteroidList=[]
    bulletList=[]
    alienShipList=[]
    alienBulletList=[]
    bossBulletList=[]
    arr[0]=None
    arr[1] = 360
    arr[2] = 480
    arr[3]=0
    arr[4]=0
    arr[5]=0
    arr[6]=0
    arr[7]=False
    arr[8]=False
    arr[9]=False
    arr[10]=4
    arr[11]=1
    arr[12]=1
    arr[13]=False
    arr[14]=True
    return arr

def main():
    global gameDisplay
    global alienShipList
    # pygame.init()
    black = (0,0,0)
    white = (255,255,255)
    crashed = False
    background=pygame.image.load('asteroidsbackground.jpg')
    background=pygame.transform.scale(background,(1200,800))
    ship = pygame.image.load('ship.png')
    ship=pygame.transform.scale(ship, (200,150))
    shipRect=ship.get_rect()
    bulletTeal=pygame.image.load('bulletTeal.png')
    bulletTeal=pygame.transform.scale(bulletTeal,(50,50))
    bulletFire=pygame.image.load('bulletFire.png')
    bulletFire=pygame.transform.scale(bulletFire,(40,40))
    bulletGreen=pygame.image.load('bulletLightGreen.png')
    bulletGreen=pygame.transform.scale(bulletGreen,(50,50))
    asteroid1=pygame.image.load('asteroidDarkGrey.png')
    asteroid2=pygame.image.load('asteroidGreen.png')
    asteroid3=pygame.image.load('asteroidRed.png')
    asteroid4=pygame.image.load('asteroidBlue.png')
    asteroid5=pygame.image.load('asteroidLightGrey.png')
    asteroidImageList=[asteroid1,asteroid2,asteroid3,asteroid4,asteroid5]
    alienShip=pygame.image.load('alien.png')
    alienShip=pygame.transform.scale(alienShip,(100,100))
    alienBoss=pygame.image.load('boss.png')
    alienBoss=pygame.transform.scale(alienBoss,(200,200))
    boss=None
    x = 360
    y = 480
    displacement=0
    angle=0
    angleChange=0
    rocketAngle=0
    fireTeal=False
    fireFire=False
    fireGreen=False
    numberofAsteroids=4
    level=1
    alienShipCount=1
    stopGame=False
    makeBoss=True
    game_intro()
    while not crashed:
        for event in pygame.event.get():            
            if event.type == pygame.QUIT:
                crashed = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    angleChange+=5
                elif event.key == pygame.K_RIGHT:
                    angleChange-=5
                elif event.key==pygame.K_UP:
                    displacement=10
                elif event.key==pygame.K_DOWN:
                    displacement=-10
                    # print(displacement)
                elif event.key==pygame.K_SPACE:
                    generateBullet(13,13,bulletTeal,[x,y],rocketAngle-5)
                    generateBullet(13,13,bulletFire,[x,y],rocketAngle)
                    generateBullet(13,13,bulletTeal,[x,y],rocketAngle+5)

                    # fire=True
                # elif event.key==pygame.K_h:
                #     fireTeal=True
                # elif event.key==pygame.K_j:
                #     fireFire=True
                # elif event.key==pygame.K_k:
                #     fireGreen=True
                # elif event.key==pygame.K_l:
                #     generateAsteroid(asteroidImageList)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    angleChange=0
                elif event.key==pygame.K_UP or event.key==pygame.K_DOWN:
                    displacement=0
                # elif event.key==pygame.K_SPACE:
                #     fire=False
                # elif event.key==pygame.K_h:
                #     fireTeal=False
                # elif event.key==pygame.K_j:
                #     fireFire=False
                # elif event.key==pygame.K_k:
                #     fireGreen=False
        # print("hello")
        angle+=angleChange
        rocketAngle=findRocketRotationAngle(correctAngle(angle))
        x,y=rocketLocation(displacement,rocketAngle,x,y)
        x,y=isOffScreen(x,y)
        gameDisplay.blit(background,(0,0))
        shipRect=blitShip(ship,x,y,angle)
        updateBulletLocs()
        fightBoss=level%5==0
        if not fightBoss:
            updateAsteroidLocs()
            cycleAsteroids(shipRect,0)
            stopGame=compareShipToAsteroids(shipRect)
            astListLen=deleteDestroyedAsteroids(0)
            if stopGame:
                # input("YOUR DEAD, Press enter to continue")
                game_intro()
                newvals=resetGame([boss,x,y,displacement,angle,angleChange,rocketAngle,fireTeal,fireFire,fireGreen,numberofAsteroids,level,alienShipCount,stopGame,makeBoss])
                boss=newvals[0]
                x = newvals[1]
                y = newvals[2]
                displacement=newvals[3]
                angle=newvals[4]
                angleChange=newvals[5]
                rocketAngle=newvals[6]
                fireTeal=newvals[7]
                fireFire=newvals[8]
                fireGreen=newvals[9]
                numberofAsteroids=newvals[10]
                level=newvals[11]
                alienShipCount=newvals[12]
                stopGame=newvals[13]
                makeBoss=newvals[14]
                # print(newvals)
            if astListLen==0:
                generateAsteroid(asteroidImageList,numberofAsteroids)
                numberofAsteroids=numberofAsteroids+1
                level=level+1
                if level>=4:
                    generateAlienShip(level-3,alienShip,bulletGreen)
            updateAlienShipLocs()
            compareAlienToBullets(0)
            fireAlienShips(shipRect)
            updateAlienBulletLocs()
            stopGame=compareShipToAlienBullets(shipRect)
            # if stopGame:
            #     game_intro()
            # input("YOUR DEAD, Press enter to continue")
        if fightBoss:
            if makeBoss==True:
                boss=generateBoss(alienBoss,bulletGreen)
                makeBoss=False
            boss=updateBoss(boss)
            generateBossBullets(boss)
            updateBossBullets()
            deleteOffScreenBossBullets(0)
            compareBulletsToBoss(boss,0)
            if boss.numberofTimesShot==50:
                fightBoss=False
                makeBoss=True
                level=level+1
                del boss
            stopGame=compareShipToBossBullets(shipRect)
            if stopGame:
                game_intro()
                newvals=resetGame([boss,x,y,displacement,angle,angleChange,rocketAngle,fireTeal,fireFire,fireGreen,numberofAsteroids,level,alienShipCount,stopGame,makeBoss])
                boss=newvals[0]
                x = newvals[1]
                y = newvals[2]
                displacement=newvals[3]
                angle=newvals[4]
                angleChange=newvals[5]
                rocketAngle=newvals[6]
                fireTeal=newvals[7]
                fireFire=newvals[8]
                fireGreen=newvals[9]
                numberofAsteroids=newvals[10]
                level=newvals[11]
                alienShipCount=newvals[12]
                stopGame=newvals[13]
                makeBoss=newvals[14]
                # input("YOUR DEAD, Press enter to continue")
	#clock.tick() this slows or speeds up frame rate refresh
        pygame.display.update()
        

main()
pygame.quit()
quit()



