import pygame
import time
import heapq
import math
import random

pygame.init()


walkRight = [pygame.image.load('img/R1.png'), pygame.image.load('img/R2.png'), pygame.image.load('img/R3.png'),
             pygame.image.load('img/R4.png'), pygame.image.load('img/R5.png'), pygame.image.load('img/R6.png'),
             pygame.image.load('img/R7.png'), pygame.image.load('img/R8.png'), pygame.image.load('img/R9.png')]
walkLeft = [pygame.image.load('img/L1.png'), pygame.image.load('img/L2.png'), pygame.image.load('img/L3.png'),
            pygame.image.load('img/L4.png'), pygame.image.load('img/L5.png'), pygame.image.load('img/L6.png'),
            pygame.image.load('img/L7.png'), pygame.image.load('img/L8.png'), pygame.image.load('img/L9.png')]
bg = pygame.image.load('img/map.png')
bg_menu = pygame.image.load('img/Forest_back.png')

bg = pygame.transform.scale(bg, (1700, 900))
bg_menu = pygame.transform.scale(bg_menu, (1700, 900))

char = pygame.image.load('img/standing.png')


class Anamy(object):
    walkRight = [
        pygame.image.load('img/R1E.png'), pygame.image.load('img/R2E.png'), pygame.image.load('img/R3E.png'),
        pygame.image.load('img/R4E.png'), pygame.image.load('img/R5E.png'), pygame.image.load('img/R6E.png'),
        pygame.image.load('img/R7E.png'), pygame.image.load('img/R8E.png'), pygame.image.load('img/R9E.png'),
        pygame.image.load('img/R10E.png'), pygame.image.load('img/R11E.png')
    ]
    
    walkLeft = [
        pygame.image.load('img/L1E.png'), pygame.image.load('img/L2E.png'), pygame.image.load('img/L3E.png'),
        pygame.image.load('img/L4E.png'), pygame.image.load('img/L5E.png'), pygame.image.load('img/L6E.png'),
        pygame.image.load('img/L7E.png'), pygame.image.load('img/L8E.png'), pygame.image.load('img/L9E.png'),
        pygame.image.load('img/L10E.png'), pygame.image.load('img/L11E.png')
    ]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.walkcount = 0
        self.val = 1.3  
        self.hitbox = (self.x + 17, self.y, 32, 70)
        self.direction = 1  
        self.path = [self.x, self.end]
        self.anamy_platform=5

    def teleport_to_next_platform(self, drum_optimal, graf):
        if not drum_optimal:
            return 
        next_platform_number = drum_optimal[1] 
        if next_platform_number != self.anamy_platform:
            
            next_platform = graf.platforme[next_platform_number]
            self.x = next_platform.x + next_platform.width // 2 
            self.y = next_platform.y - self.height+50  
            self.anamy_platform = next_platform_number 
            drum_optimal.pop(0)     

    def draw(self, window, player):
   
        
        if self.walkcount + 1 >= 33:
            self.walkcount = 0
        if self.direction > 0:  
            window.blit(self.walkRight[self.walkcount // 3], (self.x, self.y))
        else: 
            window.blit(self.walkLeft[self.walkcount // 3], (self.x, self.y))
        self.walkcount += 1

       
        self.hitbox = (self.x + 17, self.y, 32, 70)
        pygame.draw.rect(window, (0, 0, 0), self.hitbox, 2)

    def draw_default(self, window):
        self.move_default()
        if self.walkcount + 1 >= 33:
            self.walkcount = 0
        if self.val > 0:
            window.blit(self.walkRight[self.walkcount // 3], (self.x, self.y))
            self.walkcount += 1
        else:
            window.blit(self.walkLeft[self.walkcount // 3], (self.x, self.y))
            self.walkcount += 1
        self.hitbox = (self.x + 17, self.y, 32, 70)  
        pygame.draw.rect(window, (0, 0, 0), self.hitbox, 2)  

    def move_default(self):
        if self.val > 0:
            if self.x + self.val < self.path[1]:
                self.x += self.val
            else:
                self.val *= -1
                self.walkcount = 0
        else:
            if self.x - self.val > self.path[0]:
                self.x += self.val
            else:
                self.val *= -1
                self.walkcount = 0        

    def move(self, player):
        
        print("goblinul se afla pe platforma ",self.anamy_platform) 

        
    def hit(self):
        print("hit")
class Platrforms:
    def __init__(self, platform_number, x, y, width, height):
        self.platform_number = platform_number
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jump_force = 10
        self.vecini = []

    def draw(self, window, r, g, b):
        red_color = (r, g, b)  
        pygame.draw.rect(window, red_color, (self.x, self.y, self.width, self.height))

    def adauga_vecin(self, vecin, cost):
        self.vecini.append((vecin, cost))

    def distanta_euclidiana(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)  

class GameOver:

    def __init__(self,x,y,width,height,color,text):

        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.color=color
        self.text=text
        self.font = pygame.font.Font(None, 36) 

    def draw(self, window):
        
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

        # Render the text
        text_surface = self.font.render(self.text, True, (255, 255, 255)) 
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2)) 
        window.blit(text_surface, text_rect)
    



class Graf:
    def __init__(self):
        self.platforme = {}

    def adauga_platforma(self, number, x, y, w, h):
        platforma = Platrforms(number, x, y, w, h)
        self.platforme[number] = platforma
        return platforma

    def adauga_legatura(self, num_1, num_2, cost):
        if num_1 in self.platforme and num_2 in self.platforme:
            self.platforme[num_1].adauga_vecin(self.platforme[num_2], cost)
            self.platforme[num_2].adauga_vecin(self.platforme[num_1], cost)

    def a_star(self, start, end):
        deschis = []  
        heapq.heappush(deschis, (0, self.platforme[start]))  
        costuri = {nume: float('inf') for nume in self.platforme}  
        costuri[start] = 0
        parinte = {nume: None for nume in self.platforme} 

        while deschis:
            f_current, current = heapq.heappop(deschis) 
         
            if current.platform_number == end:
                drum = []
                while current:
                    drum.append(current.platform_number)
                    current = parinte[current.platform_number]
                return drum[::-1] 
      
            for vecin, cost in current.vecini:
                g_cost = costuri[current.platform_number] + cost
               
                f_cost = g_cost + current.distanta_euclidiana(self.platforme[end]) 

            
                if g_cost < costuri[vecin.platform_number]:
                    costuri[vecin.platform_number] = g_cost
                    parinte[vecin.platform_number] = current
                    heapq.heappush(deschis, (f_cost, vecin)) 

        return None 

class player():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.prev_y=0
        self.width = width
        self.height = height
        self.step = 5
        self.is_jump = False
        self.left = False
        self.right = False
        self.walk_count = 0
        self.jump_count=True
        self.jump_speed=0.15
        self.repause = True
        self.hitbox = (self.x + 17, self.y, 32, 70)
        self.platform=0

    
        
        
    def hit(self):
        print("hit")

    def on_platform(self, platform_1, platform_2, platform_3, platform_4, platform_5,platform_6,platform_8,platform_7,platform_9,platform_11,platform_10,platform_13,platform_12,platform_14,platform_15,platform_16,base_platform_left,base_platfor_right):

        if self.platform==platform_1.platform_number:
              
           

            if self.x>platform_5.x+platform_5.width+100:

                self.x=platform_6.x
                self.platform=platform_6.platform_number
                return platform_6.y



        if self.platform==base_platform_left.platform_number:    
            if self.x > platform_1.x and self.x < platform_1.x + platform_1.width and self.y == base_platform_left.y:
                self.platform = platform_1.platform_number
                
                return platform_1.y

            if self.x>base_platform_left.x+base_platform_left.width-180:
                self.platform=platform_3.platform_number
                return platform_3.y    
            
        if self.platform==base_platform_left.platform_number:
              if self.x > platform_2.x and self.x < platform_2.x + platform_2.width and self.y == base_platform_left.y:
                self.platform = platform_2.platform_number
                return platform_2.y

        if self.platform==base_platfor_right.platform_number:
              if self.x > platform_4.x and self.y == base_platform_left.y:
                self.platform = platform_4.platform_number
                return platform_4.y

            
        if self.platform==platform_1.platform_number or self.platform==platform_2.platform_number:    
              if self.x > platform_5.x and self.x < platform_5.x + platform_5.width and self.y==platform_1.y or self.y==platform_2.y :
                
                self.platform = platform_5.platform_number
                return platform_5.y
              
              

        if self.platform==platform_5.platform_number:    
              if self.x >= platform_8.x and self.x < platform_8.x + platform_8.width and self.y==platform_5.y  :
                
                self.platform = platform_8.platform_number
                return platform_8.y
              if self.x>platform_5.x+165 and self.x<=platform_5.x+platform_5.width/2+80:
                  self.x=platform_13.x+20
                  self.platform=platform_13.platform_number
                  return platform_13.y
        if self.platform==base_platform_left.platform_number:    
              if self.x>platform_3.x and self.x<platform_3.width+platform_3.x and self.y==base_platform_left.y:

                self.platform=platform_3.platform_number
                return platform_3.y
        
        if self.platform==platform_3.platform_number:
            if self.x>platform_3.x and self.x < platform_3.x+40 and self.y==platform_3.y:
                
                self.platform=platform_6.platform_number
                self.x+platform_6.x+platform_6.width-10
                return platform_6.y

            if self.x>platform_3.x+platform_3.width/2+20:
                self.platform=platform_7.platform_number 
                self.x=platform_7.x+10   
                return platform_7.y
            
        if self.platform==platform_6.platform_number:

            if self.x>platform_6.x and self.x<platform_6.x+200:
                self.platform=platform_8.platform_number
                self.x=platform_8.x+platform_8.width-20
                return platform_8.y           
        

        if self.platform==platform_7.platform_number or self.platform==platform_4.platform_number:

            if self.x>platform_3.x+platform_3.width/2 and self.x<platform_3.x+platform_3.width:
                self.x=platform_7.x
                self.platform=platform_7.platform_number
                return platform_7.y
            if self.x>platform_4.x and self.x<platform_4.x+50 and self.y==platform_4.y:
                self.x=platform_7.x+platform_7.width-20
                self.platform=platform_7.platform_number
                return platform_7.y


        if self.platform==platform_8.platform_number:
                
            if self.x>platform_8.x+platform_8.width/2 and self.x<platform_8.x+platform_8.width and self.y==platform_8.y:
               
               
               self.x=platform_9.x+30
               self.platform=platform_9.platform_number
               return platform_9.y



        if self.platform==platform_7.platform_number:

            if self.x>platform_7.x+platform_7.width/2:
                self.platform=platform_11.platform_number
                return platform_11.y

        if self.platform==platform_11.platform_number:
            if self.x>platform_11.x and self.x<platform_11.x+platform_11.width/2 and self.y==platform_11.y:

                self.x=platform_10.x+platform_10.width
                self.platform=platform_10.platform_number
                return platform_10.y
            if self.x>platform_11.x+platform_11.width/2+10 and self.y==platform_11.y:

                self.x=platform_16.x
                self.platform=platform_16.platform_number
                return platform_16.y
        if self.platform==platform_10.platform_number:
             if self.x>platform_10.x+platform_10.width/2 and self.x<platform_10.x+platform_10.width and self.y==platform_10.y:
                self.x=platform_11.x
                self.platform=platform_11.platform_number
                return platform_11.y
             if self.x>platform_10.x and self.x<platform_10.x+platform_10.width/2 and self.y==platform_10.y:
                self.x=platform_14.x+platform_14.width-10
                self.platform=platform_14.platform_number
                return platform_14.y
        if self.platform==platform_9.platform_number:
            if self.x>platform_9.x+platform_9.width/2+30:
                self.x=platform_10.x+20
                self.platform=platform_10.platform_number
                return platform_10.y
            if self.x>platform_9.x and self.x<platform_9.x+platform_9.width/2+30:
                self.x=platform_14.x
                self.platform=platform_14.platform_number
                return platform_14.y
        if self.platform==platform_13.platform_number:
            if self.x>platform_13.x and self.x<platform_13.x+50 and self.y==platform_13.y:
                self.platform=platform_12.platform_number
                self.x=platform_12.x+platform_12.width-10
                return platform_12.y 

        if self.platform==platform_12.platform_number:

            if self.x>platform_12.x+platform_12.width/2 and self.x<platform_12.x+platform_12.width and self.y==platform_12.y:
                
                self.x=platform_13.x+10
                self.platform=platform_13.platform_number
                return platform_13.y

        if self.platform==platform_14.platform_number:

            if self.x>platform_14.x+platform_14.width/2 and self.y==platform_14.y:
                self.x=platform_15.x
                self.platform=platform_15.platform_number
                return platform_15.y        

        if self.platform==platform_15.platform_number:

            if self.x>platform_15.y+platform_15.width/2 and self.y==platform_15.y:
                self.x=platform_16.x
                self.platform=platform_16.platform_number
                return platform_16.y

        if self.platform==platform_16.platform_number:

            if self.x>platform_16.x and self.x<platform_16.x+platform_16.width/2 and self.y==platform_16.y:
                self.x=platform_15.x+platform_15.wifth-10
                self.platform=platform_15.platform_number
                return platform_15.y


        return self.y
    
          

    def fall(self, platform_1, platform_2, platform_3, platform_4, platform_5,platform_6,platform_8,platform_7,platform_9,platform_11,platform_10,platform_13,platform_12,platform_14,platform_15,platform_16,base_platform_left,base_platform_right):
        if self.platform == platform_1.platform_number:
            if self.x < platform_1.x or self.x > platform_1.x + platform_1.width and self.y == platform_1.y:
                self.platform=base_platform_left.platform_number
                return base_platform_left.y
            else:
                return platform_1.y
            


        if self.platform == platform_2.platform_number:
            if  self.x > platform_2.x + platform_2.width and self.y == platform_2.y:
                self.platform=base_platfor_left.platform_number
                return base_platform_left.y
            else:
                return platform_2.y
            
         
        
                
        if self.platform == platform_5.platform_number:
            if  self.x > platform_5.x + platform_5.width and self.y == platform_5.y:
                self.platform=platform_1.platform_number
                return platform_1.y
            
            if self.x < platform_5.x and self.y == platform_5.y:
                self.platform=platform_2.platform_number
                return platform_2.y

            else:
                return platform_5.y
            
        if self.platform == platform_8.platform_number:
            
            if  self.x > platform_8.x + platform_8.width and self.y == platform_8.y:
                
                self.platform=platform_6.platform_number
                return platform_6.y
           
            
            
            elif self.x < platform_8.x and self.y == platform_8.y:
                self.platform=platform_5.platform_number
                return platform_5.y

            else:
                return platform_8.y
        
        if self.platform==platform_6.platform_number:

            if self.x>(platform_6.x+platform_6.width) and self.y==platform_6.y:
                self.platform=platform_3.platform_number
                return platform_3.y
            elif self.x<platform_6.x and self.y==platform_6.y:
                self.platform=platform_1.platform_number
                self.x=platform_1.x+platform_1.width-50
                return platform_1.y
            else:
                return platform_6.y    
        if self.platform==platform_3.platform_number:

            if self.x<platform_3.x or self.x>platform_3.x+platform_3.width and self.y==platform_3.y:
                
                self.platform=base_platform_left.platform_number
                return base_platform_left.y
            else:
                return platform_3.y 
        
       
        if self.platform==platform_4.platform_number:

            if self.x<platform_4.x and self.y==platform_4.y:
                self.platform=base_platform_right.platform_number
                return base_platform_right.y     
            else:
                return platform_4.y

        if self.platform==platform_7.platform_number:

            if self.x<platform_7.x and self.y==platform_7.y:
                self.x=platform_3.x+platform_3.width
                self.platform=platform_3.platform_number
                return platform_3.y    

            if self.x>platform_7.x+platform_7.width and self.y==platform_7.y:
               self.x=platform_4.x
               self.platform=platform_4.platform_number
               return platform_4.y     

        if self.platform==platform_9.platform_number:

            if self.x<platform_9.x and self.y==platform_9.y:

                self.platform=platform_6.platform_number
                self.x=platform_6.x+50
                return platform_6.y
                    
            elif self.x>platform_9.x+platform_9.width and self.y==platform_9.y:

                self.platform=platform_3.platform_number
                self.x=platform_3.x+50
                return platform_3.y

        if self.platform==platform_11.platform_number:
            if self.x<platform_11.x and self.y==platform_11.y:
                  self.platform=platform_7.platform_number
                  return platform_7.y
            
        if self.platform==platform_10.platform_number:
            
            if self.x>platform_10.x+platform_10.width and self.y==platform_10.y:
                self.platform=platform_7.platform_number
                return platform_7.y   
            
            if self.x<platform_10.x and self.y==platform_10.y:
                self.platform=platform_3.platform_number
                return platform_3.y
            

        if self.platform==platform_13.platform_number:

            if self.x>platform_13.x+platform_13.width and self.y==platform_13.y:
                self.platform=platform_8.platform_number
                return platform_8.y  

            if self.x<platform_13.x and self.y==platform_13.y:
                self.platform=platform_5.platform_number
                return platform_5.y  
            
        if self.platform==platform_12.platform_number:

            if self.x>platform_12.x+platform_12.width and self.y==platform_12.y:
                self.platform=platform_5.platform_number
                return platform_5.y

        if self.platform==platform_14.platform_number:

            if self.x<platform_14.x and self.y==platform_14.y:
                self.platform=platform_9.platform_number
                return platform_9.y

            if self.x>platform_14.x+platform_14.width and self.y==platform_14.y:
                self.x=platform_10.x+10
                self.platform=platform_10.platform_number
                return platform_10.y


        if self.platform==platform_15.platform_number:
            if self.x<platform_15.x and self.y==platform_15.y:
                self.platform=platform_10.platform_number
                return platform_10.y


            if self.x>platform_15.x+platform_15.width and self.y==platform_15.y:
                self.platform=platform_11.platform_number
                return platform_11.y    


        if self.platform==platform_16.platform_number:
            if self.x<platform_16.x and self.y==platform_16.y:
                self.platform=platform_11.platform_number
                return platform_11.y
        if self.platform==base_platform_left.platform_number:

            if self.x>base_platform_left.x+base_platform_left.width and self.y==base_platform_left.y:
                self.x=0
        if self.platform==base_platfor_right.platform_number:

            if self.x<base_platform_right.x and self.y==base_platform_right.y:
                self.x=0
                self.platform=base_platform_left.platform_number
                return base_platform_left.y

        return self.y

                       
       

  


    def draw(self, window):
        if self.walk_count + 1 >= 27:
            self.walk_count = 0
        if not self.repause:
            if self.left:
                window.blit(walkLeft[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
            elif self.right:
                window.blit(walkRight[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
        else:
            if self.left:
                window.blit(walkLeft[0], (self.x, self.y))
            else:
                window.blit(walkRight[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y, 32, 70)
        pygame.draw.rect(window, (0, 0, 0), self.hitbox, 2)


class projectil(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)


class projectilAnamy(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)
      
class healthBar():

    def __init__(self,x,y,width,height,hp_max):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.hp=hp_max
        self.hp_max=hp_max
        self.color_red=(230, 37, 23)
        self.color_green=(58, 230, 23)
        
        
    def draw(self, surface):
        #calculate health ratio
        ratio = self.hp / self.hp_max
        pygame.draw.rect(window, self.color_red, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(window, self.color_green, (self.x, self.y, self.width * ratio, self.height))


class energyBar():

    def __init__(self,x,y,width,height,hp_max):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.hp=hp_max
        self.hp_max=hp_max
        self.color_red=(230, 37, 23)
        self.color_blue=(23, 116, 230)
        
        
    def draw(self, window):
        #calculate health ratio
        ratio = self.hp / self.hp_max
        pygame.draw.rect(window, self.color_red, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(window, self.color_blue, (self.x, self.y, self.width * ratio, self.height))

class armourBar():

    def __init__(self,x,y,width,height,hp_max):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.hp=hp_max
        self.hp_max=hp_max
        self.color_red=(230, 37, 23)
        self.color_green=(148, 148, 148)
        
        
    def draw(self, surface):
        #calculate health ratio
        ratio = self.hp / self.hp_max
        pygame.draw.rect(window, self.color_red, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(window, self.color_green, (self.x, self.y, self.width * ratio, self.height))

class scoreBox:

    def __init__(self,x,y,width,height,color,text):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.color=color
        self.text=text
        self.font = pygame.font.Font(None, 36) 
    

    def draw(self, window):
        
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

        # Render the text
        text_surface = self.font.render(self.text, True, (255, 255, 255)) 
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2)) 
        window.blit(text_surface, text_rect)



class gift:

    def __init__(self,x,y,color):

        self.x=x
        self.y=y
        self.color=color
        self.width=0
        self.radius=10
        self.center=(x,y)
        
    def draw(self,window):

        pygame.draw.circle(window, self.color, self.center, self.radius, self.width)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Fonturi
font = pygame.font.Font(None, 50)
screen_menu = pygame.display.set_mode((620, 465))

class Button:
    def __init__(self, text, x, y, width, height, color, text_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text_color = text_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text = font.render(self.text, True, self.text_color)
        screen.blit(text, (self.rect.x + (self.rect.width - text.get_width()) // 2, 
                           self.rect.y + (self.rect.height - text.get_height()) // 2))

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]


transparent_color = (245, 10, 225, 100) 
win_width = 1700
win_height = 900
window = pygame.display.set_mode((win_width, win_height))


goblin = Anamy(5, 1200, 64, 64, win_width-100)
goblin_2 = Anamy(10, 730, 64, 64, win_width-100)
health_bar = healthBar(50, 50, 200, 20, 100)
goblin_healt_bar=healthBar(1470,50,200,20,100)
energy_bar = energyBar(50, 80, 200, 20, 100)
armour_bar = armourBar(50, 110, 200, 20, 100)



game_over_box = GameOver(
    x=550,           
    y=300,         
    width=500,       
    height=100,       
    color=(0, 0, 0), 
    text="Game Over"  
)

return_button = Button("Back to menu", 100, 800, 200, 50, (222, 169, 113), BLACK)



score_box = scoreBox(
    x=1470,           
    y=830,         
    width=200,       
    height=50,       
    color=(0, 0, 0), 
    text="0"
)

gift_item=gift(0,0,(252, 3, 3))


base_platfor_left=Platrforms(1,0,730,885,50)
base_platfor_right=Platrforms(5,1280,730,485,50)
platform_1 = Platrforms(2, 300, 538, 280, 50)
platform_2 = Platrforms(3, 0, 545, 100, 50)
platform_3 = Platrforms(4, 850, 520, 260, 50)
platform_4 = Platrforms(6, 1450, 600, 230, 50)
platform_5 = Platrforms(16, 90, 370, 320, 50)
platform_6 = Platrforms(15, 620, 420, 295, 50)
platform_7=Platrforms(7,1155,460,330,50)
platform_8 = Platrforms(14, 400, 280, 230, 50)
platform_9=Platrforms(13,700,230,230,50)
platform_10=Platrforms(11,1050,225,180,50)
platform_11=Platrforms(8,1350,260,330,50)
platform_12=Platrforms(18,30,170,185,50)
platform_13=Platrforms(17,290,60,325,50)
platform_14=Platrforms(12,850,100,180,50)
platform_15=Platrforms(10,1220,60,250,50)
platform_16=Platrforms(9,1580,100,120,50)


platform_arr = [
    base_platfor_left,
    base_platfor_right,
    platform_1,
    platform_2,
    platform_3,
    platform_4,
    platform_5,
    platform_6,
    platform_7,
    platform_8,
    platform_9,
    platform_10,
    platform_11,
    platform_12,
    platform_13,
    platform_14,
    platform_15,
    platform_16,
]


def get_random_platform(platforms):

    return random.choice(platforms)



jony = player(50, base_platfor_left.y, 64, 64)
jony.platform=base_platfor_left.platform_number

graf = Graf()

graf.adauga_platforma(1,0,730,885,50)
graf.adauga_platforma(5,1280,730,485,50)
graf.adauga_platforma(2, 300, 538, 280, 50)
graf.adauga_platforma(3, 0, 545, 100, 50)
graf.adauga_platforma(4, 850, 520, 260, 50)
graf.adauga_platforma(6, 1450, 600, 230, 50)
graf.adauga_platforma(16, 90, 370, 320, 50)
graf.adauga_platforma(15, 620, 420, 295, 50)
graf.adauga_platforma(7, 1155, 460, 330, 50)
graf.adauga_platforma(14, 400, 280, 230, 50)
graf.adauga_platforma(13, 700, 230, 230, 50)
graf.adauga_platforma(11, 1050, 225, 180, 50)
graf.adauga_platforma(8, 1350, 260, 330, 50)
graf.adauga_platforma(18, 30, 170, 185, 50)
graf.adauga_platforma(17, 290, 60, 325, 50)
graf.adauga_platforma(12, 850, 100, 180, 50)
graf.adauga_platforma(10, 1220, 60, 250, 50)
graf.adauga_platforma(9, 1580, 100, 120, 50)

graf.adauga_legatura(1, 2, math.sqrt((platform_1.x - base_platfor_left.x)**2 + (platform_1.y - base_platfor_left.y)**2))
graf.adauga_legatura(1, 3, math.sqrt((platform_2.x - base_platfor_left.x)**2 + (platform_2.y - base_platfor_left.y)**2))
graf.adauga_legatura(1, 4, math.sqrt((platform_3.x - base_platfor_left.x)**2 + (platform_3.y - base_platfor_left.y)**2))
graf.adauga_legatura(1, 5, math.sqrt((platform_4.x - base_platfor_left.x)**2 + (platform_4.y - base_platfor_left.y)**2))
graf.adauga_legatura(2, 16, math.sqrt((platform_5.x - platform_1.x)**2 + (platform_5.y - platform_1.y)**2))
graf.adauga_legatura(2, 15, math.sqrt((platform_6.x - platform_1.x)**2 + (platform_6.y - platform_1.y)**2))
graf.adauga_legatura(3, 16, math.sqrt((platform_5.x - platform_2.x)**2 + (platform_5.y - platform_2.y)**2))
graf.adauga_legatura(4, 15, math.sqrt((platform_6.x - platform_3.x)**2 + (platform_6.y - platform_3.y)**2))
graf.adauga_legatura(4, 7, math.sqrt((platform_7.x - platform_3.x)**2 + (platform_7.y - platform_3.y)**2))
graf.adauga_legatura(6, 5, math.sqrt((platform_4.x - base_platfor_right.x)**2 + (platform_7.y - base_platfor_right.y)**2))
graf.adauga_legatura(6, 7, math.sqrt((platform_7.x - platform_4.x)**2 + (platform_7.y - platform_4.y)**2))  
graf.adauga_legatura(16, 14, math.sqrt((platform_8.x - platform_5.x)**2 + (platform_8.y - platform_5.y)**2))
graf.adauga_legatura(16, 17, math.sqrt((platform_13.x - platform_5.x)**2 + (platform_13.y - platform_5.y)**2))
graf.adauga_legatura(15, 2, math.sqrt((platform_1.x - platform_6.x)**2 + (platform_1.y - platform_6.y)**2))
graf.adauga_legatura(15, 4, math.sqrt((platform_3.x - platform_6.x)**2 + (platform_3.y - platform_6.y)**2))
graf.adauga_legatura(15, 14, math.sqrt((platform_8.x - platform_6.x)**2 + (platform_8.y - platform_6.y)**2))
graf.adauga_legatura(7, 4, math.sqrt((platform_3.x - platform_7.x)**2 + (platform_3.y - platform_7.y)**2))
graf.adauga_legatura(7, 6, math.sqrt((platform_4.x - platform_7.x)**2 + (platform_4.y - platform_7.y)**2))
graf.adauga_legatura(7, 8, math.sqrt((platform_11.x - platform_7.x)**2 + (platform_11.y - platform_7.y)**2))
graf.adauga_legatura(14, 13, math.sqrt((platform_9.x - platform_8.x)**2 + (platform_9.y - platform_8.y)**2))
graf.adauga_legatura(14, 15, math.sqrt((platform_6.x - platform_8.x)**2 + (platform_6.y - platform_8.y)**2))
graf.adauga_legatura(13, 12, math.sqrt((platform_14.x - platform_9.x)**2 + (platform_14.y - platform_9.y)**2))
graf.adauga_legatura(13, 11, math.sqrt((platform_10.x - platform_9.x)**2 + (platform_10.y - platform_9.y)**2))
graf.adauga_legatura(13, 4, math.sqrt((platform_3.x - platform_9.x)**2 + (platform_3.y - platform_9.y)**2))
graf.adauga_legatura(11, 8, math.sqrt((platform_11.x - platform_10.x)**2 + (platform_11.y - platform_10.y)**2))
graf.adauga_legatura(11, 12, math.sqrt((platform_14.x - platform_10.x)**2 + (platform_14.y - platform_10.y)**2))
graf.adauga_legatura(11, 7, math.sqrt((platform_7.x - platform_10.x)**2 + (platform_7.y - platform_10.y)**2))
graf.adauga_legatura(8, 7, math.sqrt((platform_7.x - platform_11.x)**2 + (platform_7.y - platform_11.y)**2))
graf.adauga_legatura(8, 9, math.sqrt((platform_16.x - platform_11.x)**2 + (platform_16.y - platform_11.y)**2))
graf.adauga_legatura(8, 11, math.sqrt((platform_10.x - platform_11.x)**2 + (platform_10.y - platform_11.y)**2))
graf.adauga_legatura(18, 16, math.sqrt((platform_5.x - platform_12.x)**2 + (platform_5.y - platform_12.y)**2))
graf.adauga_legatura(18, 17, math.sqrt((platform_13.x - platform_12.x)**2 + (platform_13.y - platform_12.y)**2))
graf.adauga_legatura(17, 16, math.sqrt((platform_5.x - platform_13.x)**2 + (platform_5.y - platform_13.y)**2))
graf.adauga_legatura(17, 14, math.sqrt((platform_8.x - platform_13.x)**2 + (platform_8.y - platform_13.y)**2))
graf.adauga_legatura(12, 13, math.sqrt((platform_9.x - platform_14.x)**2 + (platform_9.y - platform_14.y)**2))
graf.adauga_legatura(12, 11, math.sqrt((platform_10.x - platform_14.x)**2 + (platform_10.y - platform_14.y)**2))
graf.adauga_legatura(12, 10, math.sqrt((platform_15.x - platform_14.x)**2 + (platform_15.y - platform_14.y)**2))
graf.adauga_legatura(10, 11, math.sqrt((platform_10.x - platform_15.x)**2 + (platform_10.y - platform_15.y)**2))
graf.adauga_legatura(10, 8, math.sqrt((platform_11.x - platform_15.x)**2 + (platform_11.y - platform_15.y)**2))
graf.adauga_legatura(10, 9, math.sqrt((platform_16.x - platform_15.x)**2 + (platform_16.y - platform_15.y)**2))
graf.adauga_legatura(9, 10, math.sqrt((platform_15.x - platform_16.x)**2 + (platform_15.y - platform_16.y)**2))
graf.adauga_legatura(9, 8, math.sqrt((platform_11.x - platform_16.x)**2 + (platform_11.y - platform_16.y)**2))

start_platform = 1 
current_platform = None  
drum_optimal = []



pygame.display.set_caption("My Game")

clock = pygame.time.Clock()
FPS = 60


def redraw_game_window():
    window.blit(bg, (0, 0))
    jony.draw(window)
    goblin.draw(window, jony)
    #goblin_2.draw_default(window) 
    health_bar.draw(window)
    energy_bar.draw(window)
    armour_bar.draw(window)
    goblin_healt_bar.draw(window)
    score_box.draw(window)
    if draw_gift:
        gift_item.draw(window)
    if game_over:
        game_over_box.draw(window)
        return_button.draw(window)
        
   
    for bomb in bombs:
        bomb.draw(window)

    for bomb_anamy in bombs_anamy:
        bomb_anamy.draw(window)    
    pygame.display.update()



def prioritize_bars(health, armor, energy):
    
    max_health, max_armor, max_energy = 100, 100, 100
    health_percent = (health / max_health) * 100
    armor_percent = (armor / max_armor) * 100
    energy_percent = (energy / max_energy) * 100
    
   
    scores = {
        "health": 100 - health_percent,
        "armor": 100 - armor_percent,
        "energy": 100 - energy_percent
    }
    
   
    sorted_bars = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_bars[0][0] 
import math



def check_if_jony_find_gift():
    
    jony_center = (jony.x, jony.y)
    gift_center = gift_item.center
    gift_radius = gift_item.radius 
    player_tolerance = 50  

    
    distance = math.sqrt((jony_center[0] - gift_center[0])**2 + (jony_center[1] - gift_center[1])**2)
    
    
    if distance <= gift_radius + player_tolerance:
        return True
    else:
        return False


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLOR_INACTIVE = (222, 169, 113)  
COLOR_ACTIVE = pygame.Color('dodgerblue2') 

font = pygame.font.Font(None, 32)
def text_box():
    print("text box")

    
    input_box = pygame.Rect(630, 340, 300, 40)  
    
    label_box = pygame.Rect(630, 300, 300, 40)  

   
    active = False
    text = ''
    color = COLOR_INACTIVE

    running = True
    while running:
        window.blit(bg_menu, (0, 0))
        pygame.draw.rect(window, COLOR_INACTIVE, label_box)  
        label_text = font.render("Enter your name", True, BLACK) 
        window.blit(label_text, (label_box.x + 5, label_box.y + 5)) 
             
        pygame.draw.rect(window, color, input_box)  
        txt_surface = font.render(text, True, BLACK) 
        window.blit(txt_surface, (input_box.x + 5, input_box.y + 5))  
 
        pygame.draw.rect(window, (0, 0, 0), input_box, 2) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
               
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = COLOR_ACTIVE if active else COLOR_INACTIVE
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print(text) 
                        with open("current_player.txt","w") as f:
                            f.write(text)
                        text = '' 
                        return True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]  
                    else:
                        text += event.unicode  

       
        pygame.display.flip()
     

    pygame.quit()

MIN_RUN = 32

def insertion_sort(arr, left, right):
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
     
        while j >= left and arr[j][1] < key[1]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def merge(arr, left, mid, right):
    left_part = arr[left:mid + 1]
    right_part = arr[mid + 1:right + 1]

    i, j, k = 0, 0, left

    while i < len(left_part) and j < len(right_part):
       
        if left_part[i][1] >= right_part[j][1]: 
            arr[k] = left_part[i]
            i += 1
        else:
            arr[k] = right_part[j]
            j += 1
        k += 1

    while i < len(left_part):
        arr[k] = left_part[i]
        i += 1
        k += 1

    while j < len(right_part):
        arr[k] = right_part[j]
        j += 1
        k += 1

def tim_sort(arr):
    n = len(arr)

    for i in range(0, n, MIN_RUN):
        insertion_sort(arr, i, min(i + MIN_RUN - 1, n - 1))

    size = MIN_RUN
    while size < n:
        for start in range(0, n, size * 2):
            mid = min(n - 1, start + size - 1)
            end = min((start + 2 * size - 1), (n - 1))
            if mid < end:
                merge(arr, start, mid, end)
        size *= 2

def score_board():
    counter = 0
    print("text box")

    text_box = pygame.Rect(600, 340, 700, 300)  
    title_box = pygame.Rect(600, 300, 300, 40) 

    players_data = []

    with open("data_file.txt", "r") as f:
        for line in f:
            line = line.strip()
            parts = line.split(",")
            if len(parts) == 3:
                name = parts[0]
                score = int(parts[1])
                value = int(parts[2])
                players_data.append((name, score, value))

    print("Date inițiale:", players_data)

 
    tim_sort(players_data)

    print("Date sortate descrescător după scor:", players_data)

    top_players = players_data[:10]  

    running = True

    while running:
        

        exit_button = Button("Back to menu", 100, 800, 200, 50, (222, 169, 113), BLACK)
        exit_button.draw(window)


        pygame.draw.rect(window, (222, 169, 113), title_box)
        title_text = font.render("Top 10 players:", True, BLACK)
        window.blit(title_text, (title_box.x + 5, title_box.y + 5))

        pygame.draw.rect(window, (154, 232, 95), text_box)
        y_offset = text_box.y + 5  
        for player in top_players:
            player_text = f"{player[0]} - Score: {player[1]}"
            rendered_text = font.render(player_text, True, BLACK)
            window.blit(rendered_text, (text_box.x + 5, y_offset))
            y_offset += 30 

        for event in pygame.event.get():


            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if exit_button.is_clicked(mouse_pos):
                    
                    menu()


            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

    pygame.quit()




def menu():
    running = True  
    text_is=False
    while running:
        screen_menu.blit(bg_menu, (0, 0))
        start_button = Button("Start Game", 690, 300, 200, 50, (222, 169, 113), BLACK)
        info_button = Button("Info", 690, 400, 200, 50, (222, 169, 113), BLACK)
        exit_button = Button("Exit", 690, 500, 200, 50, (222, 169, 113), BLACK)

       
        start_button.draw(window)
        info_button.draw(window)
        exit_button.draw(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if start_button.is_clicked(mouse_pos):
                    print("Jocul începe!")
                    if not text_is:
                        text_is=text_box()
                        
                    
                    if text_is:
                        return True 

                if info_button.is_clicked(mouse_pos):
                    print("Opțiuni selectate!")
                    score_board()

                if exit_button.is_clicked(mouse_pos):
                    print("Ieșire din joc!")
                    pygame.quit()
                    quit()
        
       
        mouse_pos = pygame.mouse.get_pos()
        if start_button.is_hovered(mouse_pos):
            start_button.color = (0, 255, 0)
        else:
            start_button.color = GREEN

        if info_button.is_hovered(mouse_pos):
            info_button.color = (0, 0, 255) 
        else:
            info_button.color = BLUE

        if exit_button.is_hovered(mouse_pos):
            exit_button.color = (255, 0, 0) 
        else:
            exit_button.color = RED

        pygame.display.update()
    return False

        


run = True
bombs = []
bombs_anamy=[]
is_on_nivel_0=True
is_on_nivel_1=False
is_on_nivel_2=False

ori=0
jump_cooldown = 200  
last_jump_time = 0

start_platform = goblin.anamy_platform
end = jony.platform
last_teleport_time = 0
teleport_cooldown = 3000 

last_shooting_time = 0
last_energy_regenerate_time=0
energy_cooldown=3000
shooting_cooldown = 4000 
game_over=False
score=0
goblin_hp_nivel=10
last_gift_time=0
gift_cooldown=5000
option=False
draw_gift=False
time_in_game=0
start=False

write_data_in_file=False





while run:
    if not start:
        start_time = pygame.time.get_ticks()
        start=True 
        game_over=False



    clock.tick(FPS)




    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    if not option:
        
        option=menu()  



    if option:  
          
            
        if not game_over:
                for bomb in bombs:
                    if bomb.y - bomb.radius < goblin.hitbox[1] + goblin.hitbox[3] and bomb.y + bomb.radius > goblin.hitbox[1]:
                        if bomb.x + bomb.radius > goblin.hitbox[0] and bomb.x - bomb.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                            goblin.hit()
                            goblin_healt_bar.hp-=goblin_hp_nivel
                            if goblin_healt_bar.hp<=0:

                                score+=1
                                score_box.text=str(score) 
                                goblin_healt_bar.hp=100
                                if score<5:
                                    goblin_hp_nivel-=2
                                if score>4:
                                    goblin_hp_nivel-=0.5    
                                goblin.anamy_platform=base_platfor_right.platform_number
                            
                            bombs.pop(bombs.index(bomb))

                    if 0 < bomb.x < 1700:
                        bomb.x += bomb.vel
                    else:
                        bombs.pop(bombs.index(bomb))


                

                keys = pygame.key.get_pressed()

                if keys[pygame.K_SPACE]:

                    if energy_bar.hp>0:
                        facing = -1 if jony.left else 1
                        if len(bombs) < 5:
                            bombs.append(projectil(round(jony.x + jony.width // 2), round(jony.y + jony.height // 2), 5, (247, 120, 2), facing))
                            energy_bar.hp-=5
                if keys[pygame.K_LEFT] and jony.x > 0:
                    jony.x -= jony.step
                    jony.left = True
                    jony.right = False
                    jony.repause = False
                    
                elif keys[pygame.K_RIGHT] and jony.x + jony.width < win_width:
                    jony.x += jony.step
                    jony.right = True
                    jony.left = False
                    jony.repause = False
                    
                else:
                    jony.repause = True
                    jony.walk_count = 0

            
                current_time = pygame.time.get_ticks()

                            
                if keys[pygame.K_UP] and (current_time - last_jump_time > jump_cooldown):
                                    
                                    last_jump_time = current_time
                                    jony.is_jump = True
                                    jony.walk_count = 0

                                    
                                    
                                    jony.y=jony.on_platform(platform_1,platform_2,platform_3,platform_4,platform_5,platform_6,platform_8,platform_7,platform_9,platform_11,platform_10,platform_13,platform_12,platform_14,platform_15,platform_16,base_platfor_left,base_platfor_right)
                                
                                    #print("platform", jony.platform)
                            

                            
                jony.y=jony.fall(platform_1,platform_2,platform_3,platform_4,platform_5,platform_6,platform_8,platform_7,platform_9,platform_11,platform_10,platform_13,platform_12,platform_14,platform_15,platform_16,base_platfor_left,base_platfor_right)           
            
            
            
                current_platform_jucator = jony.platform
                current_platform_goblin = goblin.anamy_platform

            
                if current_platform_jucator != current_platform_goblin:
                    start_platform = goblin.anamy_platform 
                    end = jony.platform  
                    drum_optimal = graf.a_star(start_platform, end)

            
                if drum_optimal:
                    current_time = pygame.time.get_ticks()  

                    if current_time - last_teleport_time >= teleport_cooldown:
                        goblin.teleport_to_next_platform(drum_optimal, graf)
                        last_teleport_time = current_time  
                    
                        if goblin.anamy_platform == jony.platform:
                            drum_optimal = None  
                            start_platform = goblin.anamy_platform  #
                    
                            
                

                for bomb_anamy in bombs_anamy:
                    if bomb_anamy.y - bomb_anamy.radius < jony.hitbox[1] + jony.hitbox[3] and bomb_anamy.y + bomb_anamy.radius > jony.hitbox[1]:
                        if bomb_anamy.x + bomb_anamy.radius > jony.hitbox[0] and bomb_anamy.x - bomb_anamy.radius < jony.hitbox[0] + jony.hitbox[2]:
                            jony.hit()
                            if armour_bar.hp>0:
                                armour_bar.hp-=10

                            else:
                                health_bar.hp-=10
                            

                            
                            if health_bar.hp<=0:

                            
                                print("game over")
                                game_over=True
                            bombs_anamy.pop(bombs_anamy.index(bomb_anamy))

                    if 0 < bomb_anamy.x < 1700:
                        bomb_anamy.x += bomb_anamy.vel
                    else:
                        bombs_anamy.pop(bombs_anamy.index(bomb_anamy))


                current_time_g = pygame.time.get_ticks()

                
                #if jony.platform==goblin.anamy_platform:
                
                if goblin.x<jony.x:

                    
                        goblin.x+=1
                elif goblin.x>jony.x:

                    goblin.x-=1

                else:

                    goblin.x=jony.x    

                if goblin.y==jony.y or goblin.y<jony.y and goblin.y>jony.y-50:
                    if jony.x<goblin.x:
                            facing_g=-1
                           
                           
                    else:
                            facing_g=1
                         
                             

                    if current_time - last_shooting_time >= shooting_cooldown:    
                        if len(bombs_anamy) < 10:
                                bombs_anamy.append(projectil(round(goblin.x + goblin.width // 2), round(goblin.y + goblin.height // 2), 10, (247, 120, 2), facing_g))        
                                last_shooting_time = current_time_g  
                    #print("x=",jony.x)  
                # print("y=",jony.y)  
               



                priority = prioritize_bars(health_bar.hp,armour_bar.hp, energy_bar.hp)
                #print(f"Prioritatea este să reumplem: {priority}")

                if jony.x<goblin.x:
                    goblin.direction=-1

                else:
                    goblin.direction=1                    

                current_time_gift=pygame.time.get_ticks()

                if current_time_gift-last_gift_time>=gift_cooldown:
                    random_platform = get_random_platform(platform_arr)
                    if str(priority)=='energy':
                        print(f"Prioritatea este să reumplem: {priority}")
                        gift_item=gift(random_platform.x+50,random_platform.y+30,(3, 144, 252))
                        draw_gift=True
                        
                        last_gift_time=current_time_gift   

                    if str(priority)=='health':
                        print(f"Prioritatea este să reumplem: {priority}")
                        gift_item=gift(random_platform.x+50,random_platform.y+30,(252, 3, 3))
                        draw_gift=True
                        
                        last_gift_time=current_time_gift 

                    if str(priority)=='armor':
                        print(f"Prioritatea este să reumplem: {priority}")
                        gift_item=gift(random_platform.x+50,random_platform.y+30,(128, 128, 128))
                        draw_gift=True
                        
                        last_gift_time=current_time_gift 
                
                if check_if_jony_find_gift():

                    if gift_item.color==(3, 144, 252):

                        energy_bar.hp=100
                    if gift_item.color==(252, 3, 3):

                        if health_bar.hp<=100:
                            health_bar.hp+=0.1  
                    if gift_item.color==(128, 128, 128):
                        
                        if armour_bar.hp<=100:
                            armour_bar.hp+=0.5   

                else:
                    current_time_energy = pygame.time.get_ticks()
                    if current_time_energy - last_energy_regenerate_time >= energy_cooldown and energy_bar.hp<100:   
                    
                        energy_bar.hp+=10 

                        last_energy_regenerate_time=current_time_energy
            
                redraw_game_window()

        else:
            
            
            current_time = pygame.time.get_ticks()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if return_button.is_clicked(mouse_pos):
                    menu()
                    health_bar.hp=100
                    armour_bar.hp=100
                    energy_bar.hp=100
                    score=0
                    game_over=False


            if not write_data_in_file:
                time_in_game=current_time - start_time
                

                with open("current_player.txt","r") as f:

                    player_name=f.read()

                print(f"jucatorul se numeste {player_name}") 


                with open("data_file.txt","a") as f:

                    f.write(f"{player_name},{score},{time_in_game}\n")

                write_data_in_file=True
                
            redraw_game_window()
   

pygame.quit()
