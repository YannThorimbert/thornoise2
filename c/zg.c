/*(C) 2016 Yann Thorimbert
 *
 *  This code generates a coherent noise that can be used for terrain generation,
 *  by applying the zero-gradient D2M1N3 method presented in my article.
 *
 *
 *  A Makefile is provided with this file.
 *
 * */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <stdbool.h>
#include <string.h>

typedef float T;
const int S = 256; //resolution in pixels

#include "imagewriter.h"

// Writes terrain height in array <terrain>, with boundary condition <h>, using <nOctaves> octaves
void zgTerrain(int nOctaves, T** h, T** terrain)
{
    T x2, y2, smoothx, smoothy;
    T xRel = (T)0;
    T xRelm1 = xRel - (T)1;
    T yRel = (T)0;
    T yRelm1 = yRel - (T)1;
    T deltaX, deltaY, A, dh;
    T delta;
    T h00,h01,h10,h11;
    int res = S;
    int idx, idy, idx1, idy1; //index of gradient values
    bool changeCell = true; //indicates when polynomial coeffs have to be recomputed
    T amplitude = (T)1;
    for(int i=0;i<nOctaves;i++)
    {
        delta = (T)1/(T)res;
        xRel = (T)0;
        idx = 0;
        idx1 = 0;
        for(int x=0;x<S;x++)
        {
            idy = 0;
            idy1 = 0;
            yRel = (T)0;
            x2 = xRel*xRel;
            smoothx = (T)3*x2 - (T)2*xRel*x2;
            if (x%res == 0){
                idx = idx1;
                idx1 += res-1;
                changeCell = true;
            }
            for(int y=0;y<S;y++)
            {
                y2 = yRel*yRel;
                smoothy = (T)3*y2 - (T)2*yRel*y2;
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
                //
                dh = h00 + smoothx*deltaX + smoothy*deltaY + A*(xRel*yRel - smoothx*yRel - smoothy*xRel);
                terrain[x][y] += amplitude*dh;
                //
                yRel += delta;
                if(yRel >= (T)1)
                    yRel = (T)0;
            }//for y
            xRel += delta;
            if(xRel >= (T)1)
                xRel = (T)0;
        }// for x
    res /= 2;
    amplitude /= (T)2;
    }// for octave
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
    int seed = 10; //choose an arbitrary seed;
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

    const int nOctaves = 8; //number of octaves wanted

    if(nOctaves > MAX_OCTAVES)
    {
        printf("nOctaves is too high for this resolution");
        exit(1);
    }

    //generate terrain
    zgTerrain(nOctaves,h,terrain);

    //write an image
    writeToBmp(terrain);

    free(h[0]);
    free(h);

    free(terrain[0]);
    free(terrain);

    return 0;
}