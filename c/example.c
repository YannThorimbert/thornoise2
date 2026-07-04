/*(C) 2016 Yann Thorimbert
 *
 *  This code generates a coherent noise that can be used for terrain generation,
 *  by applying the zero-gradient D2M1N3 method presented in my article.
 *
 *
 *  A Makefile is provided with this file.
 *  Use : type make and then run ./example.exe
 * 
 *  Edit the parameters in the main to tweak the results ; the image resolution is declared just after headers
 *
 * */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <stdbool.h>
#include <string.h>

typedef float T;
const int S = 512; //resolution in pixels

#include "imagewriter.h"

// Writes terrain height in array <terrain>, with boundary condition <h>, using <nOctaves> octaves
void zgTerrain(int nOctaves, T persistance, T** h, T** terrain)
{
    T x2, y2, smoothx, smoothy;
    T xRel = (T)0;
    T yRel = (T)0;
    T deltaX, deltaY, A, dh;
    T delta;
    T h00,h01,h10,h11;
    int res = S;
    int idx, idy, idx1, idy1; //index of gradient values
    bool changeCell = true; //indicates when polynomial coeffs have to be recomputed
    T amplitude = (T)1;
    for(int i=0;i<nOctaves;i++) // octave loop
    {
        delta = (T)1/(T)res;
        xRel = (T)0;
        idx = 0;
        idx1 = 0;
        changeCell = true;
        for(int x=0;x<S;x++) // x-pixel loop
        {
            idy = 0;
            idy1 = 0;
            yRel = (T)0;
            x2 = xRel*xRel;
            smoothx = (T)3*x2 - (T)2*xRel*x2; // this is really just the smoothstep
            if (x%res == 0){ //we are on a grid point, so we need to update the cell
                idx = idx1;
                idx1 += res-1;
                changeCell = true;
            }
            for(int y=0;y<S;y++) // y-pixel loop
            {
                y2 = yRel*yRel;
                smoothy = (T)3*y2 - (T)2*yRel*y2; // this is really just the smoothstep
                if (y%res == 0){
                    idy = idy1;
                    idy1 += res-1;
                    changeCell = true;
                }
                //
                if (changeCell)
                {
                    h00 = h[idx][idy];
                    h01 = h[idx][idy1];
                    h10 = h[idx1][idy];
                    h11 = h[idx1][idy1];
                    deltaX = h10 - h00;
                    deltaY = h01 - h00;
                    A = deltaX - h11 + h01;
                    changeCell = false;
                }
                // Final increment according to the article
                dh = h00 + smoothx*deltaX + smoothy*deltaY + A*(xRel*yRel - smoothx*yRel - smoothy*xRel);
                terrain[x][y] += amplitude*dh;
                // handle y-periodicity (could use fmodf)
                yRel += delta;
                if(yRel >= (T)1)
                    yRel = (T)0;
            }//end for y
            // handle x-periodicity (could use fmodf)
            xRel += delta;
            if(xRel >= (T)1)
                xRel = (T)0;
        }// end for x
    res /= 2;
    amplitude /= (T)persistance;
    }// end for octave
}

T** buildArray(int N)
{
    T* f_memory  = (T*) malloc(N*N*sizeof(T));
    T** f  = (T**) malloc(N*sizeof(T*));

    for(int i=0; i<N; i++)
        f[i] = (T*) f_memory + i*N;

    return f;
}

T generateRandom()
{
    return (T)(-1) + (T)2*(T)rand() / (T)RAND_MAX ;
}

void fillRandom(T** a)
{
    for(int i=0;i<S;i++)
        for(int j=0;j<S;j++)
            a[i][j] = generateRandom();
}


int main()
{



    int seed = 14; //choose an arbitrary seed;
    srand(seed); //seeded
    //srand(time(NULL)); //randomized

    // Boundary conditions
    T** h = buildArray(S);
    fillRandom(h);

    // Actual terrain
    T** terrain = buildArray(S);
    for(int i=0;i<S;i++)
        for(int j=0;j<S;j++)
            terrain[i][j] = (T)0;

    const int MAX_OCTAVES = (int) (log(S)/log(2));
    const int N_OCTAVES = 8; //number of octaves wanted
    const T PERSISTANCE = 1.41; //Divider of the amplitude each octave

    if(N_OCTAVES > MAX_OCTAVES)
    {
        printf("nOctaves is too high for this resolution");
        exit(1);
    }

    //generate terrain
    zgTerrain(N_OCTAVES, PERSISTANCE, h, terrain);

    //write an image
    writeToBmp(terrain);

    free(h[0]);
    free(h);

    free(terrain[0]);
    free(terrain);

    return 0;
}
