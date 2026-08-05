
from random import choice
from src.constants import *

class TetrisBoard:

    def __init__(self, w:int, h:int, d:int,
                 score=0,
                 lines=0,
                 block_held_type=BLOCK_NONE,
                 block_next_type=BLOCK_NONE,
                 block_falling_type=BLOCK_NONE,
                 block_falling_x=None,
                 block_falling_y=None,
                 block_falling_r=None,
                 can_swap_blocks=True):
        self.w = w
        self.h = h
        self.difficulty = d
        self.board = [[BLOCK_NONE for _ in range(w)] for _ in range(h)]
        self.score = score
        self.lines = lines
        self.is_gameover = False
        self.can_swap_blocks = can_swap_blocks
        self.block_held_type = block_held_type
        self.block_next_type = block_next_type
        self.block_falling_type = block_falling_type
        self.block_falling_x = block_falling_x
        self.block_falling_y = block_falling_y
        self.block_falling_r = block_falling_r

        # This two vairables initialize game if its new
        if self.block_next_type == BLOCK_NONE:
            self.get_new_block_next()

        if self.block_falling_type == BLOCK_NONE:
            self.get_new_block_falling()

    # Generate new block falling, return True on success, False if gameover
    def get_new_block_falling(self) -> bool:
        x0 = (self.w - BLOCK_WIDTHS[self.block_falling_type])//2
        y0 = 0
        r0 = 0
        nt = self.block_next_type
        # Test if it's possible to put next block at origin. If it's
        # not possible, then the board if 'full' and that indicates
        # Game over.
        can_generate =  self.can_move_block_falling_to(x0, y0, r0, nt)
        if can_generate:
            self.block_falling_type = nt
            self.block_falling_y = y0
            self.block_falling_x = x0
            self.block_falling_r = r0
            self.get_new_block_next()
            self.can_swap_blocks = True
        self.is_gameover = not can_generate
        return can_generate

    def interchange(self) -> bool:
        if self.can_swap_blocks:
            # When a new game starts, self.block_held_type == BLOCK_NONE
            # For this reason, first interchange fill simply replace
            # held block by falling block.
            if self.block_held_type != BLOCK_NONE:
                t = self.block_falling_type
                self.block_falling_type = self.block_held_type
                self.block_held_type = t
                self.block_falling_y = 0
                self.block_falling_x = (self.w - BLOCK_WIDTHS[self.block_falling_type])//2
                self.block_falling_r = 0
            else:
                self.block_held_type = self.block_falling_type
                self.get_new_block_falling()
            self.can_swap_blocks = False
            return True
        else:
            return False


    # Generate a new block next
    def get_new_block_next(self):
        self.block_next_type = choice(BLOCKS)
    
    def rotate_block_falling(self, dr:int) -> bool:
        nr = (self.block_falling_r + dr)%4
        # Check if it's possible to rotate shape
        can_rotate = self.can_move_block_falling_to(
                self.block_falling_x, self.block_falling_y,
                nr, self.block_falling_type)
        if can_rotate:
            self.block_falling_r = nr
        # Return true if could be rotated, else False
        return can_rotate

    def displace_block_falling(self, dx:int, dy:int) -> bool:
        nx = self.block_falling_x + dx
        ny = self.block_falling_y + dy
        # check if it's possible to dispace
        can_displace = self.can_move_block_falling_to(
                nx, ny, self.block_falling_r,
                self.block_falling_type)
        if can_displace:
            self.block_falling_x = nx
            self.block_falling_y = ny
        # Return true if could be displaced, else False
        return can_displace


    # checks if it's possible to place a falling block given
    # coordinates tx, tx, rotatioo tx and its type. That means that
    # 1) Given tetromino is within the board (not out of index)
    # 2) Given tetromino doesn't coincide with other fixed tetromino
    def can_move_block_falling_to(self, tx, ty, tr, type):
        for i,j in BLOCKS_ROTS[type][tr]:
            # Check if figure is within board and if there are
            # Any block in given position
            xx, yy = tx+i, ty+j
            if (xx < 0 or xx >= self.w or
                yy < 0 or yy >= self.h or
                self.board[yy][xx]):
                # Cannot move to position
                return False
        # Can move
        return True

    # Move block falling down, checks game over, generate new block
    def update(self) -> bool:
        ny = self.block_falling_y + 1
        can_move_down = self.can_move_block_falling_to(
                self.block_falling_x, ny,
                self.block_falling_r, self.block_falling_type)
        if can_move_down:
            self.block_falling_y = ny
        else:
            self.fix_block_falling_into_board()
            self.score += 1
            self.delete_full_rows()
            self.get_new_block_falling()
        return can_move_down


    # Fix tetromino into board
    def fix_block_falling_into_board(self):
        for x,y in BLOCKS_ROTS[self.block_falling_type][self.block_falling_r]:
            self.board[self.block_falling_y+y][self.block_falling_x+x] = self.block_falling_type

    def delete_full_rows(self):
        y = self.h-1
        while y >= 0:
            for x in range(self.w):
                if self.board[y][x] == BLOCK_NONE:
                    y -= 1
                    break
            else:
                # Deletes full row
                self.board.pop(y)
                # Insert empty row at the beginning of the board
                self.board.insert(0, [BLOCK_NONE for _ in range(self.w)])
                self.lines += 1
    
