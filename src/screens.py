
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
        self.config.tetris = config.tetris
        self.audio = config.audio

        self.move_block_interval = 900 # milliseconds
        self.dec_interval = 20 # milliseconds

        # variables related with game working

        self.update_label_surfaces()
        self.update_score_surface()
        self.update_lines_surface()
        self.update_render = True
        self.time_counter = 0
        self.max_time_delta = 1000



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

    def quit(self, state):
        self.config.state = state
        self.running = False
        if state == STATE_GAMEOVER:
            self.audio.play("game over")
        elif state == STATE_GAME:
            w = self.config.tetris.w
            h = self.config.tetris.h
            d = self.config.tetris.difficulty
            self.config.tetris = TetrisBoard(w, h, d)
        elif state == STATE_PAUSE:
            pass
            

    def run_loop(self):

        pygame.display.set_caption("Tetris")

        self.running = True
        while self.running:
            self.handle_events()

            # This part automatically calculates times to uptade
            # bock falling
            delta = self.max_time_delta//((self.config.tetris.difficulty + self.config.tetris.score)/15+1)
            if self.time_counter > delta:
                self.time_counter = 0
                self.config.tetris.update()
                self.update_render = True
                if self.config.tetris.is_gameover:
                    self.quit(STATE_GAMEOVER)

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
                    COLOR_BLOCK[self.config.tetris.board[y][x]],
                    pygame.Rect( bsz*x + x0, bsz*y + y0, bsz, bsz)
                                 )
        # rendering falling block
        fbt = self.config.tetris.block_falling_type
        fbx = self.config.tetris.block_falling_x
        fby = self.config.tetris.block_falling_y
        fbr = self.config.tetris.block_falling_r
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

        pbsz = min(scrn_h*0.06, scrn_w*0.03)
        # rendering next block background
        pygame.draw.rect(window, COLOR_BLOCK[BLOCK_NONE],
            pygame.Rect(
                x1 - pbsz * 2.25,  y2 + nxtlbl_sfc.height,
                pbsz * 4.5, pbsz * 4.5))
        # render next block
        bct = self.config.tetris.block_next_type
        for x,y in BLOCKS_ROTS[bct][0]:
             pygame.draw.rect(window, COLOR_BLOCK[bct],
                (x1 + pbsz * (-BLOCK_WIDTHS[bct]/2 + x),
                y2 + nxtlbl_sfc.height + pbsz * (2.25 + y - BLOCK_HEIGHTS[bct]/2),
                 pbsz, pbsz))


        # rendering hold block label
        hldlbl_sfc = self.hold_label_surface
        window.blit(hldlbl_sfc,
                    (x2 - hldlbl_sfc.width/2, y2))

        # rendering hold_block background
        pygame.draw.rect(window, COLOR_BLOCK[BLOCK_NONE],
            pygame.Rect(
                x2 - pbsz * 2.25,  y2 + hldlbl_sfc.height,
                pbsz * 4.5, pbsz * 4.5))
        # rendering hold block
        bht = self.config.tetris.block_held_type
        for x,y in BLOCKS_ROTS[bht][0]:
            color = COLOR_BLOCK[bht]
            if not self.config.tetris.can_swap_blocks:
                color = tuple(map(lambda i: int(i*0.4), color))
            pygame.draw.rect(window, color,
             (x2 + pbsz * (-BLOCK_WIDTHS[bht]/2 + x),
                 y2 + hldlbl_sfc.height + pbsz * (2.25 + y - BLOCK_HEIGHTS[bht]/2),
                 pbsz, pbsz))

        pygame.display.flip()


    def update_score_surface(self):
        self.score_points_surface = self.font.render(
            f'{self.config.tetris.score}', True, COLOR_FONT)

    def update_lines_surface(self):
        self.lines_points_surface = self.font.render(
            f'{self.config.tetris.lines}', True, COLOR_FONT)

    def quit(self, state:int):
        self.config.state = state
        self.running = False


    def handle_events(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.quit(STATE_QUIT)

            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_p:
                    self.quit(STATE_PAUSE)
                
                # Displace falling block to left and right
                elif ev.key == pygame.K_LEFT or ev.key == pygame.K_h:
                    if self.config.tetris.displace_block_falling(-1,0):
                        self.audio.play("displace")
                elif ev.key == pygame.K_RIGHT or ev.key == pygame.K_l:
                    if self.config.tetris.displace_block_falling(1,0):
                        self.audio.play("displace")
                # Move tetromino down until finds floor
                elif ev.key == pygame.K_SPACE or ev.key == pygame.K_u:
                    while self.config.tetris.update():
                        self.render()
                        pygame.time.delay(2)
                    self.audio.play('drop')
                    if self.config.tetris.is_gameover:
                        self.quit(STATE_GAMEOVER)
                # Move tetromino down
                elif ev.key == pygame.K_DOWN or ev.key == pygame.K_j:
                    self.config.tetris.update()
                    if self.config.tetris.is_gameover:
                        self.quit(STATE_GAMEOVER)
                # Rotates tetromino
                elif ev.key == pygame.K_UP or ev.key == pygame.K_k:
                    if self.config.tetris.rotate_block_falling(1):
                        self.audio.play("rotate")
                elif ev.key == pygame.K_c or ev.key == pygame.K_i:
                    # Swaps falling and held blocks
                    if self.config.tetris.interchange():
                        self.audio.play("interchange")
                    else:
                        self.audio.play("deny")

                # exit app
                elif ev.key == pygame.K_q:
                    self.config.state = STATE_QUIT
                    self.quit(STATE_QUIT)
                # toggle audio
                elif ev.key == pygame.K_m:
                    self.audio.mute = not self.audio.mute

                elif ev.key == pygame.K_r:
                    self.quit(STATE_GAME)

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
    
    def __init__(self, config):
        self.config = config

        self.title = "Pause"
        self.keys_bindings = (
                ('h | LEFT', 'Move left'),
                ('l | RIGHT', 'Move right'),
                ('j | DOWN', 'Move down'),
                ('k | UP', 'Move up'),
                ('p', 'Pause | Resume Game'),
                ('c | i', 'Interchange blocks'),
                ('u | SPACE', 'Drop block'),
                ('m', 'Mute | Unmute sound'),
                ('r', 'Restart game'),
                ('q', 'Quit game'),
                )

        st, nd = 0.25, 0.95
        self.keys_bindings_pos = tuple(
                (0.33, 0.55, st + y*(nd-st)/len(self.keys_bindings))
                for y in range(len(self.keys_bindings))
                )

        self.update_scales()
        self.update_render = True

    def run_loop(self):
        pygame.display.set_caption("Pause")

        self.running = True
        while self.running:
            self.handle_events()
            if self.update_render:
                self.render()
            self.config.clock.tick(MAX_FPS)

    def render(self):
        window = self.config.window
        ww,wh = pygame.display.get_window_size()

        window.fill(COLOR_BACKGROUND)
        window.blit(self.title_surface,
            ((ww - self.title_surface.width)/2,
            wh*0.1 - self.title_surface.height/2))

        for pos, sfc in zip(self.keys_bindings_pos, self.keys_surfaces):
            y0 = wh*pos[2] - sfc[0].height/2
            x0 = ww*pos[0]
            window.blit(sfc[0],(x0 - sfc[0].width/2, y0))
            window.blit(sfc[1],(ww*pos[1], y0))

        pygame.display.flip()

    def update_scales(self):
        w,h = pygame.display.get_window_size()
        ref = min(w,h)
        font_title = pygame.font.Font(FONT_FILEPATH, int(ref*0.15))
        self.title_surface = font_title.render(
                self.title, True, COLOR_FONT, COLOR_BACKGROUND)

        font_keys = pygame.font.Font(FONT_FILEPATH, int(ref*0.05))
        self.keys_surfaces = tuple(
                (
                font_keys.render(k, True, COLOR_FONT, COLOR_BACKGROUND),
                font_keys.render(t, True, COLOR_FONT, COLOR_BACKGROUND)
                    )
                for k, t in self.keys_bindings
                )

    def quit(self, state:int):
        self.config.state = state
        self.running = False

    def handle_events(self):
        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                self.quit(STATE_QUIT)

            elif ev.type == pygame.KEYDOWN:

                if ev.key == pygame.K_p:
                    self.quit(STATE_GAME)

                elif ev.key == pygame.K_q:
                    self.quit(STATE_QUIT)

            elif ev.type == pygame.VIDEORESIZE:
                self.update_render = True
                self.update_scales()

class GameOver:
    
    def __init__(self, config):
        self.config = config

        # it controls wherther "Press any Key" is displayed or not
        self.visible = True
        pygame.time.set_timer(self.config.blink_event, 800)

        self.labels = (
                "Game over!",
                f"Score: {self.config.tetris.score} | Lines: {self.config.tetris.lines}",
                "Press any key"
                )

        self.labels_pos = (0.5, 0.25), (0.5, 0.5), (0.5, 0.75)
        self.labels_scales = 0.15, 0.16, 0.14
        self.labels_blink = [True, True, False]

        self.update_label_scales()

        self.update_render = True


    def run_loop(self):

        pygame.display.set_caption("Game Over")

        self.running = True
        while self.running:
            self.handle_events()
            if self.update_render:
                self.render()
                self.update_render = False
            self.config.clock.tick(MAX_FPS)

    def quit(self, new_state:int):
        self.running = False
        self.config.state = new_state
        pygame.time.set_timer(self.config.blink_event, 0)
        if new_state == STATE_GAME:
            w = self.config.tetris.w
            h = self.config.tetris.h
            d = self.config.tetris.difficulty
            self.config.tetris = TetrisBoard(w, h, d)
        elif new_state == STATE_QUIT:
            pass


    def render(self):

        window = self.config.window
        window.fill(COLOR_BACKGROUND)

        scrn_w, scrn_h = pygame.display.get_window_size()

        for pos, sfc, blink in zip(self.labels_pos, self.labels_surface, self.labels_blink):
            x = scrn_w * pos[0] - sfc.width*0.5
            y = scrn_h * pos[1] - sfc.height*0.5
            if blink or self.visible:
                window.blit(sfc, (x,y))
        
        pygame.display.flip()

    def update_label_scales(self):
        # this function update the dsplayed fonts sizes
        # when window is resized
        scrn_w, scrn_h = pygame.display.get_window_size()
        ref = min(scrn_w, scrn_h)

        fonts = [pygame.font.Font(FONT_FILEPATH, int(ref* i)) for i in self.labels_scales]

        self.labels_surface = [
                f.render(t, True, COLOR_FONT, COLOR_BACKGROUND) 
                for f,t in zip(fonts, self.labels)
                ]

    def handle_events(self):
        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                self.quit(STATE_QUIT)

            elif ev.type == pygame.KEYDOWN:

                if ev.key == pygame.K_q:
                    self.quit(STATE_QUIT)
                else:
                    self.quit(STATE_GAME)


            elif ev.type == pygame.VIDEORESIZE:
                self.update_label_scales()

            elif ev.type == self.config.blink_event:
                self.visible = not self.visible
                self.update_render = True

            # End events type
            else:
                pass

