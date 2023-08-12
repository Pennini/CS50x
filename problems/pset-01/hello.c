#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // Get the name from the user
    string name = get_string("What's your name? ");
    // Print Hello with the user name
    printf("Hello, %s\n", name);
}