from random import sample
from selection import SelectNumber
from copy import deepcopy

def create_line_coordinates(cell_size: int) -> list[list[tuple]]:
    #creates the x,y coordinates for drawing the grid lines.
    points = []
    for y in range(1,9):
        #horizontal lines
        temp = []
        temp.append((0, y * cell_size)) # x,y points [(0, 100), (0, 200), .....]
        temp.append((900, y * cell_size)) # x,y points [(900, 100), (900, 200), ....]
        points.append(temp)

    for x in range(1,10):
        # vertical lines - from 1 to 10, to close the grid on the right side
        temp = []
        temp.append((x * cell_size, 0)) #x,y points [(100,0), (200,0), .....]
        temp.append((x * cell_size, 900)) # x,y points [(100, 900), (200,900), ....]
        points.append(temp)
    #print(points)
    return points


SUB_GRID_SIZE = 3
GRID_SIZE = SUB_GRID_SIZE * SUB_GRID_SIZE

def pattern(row_num: int, col_num: int) -> int:
    return(SUB_GRID_SIZE * (row_num % SUB_GRID_SIZE) + row_num//SUB_GRID_SIZE + col_num) % GRID_SIZE

def shuffle(samp: range) -> list:
    return sample(samp, len(samp))

def create_grid(sub_grid: int) -> list[list]:
    #create the 9x9 grid filled with random numbers 
    row_base = range(sub_grid)
    rows = [g * sub_grid + r for g in shuffle(row_base) for r in shuffle(row_base)]
    cols = [g * sub_grid + c for g in shuffle(row_base) for c in shuffle(row_base)]
    nums = shuffle(range(1, sub_grid * sub_grid + 1))
    return [[nums[pattern(r, c)] for c in cols] for r in rows]


def remove_numbers(grid: int) -> None:
    # randomly sets numbers to 0 on the grid
    num_of_cells = GRID_SIZE * GRID_SIZE
    empties = num_of_cells * 3 // 7 # 7 is ideal - higher this number means easier game
    for i in sample(range(num_of_cells), empties):
        grid[i // GRID_SIZE][i % GRID_SIZE] = 0 

class Grid:
    def __init__(self, pygame,font):
        self.cell_size = 100
        self.num_x_offset = 40
        self.num_y_offset = 30
        self.line_coordinates = create_line_coordinates(self.cell_size)
        self.win = False
        self.game_font = font

        self.grid = create_grid(SUB_GRID_SIZE)
        self.__test_grid = deepcopy(self.grid) # create a copy before removing numvers
        
        #print(self.__test_grid)  
        remove_numbers(self.grid)
        self.occupied_cell_cordinated = self.pre_occupied_cells()
        #print(self.occupied_cell_cordinated)

        

        self.selection = SelectNumber(pygame, self.game_font)
    
    def restart(self) -> None:
        self.grid = create_grid(SUB_GRID_SIZE)
        self.__test_grid = deepcopy(self.grid)
        remove_numbers(self.grid)
        self.occupied_cell_cordinated = self.pre_occupied_cells()
        self.win = False

    def check_grids(self):
        #checks if all the cells in the main grid and the test grid are equal 
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] != self.__test_grid[y][x]:
                    return False
        return True
    

    def is_cell_preoccupied(self, x: int, y: int) -> bool:
        # check for non playable cells 
        for cell in self.occupied_cell_cordinated:
            if x == cell[1] and y == cell[0]:   # x is column, y is row
                return True
        return False


    def get_mouse_click(self, x: int, y: int) -> None:
        if x <= 900:
            grid_x, grid_y = x // 100, y // 100
            #print(grid_x, grid_y)
            if not self.is_cell_preoccupied(grid_x, grid_y):
                self.set_cell(grid_x, grid_y, self.selection.selected_number)
        self.selection.button_clicked(x,y)
        if self.check_grids():
            print("Won, Game Over!!!")
            self.win = True

    def pre_occupied_cells(self) -> list[tuple]:
        #gather the u and x xoordinates for all preoccupied cells
        occupied_cell_coordinates = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.get_cell(x, y) != 0:
                    occupied_cell_coordinates.append((y, x)) # first the row, then the column: y,x
        return occupied_cell_coordinates



    def __draw_lines(self, pg, surface) -> None:
        for index, point in enumerate(self.line_coordinates):
            pg.draw.line(surface, (0, 50, 0), point[0], point[1])
            if index == 2 or index == 5 or index == 10 or index == 13:
                pg.draw.line(surface, (255, 200, 0), point[0], point[1])
            else:
                pg.draw.line(surface, (0, 50, 0), point[0], point[1])


    def __draw_numbers(self, surface) -> None:
        #Draw the grid numbers:
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.get_cell(x,y) != 0:
                    if (y, x) in self.occupied_cell_cordinated:
                        text_surface = self.game_font.render(str(self.get_cell(x, y)), False, (0, 200, 255))
                    else:
                        text_surface = self.game_font.render(str(self.get_cell(x, y)), False, (0, 255, 0))
                    
                    if self.get_cell(x, y) != self.__test_grid[y][x]:  #self.get_cell(x, y) != self.__test_grid[y][x]
                        text_surface = self.game_font.render(str(self.get_cell(x,y)), False, (255, 0, 0))
                    surface.blit(text_surface, (x * self.cell_size + self.num_x_offset, y * self.cell_size + self.num_y_offset))
    
    def draw_all(self, pg, surface):
        self.__draw_lines(pg, surface)
        self.__draw_numbers(surface)
        self.selection.draw(pg, surface)

    def get_cell(self, x: int, y: int) -> int:
        # get a cell valur at y, x coordinates
        return self.grid[y][x]
    
    def set_cell(self, x: int, y: int, value: int) -> None:
        # set a cell value at y, x coordinates
        self.grid[y][x] = value


    def show(self):
        for cell in self.grid:
            print(cell)

if __name__ == "__main__":
    grid = Grid()
    grid.show()