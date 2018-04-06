class Object:
    # def __init__(self,image,currPosition,deltaX,deltaY):
    def __init__(self,xspeed,yspeed,image,currPosition,angle):
        self.image=image
        self.centerx=currPosition[0]
        self.centery=currPosition[1]
        self.angle=angle
        # self.speed=speed
        self.xspeed=xspeed
        self.yspeed=yspeed
        self.timesDivided=0
        # self.deltaX=deltaX
        # self.deltaY=deltaY
        
        
        
class AlienShip:
    def __init__(self,xspeed,yspeed,shipImage,bulletImage,currPosition,angle):
        # self.speed=speed
        self.xspeed=xspeed
        self.yspeed=yspeed
        self.shipImage=shipImage
        self.bulletImage=bulletImage
        self.centerx=currPosition[0]
        self.centery=currPosition[1]
        self.angle=angle
        self.numberofTimesShot=0
        self.isHit=False
        
    # def setTimesDivided(self,divisions):
    #     self.timesDivided=divisions
    
    
    # def __init__(self,speed,image,currPosition,angle):
    #     self.image=image
    #     self.x=currPosition[0]
    #     self.y=currPosition[1]
    #     self.angle=angle
    #     self.speed=speed
    #     # self.deltaX=deltaX
    #     # self.deltaY=deltaY
    # # def calcDeltaxandDeltay