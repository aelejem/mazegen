# Randomized Prim's algorithm

import pygame, random

base = (100, 100, 100)
wall = (0, 0, 0)
visited = (220, 220, 220)
char = (100, 100, 200)
fin = (124, 255, 0)
frontier = (150, 150, 150)

width = height = 801
tile = 10
startx = starty = width // tile // 2

class Cell:
    def __init__(self, x, y):
        self.walls = {'top': True, 'bottom': True, 'left': True, 'right': True}
        self.x, self.y = x, y

        self.linecolor = wall
        self.visited = False
        self.finish = False
        self.frontier = False

    def draw(self):
        if self.finish:
            pygame.draw.rect(screen, fin, pygame.Rect(self.x, self.y, tile+2, tile+2))
            if self.visited:
                self.frontier = False
        elif self.visited:
            self.frontier = False
            pygame.draw.rect(screen, visited, pygame.Rect(self.x, self.y, tile+2, tile+2))
        else:
            if self.frontier:
                pygame.draw.rect(screen, frontier, pygame.Rect(self.x, self.y, tile+2, tile+2))

        if self.walls['top']:
            pygame.draw.line(screen, self.linecolor, (self.x, self.y), (self.x+tile, self.y), 2)
        if self.walls['bottom']:
            pygame.draw.line(screen, self.linecolor, (self.x, self.y+tile), (self.x+tile, self.y+tile), 2)
        if self.walls['left']:
            pygame.draw.line(screen, self.linecolor, (self.x, self.y), (self.x, self.y+tile), 2)
        if self.walls['right']:
            pygame.draw.line(screen, self.linecolor, (self.x+tile, self.y), (self.x+tile, self.y+tile), 2)
    
    def __str__(self):
        return f'Cell at pos ({self.x//tile}, {self.y//tile})'

    def __repr__(self):
        return f'Cell({self.x}, {self.y})'
    

class Generator:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frontier = []
        grid[x][y].visited = True
        self.set_frontier()


    def draw(self):
        pygame.draw.rect(screen, char, pygame.Rect(self.x*tile+2, self.y*tile+2, tile-2, tile-2))


    def rm(self, direction):
        grid[self.x][self.y].visited = True
        if direction == 'right':
            grid[self.x][self.y].walls['right'] = False
            grid[self.x+1][self.y].walls['left'] = False
        if direction == 'left':
            grid[self.x][self.y].walls['left'] = False
            grid[self.x-1][self.y].walls['right'] = False
        if direction == 'top':
            grid[self.x][self.y].walls['top'] = False
            grid[self.x][self.y-1].walls['bottom'] = False
        if direction == 'bottom':
            grid[self.x][self.y].walls['bottom'] = False
            grid[self.x][self.y+1].walls['top'] = False
        
    def set_frontier(self):
        # poke top
        if self.y - 1 < 0:
            pass
        else:
            cgrid = grid[self.x][self.y - 1]
            if not (cgrid.visited or cgrid in self.frontier): 
                cgrid.frontier = True
                self.frontier.append(cgrid)
        
        # poke bottom
        if self.y + 1 >= rows:
            pass
        else:
            cgrid = grid[self.x][self.y + 1]
            if not (cgrid.visited or cgrid in self.frontier): 
                cgrid.frontier = True
                self.frontier.append(cgrid)
        
        # poke right
        if 1 + self.x >= cols:
            pass
        else:
            cgrid = grid[self.x + 1][self.y]
            if not (cgrid.visited or cgrid in self.frontier): 
                cgrid.frontier = True
                self.frontier.append(cgrid)
        
        # poke left
        if self.x-1 < 0:
            pass
        else:
            cgrid = grid[self.x - 1][self.y]
            if not (cgrid.visited or cgrid in self.frontier): 
                cgrid.frontier = True
                self.frontier.append(cgrid)

    
    def get_visited(self):
        visited = []

        # poke top
        if self.y - 1 < 0:
            pass
        elif grid[self.x][self.y - 1].visited:
            visited.append('top')
        
        # poke bottom
        if self.y + 1 >= rows:
            pass
        elif grid[self.x][self.y + 1].visited:
            visited.append('bottom')
        
        # poke right
        if 1 + self.x >= cols:
            pass
        elif grid[self.x + 1][self.y].visited:
            visited.append('right')
        
        # poke left
        if self.x-1 < 0:
            pass
        elif grid[self.x - 1][self.y].visited:
            visited.append('left')

        return visited


    def rpa(self):
        random_cell = random.choice(self.frontier)
        self.frontier.remove(random_cell)

        self.x, self.y = random_cell.x//tile, random_cell.y//tile
        choice = random.choice(self.get_visited())
        
        if choice == 'top':
            self.rm('top')
        elif choice == 'bottom':
            self.rm('bottom')
        elif choice == 'left':
            self.rm('left')
        elif choice == 'right':
            self.rm('right')
        
        self.set_frontier()

        if not self.frontier:
            location = 'path_to_your_folder'
            filename = 'rpa.bin'
            i = lambda x: '1' if cell.walls[x] else '0'
            bin_string = ''

            for line in grid:
                for cell in line:
                    bin_string += i('top') + i('bottom') + i('left') + i('right')

            binary_data = int(bin_string, 2).to_bytes(len(bin_string) // 8, byteorder="big")
                
            with open(location + '/' + filename, 'wb') as file:
                file.write(binary_data)


cols, rows = width // tile, height // tile
pt = True

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

grid = [[Cell(x*tile, y*tile) for y in range(rows)] for x in range(cols)]

a = Generator(startx, starty)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(pygame.Color(base))
    for line in grid:
        for cell in line:
            cell.draw()

    for i in range(1):
        if a.frontier:
            a.rpa()
            a.draw()
    
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
