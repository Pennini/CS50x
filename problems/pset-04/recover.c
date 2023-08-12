#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef uint8_t BYTE;
const int SIZE = 512;
BYTE buffer[sizeof(BYTE) * SIZE];
int count = 0;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        return 1;
    }
    char *filename = malloc(8 * sizeof(char));
    while (fread(buffer, sizeof(BYTE), SIZE, file) == SIZE)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            sprintf(filename, "%03i.jpg", count);
            FILE *copy = fopen(filename, "w");
            if (copy == NULL)
            {
                fclose(copy);
                continue;
            }
            fwrite(buffer, sizeof(BYTE), SIZE, copy);
            fclose(copy);
            count++;
        }
        else
        {
            if (count > 0)
            {
                FILE *copy = fopen(filename, "a");
                if (copy == NULL)
                {
                    fclose(copy);
                    continue;
                }
                fwrite(buffer, sizeof(BYTE), SIZE, copy);
                fclose(copy);
            }
        }
    }
    free(filename);
    fclose(file);
    return 0;
}