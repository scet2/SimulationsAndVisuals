import pygame
import random
from pygame.locals import *
import math
import colorsys

pygame.init()

#settings
WIDTH = 800
HEIGHT = 600
FPS = 60

clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
bg = (0,0,0) #backround color

#variables
noise = 10
threshold = 10 #closness threshold
threshold_squared = threshold**2
bias = 2 #bias for y movement
starting_hue = 200

#class for particles
class Paricle:
     def __init__(self, id, radius):  
          self.id = id
          self.radius = radius
          #particle born on random x and y position
          self.x = random.randint(0, WIDTH) 
          self.y = random.randint(0, HEIGHT)

          #set starting color 
          self.hue = starting_hue
          self.rgb = colorsys.hsv_to_rgb(self.hue/360, 1.0, 1.0) #saturation and brightness at max = vibrant colors
          self.color = tuple(int(x*255) for x in self.rgb) #return numbers between 0-255 for rgb

          #check frozen
          self.frozen = False
          
          #parent for coloring
          self.parent = None #initially no parent since not frozen

     def update(self):
          #check if frozen
          if not self.frozen:
               self.x += random.uniform(-noise, noise)
               self.y += random.uniform(-noise, noise) +bias #adding bias to y for falling effect

               #wrap around logic: modulo operator: gives the remainder after divison
               self.x = (self.x+WIDTH) % WIDTH
               #self.y = (self.y+HEIGHT) % HEIGHT
               if self.y > HEIGHT:
                    self.y = 1
                    self.x = random.randint(0, HEIGHT) #random location when wrapping around
               self.check_freezing()
     
     def check_freezing(self):
          #each particle checks distance to frozen particles only
          for i in range(n):
               if particles_list[i].frozen:
                    dx = self.x - particles_list[i].x
                    #check y if only x is less then threshold
                    if dx < threshold:
                         dy = self.y - particles_list[i].y
                         #using pythagorem theorem
                         distance = dx**2 + dy**2
                         #check if the particle is close enough and already frozen
                         if distance < threshold_squared: 
                              self.frozen = True
                              self.parent = particles_list[i]
                              self.hue = self.parent.hue + 5
                              self.hue = self.hue %360 #wrap around to keep hue 0-360
                              #convert hue-saturation-value to rgb values
                              self.rgb = colorsys.hsv_to_rgb(self.hue/360, 1.0, 1.0) #update rgb
                              self.color = tuple(int(x*255) for x in self.rgb)
                              #particles get smaller and smaller
                              #self.radius = self.parent.radius * 0.98 #2% smaller but never reaches 0
                              return #early exit if close frozen particle found

     #display particle
     def draw(self, screen):
          pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
          #draw a line between parent and child for smoother animation
          if self.parent != None: #either check if frozen or has parent
               pygame.draw.line(screen, self.color, (self.x, self.y), (self.parent.x, self.parent.y), 3)

particles_list = []
n=500

for i in range(n):
     particles_list.append(Paricle(id = i, radius = 3))

#seed frozen particle (can be random)
seed = particles_list[0] 
seed.frozen = True
#position the frozen particle
seed.x = WIDTH // 2
seed.y = HEIGHT- seed.radius *2

#main loop
def main():
     run = True
     while run:
          clock.tick(FPS)
          screen.fill(bg) #clears the screen each run, so that the particles don't trail of like snakes but are positined at their new position

          for event in pygame.event.get():
               if event.type == QUIT:
                    run = False

          #different loops for update and draw so all particles are in sync
          for particle in particles_list:
               particle.update()

          for particle in particles_list:
               particle.draw(screen)
          
          pygame.display.update()
                    
     pygame.quit()

if __name__ == '__main__':
     main()