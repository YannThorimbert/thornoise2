# (c) Yann Thorimbert 2017
"""This example module shows how to generate fast 2D terrain or noise with
numpy.

Since it aims at performance, the code is more complex that strictly necessary for
understanding the noise. One should use the pure python version if the performance
is not crucial.

usage : run the following command from the parent folder of the package:
'python -m thornoise2.examples.example_numpy'
"""

# Faire marcher seed. Note sur prng. typing
# vendredi 14h45 rue de lyon

import numpy as np

from ..numpygen import colorscale #type:ignore
from ..numpygen import noisegen as ng

if __name__ == "__main__":
    ##### First, choose the type of noise #######################################
    c = ng.ZeroGradient() #fastest !
    # c = cache.NoiseCache() #prettiest ?
    # c = ng.Perlin() #most famous ?
    ##### Now, customize the params #############################################
    # c.SEED = 18
    # c.DEPTH = 2
    # c.MIN_N = 4
    # c.S = 12
    # c.DOM_DIVIDER = 2 #if you modify this, try adjusting also S and MIN_N
    # c.H_DIVIDER = 1.7
    # c.WORLD_SIZE = (4,4) #size in number of chunks. The world is a torus.
    ##### Then build it and choose a colorscale (optional) ######################
    c.build()
    colormap = colorscale.SUMMER #How height is transformed into color
    init_chunk = (0,230) #any couple of positive integers
    chunk = np.array(init_chunk)%c.WORLD_SIZE #dont go further than world limit
    chunk = tuple(init_chunk)
    hmap = ng.generate_terrain(chunk, c) #generate actual data
    hmap = ng.normalize(hmap) #scales to [0,1] range
    # hmap = ng.theoretical_normalize(hmap, c) #scales to [0,1] range in a tileable way
    cmap = colormap.get(hmap) #array of colors
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
        pygame.init()
        screen = pygame.display.set_mode((c.S,c.S))
        surface = pygame.surfarray.make_surface(cmap) #convert to surface using cmap
        screen.blit(surface,(0,0)) #draw on screen
        pygame.display.flip() #refresh screen
        #
        looping = True
        while looping:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    looping = False
        pygame.quit()
