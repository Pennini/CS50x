#include <stdio.h>
#include <string.h>
#include <stdbool.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is the number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner and loser
typedef struct
{
    int winner;
    int loser;
} pair;

// Array of candidates
char candidates[MAX][50]; // Assuming maximum candidate name length is 49 characters

pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, char name[], int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
bool cycle(int winner, int loser);
void lock_pairs(void);
void print_winner(void);

int main(int argc, char *argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        strcpy(candidates[i], argv[i + 1]);
    }

    // Clear graph of locked-in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count;
    printf("Number of voters: ");
    scanf("%d", &voter_count);

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            char name[50]; // Assuming maximum candidate name length is 49 characters
            printf("Rank %i: ", j + 1);
            scanf("%s", name);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, char name[], int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(name, candidates[i]) == 0)
        {
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            if (i < j)
            {
                preferences[ranks[i]][ranks[j]]++;
            }
        }
    }
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    for (int i = 0, n = candidate_count; i < n; i++)
    {
        for (int j = i + 1; j < n; j++)
        {
            if (preferences[i][j] > preferences[j][i])
            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
                pair_count++;
            }
            else if (preferences[i][j] < preferences[j][i])
            {
                pairs[pair_count].winner = j;
                pairs[pair_count].loser = i;
                pair_count++;
            }
        }
    }
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    pair aux;
    int diff1;
    int diff2;
    if (pair_count > 1)
    {
        for (int i = 0; i < pair_count; i++)
        {
            for (int j = 1; j < pair_count; j++)
            {
                if (i < j)
                {
                    diff1 = preferences[pairs[i].winner][pairs[i].loser] - preferences[pairs[i].loser][pairs[i].winner];
                    diff2 = preferences[pairs[j].winner][pairs[j].loser] - preferences[pairs[j].loser][pairs[j].winner];
                    if (diff1 < diff2)
                    {
                        aux = pairs[i];
                        pairs[i] = pairs[j];
                        pairs[j] = aux;
                    }
                }
            }
        }
    }
}

bool cycle(int winner, int loser)
{
    if (locked[loser][winner] == true)
    {
        return true;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        if (locked[loser][i] == true && cycle(winner, i))
        {
            return true;
        }
    }
    return false;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    for (int i = 0; i < pair_count; i++)
    {
        int winner = pairs[i].winner;
        int loser = pairs[i].loser;
        if (!cycle(winner, loser))
        {
            locked[winner][loser] = true;
        }
    }
}

// Print the winner of the election
void print_winner(void)
{
    for (int i = 0, n = candidate_count; i < n; i++)
    {
        bool winner = true;
        for (int j = 0; j < n; j++)
        {
            if (locked[j][i])
            {
                winner = false;
                break;
            }
        }
        if (winner)
        {
            printf("%s\n", candidates[i]);
            return;
        }
    }
}
