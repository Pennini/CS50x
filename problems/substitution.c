#include <stdio.h>
#include <string.h>
#include <ctype.h>

void encrypt(char word[], const char encryption[]);

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    else if (strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }
    else
    {
        int length = strlen(argv[1]);
        for (int i = 0; i < length; i++)
        {
            if (!isalpha(argv[1][i]))
            {
                printf("Key must only contain alphabetic characters.\n");
                return 1;
            }
        }

        for (int i = 0; i < length - 1; i++)
        {
            int j = i + 1;
            if (toupper(argv[1][i]) == toupper(argv[1][j]))
            {
                printf("Key must not contain repeated characters.\n");
                return 1;
            }
        }

        char word[500]; // Assuming the input word will not exceed 500 characters.
        printf("plaintext: ");
        fgets(word, sizeof(word), stdin);
        word[strcspn(word, "\n")] = '\0'; // Remove the newline character from the input.

        char cipher[strlen(word) + 1]; // Add 1 for the null-terminator.
        encrypt(word, argv[1]);
        strcpy(cipher, word);

        printf("ciphertext: %s\n", cipher);
        return 0;
    }
}

void encrypt(char word[], const char encryption[])
{
    char arr[] = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'};

    for (int i = 0, n = strlen(word); i < n; i++)
    {
        if (isalpha(word[i]))
        {
            for (int j = 0, k = strlen(arr); j < k; j++)
            {
                if (isupper(word[i]))
                {
                    if (toupper(arr[j]) == word[i])
                    {
                        word[i] = toupper(encryption[j]);
                        break;
                    }
                }
                else if (islower(word[i]))
                {
                    if (tolower(arr[j]) == word[i])
                    {
                        word[i] = tolower(encryption[j]);
                        break;
                    }
                }
            }
        }
    }
}
