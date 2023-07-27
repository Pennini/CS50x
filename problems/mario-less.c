#include <cs50.h>
#include <stdio.h>

int get_size(void);
void pyramid(int x);

int main(void)
{
    // TODO: Prompt for Height
    int n = get_size();
    // TODO: Make the pyramid
    pyramid(n);
}
// Function to get the height of the pyramid
int get_size(void)
{
    int n;
    do
    {
        n = get_int("Height: ");
    }
    // loop that continues to prompt until the height is between 1 and 8
    while (n < 1 || n > 8);

    return n;
}
// function to make the pyramid
void pyramid(int x)
{
    for (int i = 1; i <= x; i++)
    {
        // Print spaces
        for (int j = 0; j < x - i; j++)
        {
            printf(" ");
        }

        // Print hashes
        for (int j = 0; j < i; j++)
        {
            printf("#");
        }

        printf("\n");
    }
}