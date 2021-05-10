import pygame
from random import randint
import numpy as np
 
 
w, h = 800, 600
pygame.init()
screen = pygame.display.set_mode((w, h))

FPS = 30
clock = pygame.time.Clock()
 
BLACK = pygame.Color("black")
WHITE = pygame.Color("white")
GREEN = pygame.Color("green")
GREEN_FILL = pygame.Color(10,70,10)
PINK = pygame.Color("magenta")
 

def create_rand_points(n, offsetx=100, offsety=100):
    return [np.array([randint(offsetx,w-offsetx), randint(offsety,h-offsety)]) for _ in range(n)]

class Hull():
    def __init__(self, points):
        self.vertices = points
        self.curr_vert, self.start_index = self.left_most()
        self.check_index = (self.start_index + 1) % len(self.vertices)
        self.next_vert = self.test_vert = self.vertices[0]
        self.hull = [self.curr_vert]

    def left_most(self):
        left = None
        index = 0
        for i in range(len(self.vertices)):
            v = self.vertices[i]
            if left is None or v[0] < left[0]:
                left = v
                index = i
        return left, index  

    def draw_hull_progress(self):
        for v in [self.curr_vert, self.next_vert, self.test_vert]:
            pygame.draw.circle(screen, GREEN, v, 5)
        pygame.draw.line(screen, PINK, self.curr_vert, self.next_vert)
        pygame.draw.line(screen, GREEN, self.curr_vert, self.test_vert)
    
    def draw_hull(self):
        if len(self.hull) > 1:
            pygame.draw.lines(screen, WHITE, False, self.hull, 2)
    

def main():
 
    n = 20
    points = create_rand_points(n)
    hull = Hull(points)

    done = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                points = create_rand_points(n)
                hull = Hull(points)
                done = False

        screen.fill(BLACK)

        if not done:
            hull.draw_hull()
            hull.draw_hull_progress()

            if np.array_equal(hull.curr_vert, hull.next_vert):
                hull.next_vert = hull.test_vert

            if not np.array_equal(hull.curr_vert, hull.test_vert):
                if np.cross(hull.curr_vert-hull.test_vert, hull.curr_vert-hull.next_vert) > 0:
                    hull.next_vert = hull.test_vert
            hull.test_vert = hull.vertices[hull.check_index]
            hull.check_index = (hull.check_index + 1) % len(hull.vertices)

            if hull.check_index == hull.start_index:
                hull.hull.append(hull.next_vert)
                hull.start_index = hull.check_index
                hull.curr_vert = hull.next_vert
        else:
            pygame.draw.polygon(screen, GREEN_FILL, hull.hull)
            pygame.draw.polygon(screen, GREEN, hull.hull, 2)
        
        if len(hull.hull) > 1 and np.array_equal(hull.hull[0], hull.hull[-1]):
            done = True

        for p in points:
            pygame.draw.circle(screen, WHITE, p, 5, 1)

        pygame.display.flip()
        clock.tick(FPS)
 

if __name__ == "__main__":
    main()
