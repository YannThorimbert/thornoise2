/*(C) 2016 Yann Thorimbert
 *
 *  This code generates and writes BMP image according to height map.
 *  It does not aims at performance !
 *
 * */


#ifndef IMAGEWRITER_H_INCLUDED
#define IMAGEWRITER_H_INCLUDED

#define min( a, b ) ( ((a) < (b)) ? (a) : (b) )


void normalizeArray(T **a)
{
    T minValue = 1;
    T maxValue = -1;
    for (int i=0;i<S;i++)
        for (int j=0;j<S;j++)
        {
            T value = a[i][j];
            if (value < minValue){minValue=value;}
            else if (value > maxValue){maxValue=value;}
        }
    T offset = minValue;
    T divider = maxValue-minValue;
    for (int i=0;i<S;i++)
        for (int j=0;j<S;j++)
            a[i][j] = (a[i][j]-offset)/divider;
}

void interpColor(const int c1[], const int c2[], T value, T h1, T h2, int c3[])
{
    T k = (T) (value - h1)/(h2-h1);
    for(int i=0;i<3;i++)
        c3[i] = c1[i] + k*(c2[i]-c1[i]);
}



void writeToBmp(T **terrain)
{
   unsigned char *img = NULL;
   int i,j;
   int x,y;
   int w,h;
   int padding, filesize, datasize;
   double v,r,g,b;
   char filename[50];
   FILE *f;
   unsigned char bmpfileheader[14] = {'B','M',0,0,0,0,0,0,0,0,54,0,0,0};
   unsigned char bmpinfoheader[40] = {40, 0, 0, 0,
                                       0, 0, 0, 0,
                                       0, 0, 0, 0,
                                       1, 0,24, 0};

   w = S; // width
   h = S; // height

   normalizeArray(terrain);

   padding = (4 - (w*3) % 4) % 4;

   datasize = (3*w + padding)*h;
   filesize = 54 + datasize;

   img = (unsigned char *)calloc(datasize, 1);

   const int deepwater[3] = {0,0,0};
   const int water[3] = {0,0,100}; T hwater = 0.;
   const int shallowWater[3] = {0,30,255}; T hshallow = 0.52;
   const int sand[3] = {137,131,200}; T hsand = 0.597;
   const int sand2[3] = {237,201,175}; T hsand2 = 0.6;
   const int jungle[3] = {50,85,10}; T hjungle = 0.605;
   const int forest[3] = {50,180,50}; T hforest = 0.78;
   const int heights[3] = {150,180,150}; T hheights = 0.85;
   const int snow[3] = {255,255,255}; T hsnow = 1.;

    for(i = 0; i < w; i++){
        for(j = 0; j < h; j++){

            v = terrain[j][i];
            int rgb[3];

// For terrain colorscale

            if (v<hshallow)
                interpColor(water,shallowWater,v,hwater,hshallow,rgb);
            else if (v<hsand)
                interpColor(shallowWater,sand,v,hshallow,hsand,rgb);
            else if (v<hsand2)
                interpColor(sand,sand2,v,hsand,hsand2,rgb);
            else if (v<hjungle)
                interpColor(sand2,jungle,v,hsand2,hjungle,rgb);
            else if (v<hforest)
                interpColor(jungle,forest,v,hjungle,hforest,rgb);
            else if (v<hheights)
                interpColor(forest,heights,v,hforest,hheights,rgb);
            else if (v<=hsnow)
                interpColor(heights,snow,v,hheights,hsnow,rgb);


// For black and white scale
//            r = v * 255; // Red channel
//            g = v * 255; // Green channel
//            b = v * 255; // Red channel
//
//            r = min(r, 255);
//            g = min(g, 255);
//            b = min(b, 255);

            x = i;
            y = (h -1) - j;

            img[(x + y*w)*3 + y*padding + 2] = (unsigned char)(rgb[0]);
            img[(x + y*w)*3 + y*padding + 1] = (unsigned char)(rgb[1]);
            img[(x + y*w)*3 + y*padding + 0] = (unsigned char)(rgb[2]);
     }
   }

   bmpfileheader[ 2] = (unsigned char)(filesize      );
   bmpfileheader[ 3] = (unsigned char)(filesize >>  8);
   bmpfileheader[ 4] = (unsigned char)(filesize >> 16);
   bmpfileheader[ 5] = (unsigned char)(filesize >> 24);

   bmpinfoheader[ 4] = (unsigned char)(       w      );
   bmpinfoheader[ 5] = (unsigned char)(       w >>  8);
   bmpinfoheader[ 6] = (unsigned char)(       w >> 16);
   bmpinfoheader[ 7] = (unsigned char)(       w >> 24);
   bmpinfoheader[ 8] = (unsigned char)(       h      );
   bmpinfoheader[ 9] = (unsigned char)(       h >>  8);
   bmpinfoheader[10] = (unsigned char)(       h >> 16);
   bmpinfoheader[11] = (unsigned char)(       h >> 24);
   bmpinfoheader[20] = (unsigned char)(datasize      );
   bmpinfoheader[21] = (unsigned char)(datasize >>  8);
   bmpinfoheader[22] = (unsigned char)(datasize >> 16);
   bmpinfoheader[23] = (unsigned char)(datasize >> 24);


   char fn[50];
   strcpy( fn, "result.bmp" );
   f = fopen(fn, "w");

   fwrite(bmpfileheader, 1, 14,f);
   fwrite(bmpinfoheader, 1, 40,f);

   fwrite(img, 1, datasize, f);

   fclose(f);

   free(img);
  }


#endif // IMAGEWRITER_H_INCLUDED