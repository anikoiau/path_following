# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 11:37:12 2020

@author: soumitra
"""

import math
import sys
import pygame
from pygame import Vector2

width = 800
height = 800


con = 0




class Line():
    def __init__(self, start, end):
        self.start = start
        self.end = end
        
        
    def draw(self, screen):

        pygame.draw.line(screen, (255, 255, 255), self.start, self.end, 1)
        

        
class Points():
    def __init__(self, pos):
        self.pos = pos
        self.reached = False
        
        
    def reach(self):
        self.reached = True
        
        
    def isReached(self):
        return self.reached
        
        
class Car():
    def __init__(self, pos):
        self.pos = pos
        self.v = Vector2(0, 1)
        self.a = Vector2(0, 0)
        self.r = 10
        
        self.maxspeed = 5
        self.maxforce = .5
        
        
    def update(self):
        
        self.v += self.a
        
        if self.v.length() > self.maxspeed:
            self.v.scale_to_length(self.maxspeed)
            
        self.pos += self.v
  
        self.a *= 0
        
    
    
    def draw(self, screen):
        
        
        
        if self.v.length() < .00000001:
            return
        
        ro = self.v.rotate(90)
        
        if ro.length() > .000001:

            ro.scale_to_length(self.r)
            
            p1 = (self.pos.x - ro.x // 2, self.pos.y - ro.y // 2)
            p2 = (self.pos.x + ro.x // 2, self.pos.y + ro.y // 2)
            
            p3 = (self.pos.x + 3 * self.r * math.cos(math.atan2(self.v.y, self.v.x)), self.pos.y + 3 * self.r * math.sin(math.atan2(self.v.y, self.v.x)))
            
            
            pygame.draw.polygon(screen, (255, 255, 255), [p1, p2, p3], 0)
   
            
            
            
    def get_normal_point(self, x0, y0, a, b):
        p = Vector2(x0, y0)
        
        ap = Vector2(p - a)
        ab = Vector2(b - a)
        
        ab.normalize_ip()
        
        t = ap.dot(ab)
        
        ab *= t
        
        normal = Vector2(a + ab)
       
        return normal
         
        
       
        
       
    def seek(self, target, repel = None, repMag = None):
        
        if self.pos.x < 10 or self.pos.x > (width - 10) or self.pos.y < 10 or self.pos.y > (height - 10):
            self.t = Vector2(height / 2, width / 2)
            self.d = self.t - self.pos
            
            
            if self.d.length() != 0:
                self.d.scale_to_length(self.maxspeed)
              
                self.st = Vector2(self.d - self.v)
            
                if self.st.length() > self.maxforce:
                    # print(self.st.length())
                    self.st.scale_to_length(self.maxforce)
            
                self.applyForce(self.st)
        
        
        self.desired = Vector2(target - self.pos)
        
        if self.desired.length() != 0:
        
            speed = self.maxspeed * (self.pos.distance_to(target) / 1)
            
            if speed > self.maxspeed:
                speed = self.maxspeed
                
            # if speed < .001:
            #     speed = .001
                
            self.desired.scale_to_length(speed)
            self.steer = Vector2(self.desired - self.v)
               
            if self.steer.length() > self.maxforce:
                self.steer.scale_to_length(self.maxforce)
            
            
            
            self.applyForce(self.steer)
        
        
        
        if repel != None:    
            self.rep = Vector2(repel - self.pos)
            
            if self.rep.length() != 0:
                self.rep.scale_to_length(self.maxspeed)
                self.st = Vector2(self.rep - self.v)
                if self.st.length() > self.maxforce:
                    self.st.scale_to_length(self.maxforce)
                    
                    
                self.st *= repMag
                
                self.applyForce(self.st)
            
            
        
        
        
        
    def applyForce(self, steer):
        # if self.steer.length() > self.maxforce:
        #     self.steer.scale_to_length(self.maxforce)
        self.a += steer
    



        
    # def get_normal_point(self, x0, y0, line):
    #     # start point
    #     x1 = line.start.x
    #     y1 = line.start.y
    #     # end point
    #     x2 = line.end.x
    #     y2 = line.end.y
    
    #     #position of the ray
    #     x3 = x0
    #     y3 = y0
    #     x4 = x0 + self.v.x
    #     y4 = y0 + self.v.y
    
    #     #denominator
    #     deno = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    #     #numerator
    #     nume = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
    #     if deno == 0:
    #         return Vector2(0, 0)
        
    #     #formulas
    #     t = nume / deno
    #     u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / deno
    
    #     if t > 0 and t < 1 and u > 0:
    #         #Px, Py
    #         x = x1 + t * (x2 - x1)
    #         y = y1 + t * (y2 - y1)
            
    #         pot = Vector2(x, y)
            
    #         return pot
       
     
       
    
      
        
    # def chase_points_to_stay_on_track(self, points):
        
    #     closest = None
    #     dist = 100000000
        
    #     for point in points:
    #         if point.reached == True:
    #             continue
            
    #         d = point.pos.distance_to(self.pos)
            
    #         if d < dist:
    #             dist = d
    #             target = Vector2(point.pos)
            
    #     self.seek(target)
    #     point.reached = True
        
       
    # def stay_in_line(self, points):
        
    #     # closest = None
    #     # dist = 1000000000
        
    #     # for line in lines:
    #     #     num = abs((line.end.y - line.start.y) * self.pos.x - (line.end.x - line.start.x) * self.pos.y +\
    #     #               line.end.x * line.start.y - line.end.y * line.start.x)
                
    #     #     den = math.sqrt((line.start.x - line.end.x) ** 2 + (line.end.y - line.start.y) ** 2)
            
    #     #     if den != 0:
    #     #         d = num / den
            
    #     #     if d < dist:
    #     #         dist = d
    #     #         closest = line
        
    #     closest = None
    #     dist = 1000000
    #     actualNormal = None
    #     target = None
        
    #     global con
        
        
    #     temp = Vector2(self.pos)
        
    #     dire = Vector2(self.v)
        
    #     dire.normalize_ip()
        
    #     dire *= 10
        
        
    #     temp = temp + dire
        
    #     actualA = None
    #     actualB = None
    #     actualI = None
        
        
        
        
    #     for i in range(len(points) - 1):
            
    #         a = Vector2(points[i].pos)
    #         b = Vector2(points[i + 1].pos)
            
            
    #         if line.start.distance_to(line.end) == 0:
    #             continue
            
    #         normal = self.get_normal_point(temp.x, temp.y, a, b)
            
            
    #         # t2 = Vector2(self.pos + self.v)
            
    #         # if t2.distance_to(normal) >= self.maxspeed:
                
    #         # cross1 = Vector2(line.end - line.start)
    #         # cross2 = Vector2(normal - line.start)
            
    #         # c = cross1.cross(cross2)
            
    #         # print(type(cross1), type(cross2), type(c), c)
            
    #         # if c <= .0000001 and Vector2(line.end - line.start).dot(normal - line.start) > 0 and Vector2(line.end - line.start).dot(normal - line.start) < (cross1.length() ** 2):
    #         #     normal = Vector2(line.end)
            
            
    #         # if normal.distance_to(a) + normal.distance_to(b) >= a.distance_to(b):
                
    #         #     normal = b
                
    #         #     normal = Vector2(line.end)
                
    #             # lin = Vector2(line.end - line.start)
                
    #             # lin.scale_to_length(15)
                
    #             # normal += lin
    #             # continue
                
    #             # normal /= 2
                
                
    #         if math.sqrt((a.x - normal.x) ** 2 + (a.y - normal.y) ** 2) + math.sqrt((b.x - normal.x) ** 2 + (b.y - normal.y) ** 2) >= math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2):
    #             normal = b
    #             # print('YES')
                
                
    #         # if b.distance_to(normal) < 2 and self.pos.distance_to(b) < 20:
            
    #         #     points[(i + 1)].reached = True
    #         #     self.seek(points[(i + 2) % len(points)].pos, repel = points[i + 1].pos, repMag = 0)
    #         #     print('YES')
                
    #         #     return
            

    #         d = math.sqrt((temp.x - normal.x) ** 2 + (temp.y - normal.y) ** 2)
            
    #         # if d < 10:
    #         #     return
            
    #         # if d < self.v.length():
    #         #     continue
            
            
    #         if d < dist:
                
                
    #             # if normal.distance_to(line.start) + normal.distance_to(line.end) != line.start.distance_to(line.end):
                
                
    #             #     normal = Vector2(line.end)
    #             #     lin = Vector2(line.end - line.start)
                
    #             #     lin.scale_to_length(15)
                    
    #             #     normal += lin
                
                
    #             # if normal.x < min(line.start.x, line.end.x) or normal.x > max(line.start.x, line.end.x):
    #             #     normal = line.end
                    
    #             dist = d
    #             actualNormal = normal
    #             actualA = Vector2(a)
    #             actualB = Vector2(b)
    #             actualI = i
                
                
                
    #             te = Vector2(b - a)
                
    #             te.normalize_ip()
                
    #             direc = Vector2(self.v)
        
    #             direc.normalize_ip()
                
    #             direc *= 50
        
    #             te *= 15
                
                
    #             target = actualNormal + te
                
           
    #         # pygame.draw.line(screen, (255, 255, 255), (temp.x, temp.y), (actualNormal.x, actualNormal.y), 3)
    #         # actualNormal.reached
            
                
    #     # print(self.pos.distance_to(actualB))
        
              
    #     if points[(actualI + 1)].pos.distance_to(actualNormal) < 2 and self.pos.distance_to(points[(actualI + 1)].pos) < 20:
            
    #         # points[(actualI + 1)].reached = True
    #         self.seek(points[(actualI + 2) % len(points)].pos)
    #         pygame.draw.circle(screen, (0, 255, 0), (int(points[(actualI + 2) % len(points)].pos.x), int(points[(actualI + 2) % len(points)].pos.y)), 3)
    #         print('YES')
            
    #         con = 1
            
                

        
    #     # target = actualNormal + te
        
    #     # if target.length() != 0:
    #     #     target.scale_to_length(self.v.length())
        
    #     # target += actualNormal
        
            
    #     # if temp.distance_to(actualNormal) >= self.v.length():
        
    #     elif dist > 20:
    #         # if target == None:
    #         #     self.applyForce(Vector2(0, 0))
    #         #     return
            
    #         # if points[actualI + 1].reached != True:
    #         if con > 0 and con < 100:
    #             con += 1
            
    #         else:
    #             self.seek(target)
    #             pygame.draw.circle(screen, (255, 0, 0), (int(actualNormal.x), int(actualNormal.y)), 3)
    #             pygame.draw.circle(screen, (0, 255, 0), (int(target.x), int(target.y)), 3)
                
    #             # points[actualI + 1].reached = False
                
    #             print('NO')
                
    #             con = 0
        
    #         # print(dist)
       
        
            
        
    
   
    
            

        
        
def drawPoints(points, screen):
    
    for point in points:
        
        pygame.draw.circle(screen, (0, 0, 255), (int(point.pos.x), int(point.pos.y)), 4)
        
            
            

screen = pygame.display.set_mode((width, height))


screen.fill((0, 0, 0))

count = 0
pressed = False

lines = []

points = []

car = Car(Vector2(width // 2, height // 2))

carToggle = False


i = 0





while True:
    
    pygame.time.Clock().tick(100)
    
    screen.fill((0, 0, 0))
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()



        if e.type == pygame.MOUSEMOTION or e.type == pygame.MOUSEBUTTONUP:
            if count % 2 == 1:
                end_pos = e.pos
                pygame.draw.line(screen, (255, 255, 255), start_pos, end_pos, 1)
                # print('inside mousemotion', count, end_pos)
            
        if e.type == pygame.MOUSEBUTTONDOWN:
            
            if e.button == 3:
                count += 1
        
            if e.button == 1:
                if count % 2 == 0:
                    start_pos = Vector2(e.pos)
                    
                    # points.append(Points(start_pos))
                    
                    count += 1
                    
                    # print('inside mousedown', count, start_pos)
                else:
                    end_pos = Vector2(pygame.mouse.get_pos())
                    # pygame.draw.line(screen, (255, 255, 255), start_pos, end_pos, 3) 
                    count += 1
                    
                    # print('inside mousedown', count, end_pos)
                    
                    points.append(Points(end_pos))
                    
                    lines.append(Line(start_pos, end_pos))
                
                # if prev_event == pygame.MOUSEBUTTONUP or prev_event == pygame.MOUSEMOTION:
                #     start_pos = pygame.mouse.get_pos()
            
        # if e.type == pygame.K_SPACE:
        #     pos = Vector2(pygame.mouse.get_pos())
            
        #     car = Car(pos)
            
            
    keys = pygame.key.get_pressed()
           
    for line in lines:
        line.draw(screen)
     
        
    if keys[pygame.K_DOWN]:
        # prev_length = car.v.length()
        
        # car.v.scale_to_length(prev_length - .01)
        
        car.maxspeed -= .05
        
      
        
    if keys[pygame.K_UP]:
        # prev_length = car.v.length()
        
        # car.v.scale_to_length(prev_length + .01)
    
        car.maxspeed += .05
        
        
    if keys[pygame.K_RIGHT]:
        
        car.maxforce += .005
        
        
    if keys[pygame.K_LEFT]:
        
        car.maxforce -= .005
        
        
    
    drawPoints(points, screen)
    
    if keys[pygame.K_SPACE]:
        carToggle = True
        
    
    
    if carToggle == True:
        
        
        # car.stay_in_line(lines)
       
        # if points[i].reached != True:
        car.seek(points[i].pos)
        
        a = points[(i - 1) % len(points)].pos
        b = points[i].pos
        
        line = Vector2(b - a)
        
        normal = car.get_normal_point(car.pos.x + car.v.x, car.pos.y + car.v.y, a, b)
        
        if normal.distance_to(car.pos + car.v) > 10:
            line.normalize_ip()
            line *= 10
            
            car.seek(normal + line, b, -.5)
            
            pygame.draw.circle(screen, (255, 0, 0), (int(normal.x), int(normal.y)), 4)
            pygame.draw.circle(screen, (0, 255, 0), (int(normal.x + line.x), int(normal.y + line.y)), 4)
        
            
        if car.pos.distance_to(b) <= 50:
            i = (i + 1) % len(points)
            # i += 1
            
            # if i >= len(points):
            #     i = len(points) - 1
            
        
        else:
            if i >= len(points):
                # for point in points:
                #     point.reached = False
                
                i = 0
                    
              
        
        
        print(car.v.length())
        
        car.draw(screen)
        
        # drawPoints(points, screen)
        
        car.update()
        
        car.draw(screen)
        
        # flag = 1
        # for pt in points:
        #     if pt.reached == False:
        #         flag = 0
        
        # if flag == 1:
        #     for pt in points:
        #         pt.reached = False
    
    pygame.display.update()