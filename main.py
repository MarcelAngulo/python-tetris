from numpy import ndarray
from random import choice
import pygame as pg
import atexit

# constants
BOARD_WITDH  = 10
BOARD_HEIGHT = 20


# types of blocks
NO_BLOCK = 0
BLOCK1 = 1
# @@
# @@
BLOCK2 = 2
# @@@@
BLOCK3 = 3
# @
# @@@
BLOCK4 = 4
#   @
# @@@
BLOCK5 = 5
#  @
# @@@
BLOCK6 = 6
#  @@
# @@
BLOCK7 = 7
# @@
#  @@
BLOCKS = BLOCK1, BLOCK2, BLOCK3, BLOCK4, BLOCK5, BLOCK6, BLOCK7

# block heights and widths at first rotation postition
BLOCK_HEIGHTS = 0, 2, 1, 2, 2, 2, 2, 2
BLOCK_WIDTHS  = 0, 2, 4, 3, 3, 3, 3, 3

BLOCK1_ROTS = (
	((0,0), (1,0), (0,1), (1,1)),
	((0,0), (1,0), (0,1), (1,1)),
	((0,0), (1,0), (0,1), (1,1)),
	((0,0), (1,0), (0,1), (1,1))
				)

BLOCK2_ROTS = (
	((0,0), (1,0), (2,0), (3,0)),
	((1,-2), (1,-1), (1,0), (1,1)),
	((0,-1), (1,-1), (2,-1), (3,-1)),
	((2,-2), (2,-1), (2,0), (2,1)),
				)

BLOCK3_ROTS = (
	((0,0), (0,1), (1,1), (2,1)),
	((1,0), (2,0), (1,1), (1,2)),
	((0,1), (1,1), (2,1), (2,2)),
	((1,0), (1,1), (1,2), (0,2)),
				)
BLOCK4_ROTS = (
	((0,1), (1,1), (2,1), (2,0)),
	((1,0), (1,1), (1,2), (2,2)),
	((0,1), (1,1), (2,1), (0,2)),
	((1,0), (1,1), (1,2), (0,0)),
				)
BLOCK5_ROTS = (
	((0,1), (1,1), (2,1), (1,0)),
	((1,0), (1,1), (1,2), (2,1)),
	((0,1), (1,1), (2,1), (1,2)),
	((1,0), (1,1), (1,2), (0,1)),
				)
BLOCK6_ROTS = (
	((0,1), (1,1), (1,0), (2,0)),
	((1,0), (1,1), (2,1), (2,2)),
	((0,2), (1,2), (1,1), (2,1)),
	((0,0), (0,1), (1,1), (1,2)),
				)
BLOCK7_ROTS = (
	((0,0), (1,0), (1,1), (2,1)),
	((2,0), (2,1), (1,1), (1,2)),
	((0,1), (1,1), (1,2), (2,2)),
	((1,0), (1,1), (0,1), (0,2)),
				)

BLOCKS_ROTS = (((),), BLOCK1_ROTS, BLOCK2_ROTS, BLOCK3_ROTS,
	BLOCK4_ROTS, BLOCK5_ROTS, BLOCK6_ROTS, BLOCK7_ROTS)

# blocks' colors
BLOCK_COLORS = (
	0x00141414,
	0x00ff0000,
	(0, 255, 0),
	(0, 0, 255),
	(255, 255, 0),
	(255, 0, 255),
	(0, 255, 255),
	(255, 255, 255)
	)

GAME, GAME_OVER, PAUSE = 0, 1, 2
FONT_FILE = "BebasNeue-Regular.ttf"

class Pause:
	
	def __init__(self, scrn, clock):
		self.scrn = scrn
		self.scrn_w = self.scrn.get_width()
		self.scrn_h = self.scrn.get_height()
		self.clock = clock

		self.f_color    = 255, 255, 255
		self.bg_color   =   0,   0,   0
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
		pg.display.set_caption("Pause")
		self.in_loop = True
		self.time_count = pg.time.get_ticks()

		while self.in_loop:
			self.handle_events()
			self.update_state()
			self.render()
			self.clock.tick(60)
		else:
			return self.return_vals

	def render(self):

		self.scrn.fill(self.bg_color)

		self.scrn.blit(self.pause_label_sfc,
			(self.scrn_w*0.5 - self.pause_label_w*0.5, self.scrn_h*0.1))

		pg.draw.line(self.scrn,
			self.line_color,
			(self.scrn_w*0.5, self.scrn_h*0.1 + self.pause_label_h), # start point
			(self.scrn_w*0.5, self.scrn_h*0.9), width=2
			)

		n_items = 3
		items = zip(
			self.left_side_keys_sfc,
			self.left_side_labels_sfc,
			range(n_items))
		for ksfc, lblsfc, i in items:
			kw = ksfc.get_width()
			kh = ksfc.get_height()
			dy = (self.scrn_h*0.8 - self.pause_label_h) / (n_items + 1)
			self.scrn.blit(ksfc,
				(self.scrn_w*0.1 - kw*0.5, self.scrn_h*0.2 + self.pause_label_h + i*dy))
			self.scrn.blit(lblsfc,
				(self.scrn_w*0.2 + kw, self.scrn_h*0.2 + self.pause_label_h + i*dy))
			pg.draw.rect(
				self.scrn, self.rect_color,
				pg.Rect(self.scrn_w*0.1 - kh*0.5, self.scrn_h*0.2 + self.pause_label_h + i*dy, kh, kh), width=self.ln_w
				)

		dy = (self.scrn_h*0.8 - self.pause_label_h) / (n_items + 1)

		n_items = 3
		items = zip(
			self.right_side_keys_sfc,
			self.right_side_labels_sfc,
			range(n_items))
		for k_sfcs, lbl_sfcs, i in items:
			n_subitems = 3
			subitems = zip(k_sfcs, lbl_sfcs, range(n_subitems))
			for ksfc, lblsfc, j in subitems:
				kh = ksfc.get_height()
				kw = ksfc.get_width()
				self.scrn.blit(ksfc,
					(self.scrn_w/8 * (5+j) - kw*0.5, self.scrn_h*0.1 + self.pause_label_h + (i+1)*dy - kh))
				self.scrn.blit(lblsfc,
					(self.scrn_w/8 * (5+j) - lblsfc.get_width()*0.5, self.scrn_h*0.1 + self.pause_label_h + (i+1)*dy))
				if self.right_side_keys[i][j]:
					pg.draw.rect(self.scrn, self.rect_color,
						pg.Rect(self.scrn_w/8 * (5+j) - kh*0.5, self.scrn_h*0.1 + self.pause_label_h + (i+1)*dy - kh, kh, kh), width=self.ln_w)

		n_items = 2
		items = zip(
			self.right_side_keys2_sfc,
			self.right_side_labels2_sfc,
			range(n_items))
		for ksfc, lblsfc, i in items:
			kw = ksfc.get_width()
			kh = ksfc.get_height()
			self.scrn.blit(ksfc,
				(self.scrn_w/6 * (4+i) - kw*0.5, self.scrn_h*0.15 + self.pause_label_h + 3*dy - kh))
			self.scrn.blit(lblsfc,
				(self.scrn_w/6 * (4+i) - lblsfc.get_width()*0.5, self.scrn_h*0.15 + self.pause_label_h + 3*dy))
			rw = max(kh,kw)
			pg.draw.rect(self.scrn, self.rect_color,
						pg.Rect(self.scrn_w/6 * (4+i) - max(kh,kw)*0.5, self.scrn_h*0.15 + self.pause_label_h + 3*dy - kh, rw, kh), width=self.ln_w)

		pg.display.flip()

	def update_scales(self):

		self.scrn_w = self.scrn.get_width()
		self.scrn_h = self.scrn.get_height()
		ref = min(self.scrn_w, self.scrn_h)
		self.font1_sz = ref//6
		self.font2_sz = ref//10
		self.font3_sz = ref//15
		self.font4_sz = ref//17
		self.ln_w = max(1, ref//150)

		self.font1 = pg.font.Font(FONT_FILE, self.font1_sz)
		self.font2 = pg.font.Font(FONT_FILE, self.font2_sz)
		self.font3 = pg.font.Font(FONT_FILE, self.font3_sz)
		self.font4 = pg.font.Font(FONT_FILE, self.font4_sz)

		self.pause_label_sfc = self.font1.render(
			"Pause", True, self.f_color, self.bg_color)
		self.pause_label_w = self.pause_label_sfc.get_width()
		self.pause_label_h = self.pause_label_sfc.get_height()

		self.left_side_keys_sfc = tuple(map(
			lambda k: self.font2.render(k, True, self.f_color, self.bg_color), self.left_side_keys))
		self.left_side_labels_sfc = tuple(map(
			lambda lbl: self.font2.render(lbl, True, self.f_color, self.bg_color), self.left_side_labels))

		self.right_side_keys_sfc = tuple(map(
			lambda ks: tuple(map(lambda k: self.font3.render(k, True, self.f_color, self.bg_color), ks)), self.right_side_keys))
		self.right_side_labels_sfc = tuple(map(
			lambda lbls: tuple(map(lambda lbl: self.font3.render(lbl, True, self.f_color, self.bg_color), lbls)), self.right_side_labels))

		self.right_side_keys2_sfc = tuple(map(lambda k: self.font3.render(k, True, self.f_color, self.bg_color), self.right_side_keys2))
		self.right_side_labels2_sfc = tuple(map(lambda lbl: self.font4.render(lbl, True, self.f_color, self.bg_color), self.right_side_labels2))

	def handle_events(self):
		for ev in pg.event.get():

			if ev.type == pg.QUIT:
				exit(0)

			elif ev.type == pg.KEYDOWN:

				if ev.key == pg.K_p:
					self.in_loop = False
					self.return_vals = GAME, {"init new game": False}

				elif ev.key == pg.K_r:
					self.in_loop = False
					self.return_vals = GAME, {"init new game": True}

				elif ev.key == pg.K_q:
					exit(0)

			elif ev.type == pg.VIDEORESIZE:
				self.scrn_w, self.scrn_h = ev.size
				self.update_scales()

	def update_state(self):
		pass

	def pass_kwargs(self, **kwargs):
		pass

class Game:
	
	def __init__(self, scrn, clock):
		self.scrn = scrn
		self.scrn_w = scrn.get_width()
		self.scrn_h = scrn.get_height()
		self.clock = clock

		# variables score and line points
		self.score = 0
		self.lines = 0

		self.time_count = 0
		self.move_block_interval = 900 # milliseconds
		self.dec_interval = 20 # milliseconds

		self.panel_color =  60,  60,  60
		self.bg_color 	 =   0,   0,   0
		self.f_color 	 = 255, 255, 255
		self.grid_color  =  50,  50,  50

		# variables related with game working
		self.board = ndarray((BOARD_WITDH, BOARD_HEIGHT), dtype=int)
		self.new_game = True
		self.init_new_game()

	def start_loop(self):
		if self.new_game:
			self.init_new_game()
			self.new_game = False

		self.update_scales()
		pg.display.set_caption("Tetris")
		self.in_loop = True
		self.time_count = pg.time.get_ticks()

		while self.in_loop:
			self.handle_events()
			self.update_state()
			self.render()
			self.clock.tick(60)
		else:
			return self.return_vals

	def init_new_game(self):

		self.board[:,:] = NO_BLOCK
		
		self.hld_block_t = NO_BLOCK
		self.nxt_block_t = choice(BLOCKS)
		self.fll_block_t = choice(BLOCKS)
		self.init_fll_block_pos()
		self.interchangeable = True

		self.score = 0
		self.lines = 0

	def init_fll_block_pos(self):
		self.fll_block_y_pos = 0
		self.fll_block_x_pos = BOARD_WITDH//2 - BLOCK_WIDTHS[self.fll_block_t]//2
		self.fll_block_r_pos = 0

	def render(self):
		# ------------------------------
		# rendering the left screen side
		# ------------------------------
		self.scrn.fill(self.bg_color,
			pg.Rect(0, 0, self.scrn_w/2, self.scrn_h))

		# rendering board blocks
		for x in range(BOARD_WITDH):
			for y in range(BOARD_HEIGHT):
				pg.draw.rect(self.scrn,
					BLOCK_COLORS[self.board[x, y]],
					pg.Rect(
						self.block_sz*x + self.dx_brd,
						self.block_sz*y + self.dy_brd,
						self.block_sz, self.block_sz
						))
		# rendering falling block
		for x, y in BLOCKS_ROTS[self.fll_block_t][self.fll_block_r_pos]:
			pg.draw.rect( self.scrn, BLOCK_COLORS[self.fll_block_t],
				pg.Rect(
					self.block_sz * (self.fll_block_x_pos + x) + self.dx_brd,
					self.block_sz * (self.fll_block_y_pos + y) + self.dy_brd,
					self.block_sz, self.block_sz))
		
		# rendering board grid
		for x in range(BOARD_WITDH + 1): # vertical lines
			pg.draw.line(self.scrn, self.grid_color,
				(self.dx_brd + x * self.block_sz, self.dy_brd), # start point
				(self.dx_brd + x * self.block_sz, self.scrn_h - self.dy_brd), # end point
				width=2)
		for y in range(BOARD_HEIGHT + 1): # horizontal lines
			pg.draw.line(self.scrn, self.grid_color,
				(self.dx_brd, self.dy_brd + y * self.block_sz), # start point
				(self.scrn_w//2 - self.dx_brd, self.dy_brd + y * self.block_sz), # end point
				width=2)

		# -------------------------------
		# rendering the right screen side
		# -------------------------------
		self.scrn.fill(self.panel_color, pg.Rect(self.scrn_w/2, 0, self.scrn_w/2, self.scrn_h))

		# rendering score label
		self.scrn.blit(self.score_label_sfc, (self.scrn_w * 0.625 - self.score_label_w/2, self.scrn_h/4 - self.score_label_h))

		# rendering score points
		self.scrn.blit(self.score_points_sfc, (self.scrn_w * 0.625 - self.score_points_w/2, self.scrn_h/4))

		# rendering lines label
		self.scrn.blit(self.lines_label_sfc, (self.scrn_w * 0.875 - self.lines_label_w/2, self.scrn_h/4 - self.lines_label_h))

		# rendering lines points
		self.scrn.blit(self.lines_points_sfc, (self.scrn_w * 0.875 - self.lines_points_w/2, self.scrn_h/4))

		# rendering next block label
		self.scrn.blit(self.next_label_sfc, (self.scrn_w * 0.625 - self.next_label_w/2, self.scrn_h/2))

		# rendering next block background
		pg.draw.rect(self.scrn, BLOCK_COLORS[NO_BLOCK],
			pg.Rect(
				self.scrn_w * 0.625 - self.block_sz * 2.25,  self.scrn_h/2 + self.next_label_h,
				self.block_sz * 4.5, self.block_sz * 4.5))
		# rendering next block
		for x,y in BLOCKS_ROTS[self.nxt_block_t][0]:
		 	pg.draw.rect(self.scrn, BLOCK_COLORS[self.nxt_block_t],
	 		(self.scrn_w * 0.625 + self.block_sz * (-BLOCK_WIDTHS[self.nxt_block_t]/2 + x),
		 		self.scrn_h/2 + self.next_label_h + self.block_sz * (2.25 + y - BLOCK_HEIGHTS[self.nxt_block_t]/2),
		 		self.block_sz, self.block_sz))


		# rendering hold block label
		self.scrn.blit(self.hold_label_sfc, (self.scrn_w * 0.875 - self.hold_label_w/2, self.scrn_h/2))

		# rendering hold_block background
		pg.draw.rect(self.scrn, BLOCK_COLORS[NO_BLOCK],
			pg.Rect(
				self.scrn_w * 0.875 - self.block_sz * 2.25,  self.scrn_h/2 + self.next_label_h,
				self.block_sz * 4.5, self.block_sz * 4.5))
		# rendering hold block
		for x,y in BLOCKS_ROTS[self.hld_block_t][0]:
		 	pg.draw.rect(self.scrn, BLOCK_COLORS[self.hld_block_t],
	 		(self.scrn_w * 0.875 + self.block_sz * (-BLOCK_WIDTHS[self.hld_block_t]/2 + x),
		 		self.scrn_h/2 + self.hold_label_h + self.block_sz * (2.25 + y - BLOCK_HEIGHTS[self.hld_block_t]/2),
		 		self.block_sz, self.block_sz))

		pg.display.flip()

	def update_scales(self):

		self.scrn_w = self.scrn.get_width()
		self.scrn_h = self.scrn.get_height()
		ref = min(self.scrn_w, self.scrn_h)
		self.block_sz = ref/(BOARD_WITDH * 2)
		self.font1_sz = ref//10

		self.dx_brd = (self.scrn_w/2 - self.block_sz * BOARD_WITDH)/2
		self.dy_brd = (self.scrn_h - self.block_sz * BOARD_HEIGHT)/2

		self.font1 = pg.font.Font(FONT_FILE, self.font1_sz)

		self.score_label_sfc = self.font1.render(
			"Score", True, self.f_color, self.panel_color)
		self.score_label_w = self.score_label_sfc.get_width()
		self.score_label_h = self.score_label_sfc.get_height()

		self.lines_label_sfc = self.font1.render(
			"Lines", True, self.f_color, self.panel_color)
		self.lines_label_w = self.lines_label_sfc.get_width()
		self.lines_label_h = self.lines_label_sfc.get_height()

		self.next_label_sfc = self.font1.render(
			"Next", True, self.f_color, self.panel_color)
		self.next_label_w = self.next_label_sfc.get_width()
		self.next_label_h = self.next_label_sfc.get_height()

		self.hold_label_sfc = self.font1.render(
			"Hold", True, self.f_color, self.panel_color)
		self.hold_label_w = self.hold_label_sfc.get_width()
		self.hold_label_h = self.hold_label_sfc.get_height()

		self.update_score_points_sfc()
		self.update_lines_points_sfc()

	def update_score_points_sfc(self):
		text = f'{self.score}'
		self.score_points_sfc = self.font1.render(
			text, True, self.f_color, self.panel_color)
		self.score_points_w = self.score_points_sfc.get_width()
		self.score_points_h = self.score_points_sfc.get_height()

	def update_lines_points_sfc(self):
		text = f'{self.lines}'
		self.lines_points_sfc = self.font1.render(
			text, True, self.f_color, self.panel_color)
		self.lines_points_w = self.lines_points_sfc.get_width()
		self.lines_points_h = self.lines_points_sfc.get_height()

	def handle_events(self):
		for ev in pg.event.get():
			if ev.type == pg.QUIT:
				exit(0)

			elif ev.type == pg.KEYDOWN:
				if ev.key == pg.K_p:
					self.in_loop = False
					self.return_vals = PAUSE, {}
				elif ev.key == pg.K_LEFT:
					next_x_pos = self.fll_block_x_pos - 1
					if self.can_move_falling_block_to(
						next_x_pos,self.fll_block_y_pos,
						self.fll_block_r_pos,self.fll_block_t,
						lambda x, y: x < 0 or self.board[x,y]):
						self.fll_block_x_pos = next_x_pos
				elif ev.key == pg.K_RIGHT:
					next_x_pos = self.fll_block_x_pos + 1
					if self.can_move_falling_block_to(
						next_x_pos, self.fll_block_y_pos,
						self.fll_block_r_pos, self.fll_block_t,
						lambda x, y: x >= BOARD_WITDH or self.board[x,y]):
						self.fll_block_x_pos = next_x_pos
				elif ev.key == pg.K_SPACE:
					# it makes falling block come down until
						# the block touch floor
					while self.move_fll_block_down():
						pass
				elif ev.key == pg.K_DOWN:
					self.move_fll_block_down()
				elif ev.key == pg.K_UP:
					next_rot = (self.fll_block_r_pos + 1) % 4
					if self.can_move_falling_block_to(
						self.fll_block_x_pos, self.fll_block_y_pos,
						next_rot, self.fll_block_t,
						lambda x, y: (not 0 <= x < BOARD_WITDH) or
									(not 0 <= y < BOARD_HEIGHT) or
									self.board[x, y]):
							self.fll_block_r_pos = next_rot
				elif ev.key == pg.K_c:
					if self.interchange_block:
						# check wherther there is no holded block
						if self.hld_block_t:
							self.init_fll_block_pos()
							self.fll_block_t, self.hld_block_t = self.hld_block_t, self.fll_block_t
						else:
							self.hld_block_t = self.fll_block_t
							self.generate_falling_block()
						self.interchange_block = False
				elif ev.key == pg.K_q:
					exit(0)

			elif ev.type == pg.VIDEORESIZE:
				self.scrn_w, self.scrn_h = ev.size
				self.update_scales()
			else:
				pass

	def generate_falling_block(self):
		self.fll_block_t = self.nxt_block_t
		# it generates a new next block
		self.nxt_block_t = choice(BLOCKS)
		self.init_fll_block_pos()
		self.check_game_over()

	def check_game_over(self):
		# this means if the new falling block
		# (already initialized) cannot be placed (self.can_move_falling_block_to returns False)
		# it's because board is overloaded.
		# in other words: game over
		game_over = not self.can_move_falling_block_to(
			self.fll_block_x_pos, self.fll_block_y_pos,
			self.fll_block_r_pos, self.fll_block_t,
			lambda x, y: self.board[x, y])
		if game_over:
			self.in_loop = False
			self.return_vals = GAME_OVER, {'score':self.score, 'lines':self.lines}
		else:
			self.time_count = pg.time.get_ticks()
			self.interchange_block = True

	def update_state(self):
		# updating game state
		if pg.time.get_ticks() - self.time_count >= self.move_block_interval:
			self.time_count = pg.time.get_ticks()
			self.move_fll_block_down()

	def move_fll_block_down(self):
		'''
		move falling block one position down
		also check if the falling block has
		touched floor or other block bellow
		'''
		nxt_y_pos = self.fll_block_y_pos + 1
		f = lambda x, y: y == BOARD_HEIGHT or self.board[x,y]

		if self.can_move_falling_block_to(self.fll_block_x_pos, nxt_y_pos,self.fll_block_r_pos, self.fll_block_t,f):
			self.fll_block_y_pos = nxt_y_pos
			return True
		else:
			self.fix_fll_block()
			self.score += 1
			self.update_score_points_sfc()
			self.check_full_filled_rows()
			self.generate_falling_block()
			return False
		
	def fix_fll_block(self):
		'''
		fix falling block into the board
		also increments score
		'''
		for x,y in BLOCKS_ROTS[self.fll_block_t][self.fll_block_r_pos]:
			self.board[self.fll_block_x_pos+x, self.fll_block_y_pos+y] = self.fll_block_t

	def check_full_filled_rows(self):
		y = BOARD_HEIGHT-1
		while y > -1:
			for x in range(BOARD_WITDH):
				if not self.board[x, y]:
					y -= 1
					break
			else:
				for i in range(BOARD_WITDH):
					for j in range(y-1,-1,-1):
						self.board[i,j+1] = self.board[i,j]
				self.score += BOARD_WITDH
				self.lines += 1
				self.update_score_points_sfc()
				self.update_lines_points_sfc()

				if self.lines % 5 == 0:
					# increases difficulty
					self.move_block_interval -= self.dec_interval

	def can_move_falling_block_to(self, x, y, r, bt, f):
		'''
		check if is allowed to move a block of type t with rotation state r
		to the given position x, y, by function f
		'''
		for i, j in BLOCKS_ROTS[bt][r]:
			if f(x+i, y+j):
				return False
		else:
			return True

	def pass_kwargs(self, **kwargs):
		if kwargs["init new game"]:
			self.new_game = True

class GameOver:
	
	def __init__(self, scrn, clock):
		# related variables with pygame
		self.scrn = scrn
		self.scrn_w = scrn.get_width()
		self.scrn_h = scrn.get_height()
		self.clock = clock

		# variables score and line points
		self.score = 0
		self.lines = 0

		self.time_count = 0
		self.bip_interval = 800 # milliseconds
		# it controls wherther "Press any Key" is displayed or not
		self.visible = True

		self.bg_color =   0,   0,   0
		self.f_color  = 255, 255, 255

	def start_loop(self):

		self.update_scales()
		pg.display.set_caption("Game Over")
		self.in_loop = True
		self.time_count = pg.time.get_ticks()

		while self.in_loop:
			self.handle_events()
			self.update_state()
			self.render()
			self.clock.tick(60)
		else:
			return self.return_vals

	def render(self):
		self.scrn.fill(self.bg_color)

		# rendering game over label
		self.scrn.blit(
			self.game_over_label_sfc,
			(self.scrn_w*0.5 - self.game_over_label_w*0.5,
			self.scrn_h*0.05)
			)

		# rendering score label and score points
		self.scrn.blit(
			self.score_label_sfc,
			(self.scrn_w*0.25 - self.score_label_w*0.5,
			self.scrn_h*0.5 - self.score_label_h*0.75)
			)

		self.scrn.blit(
			self.score_points_sfc,
			(self.scrn_w*0.25 - self.score_points_w*0.5,
			self.scrn_h*0.5 + self.score_label_h*0.25)
			)

		# rendering lines label and lines points
		self.scrn.blit(
			self.lines_label_sfc,
			(self.scrn_w*0.75 - self.lines_label_w*0.5,
			self.scrn_h*0.5 - self.lines_label_h*0.75)
			)

		self.scrn.blit(
			self.lines_points_sfc,
			(self.scrn_w*0.75 - self.lines_points_w*0.5,
			self.scrn_h*0.5 + self.lines_label_h*0.25)
			)

		# renderng "press any key to continue" label
		if self.visible:
			self.scrn.blit(
				self.press_label_sfc,
				(self.scrn_w*0.5 - self.press_label_w*0.5,
				self.scrn_h - self.press_label_h*1.5)
				)


		pg.display.flip()

	def update_scales(self):
		# this function update the dsplayed fonts sizes
		# when window is resized
		self.scrn_w = self.scrn.get_width()
		self.scrn_h = self.scrn.get_height()
		ref = min(self.scrn_h, self.scrn_w)
		font1_sz = ref // 5
		font2_sz = ref // 7
		font3_sz = ref // 9

		self.font1 = pg.font.Font(FONT_FILE, font1_sz)
		self.font2 = pg.font.Font(FONT_FILE, font2_sz)
		self.font3 = pg.font.Font(FONT_FILE, font3_sz)

		self.game_over_label_sfc = self.font1.render(
			"Game Over!", True, self.f_color, self.bg_color)
		self.game_over_label_w = self.game_over_label_sfc.get_width()
		self.game_over_label_h = self.game_over_label_sfc.get_height()

		self.score_label_sfc = self.font2.render(
			"Score", True, self.f_color, self.bg_color)
		self.score_label_w = self.score_label_sfc.get_width()
		self.score_label_h = self.score_label_sfc.get_height()

		self.lines_label_sfc = self.font2.render(
			"lines", True, self.f_color, self.bg_color)
		self.lines_label_w = self.lines_label_sfc.get_width()
		self.lines_label_h = self.lines_label_sfc.get_height()

		self.score_points_sfc = self.font2.render(
			f"{self.score}", True, self.f_color, self.bg_color)
		self.score_points_w = self.score_points_sfc.get_width()
		self.score_points_h = self.score_points_sfc.get_height()

		self.lines_points_sfc = self.font2.render(
			f"{self.lines}", True, self.f_color, self.bg_color)
		self.lines_points_w = self.lines_points_sfc.get_width()
		self.lines_points_h = self.lines_points_sfc.get_height()

		self.press_label_sfc = self.font3.render(
			"Press any key to continue", True, self.f_color, self.bg_color)
		self.press_label_w = self.press_label_sfc.get_width()
		self.press_label_h = self.press_label_sfc.get_height()

	def handle_events(self):
		for ev in pg.event.get():

			if ev.type == pg.QUIT:
				exit(0)

			if ev.type == pg.KEYDOWN:

				if ev.key == pg.K_q:
					exit(0)
				else:
					self.in_loop = False
					self.return_vals = GAME, {"init new game": True}

			if ev.type == pg.VIDEORESIZE:
				self.scrn_w, self.scrn_h = ev.size
				self.update_scales()
			else:
				pass

	def update_state(self):
		if pg.time.get_ticks() - self.time_count >= self.bip_interval:
			self.visible = not self.visible
			self.time_count = pg.time.get_ticks()

	def pass_kwargs(self, **kwargs):
		# get score and lines contained in kwargs
		self.score = kwargs['score']
		self.lines = kwargs['lines']

class Main:

	def __init__(self):
		self.scrn = pg.display.set_mode((600, 500), pg.RESIZABLE)
		self.clock = pg.time.Clock()
		self.loops = (
			Game(self.scrn, self.clock),
			GameOver(self.scrn, self.clock), 
			Pause(self.scrn, self.clock)
			)

	def run(self):
		self.current_loop = self.loops[GAME]
		while True:
			next_loop, kwargs = self.current_loop.start_loop()
			self.current_loop = self.loops[next_loop]
			self.current_loop.pass_kwargs(**kwargs)

if __name__ == '__main__':
	pg.init()
	atexit.register(pg.quit)
	m = Main()
	m.run()