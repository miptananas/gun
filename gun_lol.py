
import math
from pygame.draw import *
from random import choice, randint

import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = randint(2, 14)
        self.vx = 0
        self.vy = 0
        self.g = 0.7
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        
        self.vy -= self.g
        self.x += self.vx
        self.y -= self.vy
            
        

    def draw(self):
        circle(self.screen, self.color, (self.x, self.y), self.r)

    def hittest(self, obj):
        
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        return (self.x - obj.x)**2 + (self.y - obj.y)**2 <= (self.r + obj.r)**2


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 40 
        self.length = 30+0.5*self.f2_power
        self.x2 = self.x + self.length*math.cos(self.an)
        self.y = 450
        self.vx = randint(1, 3)

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an) 
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши. При заряжании пушка становится красной"""
        if event:
            self.an = math.atan2((event.pos[1]-450), (event.pos[0]-40))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY
            
    def move(self):
        """Пушка едет с течением времени.

        Метод описывает перемещение пушки за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy и границ линии, по которой перемещется пушка.
        """
        
        self.x += self.vx
        self.x2 += self.vx
        
        if (self.x < 40 or self.x > 100):
            self.vx = -self.vx
            
    


    def draw(self):
        line(self.screen, self.color, (self.x, self.y), (self.x + self.length*math.cos(self.an), self.y + self.length*math.sin(self.an)), 10)
        circle(self.screen, self.color, (self.x, self.y), 6)
        circle(self.screen, (0, 0, 0), (self.x, self.y), 6, 2)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__ (self, screen, g, a):
        self.points = 0
        self.screen = screen
        self.vx = randint(4, 8)
        self.vy = randint(4, 8)
        self.g = g
        self.a = a
             
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        self.live = 1
        x = self.x = randint(600, 780)
        y = self.y = randint(300, 550)
        r = self.r = randint(10, 50)
        color = self.color = RED
        
    def move(self):
        """Переместить цель по прошествии единицы времени.

        Метод описывает перемещение цели за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на цель,
        и стен по краям окна (размер окна 800х600).
        """
        self.vy -= self.g
        self.vx += self.a
        
        if self.x + self.r > 800 or self.x - self.r < 0:
            self.vx = -self.vx
            
        if self.y + self.r > 600 or self.y - self.r < 0:
            self.vy = -self.vy
    
        self.x += self.vx
        self.y -= self.vy
        
        

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        circle(self.screen, self.color, (self.x, self.y), self.r)
        circle(self.screen, (0, 0, 0), (self.x, self.y), self.r, 2)
        circle(self.screen, (0, 0, 0), (self.x, self.y), 5)
        circle(self.screen, (0, 0, 0), (self.x, self.y), 8, 2)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target(screen, 0, 0)
target1 = Target(screen, 0, 0)
target2 = Target(screen, 1, 0.1)
finished = False

while not finished:
    screen.fill(WHITE)
    line(screen, (0, 0, 0), (35, 450), (105, 450))
    gun.draw()
    target.draw()
    target1.draw()
    target2.draw()
    for b in balls:
        b.draw()
    gun.move()
    target1.move()
    target2.move()
    

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
            

    for b in balls:
        b.move()
        if b.hittest(target) and target.live:
            target.live = 0
            target.hit()
            target.new_target()
        if b.hittest(target1) and target1.live:
            target1.live = 0
            target1.hit()
            target1.new_target()
        if b.hittest(target2) and target2.live:
            target2.live = 0
            target2.hit()
            target2.new_target()
    pygame.display.update()
    
        
    gun.power_up()
    

pygame.quit()