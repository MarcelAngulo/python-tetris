
import pygame
from random import choice

from src.constants import *
from src.tetrisboard import TetrisBoard

'''
This file contains GameOver, Game and Pause classes
each of them handles different events and draw different
things
'''
class Game:
    
    def __init__(self, config):
        self.config = config
        self.tetris = config.tetris

        self.move_block_interval = 900 # milliseconds
        self.dec_interval = 20 # milliseconds

        # variables related with game working

        self.update_label_surfaces()
        self.update_score_surface()
        self.update_lines_surface()
        self.update_render = True
        self.time_counter = 0
        self.max_time_delta = 1000

        self.MOVE_DOWN = pygame.event.custom_type()


    def update_label_surfaces(self):
        w,h = pygame.display.get_window_size()

        self.font = pygame.font.Font(FONT_FILEPATH, min(w,h)//10)

        self.score_label_surface = self.font.render(
            "Score", True, COLOR_FONT, COLOR_PANEL)

        self.lines_label_surface = self.font.render(
            "Lines", True, COLOR_FONT, COLOR_PANEL)

        self.next_label_surface = self.font.render(
            "Next", True, COLOR_FONT, COLOR_PANEL)

        self.hold_label_surface = self.font.render(
            "Hold", True, COLOR_FONT, COLOR_PANEL)

    def quit(self):
        self.running = False

    def run_loop(self):

        pygame.display.set_caption("Tetris")

        self.running = True
        while self.running:
            self.handle_events()

            # This part automatically calculates times to uptade
            # bock falling
            delta = self.max_time_delta//(self.tetris.difficulty/10+1)
            if self.time_counter > delta:
                self.time_counter = 0
                self.tetris.update()
                self.update_render = True
                if self.tetris.is_gameover:
                    self.config.state = STATE_GAMEOVER
                    self.quit()

            # Check if necesary to render, for saving energy and cpu
            if self.update_render:
                self.render()
                self.update_render = False
            self.time_counter += self.config.clock.tick(MAX_FPS)


    def render(self):
        window = self.config.window
        scrn_w,scrn_h = pygame.display.get_window_size()
        brdw = self.config.tetris.w
        brdh = self.config.tetris.h
        # ------------------------------
        # rendering the left screen side
        # ------------------------------
        window.fill(COLOR_BACKGROUND,
            pygame.Rect(0, 0, scrn_w/2, scrn_h))
        # Size of blocks in grid
        bsz = min(scrn_w, scrn_h)/(2*brdw)

        x0 = (scrn_w/2 - bsz *brdw)/2
        y0 = (scrn_h - bsz *brdh)/2
        # rendering board blocks
        for x in range(brdw):
            for y in range(brdh):
                pygame.draw.rect(window,
                    COLOR_BLOCK[self.tetris.board[y][x]],
                    pygame.Rect( bsz*x + x0, bsz*y + y0, bsz, bsz)
                                 )
        # rendering falling block
        fbt = self.tetris.block_falling_type
        fbx = self.tetris.block_falling_x
        fby = self.tetris.block_falling_y
        fbr = self.tetris.block_falling_r
        for x, y in BLOCKS_ROTS[fbt][fbr]:
            pygame.draw.rect( window, COLOR_BLOCK[fbt],
                pygame.Rect(
                    bsz * (fbx + x) + x0,
                    bsz * (fby + y) + y0,
                    bsz, bsz))
        
        # rendering board grid
        for x in range(brdw + 1): # vertical lines
            pygame.draw.line(window, COLOR_GRID,
                (x0 + x * bsz, y0), # start point
                (x0 + x * bsz, scrn_h - y0), # end point
                width=1)
        for y in range(brdh+ 1): # horizontal lines
            pygame.draw.line(window, COLOR_GRID,
                (x0, y0 + y * bsz), # start point
                (scrn_w//2 - x0, y0 + y * bsz), # end point
                width=1)

        # -------------------------------
        # rendering the right screen side
        # -------------------------------

        x1 = scrn_w * 0.625
        x2 = scrn_w * 0.875
        y1 = scrn_h * 0.25
        y2 = scrn_h * 0.5
        window.fill(COLOR_PANEL,pygame.Rect(scrn_w/2,0,scrn_w/2,scrn_h))

        scrlbl_sfc = self.score_label_surface
        scrpts_sfc = self.score_points_surface
        lnslbl_sfc = self.lines_label_surface
        lnspts_sfc = self.lines_points_surface

        # rendering score label
        window.blit(scrlbl_sfc,
            (x1 - scrlbl_sfc.width/2, y1 - scrlbl_sfc.height)
                    )
        # rendering score points
        window.blit(scrpts_sfc, (x1 - scrpts_sfc.width/2, y1))

        # rendering lines label
        window.blit(lnslbl_sfc,
            (x2 - lnslbl_sfc.width/2, y1 - lnslbl_sfc.height))

        # rendering lines points
        window.blit(lnspts_sfc, (x2 - lnspts_sfc.width/2, y1))


        nxtlbl_sfc = self.next_label_surface
        # rendering next block label
        window.blit(nxtlbl_sfc, (x1 - nxtlbl_sfc.width/2, y2))

        # rendering next block background
        pygame.draw.rect(window, COLOR_BLOCK[BLOCK_NONE],
            pygame.Rect(
                x1 - bsz * 2.25,  y2 + nxtlbl_sfc.height,
                bsz * 4.5, bsz * 4.5))
        # render next block
        bct = self.config.tetris.block_next_type
        for x,y in BLOCKS_ROTS[bct][0]:
             pygame.draw.rect(window, COLOR_BLOCK[bct],
                (x1 + bsz * (-BLOCK_WIDTHS[bct]/2 + x),
                y2 + nxtlbl_sfc.height + bsz * (2.25 + y - BLOCK_HEIGHTS[bct]/2),
                 bsz, bsz))


        # rendering hold block label
        hldlbl_sfc = self.hold_label_surface
        window.blit(hldlbl_sfc,
                    (x2 - hldlbl_sfc.width/2, y2))

        # rendering hold_block background
        pygame.draw.rect(window, COLOR_BLOCK[BLOCK_NONE],
            pygame.Rect(
                x2 - bsz * 2.25,  y2 + hldlbl_sfc.height,
                bsz * 4.5, bsz * 4.5))
        # rendering hold block
        bht = self.config.tetris.block_held_type
        for x,y in BLOCKS_ROTS[bht][0]:
             pygame.draw.rect(window, COLOR_BLOCK[bht],
             (x2 + bsz * (-BLOCK_WIDTHS[bht]/2 + x),
                 y2 + hldlbl_sfc.height + bsz * (2.25 + y - BLOCK_HEIGHTS[bht]/2),
                 bsz, bsz))

        pygame.display.flip()


    def update_score_surface(self):
        self.score_points_surface = self.font.render(
            f'{self.tetris.score}', True, COLOR_FONT)

    def update_lines_surface(self):
        self.lines_points_surface = self.font.render(
            f'{self.tetris.lines}', True, COLOR_FONT)

    def handle_events(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.config.state = STATE_QUIT
                self.quit()

            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_p:
                    self.config.state = STATE_PAUSE
                    self.quit()

                elif ev.key == pygame.K_LEFT or ev.key == pygame.K_h:
                    self.tetris.displace_block_falling(-1,0)
                elif ev.key == pygame.K_RIGHT or ev.key == pygame.K_l:
                    self.tetris.displace_block_falling(1,0)
                # Move tetromino down until finds floor
                elif ev.key == pygame.K_SPACE or ev.key == pygame.K_u:
                    while self.tetris.update():
                        self.render()
                        pygame.time.delay(2)
                    if self.tetris.is_gameover:
                        self.config.state = STATE_GAMEOVER
                        self.quit()
                # Move tetromino down
                elif ev.key == pygame.K_DOWN or ev.key == pygame.K_j:
                    self.tetris.update()
                    if self.tetris.is_gameover:
                        self.config.state = STATE_GAMEOVER
                        self.quit()
                # Rotates tetromino
                elif ev.key == pygame.K_UP or ev.key == pygame.K_k:
                    self.tetris.rotate_block_falling(1)
                elif ev.key == pygame.K_c or ev.key == pygame.K_i:
                    # Swaps falling and held blocks
                    self.config.tetris.interchange()
                elif ev.key == pygame.K_q:
                    self.config.state = STATE_QUIT
                    self.quit()

                self.update_score_surface()
                self.update_lines_surface()
                self.update_render = True

            elif ev.type == pygame.VIDEORESIZE:
                self.update_label_surfaces()
                self.update_score_surface()
                self.update_lines_surface()
                self.update_render = True

            # End of ev.type
            else:
                pass
        

class Pause:
    
    def __init__(self, scrn, clock):
        self.window = scrn
        scrn_w = self.window.width
        scrn_h = self.window.height
        self.clock = clock

        self.line_color = 255, 255, 255
        self.rect_color = 255, 255, 255

        self.left_side_keys = 'p', 'r', 'q'
        self.left_side_labels = "Resume", "Retart", "Quit"

        self.right_side_keys = (
            ('' , '^',  ''), 
            ('<', 'v', '>'))
        self.right_side_labels = (
            ("", "Rotate", ""),
            ("Left", "Down", "Right"))

        self.right_side_keys2 = 'c', '       space       '
        self.right_side_labels2 = "Interchange", "Drop"

    def start_loop(self):
        self.update_scales()
        pygame.display.set_caption("Pause")
        self.running = True

        while self.running:
            self.handle_events()
            self.update_state()
            self.render()
            self.clock.tick(MAX_FPS)
        else:
            return self.return_vals

    def render(self):

        self.window.fill(COLOR_BACKGROUND)

        self.window.blit(self.pause_label_sfc,
            (scrn_w*0.5 - self.pause_label_w*0.5, scrn_h*0.1))

        pygame.draw.line(self.window,
            self.line_color,
            (scrn_w*0.5, scrn_h*0.1 + self.pause_label_h), # start point
            (scrn_w*0.5, scrn_h*0.9), width=2
            )

        n_items = 3
        items = zip(
            self.left_side_keys_sfc,
            self.left_side_labels_sfc,
            range(n_items))
        for ksfc, lblsfc, i in items:
            kw = ksfc.width
            kh = ksfc.height
            dy = (scrn_h*0.8 - self.pause_label_h) / (n_items + 1)
            self.window.blit(ksfc,
                (scrn_w*0.1 - kw*0.5, scrn_h*0.2 + self.pause_label_h + i*dy))
            self.window.blit(lblsfc,
                (scrn_w*0.2 + kw, scrn_h*0.2 + self.pause_label_h + i*dy))
            pygame.draw.rect(
                self.window, self.rect_color,
                pygame.Rect(scrn_w*0.1 - kh*0.5, scrn_h*0.2 + self.pause_label_h + i*dy, kh, kh), width=self.ln_w
                )

        dy = (scrn_h*0.8 - self.pause_label_h) / (n_items + 1)

        n_items = 3
        items = zip(
            self.right_side_keys_sfc,
            self.right_side_labels_sfc,
            range(n_items))
        for k_sfcs, lbl_sfcs, i in items:
            n_subitems = 3
            subitems = zip(k_sfcs, lbl_sfcs, range(n_subitems))
            for ksfc, lblsfc, j in subitems:
                kh = ksfc.height
                kw = ksfc.width
                self.window.blit(ksfc,
                    (scrn_w/8 * (5+j) - kw*0.5, scrn_h*0.1 + self.pause_label_h + (i+1)*dy - kh))
                self.window.blit(lblsfc,
                    (scrn_w/8 * (5+j) - lblsfc.width*0.5, scrn_h*0.1 + self.pause_label_h + (i+1)*dy))
                if self.right_side_keys[i][j]:
                    pygame.draw.rect(self.window, self.rect_color,
                        pygame.Rect(scrn_w/8 * (5+j) - kh*0.5, scrn_h*0.1 + self.pause_label_h + (i+1)*dy - kh, kh, kh), width=self.ln_w)

        n_items = 2
        items = zip(
            self.right_side_keys2_sfc,
            self.right_side_labels2_sfc,
            range(n_items))
        for ksfc, lblsfc, i in items:
            kw = ksfc.width
            kh = ksfc.height
            self.window.blit(ksfc,
                (scrn_w/6 * (4+i) - kw*0.5, scrn_h*0.15 + self.pause_label_h + 3*dy - kh))
            self.window.blit(lblsfc,
                (scrn_w/6 * (4+i) - lblsfc.width*0.5, scrn_h*0.15 + self.pause_label_h + 3*dy))
            rw = max(kh,kw)
            pygame.draw.rect(self.window, self.rect_color,
                        pygame.Rect(scrn_w/6 * (4+i) - max(kh,kw)*0.5, scrn_h*0.15 + self.pause_label_h + 3*dy - kh, rw, kh), width=self.ln_w)

        pygame.display.flip()

    def update_scales(self):

        scrn_w = self.window.width
        scrn_h = self.window.height
        ref = min(scrn_w, scrn_h)
        self.font1_sz = ref//6
        self.font2_sz = ref//10
        self.font3_sz = ref//15
        self.font4_sz = ref//17
        self.ln_w = max(1, ref//150)

        self.font1 = pygame.font.Font(FONT_FILEPATH, self.font1_sz)
        self.font2 = pygame.font.Font(FONT_FILEPATH, self.font2_sz)
        self.font3 = pygame.font.Font(FONT_FILEPATH, self.font3_sz)
        self.font4 = pygame.font.Font(FONT_FILEPATH, self.font4_sz)

        self.pause_label_sfc = self.font1.render(
            "Pause", True, COLOR_FONT, COLOR_BACKGROUND)
        self.pause_label_w = self.pause_label_sfc.width
        self.pause_label_h = self.pause_label_sfc.height

        self.left_side_keys_sfc = tuple(map(
            lambda k: self.font2.render(k, True, COLOR_FONT, COLOR_BACKGROUND), self.left_side_keys))
        self.left_side_labels_sfc = tuple(map(
            lambda lbl: self.font2.render(lbl, True, COLOR_FONT, COLOR_BACKGROUND), self.left_side_labels))

        self.right_side_keys_sfc = tuple(map(
            lambda ks: tuple(map(lambda k: self.font3.render(k, True, COLOR_FONT, COLOR_BACKGROUND), ks)), self.right_side_keys))
        self.right_side_labels_sfc = tuple(map(
            lambda lbls: tuple(map(lambda lbl: self.font3.render(lbl, True, COLOR_FONT, COLOR_BACKGROUND), lbls)), self.right_side_labels))

        self.right_side_keys2_sfc = tuple(map(lambda k: self.font3.render(k, True, COLOR_FONT, COLOR_BACKGROUND), self.right_side_keys2))
        self.right_side_labels2_sfc = tuple(map(lambda lbl: self.font4.render(lbl, True, COLOR_FONT, COLOR_BACKGROUND), self.right_side_labels2))

    def handle_events(self):
        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                exit(0)

            elif ev.type == pygame.KEYDOWN:

                if ev.key == pygame.K_p:
                    self.running = False
                    self.return_vals = GAME, {"init new game": False}

                elif ev.key == pygame.K_r:
                    self.running = False
                    self.return_vals = GAME, {"init new game": True}

                elif ev.key == pygame.K_q:
                    exit(0)

            elif ev.type == pygame.VIDEORESIZE:
                scrn_w, scrn_h = ev.size
                self.update_scales()

    def update_state(self):
        pass


class GameOver:
    
    def __init__(self, scrn, clock):
        # related variables with pygame
        self.window = scrn
        scrn_w = scrn.width
        scrn_h = scrn.height
        self.clock = clock

        # variables score and line points
        self.tetris.score = 0
        self.score.lines = 0

        self.time_count = 0
        self.bip_interval = 800 # milliseconds
        # it controls wherther "Press any Key" is displayed or not
        self.visible = True

        COLOR_BACKGROUND =   0,   0,   0
        COLOR_FONT  = 255, 255, 255

    def start_loop(self):

        self.update_scales()
        pygame.display.set_caption("Game Over")
        self.running = True
        self.time_count = pygame.time.get_ticks()

        while self.running:
            self.handle_events()
            self.update_state()
            self.render()
            self.clock.tick(MAX_FPS)
        else:
            return self.return_vals

    def render(self):
        self.window.fill(COLOR_BACKGROUND)

        # rendering game over label
        self.window.blit(
            self.game_over_label_sfc,
            (scrn_w*0.5 - self.game_over_label_w*0.5,
            scrn_h*0.05)
            )

        # rendering score label and score points
        self.window.blit(
            self.tetris.score_label_sfc,
            (scrn_w*0.25 - self.tetris.score_label_w*0.5,
            scrn_h*0.5 - self.tetris.score_label_h*0.75)
            )

        self.window.blit(
            self.tetris.score_points_sfc,
            (scrn_w*0.25 - self.tetris.score_points_w*0.5,
            scrn_h*0.5 + self.tetris.score_label_h*0.25)
            )

        # rendering lines label and lines points
        self.window.blit(
            self.score.lines_label_sfc,
            (scrn_w*0.75 - self.score.lines_label_w*0.5,
            scrn_h*0.5 - self.score.lines_label_h*0.75)
            )

        self.window.blit(
            self.score.lines_points_sfc,
            (scrn_w*0.75 - self.score.lines_points_w*0.5,
            scrn_h*0.5 + self.score.lines_label_h*0.25)
            )

        # renderng "press any key to continue" label
        if self.visible:
            self.window.blit(
                self.press_label_sfc,
                (scrn_w*0.5 - self.press_label_w*0.5,
                scrn_h - self.press_label_h*1.5)
                )


        pygame.display.flip()

    def update_scales(self):
        # this function update the dsplayed fonts sizes
        # when window is resized
        scrn_w = self.window.width
        scrn_h = self.window.height
        ref = min(scrn_h, scrn_w)
        font1_sz = ref // 5
        font2_sz = ref // 7
        font3_sz = ref // 9

        self.font1 = pygame.font.Font(FONT_FILEPATH, font1_sz)
        self.font2 = pygame.font.Font(FONT_FILEPATH, font2_sz)
        self.font3 = pygame.font.Font(FONT_FILEPATH, font3_sz)

        self.game_over_label_sfc = self.font1.render(
            "Game Over!", True, COLOR_FONT, COLOR_BACKGROUND)
        self.game_over_label_w = self.game_over_label_sfc.width
        self.game_over_label_h = self.game_over_label_sfc.height

        self.tetris.score_label_sfc = self.font2.render(
            "Score", True, COLOR_FONT, COLOR_BACKGROUND)
        self.tetris.score_label_w = self.tetris.score_label_sfc.width
        self.tetris.score_label_h = self.tetris.score_label_sfc.height

        self.score.lines_label_sfc = self.font2.render(
            "lines", True, COLOR_FONT, COLOR_BACKGROUND)
        self.score.lines_label_w = self.score.lines_label_sfc.width
        self.score.lines_label_h = self.score.lines_label_sfc.height

        self.tetris.score_points_sfc = self.font2.render(
            f"{self.tetris.score}", True, COLOR_FONT, COLOR_BACKGROUND)
        self.tetris.score_points_w = self.tetris.score_points_sfc.width
        self.tetris.score_points_h = self.tetris.score_points_sfc.height

        self.score.lines_points_sfc = self.font2.render(
            f"{self.score.lines}", True, COLOR_FONT, COLOR_BACKGROUND)
        self.score.lines_points_w = self.score.lines_points_sfc.width
        self.score.lines_points_h = self.score.lines_points_sfc.height

        self.press_label_sfc = self.font3.render(
            "Press any key to continue", True, COLOR_FONT, COLOR_BACKGROUND)
        self.press_label_w = self.press_label_sfc.width
        self.press_label_h = self.press_label_sfc.height

    def handle_events(self):
        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                exit(0)

            if ev.type == pygame.KEYDOWN:

                if ev.key == pygame.K_q:
                    exit(0)
                else:
                    self.running = False
                    self.return_vals = GAME, {"init new game": True}

            if ev.type == pygame.VIDEORESIZE:
                scrn_w, scrn_h = ev.size
                self.update_scales()
            else:
                pass

    def update_state(self):
        if pygame.time.get_ticks() - self.time_count >= self.bip_interval:
            self.visible = not self.visible
            self.time_count = pygame.time.get_ticks()

    def pass_kwargs(self, **kwargs):
        # get score and lines contained in kwargs
        self.tetris.score = kwargs['score']
        self.score.lines = kwargs['lines']
