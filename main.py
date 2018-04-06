

import pygame
import math
import asteroidGameObject
import time
# import asteroid
from random import *

display_width = 1200#x
display_height = 800#y
gameDisplay = pygame.display.set_mode((display_width,display_height))
bulletList=[]
asteroidList=[]
alienShipList=[]
alienBulletList=[]
bossBulletList=[]
# pygame.display.set_caption('A bit Racey')
    
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
    # rocketAngle=findRocketRotationAngle(angleIn)
    new_image = pygame.transform.rotate(ship, angleIn)
    newRect=new_image.get_rect(center=(x,y))
    # newRect.centerx=x
    # newRect.centery=y
    # findRocketRotationAngle(angleIn)
    gameDisplay.blit(new_image, newRect)
    return newRect


def rocketLocation(movement,angle,xIn,yIn):
    global gameDisplay
    newX=xIn
    newY=yIn
    # rocketAngle=findRocketRotationAngle(correctAngle(angle))
    
    # x2=(movement*math.cos(math.radians(findRocketRotationAngle(correctAngle(angle)))))+xIn
    # y2=(movement*math.sin(math.radians(findRocketRotationAngle(correctAngle(angle)))))+yIn
    x2=(movement*math.cos(math.radians(angle)))+xIn
    y2=(movement*math.sin(math.radians(angle)))+yIn
    
    
    newX=x2
    newY=y2
        
    
    # print("X1: ",xIn,"Y1: ",yIn,"X2: ",x2,"Y2: ",y2,"RISE: ",rise,"RUN: ",run,"NEWX: ",newX,"NEWY: ",newY,"ANGLE: ",angle)
    # print("Xin: ",xIn,"Yin: ",yIn,"X2: ",x2,"Y2: ",y2,"NEWX: ",newX,"NEWY: ",newY,"ANGLE: ",angle)

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
        # print ("90>angleIn=>0")
    if 180>angleIn>=90:
        change=angleIn-90
        retAngle=180-change
        # print ("90>angleIn=>0")
    if 270>angleIn>=180:
        change=angleIn-180
        retAngle=90-change
        # print ("90>angleIn=>0")
    if 360>=angleIn>=270:
        change=angleIn-270
        retAngle=360-change
        # print ("90>angleIn=>0")
    # print("ROCKETANGLE",retAngle)
    return retAngle
    
def generateBullet(xspeed,yspeed,image,currPosition,angle):
    global bulletList
    aBullet=asteroidGameObject.Object(xspeed,yspeed,image,currPosition,angle)
    # print("ANGLE: ", angle,"HEIGHT: ",image.get_rect().height,"WIDTH: ",image.get_rect().width)

    bulletList.append(aBullet)
    # print(bulletList)

def deleteOffScreenBullets(i):
    global bulletList
    if len(bulletList)>0:
        if bulletList[i].centerx<0 or bulletList[i].centerx>1200:
            del bulletList[i]
            # bulletList.pop(i)
            # print("DELETED CROSSED X, BULLETLISTSize: ",len(bulletList))
            # listLen=len(bulletList)
        elif bulletList[i].centery<0 or bulletList[i].centery>800:
            del bulletList[i]
            # bulletList.pop(i)
            # print("DELETED CROSSED Y, BULLETLISTSize: ",len(bulletList))
            # listLen=len(bulletList)
        if i<len(bulletList)-1:
            i=i+1
            # print("BULLETLISTSize INSIDE LOOP: ",len(bulletList))
            deleteOffScreenBullets(i)
    # print("BULLETLISTSize EXITING LOOP: ",len(bulletList))    
        
def updateBulletLocs():
    global bulletList
    global gameDisplay
    deleteOffScreenBullets(0)
    for i in range(len(bulletList)):
        x,y=calcObjectLocChange(bulletList[i])
        bulletList[i].centerx=x
        bulletList[i].centery=y
        newRect=bulletList[i].image.get_rect(center=(x,y))
        # print("BULLETLIST[i].x: ", bulletList[i].x,"BULLETLIST[i].y: ",bulletList[i].y)
        # print("BULLETLISTSize: ",len(bulletList))
        gameDisplay.blit(bulletList[i].image,newRect)
        
def calcObjectLocChange(object):
    # x=(object.xspeed*math.cos(math.radians(object.angle)))+object.centerx
    # y=(object.yspeed*math.sin(math.radians(object.angle)))+object.centery
    
    iHat=(math.cos(math.radians(object.angle))*object.xspeed)+object.centerx
    jHat=(math.sin(math.radians(object.angle))*object.yspeed)+object.centery
    # return x,y
    return iHat,jHat
    
def pickAsteroid(asteroidImageList):
    image=randint(0,4)
    # image1='asteroidBlue.png'
    # image2='asteroidDarkGrey.png'
    # image3='asteroidLightGrey.png'
    # image4='asteroidGreen.png'
    # image5='asteroidRed.png'
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
    # bullet=pygame.transform.scale(bullet,(50,50))
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
        # x=randint(0,1200)
        # y=randint(0,800)
        image=pickAsteroid(asteroidImageList)
        image=sizeAsteroid(image,[200,200])
        # angle=randint(1,360)
        currPosition=[x,y]
        # print("ANGLE: ", angle,"HEIGHT: ",image.get_rect().height,"WIDTH: ",image.get_rect().width)
        aAsteroid=asteroidGameObject.Object(6,6,image,currPosition,angle)
        asteroidList.append(aAsteroid)


def asteroidBounce():
    global asteroidList
    # print ("hello")
    retAngle=0
    for i in range(len(asteroidList)):
        # print("ANGLEBEFORECHANGE: ",asteroidList[i].angle)
        # input("press enter to continue")
        if asteroidList[i].centerx<0 or asteroidList[i].centerx>1200:
            # asteroidList[i].angle=correctAngle(asteroidList[i].angle-90)
            asteroidList[i].xspeed=asteroidList[i].xspeed*-1
        elif asteroidList[i].centery<0 or asteroidList[i].centery>800:
            # asteroidList[i].angle=correctAngle(asteroidList[i].angle-90)
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
        # print("BULLETLIST[i].x: ", bulletList[i].x,"BULLETLIST[i].y: ",bulletList[i].y)
        # print("BULLETLISTSize: ",len(bulletList))
        gameDisplay.blit(asteroidList[i].image,newRect)

def calDistBetweenTwoObjects(object1,object2,radius):
    retBool=False
    x1=object1.centerx
    y1=object1.centery
    x2=object2.centerx
    y2=object2.centery
    realDistance=math.sqrt((x2-x1)**2+(y2-y1)**2)
    # radius=asteroid.image.get_rect().height+bullet.image.get_rect().height
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
    # print("cycleAsteroidsI: ",i,"ASTEROIDLISTLENGTH: ",len(asteroidList))
    # if i<len(asteroidList):
    # if len(asteroidList)>0:
    if i<len(asteroidList):
        asteroid=asteroidList[i]
        # print("ASTEROIDLISTLENGTH: ",len(asteroidList))
        
        cycleBullets(asteroid,0,i)
        # print("CYCLEAST ","ASTEROIDLISTLENGTH: ",len(asteroidList),"I: ",i)
        # isCollide=calDistBetweenShipAsteroid(asteroid,shipRect)
        # isCollide=calDistBetweenTwoObjects(asteroid,shipRect,60)
        # 
        # # if i<len(asteroidList)-1:
        # if not isCollide:
        i=i+1
        cycleAsteroids(shipRect,i)
        # THIS ELSE IS WHERE IF THE SHIP IS HIT IT WILL RETURN TRUE
        # else:
        #     return isCollide
    # deleteDestroyedAsteroids(0)
    # return len(asteroidList)
            
         

    
    
def cycleBullets(asteroid,i,asteroidIndex):
    global bulletList
    isCollide=False
    # print("cycleBulletsI: ",i,"BULLETLISTLENGHT: ",len(bulletList))
    # input("press enter to continue")
    # print("BULLETLISTSIZE: ",len(bulletList))
    if i<len(bulletList):
    # if len(bulletList)>0:
        bullet=bulletList[i]
        # isCollide=calDistBetweenAsteroidandBullet(asteroid,bulletList[i])
        isCollide=calDistBetweenTwoObjects(asteroid,bullet,25)
        # print("LINE 291")
        if isCollide:
            del bulletList[i]
            divideAsteroid(asteroid,asteroidIndex)
        # if i<len(bulletList)-1:
        i=i+1
        cycleBullets(asteroid,i,asteroidIndex)
    # return isCollide
    
# def isCollideBulletAsteroid():
#     global asteroidList
#     global bulletList
#     for i in range(len(asteroidList)):
#         asteroid=asteroidList[i]
#         for j in range(len(bulletList)):
#             # bullet=bullet[j]
#             isCollide=calDistBetweenPoints(asteroid,bulletList[j])
#             if isCollide:
#                 divideAsteroid(asteroid)


def divideAsteroid(asteroid,asteroidIndex):
    global asteroidList
    if asteroid.timesDivided==0:
        # print("timesDivided==0 ","ASTLISTLEN: ",len(asteroidList),"AsteroidIndex: ", asteroidIndex)
        del asteroidList[asteroidIndex]
        # asteroid.timesDivided=1
        # asteroid.image=pygame.transform.scale(asteroid.image,(75,75))
        # asteroid.speedx=randint(1,9)
        # asteroid.speedy=randint(1,9)
        asteroid2=asteroidGameObject.Object(randint(1,9),randint(1,9),sizeAsteroid(asteroid.image,[125,125]),[asteroid.centerx,asteroid.centery],randint(1,360))
        asteroid2.timesDivided=1
        asteroid1=asteroidGameObject.Object(randint(1,9),randint(1,9),sizeAsteroid(asteroid.image,[125,125]),[asteroid.centerx,asteroid.centery],randint(1,360))
        asteroid1.timesDivided=1
        asteroidList.append(asteroid1)
        asteroidList.append(asteroid2)
        # input("this is the first split, press enter to continue")
    elif asteroid.timesDivided==1:
        # print("timesDivided==1 ","ASTLISTLEN: ",len(asteroidList),"AsteroidIndex: ", asteroidIndex)
        del asteroidList[asteroidIndex]
        # asteroid.timesDivided=2
        # asteroid.image=pygame.transform.scale(asteroid.image,(50,50))
        # asteroid.speedx=randint(1,12)
        # asteroid.speedy=randint(1,12)
        asteroid2=asteroidGameObject.Object(randint(1,12),randint(1,12),sizeAsteroid(asteroid.image,[75,75]),[asteroid.centerx,asteroid.centery],randint(1,360))
        asteroid2.timesDivided=2
        asteroid1=asteroidGameObject.Object(randint(1,12),randint(1,12),sizeAsteroid(asteroid.image,[75,75]),[asteroid.centerx,asteroid.centery],randint(1,360))
        asteroid1.timesDivided=2
        asteroidList.append(asteroid1)
        asteroidList.append(asteroid2)
    elif asteroid.timesDivided==2:
        asteroid.timesDivided=3
    #     print("ASTEROIDIMAGE: ",asteroid.image,"timesDivided==2 ","ASTLISTLEN: ",len(asteroidList),"AsteroidIndex: ", asteroidIndex)
        
def deleteDestroyedAsteroids(i):
    global asteroidList
    # if len(asteroidList)>0:
    
    if i<len(asteroidList):
        if asteroidList[i].timesDivided==3:
            del asteroidList[i]
        i=i+1
        deleteDestroyedAsteroids(i)
    if len(asteroidList)==0:
        return len(asteroidList)
    # print("Deleted")

def generateAlienShip(alienShipCount,shipImage,bulletImage):
    # xspeed,yspeed,shipImage,bulletImage,currPosition,angle,bulletList
    global alienShipList
    for i in range(alienShipCount):
        x,y,angle=generateObjectNums()
        # print("X: ",x,"Y: ",y,"ANGLE: ",angle)
        # currPosition=[x,y]
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
        # print("BULLETLIST[i].x: ", bulletList[i].x,"BULLETLIST[i].y: ",bulletList[i].y)
        # print("BULLETLISTSize: ",len(bulletList))
        gameDisplay.blit(ship.shipImage,newRect)
        
def compareAlienToBullets(i):
    global alienShipList
    if i<len(alienShipList):
        # print("LENALIENSHIPLIST: ",len(alienShipList),"I",i)
        # alienShip=alienShipList[i]
        compareBulletsToAlien(alienShipList[i],0)
        # if isCollide:
        #     del alienShipList[i]
        i=i+1
        compareAlienToBullets(i)
    removeShotAlienShips(0)
    
        
def compareBulletsToAlien(alienShip,i):
    global bulletList
    if i<len(bulletList):
        # bullet=bulletList[i]
        isCollide=calDistBetweenTwoObjects(alienShip,bulletList[i],25)
        if isCollide:
            del bulletList[i]
            alienShip.isHit=True
        i=i+1
        compareBulletsToAlien(alienShip,i)
        # return isCollide

def removeShotAlienShips(i):
    global alienShipList
    # for i in range(len(alienShipList)):
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
            # xspeed,yspeed,image,currPosition,angle
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
        # print("BULLETLIST[i].x: ", bulletList[i].x,"BULLETLIST[i].y: ",bulletList[i].y)
        # print("BULLETLISTSize: ",len(bulletList))
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
    # global bulletList
    global asteroidList
    global alienBulletList
    global alienShipList
    # del bulletList[:]
    del asteroidList[:]
    del alienBulletList[:]
    del alienShipList[:]
    # print(boss.centerx,boss.centery)
    x,y=calcObjectLocChange(boss)
    x,y=isOffScreen(x,y)
    boss.centerx=x
    boss.centery=y
    # print(x,y)
    newRect=boss.shipImage.get_rect(center=(x,y))
    
    # print("BULLETLIST[i].x: ", bulletList[i].x,"BULLETLIST[i].y: ",bulletList[i].y)
    # print("BULLETLISTSize: ",len(bulletList))
    gameDisplay.blit(boss.shipImage,newRect) 
    return boss
    #THIS METHOD IS NOT GENERATING THE BULLETS
def generateBossBullets(boss):
    global bossBulletList
    # print("GENERATEDENTER BOSSBULLETLISTSIZE: ",len(bossBulletList))
    # for i in range(10):
    isGenerate=randint(1,100)
    # print(isGenerate%1==0)
    if isGenerate%10==0:
        aBullet=asteroidGameObject.Object(8,8,boss.bulletImage,[boss.centerx,boss.centery],randint(1,360))
        # abullet=generateBullet(8,8,boss.bulletImage,[boss.centerx,boss.centery],angle)
        # print("ABULLET: ",aBullet)
        # print("BULLETLISTBEFOREAPPEND: ",bossBulletList)
        # if abullet != None:
        bossBulletList.append(aBullet)
        # print("BULLETLISTAFTERAPPEND :", bossBulletList)
        
    # print("GENERATEDEND BOSSBULLETLISTSIZE: ",len(bossBulletList))
    
def updateBossBullets():
    global bossBulletList
    # deleteOffScreenBossBullets(0)
    # print("Update BOSSBULLETLISTSIZE: ",len(bossBulletList))
    for i in range(len(bossBulletList)):
        # print("bossBulletList",bossBulletList)
        # print("I",i)
        # print("BOSSBULLETATI",bossBulletList[i])
        # print("X: ",bossBulletList[i].centerx)
        x,y=calcObjectLocChange(bossBulletList[i])
        bossBulletList[i].centerx=x
        bossBulletList[i].centery=y
        newRect=bossBulletList[i].image.get_rect(center=(x,y))
        # print("BULLETLIST[i].x: ", bulletList[i].x,"BULLETLIST[i].y: ",bulletList[i].y)
        # print("BULLETLISTSize: ",len(bulletList))
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
        # bullet=bulletList[i]
        isCollide=calDistBetweenTwoObjects(boss,bulletList[i],25)
        if isCollide:
            del bulletList[i]
            boss.numberofTimesShot=boss.numberofTimesShot+1
        # if boss.numberofTimesShot==50:
        #     del boss
        i=i+1
        compareBulletsToBoss(boss,i)
        
def generateBoss(alienBoss,bulletGreen):
    boss=asteroidGameObject.AlienShip(6,6,alienBoss,bulletGreen,[600,200],180)
    return boss

# def clearBossElements():
#     global bossBulletList
#     del bossBulletList[:]
    

def main():
    global gameDisplay
    global alienShipList
    pygame.init()
    black = (0,0,0)
    white = (255,255,255)
    clock = pygame.time.Clock()
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
    
    # ship=pygame.draw.polygon(ship, white, [[100, 100], [100, 400],[400, 300]], 2)
    # pygame.draw.line(gameDisplay, white, [100, 100], [200, 200], 10)
    x = 360
    y = 480
    # x_change = 0
    # y_change=0
    # car_speed = 0
    displacement=0
    angle=0
    angleChange=0
    rocketAngle=0
    # fire=False
    fireTeal=False
    fireFire=False
    fireGreen=False
    # xspeed,yspeed,image,currPosition,angle
    # shipObject=asteroidGameObject.Object(displacement,displacement,ship,[x,y],angle)
    numberofAsteroids=4
    level=1
    alienShipCount=1
    stopGame=False
    makeBoss=True
    # notFightBoss=True
    # alienFireCount=0
    while not crashed:
        # print("while",crashed)
        for event in pygame.event.get():
            # print("for")
            
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
            
        # count+= 1
        # print("COUNT: ",count)
        
        angle+=angleChange
        rocketAngle=findRocketRotationAngle(correctAngle(angle))
        # print("ANGLE: ",angle,"ROCKETANGLE: ",correctAngle(angle))
        x,y=rocketLocation(displacement,rocketAngle,x,y)
        
        # x,y=rocketLocation(displacement,angle,x,y)
        x,y=isOffScreen(x,y)
        # gameDisplay.fill(black)
        gameDisplay.blit(background,(0,0))
        # if fire:
        shipRect=blitShip(ship,x,y,angle)
        # if fireTeal:
        #     generateBullet(13,13,bulletTeal,[x,y],rocketAngle)
        # if fireGreen:
        #     generateBullet(13,13,bulletGreen,[x,y],rocketAngle)
        # if fireFire:
        #     generateBullet(13,13,bulletFire,[x,y],rocketAngle)
            # time.sleep(.1)
        updateBulletLocs()
        fightBoss=level%5==0
        # print(level%5)
        if not fightBoss:
            updateAsteroidLocs()
            # count=count+1
            # print("CYCLEASTEROIDS, counttimes: ", count)
            cycleAsteroids(shipRect,0)
            stopGame=compareShipToAsteroids(shipRect)
            # print("STOPGAME AFTER COMPARETOASTEROIDS ",stopGame)
            if stopGame:
                input("YOUR DEAD, Press enter to continue")
            astListLen=deleteDestroyedAsteroids(0)
            # print(astListLen)
            if astListLen==0:
                generateAsteroid(asteroidImageList,numberofAsteroids)
                numberofAsteroids=numberofAsteroids+1
                level=level+1
                # print(level)
                if level>=4:
                    generateAlienShip(level-3,alienShip,bulletGreen)
            updateAlienShipLocs()
            compareAlienToBullets(0)
            fireAlienShips(shipRect)
            updateAlienBulletLocs()
            stopGame=compareShipToAlienBullets(shipRect)
            # print(stopGame)
            # print("STOPGAME AFTER COMPSHIPTOALIENBULLETS ", stopGame)
            # shipRect=blitShip(ship,x,y,angle)
            if stopGame:
                # print("YOUR DEAD")
                input("YOUR DEAD, Press enter to continue")
        if fightBoss:
            # notFightBoss=False
            if makeBoss==True:
                boss=generateBoss(alienBoss,bulletGreen)
                makeBoss=False
            boss=updateBoss(boss)
            generateBossBullets(boss)
            updateBossBullets()
            deleteOffScreenBossBullets(0)
            compareBulletsToBoss(boss,0)
            # print("NUMBEROFTIMESSHOT: ",boss.numberofTimesShot,"FIGHTBOSS: ",fightBoss)
            if boss.numberofTimesShot==50:
                fightBoss=False
                makeBoss=True
                level=level+1
                del boss
                # print("IF50",fightBoss)
            stopGame=compareShipToBossBullets(shipRect)
            if stopGame:
                input("YOUR DEAD, Press enter to continue")

        # clock.tick(3000000)
        pygame.display.update()
        
main()
pygame.quit()
quit()

# THINGS TO DO
    # Make explosion image for when you are Hit
    # Make program exit gracfully
    # Scoring system
    # add alien ships and the logic for them to shoot at u
        # Make three types of alien ships
        #     They shoot small white bullets



