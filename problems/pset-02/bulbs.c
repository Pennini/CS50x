#include <cs50.h>
#include <stdio.h>
#include <string.h>

const int BITS_IN_BYTE = 8;

void print_bulb(int bit);

int main(void)
{
    // TODO
    string message = get_string("Message: ");
    int length = strlen(message);
    for (int i = 0; i < length; i++)
    {
        int binary[] = {0, 0, 0, 0, 0, 0, 0, 0};
        int bit = (int) message[i];
        for (int j = BITS_IN_BYTE - 1; j >= 0; j--)
        {
            if (bit == 1)
            {
                binary[j] = 1;
                break;
            }
            else if (bit == 0)
            {
                break;
            }
            else if (bit % 2 == 0)
            {
                bit /= 2;
                binary[j] = 0;
            }
            else if (bit % 2 == 1)
            {
                bit = (bit - 1) / 2;
                binary[j] = 1;
            }
        }
        for (int k = 0; k < BITS_IN_BYTE; k++)
        {
            print_bulb(binary[k]);
        }
        printf("\n");
    }
}

void print_bulb(int bit)
{
    if (bit == 0)
    {
        // Dark emoji
        printf("\U000026AB");
    }
    else if (bit == 1)
    {
        // Light emoji
        printf("\U0001F7E1");
    }
}