# Depth-first search Maze Gen

import pygame, random

base = (100, 100, 100)
wall = (0, 0, 0)
visited = (220, 220, 220)
char = (100, 100, 200)
fin = (124, 255, 0)

width = height = 801
tile = 20
startx, starty = 20, 20

class Cell:
    def __init__(self, x, y):
        self.linecolor = wall
        self.x, self.y = x, y
        self.visited = False
        self.walls = {'top': True, 'bottom': True, 'left': True, 'right': True}
        self.finish = False

    def draw(self):
        if self.finish:
            pygame.draw.rect(screen, fin, pygame.Rect(self.x, self.y, tile+2, tile+2))
        if self.visited:
            if not self.finish:
                pygame.draw.rect(screen, visited, pygame.Rect(self.x, self.y, tile+2, tile+2))

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
        self.stack = [grid[self.x][self.y]]
        grid[x][y].visited = True

    
    def draw(self):
        pygame.draw.rect(screen, char, pygame.Rect(self.x*tile+2, self.y*tile+2, tile-2, tile-2))


    def move(self, direction):
        if direction == 'right':
            grid[self.x][self.y].walls['right'] = False
            grid[self.x+1][self.y].walls['left'] = False
            self.x += 1
        if direction == 'left':
            grid[self.x][self.y].walls['left'] = False
            grid[self.x-1][self.y].walls['right'] = False
            self.x -= 1
        if direction == 'top':
            grid[self.x][self.y].walls['top'] = False
            grid[self.x][self.y-1].walls['bottom'] = False
            self.y -= 1
        if direction == 'bottom':
            grid[self.x][self.y].walls['bottom'] = False
            grid[self.x][self.y+1].walls['top'] = False
            self.y += 1

        grid[self.x][self.y].visited = True
        self.stack.append(grid[self.x][self.y])



    def get_cell_data(self):
        available = []

        # poke top
        if not (self.y - 1 < 0 or grid[self.x][self.y - 1].visited): 
            available.append('top')
        
        # poke bottom
        if not (self.y + 1 >= rows or grid[self.x][self.y + 1].visited): 
            available.append('bottom')
        
        # poke right
        if not (1 + self.x >= cols or grid[self.x + 1][self.y].visited):
            available.append('right')
        
        # poke left
        if not (self.x-1 < 0 or grid[self.x - 1][self.y].visited):
            available.append('left')

        if grid[self.x][self.y].finish:
            return []
        return available
    

    def dfs(self):
        self.x, self.y = self.stack[-1].x//tile, self.stack[-1].y//tile
        available = self.get_cell_data()
        if available:
            random.shuffle(available)
            choice = available.pop()
            self.move(choice)
        else:
            self.stack.pop()

        if not self.stack:
            location = 'location_to_your_folder'
            filename = 'maze.bin'
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
    
    if a.stack:
        a.dfs()

    screen.fill(pygame.Color(base))
    for line in grid:
        for cell in line:
            cell.draw()
    a.draw()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()

