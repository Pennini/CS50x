#include "helpers.h"
#include <math.h>
// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            RGBTRIPLE pixel = image[i][j];
            int average = round((pixel.rgbtRed + pixel.rgbtGreen + pixel.rgbtBlue) / 3.0);
            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            RGBTRIPLE pixel = image[i][j];
            int red = round((pixel.rgbtRed * 0.393) + (pixel.rgbtGreen * 0.769) + (pixel.rgbtBlue  * 0.189));
            int green = round((pixel.rgbtRed * 0.349) + (pixel.rgbtGreen * 0.686) + (pixel.rgbtBlue  * 0.168));
            int blue = round((pixel.rgbtRed * 0.272) + (pixel.rgbtGreen * 0.534) + (pixel.rgbtBlue  * 0.131));
            if (red > 255)
            {
                red = 255;
            }
            if (green > 255)
            {
                green = 255;
            }
            if (blue > 255)
            {
                blue = 255;
            }
            image[i][j].rgbtRed = red;
            image[i][j].rgbtGreen = green;
            image[i][j].rgbtBlue = blue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE temp = image[i][width - (j + 1)];
            image[i][width - (j + 1)] = image[i][j];
            image[i][j] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int red = 0;
            int green = 0;
            int blue = 0;
            float count = 0.0;
            for (int k = -1; k < 2; k++)
            {
                for (int l = -1; l < 2; l++)
                {
                    int currenti = i + k;
                    int currentj = j + l;
                    if (currenti < 0 || currenti > (height - 1) ||currentj < 0 || currentj > (width - 1))
                    {
                        continue;
                    }
                    red += image[currenti][currentj].rgbtRed;
                    green += image[currenti][currentj].rgbtGreen;
                    blue += image[currenti][currentj].rgbtBlue;
                    count++;
                }
            }
            copy[i][j].rgbtRed = round(red / count);
            copy[i][j].rgbtGreen = round(green / count);
            copy[i][j].rgbtBlue = round(blue / count);
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = copy[i][j];
        }
    }
    return;
}