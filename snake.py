import pygame
import random
from random import randint

class Cube(object):
    rows = 20

    def __init__(self, start, dirnx=1, dirny=0, color=(0, 0, 0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = size // rows
        rw = self.pos[0]
        cm = self.pos[1]
        pygame.draw.rect(surface, self.color, (rw * dis + 1, cm * dis + 1, dis - 2, dis - 2))

        if eyes:
            center = dis // 2
            radius = 3
            circle_niddle = (rw * dis + center - radius, cm * dis + 8)
            circle_niddle2 = (rw * dis + dis - radius * 2, cm * dis + 8)
            pygame.draw.circle(surface, (255, 255, 255), circle_niddle, radius)
            pygame.draw.circle(surface, (255, 255, 255), circle_niddle2, radius)


class Snake(object):

    def __init__(self, color, pos):
        self.body = []
        self.turns = {}
        self.game_over = False
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # zamknij gre po naciśnięciu x

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.dirnx = -1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_d]:
                self.dirnx = 1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_w]:
                self.dirnx = 0
                self.dirny = -1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_s]:
                self.dirnx = 0
                self.dirny = 1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for idx, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                has_collision = self.head_has_collision_with_tail
                if has_collision():
                    self.reset()
                    break
                c.move(turn[0], turn[1])
                if idx == len(self.body) - 1:
                    self.turns.pop(p)

            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)


    def head_has_collision_with_tail(self):
        if self.body[0].pos in [x.pos for x in self.body[1:]]:

            return True
        return False

    def reset(self):

        self.game_over = True
        self.dirnx = 0
        self.dirny = 0
        for c in self.body:
            c.dirnx = 0
            c.dirny = 0
        self.head.dirnx = 0
        self.head.dirny = 0
    def add_cube(self,i):
        for x in range(i):
            tall = self.body[-1]
            dx, dy = tall.dirnx, tall.dirny
            if dx == 1 and dy == 0:
                self.body.append(Cube((tall.pos[0] - 1, tall.pos[1])))
            elif dx == -1 and dy == 0:
                self.body.append(Cube((tall.pos[0] + 1, tall.pos[1])))
            elif dx == 0 and dy == 1:
                self.body.append(Cube((tall.pos[0], tall.pos[1] - 1)))
            elif dx == 0 and dy == -1:
                self.body.append(Cube((tall.pos[0], tall.pos[1] + 1)))

            self.body[-1].dirnx = dx
            self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def draw_grid(w, rows, surface):
    size_between = w // rows
    x = 0
    y = 0
    for l in range(rows):
        x = x + size_between
        y = y + size_between
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def draw_window(surface, font):
    surface.fill((0, 255, 0))  # RGB
    s.draw(surface)
    apple.draw(surface)
    draw_grid(size, rows, surface)
    textsurface = font.render(f'Eaten apples: {apple_counter}', False, (255, 0, 0))
    surface.blit(textsurface, (10, info_y))
    textsurface2 = font.render(f'Score: {score}', False, (0, 0, 250))
    surface.blit(textsurface2, (200, info_y))
    pygame.display.update()


def random_apple(snake):
    positions = snake.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
    return (x, y)

def main():
    global size, rows, s, apple, apple_counter, score, info_y
    info_y = 658
    size = 660  # rozmiar gry
    rows = 20

    window = pygame.display.set_mode((size, size + 40))
    clock = pygame.time.Clock()
    pygame.font.init()
    active_game = True
    while active_game:
        apple_counter = 0
        x=8
        score = 0
        s = Snake((0, 0, 0), (10, 10))
        print(s, len(s.body))
        gold_or_red = 1
        apple = Cube(random_apple(s), color=(255, 0, 0))

        flag = True  # jeżeli true to gra działa
        font_comic = pygame.font.SysFont('Comic Sans MS', 20)
        while flag:

            if s.game_over:

                text = "press x for new game"
                textsurface = font_comic.render(text, False, (0, 0, 0))
                window.blit(textsurface, (150, 250))
                text2 = "press y for close game"
                text2surface = font_comic.render(text2, False, (0, 0, 0))
                window.blit(text2surface, (150, 270))
                pygame.display.update()
                #time.sleep(5)
                #pygame.time.wait(1000)
                x
                key = pygame.key.get_pressed()
                if key[pygame.K_x]:
                    flag = False

                elif key[pygame.K_y]:
                    active_game = False
                    flag = False
            pygame.time.delay(50)  # im mniejsza wartość delay tym gra szybsza
            clock.tick(x)  # im mniej tym gra wolniejsza
            s.move()

            if s.body[0].pos == apple.pos:
                if gold_or_red % 5 == 0:
                    score+=3*x
                    s.add_cube(3)
                else:
                    score+=1*x
                    s.add_cube(1)
                apple_counter+=1
                if apple_counter%3 == 0:
                    x+=1
                gold_or_red = randint(1, 10)
                if gold_or_red % 5 == 0:
                    apple = Cube(random_apple(s), color=(255, 215, 0))
                else:
                    apple = Cube(random_apple(s), color=(255, 0, 0))
                print("score: ", score)
                print("eaten apples: ", apple_counter)
            draw_window(window, font_comic)

main()
