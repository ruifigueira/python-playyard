from random import randint
import pygame
import time

def create_coord(x, y):
    return (x, y)

def get_x(coord):
    return coord[0]

def get_y(coord):
    return coord[1]

def create_board(n, active_coords = ()):
    board = [[0]*n for _ in range(n)]
    for i in range(len(active_coords)):
        set_cell_at(board, active_coords[i], 1)
    return board

def board_len(board):
    return len(board)

def cell_at(board, coord):
    size = board_len(board)
    if get_x(coord) < 0 or get_x(coord) >= size or get_y(coord) < 0 or get_y(coord) >= size:
        return 0
    return board[get_y(coord)][get_x(coord)]

def set_cell_at(board, coord, val):
    board[get_y(coord)][get_x(coord)] = val

def rand_val():
    return randint(0, 1)

def random_board(size):
    board = create_board(size)
    for l in range(size):
        for c in range(size):
            val = rand_val()
            set_cell_at(board, create_coord(c, l), val)
    return board

def count_neighbours(board, coord):
    size = board_len(board)
    count = 0
    count = count + cell_at(board, create_coord(get_x(coord) - 1, get_y(coord) - 1))
    count = count + cell_at(board, create_coord(get_x(coord) - 1, get_y(coord)))
    count = count + cell_at(board, create_coord(get_x(coord) - 1, get_y(coord) + 1))
    count = count + cell_at(board, create_coord(get_x(coord), get_y(coord) - 1))
    count = count + cell_at(board, create_coord(get_x(coord), get_y(coord) + 1))
    count = count + cell_at(board, create_coord(get_x(coord) + 1, get_y(coord) - 1))
    count = count + cell_at(board, create_coord(get_x(coord) + 1, get_y(coord)))
    count = count + cell_at(board, create_coord(get_x(coord) + 1, get_y(coord) + 1))                   
    return count

def compute_new_state(val, count):
    if val == 1 and (count < 2 or count > 3):
        return 0
    if val == 0 and count != 3:
        return 0
    return 1

def next_board(board):
    size = board_len(board)
    new_board = create_board(size)
    for l in range(size):
        for c in range(size):
            coord = create_coord(c, l)
            set_cell_at(new_board, coord, compute_new_state(cell_at(board, coord), count_neighbours(board, coord))) 
    return new_board

def paint_board(screen, zoom, board):
    size = board_len(board)
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, zoom * size, zoom * size))    

    for l in range(size):
        for c in range(size):
            coord = create_coord(c, l)
            val = cell_at(board, coord)
            count = count_neighbours(board, coord)
            color_inc = count * 16 - 1
            color = (0, 0, 0) if val == 0 else (128 + color_inc, 32 + color_inc, 32 + color_inc)
            pygame.draw.rect(screen, color, (c * zoom, l * zoom, zoom, zoom))
    pygame.display.update()

def game(board, num_iterations, zoom = 2):
    size = board_len(board)

    screen_size = size * zoom, size * zoom

    pygame.init()
    screen = pygame.display.set_mode(screen_size)

    for i in range(num_iterations):
        # from http://stackoverflow.com/a/20166290
        pygame.event.get()
        
        paint_board(screen, zoom, board)
        board = next_board(board)
        time.sleep(.1)

game(create_board(51, [(25, 25), (25, 26), (26, 26), (27, 26), (27, 25), (27, 24), (26, 27)]), 200, 4)
