#include <cs50.h>
#include <stdio.h>

// commands to show for the machine that will have code after the main that will be useful to execute the main code
int start_size(void);
int end_size(int x);
int threshold(int x, int y);
void print(int x);

int main(void)
{
//  Prompt for start size
    int n = start_size();

// Prompt for end size
    int p = end_size(n);

//  Calculate number of years until we reach threshold
    int t = threshold(n, p);

//  Print number of years
    print(t);
}
// function to get the population size from the user
int start_size(void)
{
    int n;
    do
    {
        n = get_int("Population size: ");
    }
    // loop that repeats if value is less than 9
    while (n < 9);

    return n;
}
// function to get the ending population from the user
int end_size(int x)
{
    int p;
    do
    {
        p = get_int("Ending population size: ");
    }
    // loop that repeats if value is less than the initial population
    while (p < x);

    return p;
}
// function to calculate the number of years required to achieve the final population
int threshold(int x, int y)
{
    int anos = 0;
    // loop that counts the years until the initial population reaches or passes the final population
    while (x < y)
    {
        x += (x / 3) - (x / 4);
        anos++;
    }

    return anos;
}
// function to print the amount of years takes to reach the final population
void print(int x)
{
    printf("Years: %i\n", x);
}