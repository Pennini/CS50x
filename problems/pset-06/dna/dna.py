import csv
import sys


def main():
    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)
    # Read database file into a variable
    alleles = []
    with open(sys.argv[1], "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["name"] == "name":
                continue
            alleles.append(row)
    # Read DNA sequence file into a variable
    with open(sys.argv[2], "r") as file:
        reader = csv.reader(file)
        for row in reader:
            dna = row[0]
    # Find longest match of each STR in DNA sequence
    dna_check = {}
    for i in alleles[0]:
        if i == "name":
            continue
        x = longest_match(dna, i)
        dna_check[i] = x
    # Check database for matching profiles
    person = "No match"
    len_allele = len(alleles[0]) - 1
    for i in range(len(alleles)):
        count = 0
        for j in alleles[i]:
            if j == "name":
                continue
            if int(dna_check[j]) == int(alleles[i][j]):
                count += 1
        if count == len_allele:
            person = alleles[i]["name"]
            break

    print(person)
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):
        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:
            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
