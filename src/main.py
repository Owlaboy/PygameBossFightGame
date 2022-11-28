import pygame, math, random
from functools import partial

screen = pygame.display.set_mode((1500,900))
backgroundcolor = (39,38,64)

# These two functions are used to create text on the screen.
def text_object(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()
def message(txt, size, posX, posY, color):
    if posX == None:
        posX = 750
    if posY == None:
        posY = 450
    largeFont = pygame.font.SysFont("comicsansms", size)
    
    # largeFont = pygame.font.Font(pygame.font.get_default_font(), size)
    TextSurf, TextRect = text_object(txt, largeFont, color)
    TextRect.center = (posX, posY)
    screen.blit(TextSurf, TextRect)

# The update function updates the position of most objects in the game. 
def update(obj):
    screen.blit(obj.sprite, (obj.posX, obj.posY))
    obj.Update()

# This function is called when the game ends. It displays the score of the player when winnin or losing.
def suspend(outcome, score):
    pause = True
    
    if outcome == "death":
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        Start()
                    if event.key == pygame.K_ESCAPE:
                        exit()
            pygame.draw.rect(screen, (0,0,0), (500, 400, 490, 300))
            message("You died :/", 59, None, None, (255,255,255))
            message(f"Your score was: {score}", 40, None, 550, (255,255,255))
            message("To play again, press R", 40, None, 600, (255,255,255))
            message("To exit the game, press Esc", 40, None, 650, (255,255,255))

            pygame.display.flip()
    
    elif outcome == "victory":
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        Start()
                    if event.key == pygame.K_ESCAPE:
                        exit()
            
            pygame.draw.rect(screen, (0,0,0), (425, 380, 640, 320))
            message("You Won!!!!!!" , 100, None, None, (255,255,255))
            message(f"Your score was: {score}", 40, None, 550, (255,255,255))
            message("To play again, press R", 40, None, 600, (255,255,255))
            message("To exit the game, press Esc", 40, None, 650, (255,255,255))

            pygame.display.flip()

# The star class is used to create the stars in the background
class Star:
    def __init__(self, size, posX, posY):
        self.size = size
        self.posX = posX
        self.posY = posY

    def Update(self):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.posX), int(self.posY)), int(self.size/2))
        pygame.draw.circle(screen, backgroundcolor, (int(self.posX - self.size/2), int(self.posY - self.size/2)), int(self.size/2))
        pygame.draw.circle(screen, backgroundcolor, (int(self.posX - self.size/2), int(self.posY + self.size/2)), int(self.size/2))
        pygame.draw.circle(screen, backgroundcolor, (int(self.posX + self.size/2), int(self.posY - self.size/2)), int(self.size/2))
        pygame.draw.circle(screen, backgroundcolor, (int(self.posX + self.size/2), int(self.posY + self.size/2)), int(self.size/2))

# The Enemybullet class is used to create the 
class Enemybullet:
    def __init__(self, posX, posY, velX, velY, size):
        self.size = size
        self.posX = posX
        self.posY = posY
        self.velX = velX
        self.velY = velY
        self.width= size
        
    def draw(self):
        self.posX += self.velX
        self.posY += self.velY
        pygame.draw.rect(screen, (255,0,0), (self.posX, self.posY, self.size, self.size))       

#  The class attacks creates the different methods for the boss' different attack pattern
class attacks:
    def targetting(self, startingX, startingY, target, speed):
        velX = (target.posX + target.width/2 - (startingX))
        velY = (target.posY + target.height/2 - (startingY))
        speedmodifier = speed
        velConstant = math.sqrt(velX**2 + velY**2)/speedmodifier
        velX = velX/velConstant
        velY = velY/velConstant

        return(velX, velY)

    def targettedBullet(self, target):
        velX = self.targetting(self.posX+self.width/2, self.posY+self.height, target, 10)[0]
        velY = self.targetting(self.posX+self.width/2, self.posY+self.height, target, 10)[1]

        self.bullets.append(Enemybullet(self.posX + self.width/2 ,self.posY + self.height, velX, velY, 30))
    
    def targettedBullet2(self, target):
        startHeight = self.posY+self.height
        rootX = self.posX+self.width/2
        bull1 = self.targetting(rootX - 50, startHeight, target, 10)
        bull2 = self.targetting(rootX - 25, startHeight, target, 10)
        bull3 = self.targetting(rootX, startHeight, target, 10)
        bull4 = self.targetting(rootX + 25, startHeight, target, 10)
        bull5 = self.targetting(rootX + 50, startHeight, target, 10)
        
        self.bullets.append(Enemybullet(rootX - 50, startHeight, bull1[0], bull1[1], 30))
        self.bullets.append(Enemybullet(rootX - 25, startHeight, bull2[0], bull2[1], 30))
        self.bullets.append(Enemybullet(rootX - 0,  startHeight, bull3[0], bull3[1], 30))
        self.bullets.append(Enemybullet(rootX + 25, startHeight, bull4[0], bull4[1], 30))
        self.bullets.append(Enemybullet(rootX + 50, startHeight, bull5[0], bull5[1], 30))
    
    def targettedBullet3(self, target):
        startHeight = self.posY+self.height
        rootX = self.posX+self.width/2
        bull1 = self.targetting(rootX - 150, startHeight, target, 10)
        bull2 = self.targetting(rootX - 100, startHeight, target, 10)
        bull3 = self.targetting(rootX - 50, startHeight, target, 10)
        bull4 = self.targetting(rootX, startHeight, target, 10)
        bull5 = self.targetting(rootX + 50, startHeight, target, 10)
        bull6 = self.targetting(rootX + 100, startHeight, target, 10)
        bull7 = self.targetting(rootX + 150, startHeight, target, 10)
        
        self.bullets.append(Enemybullet(rootX - 150, startHeight, bull1[0], bull1[1], 30))
        self.bullets.append(Enemybullet(rootX - 100, startHeight, bull2[0], bull2[1], 30))
        self.bullets.append(Enemybullet(rootX - 50,  startHeight, bull3[0], bull3[1], 30))
        self.bullets.append(Enemybullet(rootX + 0, startHeight,   bull4[0], bull4[1], 30))
        self.bullets.append(Enemybullet(rootX + 50, startHeight,  bull5[0], bull5[1], 30))
        self.bullets.append(Enemybullet(rootX + 100, startHeight, bull6[0], bull6[1], 30))
        self.bullets.append(Enemybullet(rootX + 150, startHeight, bull7[0], bull7[1], 30))

    def sideSweepRight(self):
        self.bullets.append(Enemybullet(0, 780, 10, 0, 19))
        self.bullets.append(Enemybullet(0, 760, 10, 0, 19))
        self.bullets.append(Enemybullet(0, 740, 10, 0, 19))
        self.bullets.append(Enemybullet(0, 720, 10, 0, 19))
        self.bullets.append(Enemybullet(0, 700, 10, 0, 19))
        self.bullets.append(Enemybullet(0, 680, 10, 0, 19))
        self.bullets.append(Enemybullet(0, 660, 10, 0, 19))

    def sideSweepRight2(self):
        self.bullets.append(Enemybullet(0, 780, 10, 0, 19))
        self.bullets.append(Enemybullet(0, 760, 10, 0, 19))
        self.bullets.append(Enemybullet(0, 740, 10, 0, 19))
        self.bullets.append(Enemybullet(0, 720, 10, 0, 19))
        self.bullets.append(Enemybullet(0, 700, 10, 0, 19))
        self.bullets.append(Enemybullet(0, 680, 10, 0, 19))
        self.bullets.append(Enemybullet(0, 660, 10, 0, 19))
        self.bullets.append(Enemybullet(0, 640, 10, 0, 19))
        self.bullets.append(Enemybullet(0, 620, 10, 0, 19))
        self.bullets.append(Enemybullet(0, 600, 10, 0, 19))
        self.bullets.append(Enemybullet(0, 580, 10, 0, 19))

    def sideSweepLeft(self):
        self.bullets.append(Enemybullet(1500, 780, -10, 0, 19))
        self.bullets.append(Enemybullet(1500, 760, -10, 0, 19))
        self.bullets.append(Enemybullet(1500, 740, -10, 0, 19))
        self.bullets.append(Enemybullet(1500, 720, -10, 0, 19))
        self.bullets.append(Enemybullet(1500, 700, -10, 0, 19))
        self.bullets.append(Enemybullet(1500, 680, -10, 0, 19))
        self.bullets.append(Enemybullet(1500, 660, -10, 0, 19))

    def sideSweepLeft2(self):
        self.bullets.append(Enemybullet(1500, 780, -10, 0, 19))
        self.bullets.append(Enemybullet(1500, 760, -10, 0, 19))
        self.bullets.append(Enemybullet(1500, 740, -10, 0, 19))
        self.bullets.append(Enemybullet(1500, 720, -10, 0, 19))
        self.bullets.append(Enemybullet(1500, 700, -10, 0, 19))
        self.bullets.append(Enemybullet(1500, 680, -10, 0, 19))
        self.bullets.append(Enemybullet(1500, 660, -10, 0, 19))
        self.bullets.append(Enemybullet(1500, 640, -10, 0, 19))
        self.bullets.append(Enemybullet(1500, 620, -10, 0, 19))
        self.bullets.append(Enemybullet(1500, 600, -10, 0, 19))
        self.bullets.append(Enemybullet(1500, 580, -10, 0, 19))

    def leftandright(self):
        self.sideSweepLeft()
        self.sideSweepRight()

    def toptobottom(self):
        displacement = random.randint(0, 300)
        for i in range(5):
            self.bullets.append(Enemybullet(i*300 + displacement,0,0,10,30))

# The class mörkö is used to create the boss and all the methods associated with the boss
class Mörkö(attacks):
    def __init__(self, target, difficulty):
        self.sprite = pygame.image.load("hirvio.png")
        self.sprite = pygame.transform.scale(self.sprite, (250, 75))
        
        self.width = 250
        self.height = 75

        self.posX = 750
        self.posY = 40
        self.i = 1
        
        self.bullets = []

        self.difficulty = difficulty

        # Here we set the health based on the game difficulty
        if self.difficulty == "easy":
            self.maxhealth = 100
            self.health = 100
        if self.difficulty == "normal":
            self.maxhealth = 200
            self.health = 200
        if self.difficulty == "hard":
            self.maxhealth = 300
            self.health = 300

        self.target = target

        # The different attack patterns of the boss are saved in lists.
        # When the boss falls under 50%. The game starts using attacks from the second list.
        # The second list contains strnger version of the same attacks.
        # The second list is called only in hard mode and in the second phase of normal mode.
        self.attacks = [partial(attacks.targettedBullet2, self, self.target), partial(attacks.sideSweepRight, self), partial(attacks.sideSweepLeft, self), partial(attacks.toptobottom, self)]
        self.attacks2 = [partial(attacks.targettedBullet3, self, self.target), partial(attacks.sideSweepLeft2, self), partial(attacks.sideSweepRight2, self), partial(attacks.leftandright, self)]

    # The Update method moves the Boss left and right. Sine and cosine are used to make the movement consistant and smooth.
    # Based on the difficulty of the game the boss moves differently.
    # On easy mode the boss always moves slowly in the middle.
    # On normal mode the boss moves like on easy mode while above 50% health.
    # After falling under 50% the boss starts moving faster and further to the left and right.
    # On hard mode the boss moves constantly from left to right and back very quickly.
    # The health doesnt change the movement of the hard mode boss.
    def Update(self):
        if self.difficulty == "easy":
            self.posX = math.cos(self.i * 0.3) * 200 + 700 - 50
            self.posY = math.sin(self.i * 2) * 50 + 75
        elif self.difficulty == "normal":
            if self.maxhealth <= self.health*2:
                self.posX = math.cos(self.i * 0.3) * 200 + 750 - 100
                self.posY = math.sin(self.i * 2) * 50 + 75
            else:
                self.posX = math.cos(self.i * 0.5) * 500 + 750 - 100
                self.posY = math.sin(self.i * 2) * 50 + 75
        elif self.difficulty == "hard":
            self.posX = math.cos(self.i * 0.7) * 500 + 750 - 100
            self.posY = math.sin(self.i * 2) * 50 + 75
        self.i += 0.05

    # This method reduces the health of the boss whenever it is called.
    # It also checks if the health goes below zero, in which case the game ends in victory
    def hit(self, dmg, score):
        self.health -= dmg
        if self.health <= 0:
            suspend("victory", score)

    # Updates all the enemy projectiles on the screen.
    def updatebullets(self):
        for bullet in self.bullets:
                bullet.draw()

# The class bullet is used to create the players attacks. Each bullet is an "ovi.png" image that has been rotated and transformed to a more appropiate size
class Bullet:
    def __init__(self, posX, posY, damage):
        self.sprite = pygame.image.load("ovi.png")
        self.sprite = pygame.transform.scale(self.sprite, (10, 20))
        self.sprite = pygame.transform.rotate(self.sprite, 180)
        
        self.damage = damage

        self.posX = posX
        self.posY = posY
        
        self.velY = -12

    def Update(self):
        self.posY += self.velY

# This class, roboto, is used to create the player charatcer
class Roboto:
    def __init__(self):
        # Creating the 
        self.sprite = pygame.image.load("robo.png")
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()
        
        # Generating the positional arguments.
        # The movement in x and y are separated
        # Player movement is handled by three variables.
        # Acceleration affects the velocity and velocity affects the position. Each frame of the game the current acceleration is added to the velocity and the current velocity is added to the position variable.
        # All the movement is handled by the update function.
        self.posX = 100
        self.posY = 700
        self.velX = 0
        self.velY = 0
        self.accelX = 0
        self.accelY = 0
        self.weight = 1
        self.velMAX = 10

        # These arguments are used to limit the movement and check how the robot should be moving
        self.moveRight = False 
        self.moveLeft = False
        self.extrajumps = 1

        self.damage = 2
        self.bullets = []

    # This methods creates the projectiles that the player shoots.
    def shoot(self):
        self.bullets.append(Bullet(self.posX + self.width/2 - 5, self.posY -10, self.damage))


    def jump(self):
        self.velY = -30
        self.extrajumps -= 1

    def Update(self):
        # The update method first handles the movement in the x direction and then the y direction.
        # Here we check in which direction we are going to move based on the moveRight and moveLeft atributes.
        # First we check if both directions are pressed down which leads to the player character to stop moving.
        if self.moveLeft and self.moveRight:
            self.accelX = 0
            self.velX = 0
        # Then we check if were going to move right or left. Depending on which direction the acceleration is set to 1 to go rigth or -1 to go left
        elif self.moveRight:
            self.accelX = 1
        elif self.moveLeft:
            self.accelX = -1
        # When no buttons are pressed the player character is slowed down by changing the acceleration to be against the current veloctiy
        # This is done by checking if the velocity is something else than 0
        # If the velocity is not 0 then we change the acceleration to be opposite to the velocity.
        elif not self.moveRight or not self.moveLeft:
            if self.velX > 0:
                self.accelX = -1
            elif self.velX < 0:
                self.accelX = 1
            else:
                self.accelX = 0

        # These two if statements check that the player isnt moving past the screen.
        if self.posX < 0:
            self.posX = 0
        if self.posX > 1500 - self.width:
            self.posX = 1500 - self.width

        # After the acceleration checks are completed we add the appropriate acceleration to the velocity
        self.velX += self.accelX
        
        # Now that we have the current velocity we check that it doesnt pass the maximum velocity.
        # If it does we set the velocity to the maximum velocity.
        if self.velX >= 0:
            self.velX = min(self.velX, self.velMAX)
        elif self.velX < 0:
            self.velX = max(self.velX, -self.velMAX)
        
        # After the velocity is sorted we add the velocity to the position atribute.
        self.posX += self.velX

        # The Y direction has a constant acceleration pulling the character down due to "gravity"
        # Due to gravity we must check if the player is in the air. If he is then the consant "self.weight" is set to 1 otherwise it is zero
        # At the same time we can also update the extra jumps to 1 whenever the player is on the ground. 
        if self.posY + self.height < 800:
            self.weight = 1
        else:
            self.weight = 0
            self.extrajumps = 1

        # Now we add the y accceleration and weight constant to the velocity.
        self.velY += self.accelY + self.weight
        if self.velY >= 0:
            self.velY = min(self.velY, self.velMAX+10)
        elif self.velY < 0:
            self.velY = max(self.velY, -self.velMAX-15)
        
        # Then the position is changed by adding the cellocity to it
        self.posY += self.velY
        
        # This if statement makes the player not fall off the screen.
        if self.posY > 800 - self.height:
            self.posY = 800 - self.height

    # This method checks if the player has come in contact with an enemy bullet
    def checkhit(self, bullet, score):
        if ((self.posX+9 >= bullet.posX and self.posX+9 <= bullet.posX+bullet.width) or (self.posX+9+30  >= bullet.posX and self.posX+9+30 <= bullet.posX+bullet.width)) and ((self.posY+6 >= bullet.posY and self.posY+6 <= bullet.posY+bullet.width) or (self.posY+6+28  >= bullet.posY and self.posY+6+28 <= bullet.posY+bullet.width)):
            suspend("death", score)

# The coin class is used to create the pickups that make the player deal more damage
class Coin:
    def __init__(self, posX, posY):
        self.posX = posX
        self.posY = posY
        self.sprite = pygame.image.load("kolikko.png")
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()
    
    # The Update method is required to use the update function
    # 
    def Update(self):
        pass 

# The MiscElements class is used to handle miscalaneous tasks 
class MiscElements:
    def __init__(self):
        self.counter = 0
        self.coins = []
        self.score = 0

    # add one to the counter
    # The counter is used to 
    def count(self):
        self.counter += 1

    # Methods for adding and subtracting points from the player's score
    def scoreup(self, points):
        self.score += points
    def scoredown(self, points):
        self.score -= points

    # Method for creating coins
    def spawncoin(self):
        self.coins.append(Coin(random.randint(0,1500), random.randint(300,780)))

    # Drawing the planet at the bottom
    def planet(self):
        pygame.draw.circle(screen, (0,0,255),(750, 3800), 3000)

    # This method creates the healthbar at the bottom.
    # The rectangle has to be moved to the right every time the boss loses health since the rectnagle is drawn from left to right.
    def healthbar(self, boss):
        frac2 = None
        frac1 = boss.health/boss.maxhealth
        frac2 = 1 - frac1
        pygame.draw.rect(screen, (255,0,0), (200 + frac2 * 1200, 850 ,  frac1 * 1200, 10))
        message("Mörkö, the Eater of Worlds", 20, 1200, 840, (255,255,255))

# The actual game is within the RobotDefence class.
class RobotDefence:
    def __init__(self, difficulty):
        screen = pygame.display.set_mode((1500,900))
        pygame.display.set_caption('Roboot defence')

        backgroundcolor = (39,38,64)
        clock = pygame.time.Clock()

        self.difficulty = difficulty

        roboot = Roboto()
        Boss = Mörkö(roboot, difficulty)
        miscElements = MiscElements()

        # Here we create the stars that go into the background
        # They are randomly generated to be everytwhere on the screen
        stars = []
        for i in range(0, 30):
           stars.append(Star(random.randint(5,10)*2, random.randint(0, 1500), random.randint(0, 800)))
           #stars.append(Star(10,100,100))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                # Checking each keypress and calling the appropiate functions/methods
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit()
                    if event.key == pygame.K_SPACE:
                        # In case of a jump we also check how many jumps he has left so that there arent infinte jumps.
                        if roboot.extrajumps > 0:
                            roboot.jump()
                    if event.key == pygame.K_RIGHT:
                        roboot.moveRight = True
                    if event.key == pygame.K_LEFT:
                        roboot.moveLeft = True
                    if event.key == pygame.K_x:
                        roboot.shoot()

                        # The attack settings for easy mode
                        if self.difficulty == "easy":
                            Boss.attacks[random.randint(0,len(Boss.attacks)-1)]()
                        
                        # The attack settings for normal mode
                        # At 50% health the boss begins to use harder attack patterns
                        # When the boss hits less than 25% health it starts to do two attacks at once
                        elif self.difficulty == "normal":
                            if Boss.health/Boss.maxhealth > 0.5:
                                Boss.attacks[random.randint(0,len(Boss.attacks)-1)]()
                            elif Boss.health/Boss.maxhealth > 0.25:
                                Boss.attacks2[random.randint(0,len(Boss.attacks2)-1)]()
                            else:
                                Boss.attacks2[random.randint(0,len(Boss.attacks2)-1)]()
                                Boss.attacks2[random.randint(0,len(Boss.attacks2)-1)]()
                        
                        # The attack settings for hard mode
                        # In hardmode the boss always shoots basic projectiles at the player and does an extra attack.
                        # At 50% health the boss begins to use harder attack patterns
                        # At less than 25% health the boss casts an extra attack
                        elif self.difficulty == "hard":
                            Boss.attacks[0]()
                            if Boss.health/Boss.maxhealth > 0.5:
                                Boss.attacks[random.randint(0,len(Boss.attacks)-1)]()
                            elif Boss.health/Boss.maxhealth > 0.25:
                                Boss.attacks2[random.randint(0,len(Boss.attacks2)-1)]()
                            else:
                                Boss.attacks2[random.randint(0,len(Boss.attacks2)-1)]()
                                Boss.attacks2[random.randint(0,len(Boss.attacks2)-1)]()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT: 
                        roboot.moveLeft = False
                    if event.key == pygame.K_RIGHT:
                        roboot.moveRight = False
                    if event.key == pygame.K_SPACE:
                        roboot.accelY = 0

            screen.fill(backgroundcolor)

            # Drawing each star 
            for star in stars:
                star.Update()

            # Drawing the player and boss
            update(Boss)
            update(roboot)
            
            # Updating and drawing all of the enemy projectiles. This is done with the updatebullets method.
            Boss.updatebullets()

            # Drawing each player bullet and checking for collisions with the boss
            for bullet in roboot.bullets:
                update(bullet)
                if bullet.posX >= Boss.posX and bullet.posX < Boss.posX + 250 and bullet.posY >= Boss.posY and bullet.posY <  Boss.posY + 75:
                    Boss.hit(bullet.damage, miscElements.score)
                    miscElements.scoreup(5)
                    roboot.bullets.remove(bullet)

            # Generating the Miscalaneous elements
            miscElements.planet()
            miscElements.healthbar(Boss)

            # Creates a coin if the random integer is equal to 1
            if random.randint(0,1000) == 1:
                miscElements.spawncoin()
            
            # Check for every coin if the coin has been picked up and update the coin to be rendered
            for coin in miscElements.coins:
                if ((coin.posX >= roboot.posX and coin.posX <= roboot.posX+roboot.width) or (coin.posX+coin.width >= roboot.posX and coin.posX+coin.width <= roboot.posX+roboot.width)) and ((coin.posY >= roboot.posY and coin.posY <= roboot.posY+roboot.height) or (coin.posY+coin.height >= roboot.posY and coin.posY+coin.height <= roboot.posY+roboot.height)): 
                    miscElements.coins.remove(coin)
                    roboot.damage += 2
                    miscElements.scoreup(20)
                update(coin)


            pygame.display.flip()
            miscElements.count()

            # The socre of the of the player is reduced by two every second
            if miscElements.counter % 30 == 0:
                miscElements.scoredown(1)

            # Check if the player has been hit by an attack
            for bullet in Boss.bullets:
                roboot.checkhit(bullet, miscElements.score)

            clock.tick(60)

# This function is used to generate the starting UI and give information about the game. 
class Start:
    def __init__(self):
        pygame.init()

        screen = pygame.display.set_mode((1500,900))
        pygame.display.set_caption('Roboot defence')

        defender = pygame.image.load("robo.png")

        screen.blit(defender,(100,700))

        message("Robot Defence", 60, None, 100, (255,255,255))
        message("Defend the planet from the scary monster, Mörkö.", 40, None, 150, (255,255,255))
        
        message("Move with the left and right arrow keys and jump with the space bar.", 40, None, 200, (255,255,255))
        message("You can shoot at the monster by pressing X.", 40, None, 250, (255,255,255))
        message("The monster launches counter attacks whenever you shoot.", 40, None, 300, (255,255,255))
        message("Worry not, as only the robot's head can be hit.", 40, None, 350, (255,255,255))
        message("Gain points by hitting the monster and picking up coins", 40, None, 400, (255,255,255))
        message("Gain points by hitting the monster and picking up coins", 40, None, 400, (255,255,255))
        
        message("To play on easy mode press E", 40, None, 600, (255,255,255))
        message("To play on normal mode press N", 40, None, 650, (255,255,255))
        message("To play on hard mode press H", 40, None, 700, (255,255,255))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit()
                    if event.key == pygame.K_e:
                        RobotDefence("easy")
                    if event.key == pygame.K_n:
                        RobotDefence("normal")
                    if event.key == pygame.K_h:
                        RobotDefence("hard")
            pygame.display.flip()

if __name__ == "__main__":
    Start()
    