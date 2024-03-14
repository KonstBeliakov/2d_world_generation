import pygame
from random import randrange

WORLD_SEED = randrange(10 ** 9)
WORLD_FOLDER_NAME = f'world{WORLD_SEED}'

# textures

textures_files = ['dirt.png', 'sand.png', 'grass.png', 'stone.png', None, 'depth_stone.png', 'log.png', 'leaves.png',
                  'none.png', 'iron_ore.png', 'coal_ore.png', 'depth_coal_ore.png', 'depth_iron_ore.png',
                  'grass_block.png', 'dense_depth_stone.png', 'reddish_stone.png', 'hell_stone.png',
                  'magma.png', 'hell_star_ore.png', 'rich_hell_star_ore.png', 'poor_hell_star_ore.png']

textures = [pygame.image.load(f'textures/{file}') if file else None for file in textures_files]

# drawing settings

BLOCK_SIZE = 16
CHUNK_SIZE = 16
LOAD_DISTANSE = 6
GENERATION_DISTANSE = 9
DRAW_DISTANSE_X = 3
DRAW_DISTANSE_Y = 2
SCREEN_SIZE = (1200, 800)
SCREEN_SENTER = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)

# world settings
DEPTH_STONE_LEVEL = 48
DEPTH_STONE_PROBABILITY = [10, 15, 20, 25, 40, 60, 75, 80, 85, 90]
REDDISH_STONE_LEVEL = 100
REDDISH_STONE_PROBABILITY = [10, 15, 20, 25, 40, 60, 75, 80, 85, 90]
HELL_STONE_LEVEL = 120
HELL_STONE_PROBABILITY = [10, 15, 20, 25, 40, 60, 75, 80, 85, 90]

# block types
DIRT = 0
SAND = 1
GRASS = 2
STONE = 3
AIR = 4
DEPTH_STONE = 5
LOG = 6
LEAVES = 7
NONE = 8
IRON_ORE = 9
COAL_ORE = 10
DEPTH_COAL_ORE = 11
DEPTH_IRON_ORE = 12
GRASS_BLOCK = 13
DENSE_DEPTH_STONE = 14
REDDISH_STONE = 15
HELL_STONE = 16
MAGMA = 17
HELL_STAR_ORE = 18
RICH_HELL_STAR_ORE = 19
POOR_HELL_STAR_ORE = 20