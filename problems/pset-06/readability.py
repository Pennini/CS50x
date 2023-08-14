from cs50 import get_string


def main():
    text = get_string("Text: ")

    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    index = 0.0588 * (letters / words * 100) - 0.296 * (sentences / words * 100) - 15.8

    if index >= 16:
        print(f"Grade 16+")
    elif index < 1:
        print(f"Before Grade 1")
    else:
        print(f"Grade {round(index)}")


def count_letters(text):
    count = 0
    for i in text:
        if i.isalpha():
            count += 1
    return count


def count_words(text):
    return text.count(" ") + 1


def count_sentences(text):
    count = 0
    for i in text:
        if i in [".", "?", "!"]:
            count += 1
    return count


main()
