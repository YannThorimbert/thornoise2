from typing import List, Tuple
color_t = Tuple[int,int,int]
import numpy as np

class ColorScale: #tricky structure to obtain fast colormap from heightmap

    def __init__(self,
                 colors:List[Tuple[str, color_t, color_t, float]],
                 minval=0.):
        self.colors = colors #list of tuples on the form [(name, color1, color2, height), ...]
        self.materials = {}
        for i in range(len(self.colors)):
            name = None
            if len(self.colors[i]) == 3:
                c1,c2,maxval = self.colors[i]
            else:
                name,c1,c2,maxval = self.colors[i]
            if i > 0:
                minval = self.colors[i-1][3]
            delta = maxval - minval
            self.colors[i] = [c1,c2,minval,maxval,delta]
            if name:
                self.materials[name] = self.colors[i]

    def get(self, data):
        w,h = data.shape
        tot = np.zeros((w,h,3),dtype=int)
        mask = np.zeros((w,h),dtype=bool)
        for c1, c2, m, M, delta in self.colors:
            new_mask = data<M
            current_mask = np.logical_and(new_mask,np.logical_not(mask))
            r = c1[0]
            g = c1[1]
            b = c1[2]
            if delta != 0:
                dmd = (data-m)/delta
                r += dmd*(c2[0]-c1[0])
                g += dmd*(c2[1]-c1[1])
                b += dmd*(c2[2]-c1[2])
            tot[current_mask,0] = r[current_mask]
            tot[current_mask,1] = g[current_mask]
            tot[current_mask,2] = b[current_mask]
            mask = np.logical_or(mask, new_mask)
        return tot
    
    def get_color_from_h(self, h):
        for c1, c2, m, M, delta in self.colors:
            if m <= h < M:
                r = c1[0]
                g = c1[1]
                b = c1[2]
                if delta != 0:
                    dmd = (h-m)/delta
                    r += dmd*(c2[0]-c1[0])
                    g += dmd*(c2[1]-c1[1])
                    b += dmd*(c2[2]-c1[2])
                return (r,g,b)
        return self.colors[-1][1]
        # return self.get(np.ones((1,1))*h)[0,0]

    def get_color_index_from_h(self, h):
        i = 0
        for c1, c2, m, M, delta in self.colors:
            if m <= h < M:
                return i
            i += 1
        return -1
    
    def get_material_from_h(self, h):
        for material, data in self.materials.items():
            c1, c2, m, M, delta = data
            if m <= h < M:
                return material
    
    def get_h_material_begin(self, material_name):
        c1, c2, m, M, delta = self.materials[material_name]
        return m
    
    def get_h_material_end(self, material_name):
        c1, c2, m, M, delta = self.materials[material_name]
        return M

##    def single_pixel(self, v):
##        tot = 0.
##        for c1, c2, m, M, delta in self.colors:
##            r = c1[0]
##            g = c1[1]
##            b = c1[2]
##            if delta != 0:
##                dmd = (data-m)/delta
##                r += dmd*(c2[0]-c1[0])
##                g += dmd*(c2[1]-c1[1])
##                b += dmd*(c2[2]-c1[2])
##            tot[current_mask,0] = r[current_mask]
##            tot[current_mask,1] = g[current_mask]
##            tot[current_mask,2] = b[current_mask]
##            mask = np.logical_or(mask, new_mask)
##        return tot



SUMMER =  ColorScale([   ["deep water", (0,0,0), (0,0,100), 0.],  
                         ["water", (0,0,100), (0,30,255), 0.52],
                         ["shallow water", (0,30,255), (137, 131, 200), 0.597],
                         ["wet sand", (137, 131, 200), (237, 201, 175), 0.6],
                         ["dry sand", (237, 201, 175), (50,85,10), 0.605],
                         ["grass", (50,85,10), (50,180,50), 0.78],
                         ["forest", (50,180,50),(150,180,150), 0.85],
                         ["snow", (150,180,150), (255,255,255), 1.000001],
                         ["white snow", (255,255,255), (255,255,255), 10.]],
                         minval = -10.)

# SUMMER =  ColorScale([   ["deep water", (0,0,0), (0,0,100), 0.],  
#                          ["water", (0,0,100), (0,30,255), 0.52],
#                          ["shallow water", (0,30,255), (65, 70, 225), 0.58],
#                          ["beach water", (65, 70, 225), (137, 131, 200), 0.597],
#                          ["wet sand", (137, 131, 200), (237, 201, 175), 0.6],
#                          ["dry sand", (237, 201, 175), (50,85,10), 0.605],
#                          ["grass", (50,85,10), (50,180,50), 0.78],
#                          ["forest", (50,180,50),(150,180,150), 0.85],
#                          ["snow", (150,180,150), (255,255,255), 1.000001],
#                          ["white snow", (255,255,255), (255,255,255), 10.]],
#                          minval = -10.)

SUMMERDRY =  ColorScale([  [(0,0,0), (0,0,100), 0.],                  #0. deep
                         [(0,0,100), (0,30,255), 0.4],             #1. shallow
                         [(0,30,255), (137, 131, 200), 0.42],      #2. sand
                         [(137, 131, 200), (237, 201, 175), 0.423],   #3. sand
                         [(237, 201, 175), (50,85,10), 0.428],      #4. sand
                         [(50,85,10), (50,180,50), 0.73],           #5. forest
                         [(50,180,50),(150,180,150), 0.8],
                         [(150,180,150), (255,255,255), 1.000001],    #6. snow
                         [(255,255,255), (255,255,255), 10.]],      #7. snow
                         minval = -10.)

SUMMERNOBEACH =  ColorScale([  [(0,0,0), (0,0,100), 0.],                  #0. deep
                         [(0,0,100), (0,30,255), 0.4],             #1. shallow
##                         [(0,30,255), (137, 131, 200), 0.42],      #2. sand
##                         [(137, 131, 200), (237, 201, 175), 0.423],   #3. sand
##                         [(237, 201, 175), (50,85,10), 0.428],      #4. sand
                         [(50,85,10), (50,180,50), 0.73],           #5. forest
                         [(50,180,50),(150,180,150), 0.8],
                         [(150,180,150), (255,255,255), 1.000001],    #6. snow
                         [(255,255,255), (255,255,255), 10.]],      #7. snow
                         minval = -10.)

SUMMERHOT =  ColorScale([[(0,0,0), (0,0,100), 0.],                  #0. deep
                         [(0,0,100), (0,30,255), 0.4],             #1. shallow
                         [(0,30,255), (137, 131, 200), 0.42],      #2. sand
                         [(137, 131, 200), (237, 201, 175), 0.423],   #3. sand
                         [(237, 201, 175), (50,85,10), 0.428],      #4. sand
                         [(50,85,10), (50,180,50), 0.73],           #5. forest
                         [(50,180,50),(150,180,150), 0.92],
                         [(150,180,150), (255,255,255), 1.000001],    #6. snow
                         [(255,255,255), (255,255,255), 10.]],      #7. snow
                         minval = -10.)

##SUMMERDRY =  ColorScale([[(0,0,255), (137, 131, 200), 0.],
##                         [(137, 131, 200), (237, 201, 175), 0.2],   #3. sand
##                         [(237, 201, 175), (50,85,10), 0.4],      #4. sand
##                         [(50,85,10), (50,180,50), 0.5],           #5. forest
##                         [(50,180,50),(150,180,150), 0.75],
##                         [(150,180,150), (255,255,255), 1.000001],    #6. snow
##                         [(255,255,255), (255,255,255), 10.]],      #7. snow
##                         minval = -10.)

a = (190,190,230)
b = (200,200,200)
c = (200,200,230)
WINTER =  ColorScale([  [(0,0,0), (0,0,100), 0.],
                         [(0,0,100), (30,30,150), 0.3],
                         [(30,30,150), (50,50,255), 0.52],
                         [(137,137,219), a, 0.603],
                         [b, c, 0.7],
                         [c, (255,255,255), 1.000001],
                         [(255,255,255), (255,255,255), 10.]],
                         minval = -10.)





BEACH = ColorScale(     [[(0,0,100), (0,100,255), 0.4],
                         [(0,100,255), (0,206,209), 0.5],
                         [(0,206,209), (0,85,0), 0.6],
                         [(0,85,0), (50,200,50), 0.75],
                         [(50,200,50), (255,255,255), 1.000001]])

BEACH2 = ColorScale(     [[(0,0,100), (0,100,255), 0.4],
                         [(0,100,255), (0,206,209), 0.5],
                         [(0,206,209), (0,85,0), 0.6],
                         [(0,85,0), (50,200,50), 0.75],
                         [(50,200,50), (255,255,255), 1.000001]])

SHARP = ColorScale([[(0,0,100), (0,100,255), 0.5],
                     [(0,85,0), (50,200,50), 0.75],
                     [(50,200,50), (255,255,255), 1.000001]])

SHARPDRY = ColorScale([[(0,0,100), (0,100,255), 0.41],
                     [(0,85,0), (50,200,50), 0.75],
                     [(50,200,50), (255,255,255), 1.000001]])

SHARPWET = ColorScale([[(0,0,100), (0,100,255), 0.6],
                     [(0,85,0), (50,200,50), 0.75],
                     [(50,200,50), (255,255,255), 1.000001]])

WET = ColorScale([[(0,0,100), (0,100,255), 0.8],
                     [(0,85,0), (50,200,50), 0.9],
                     [(50,200,50), (255,255,255), 1.000001]])

BLUE = ColorScale([[(255,255,255), (0,0,255), 1.]])
BLUE2 = ColorScale([[(0,0,255), (255,255,255), 1.001]])
BLACK = ColorScale([[(0,0,0), (255,255,255), 1.]])
WHITE = ColorScale([[(255,255,255), (0,0,0), 1.]])
GRADIENT = ColorScale([[(0,0,0), (0,0,255), 0.5],
                    [(0,0,255), (255,255,255), 1.]])

MARBLE = ColorScale([[(20,20,20), (220,245,220), 1.]])
WOOD = ColorScale([[(102, 51, 0), (182, 155, 76), 1.]])
STONE = WHITE = ColorScale([[(220,)*3, (0,0,0), 1.]])
##WOOD = ColorScale([[(86, 47, 14), (182, 155, 76), 0.5],
##                    [(182, 155, 76), (102, 51, 0), 1.]])


FIRE = ColorScale(  [[(0,0,0), (20,20,0), 0.4],
                     [(20,20,0), (55,55,0), 0.6],
                     [(55,55,0), (255,255,0), 0.7],
                     [(255,255,0), (255,255,255), 1.000001]])

FIRE2 = ColorScale(  [[(255,255,255), (255,255,155), 0.2],
                     [(255,255,155), (195,98,81), 0.3],
                     [(195,98,81), (182,84,71), 0.32],
                     [(182,84,71), (0,0,0), 0.5],
                     [(0,0,0),(0,0,0), 1.01]])

LIBNOISE = ColorScale(  [[(0,0,128), (0,0,255), -0.25/2+0.5],
                         [(0,0,255), (0,128,255), 0./2+0.5],
                         [(0,128,255), (240,240,64), 0.0625/2+0.5],
                         [(240,240,64), (32,160,0), 0.125/2+0.5],
                         [(32,160,0), (224,224,0), 0.375/2+0.5],
                         [(224,224,0), (128,128,128), 0.75/2+0.5],
                         [(128,128,128), (255,255,255), 1./2+0.5]])


def get_contour_colorscale(c1,c2,n):
    colors = []
    for v in np.linspace(0,1.000001,n)[1:]:
        colors.append([c1,c2,v])
    return ColorScale(colors)

CONTOUR_LINES = get_contour_colorscale((0,0,0),(255,255,255),10)
