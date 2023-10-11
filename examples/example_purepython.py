# (c) Yann Thorimbert 2017
"""This example module shows how to generate 2D terrain or noise with no dependencies other than built-in modules.

usage : run the following command from the parent folder of the package:
'python -m thornoise2.examples.example_purepython'
"""
import random
from ..purepython import noisegen as ng

if __name__ == "__main__":
    ######## Define a colorscale #######################################################
    summer =  ng.ColorScale([  [(0,0,0), (0,0,100), 0.],            #0. deep
                         [(0,0,100), (0,30,255), 0.52],             #1. shallow
                         [(0,30,255), (137, 131, 200), 0.597],      #2. sand
                         [(137, 131, 200), (237, 201, 175), 0.6],   #3. sand
                         [(237, 201, 175), (50,85,10), 0.605],      #4. sand
                         [(50,85,10), (50,180,50), 0.78],           #5. forest
                         [(50,180,50),(150,180,150), 0.85],
                         [(150,180,150), (255,255,255), 1.000001],    #6. snow
                         [(255,255,255), (255,255,255), 10.]],      #7. snow
                         minval = -10.)
    ######## We generate the actual terrain or noise (here we use all arguments for demo) ####
    res = 256
    terrain = ng.generate_terrain(  size=res, #Number of cells of 1 chunk (resolution of generated terrain)
                                    n_octaves=8, #depth or number of octaves (level of detail)
                                    chunk=(0,0), # chunk that is generated (NB : chunks are tilables)
                                    #NB2 : chunk is also used as a seed here
                                    persistance=2.) #parameter (play with it)
    ng.normalize(terrain)
    ##### Optional: visualization using pygame ##################################
    HAS_PYGAME = False
    try:
        import pygame
        from pygame import gfxdraw
        HAS_PYGAME = True
    except:
        print("Pygame not found on this distribution! However, "+\
              "you can use this module's 'generate_terrain' functions "+\
              "to generate terrain or noise in a 2D array.")
    if HAS_PYGAME:
        screen = pygame.display.set_mode((res,res))
        s = ng.build_surface(terrain, summer) #we build the surface
        screen.blit(s,(0,0))
        pygame.display.flip()
        #
        stay = True
        while stay:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    stay = False
        pygame.quit()

