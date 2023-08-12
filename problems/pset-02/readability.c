#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // Getting the text from the user
    string text = get_string("Text: ");

    // Counting letters, words and sentences of the text that the user gave
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    // Coleman-Liau index
    float index = 0.0588 * ((float) letters / words * 100) - 0.296 * ((float) sentences / words * 100) - 15.8;

    // Conditions to choose what to output
    if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", (int) round(index));
    }
    return 0;
}

int count_letters(string text)
{
    int count = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        // Count the letters only if is alphabetic
        if (isalpha(text[i]))
        {
            count++;
        }
    }
    return count;
}

int count_words(string text)
{
    int count = 1;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        // Count the blank spaces + 1 to give the number of words
        if (isblank(text[i]))
        {
            count++;
        }
    }
    return count;
}

int count_sentences(string text)
{
    int count = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        // Count the punctuation to give the numbers of sentences
        char letter = text[i];
        if (letter == '.' || letter == '!' || letter == '?')
        {
            count++;
        }
    }
    return count;
}