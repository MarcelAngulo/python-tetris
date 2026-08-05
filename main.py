#!/usr/bin/env python3

import pygame
import sys
import argparse

from src.screens import GameOver, Game, Pause
from src.constants import *
from src.tetrisboard import TetrisBoard
from src.audio import AudioManager

from dataclasses import dataclass

@dataclass
class GlobalConfig:
    window: pygame.Surface
    clock: pygame.Time.Clock
    audio: AudioManager
    blink_event: int
    state: int
    tetris: TetrisBoard

def positive_int(s:str) -> int:
    i = int(s)
    if i <= 0:
        raise argparse.ArgumentTypeError('Integer must be positive (>0)')
    else:
        return i

def main():

    # Argument parser
    parser = argparse.ArgumentParser(
        description="Little pure Python implementation of tetris game using pygame-ce.")
    parser.add_argument('--width', '-w', type=positive_int, default=10,
        help="The width of the board. Default is 10")
    parser.add_argument('--height', '-H', type=positive_int, default=20,
        help="The height of the board. Default is 20")
    parser.add_argument('--difficulty', '-d', type=positive_int, default=1,
        help="The difficulty of the game, starting with 1 (the easiest) to larger numbers. Default is 1")
    args = parser.parse_args()

    pygame.init()
    pygame.mixer.init(
            frequency=44100,size=-16,
            channels=2,buffer=512)


    config = GlobalConfig(
            pygame.display.set_mode((600, 500), pygame.RESIZABLE),
            pygame.time.Clock(), AudioManager(), 
            pygame.event.custom_type(), STATE_GAME,
            TetrisBoard(args.width, args.height, args.difficulty)
            )

    running = True
    # Loop which alternates between screens
    while running:
        if config.state == STATE_GAME:
            Game(config).run_loop()
        elif config.state == STATE_GAMEOVER:
            GameOver(config).run_loop()
        elif config.state == STATE_PAUSE:
            Pause(config).run_loop()
        elif config.state == STATE_QUIT:
            running = False

    pygame.mixer.quit()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()

